import base64
import json

from kafka import KafkaProducer
from localstack.testing.pytest import markers
from localstack.utils import testutil
from localstack.utils.net import wait_for_port_open
from localstack.utils.strings import short_uid, to_bytes, to_str
from localstack.utils.sync import poll_condition, retry

TEST_LAMBDA_CODE = """
import json
def handler(event, context):
    print(json.dumps(event))
"""


@markers.aws.only_localstack
@markers.only_on_amd64
def test_kafka_lambda_event_source_mapping(
    create_lambda_function,
    aws_client,
    msk_create_cluster_v2,
    create_secret,
    kms_create_key,
    create_event_source_mapping,
    cleanups,
):
    msk_client = aws_client.kafka
    func_name = f"kafka-{short_uid()}"
    cluster_name = f"msk-{short_uid()}"
    secret_name = f"AmazonMSK_{cluster_name}"

    # create Lambda function
    create_lambda_function(func_name=func_name, handler_file=TEST_LAMBDA_CODE)

    # create Kafka stream
    create_cluster_result = msk_create_cluster_v2(
        ClusterName=cluster_name,
        Provisioned={
            "KafkaVersion": "3.3.1",
            "BrokerNodeGroupInfo": {
                "ClientSubnets": [],
                "InstanceType": "kafka.m5.large",
                "BrokerAZDistribution": "DEFAULT",
            },
            "NumberOfBrokerNodes": 2,
        },
    )
    cluster_arn = create_cluster_result.get("ClusterArn")

    # wait until cluster becomes ready ...
    def _cluster_ready():
        state = msk_client.describe_cluster(ClusterArn=cluster_arn)["ClusterInfo"]["State"]
        return "ACTIVE" == state

    assert poll_condition(_cluster_ready, timeout=20), "gave up waiting for cluster to be ready"

    brokers = msk_client.get_bootstrap_brokers(ClusterArn=cluster_arn)
    broker_host = brokers["BootstrapBrokerString"]

    port = int(broker_host.split(":")[-1])
    wait_for_port_open(port, sleep_time=0.8, retries=20)

    # Create event source mapping
    secret_arn = create_secret(
        Name=secret_name, SecretString='{"username":"user","password": "123456"'
    )["ARN"]
    create_event_source_mapping(
        Topics=["topic"],
        FunctionName=func_name,
        SourceAccessConfigurations=[{"Type": "SASL_SCRAM_512_AUTH", "URI": secret_arn}],
        SelfManagedEventSource={"Endpoints": {"KAFKA_BOOTSTRAP_SERVERS": [broker_host]}},
    )

    producer = KafkaProducer(bootstrap_servers=broker_host)
    cleanups.append(producer.close)

    messages = []
    message = {"test": "topic"}
    messages.append(message)
    producer.send(
        topic="topic",
        value=to_bytes(json.dumps(message)),
        headers=[
            ("foo", b"bar"),
            ("foo", b"ed"),
            ("baz", b"fizz"),
        ],
    )
    messages_b64 = [to_str(base64.b64encode(to_bytes(json.dumps(msg)))) for msg in messages]

    # assert that Lambda has been invoked
    def check_invoked():
        logs = testutil.get_lambda_log_events(function_name=func_name, delay_time=15)
        logs = [log for log in logs if any(msg in str(log) for msg in messages_b64)]
        assert len(logs) == 1
        return logs

    events = retry(check_invoked, retries=10, sleep=1)

    # assert lambda event format
    record = events[0]["records"]["topic-1"][0]
    assert record["topic"] == "topic"
    assert record["timestampType"] == "CREATE_TIME"
    assert record["value"] == "eyJ0ZXN0IjogInRvcGljIn0="  # b64 encoded {"test": f"topic"}
    assert record["headers"] == [
        {"foo": [98, 97, 114]},
        {"foo": [101, 100]},
        {"baz": [102, 105, 122, 122]},
    ]
    # TODO validate against AWS
    assert events[0]["eventSource"] == "SelfManagedKafka"
    assert events[0]["bootstrapServers"] == broker_host
