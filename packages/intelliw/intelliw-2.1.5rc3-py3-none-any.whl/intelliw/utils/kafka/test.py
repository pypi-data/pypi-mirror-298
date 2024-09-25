import time

from intelliw.utils.kafka import get_client, handle_message
import os

os.environ['kafka.cluster.hosts'] = '172.20.32.80:9092,172.20.32.82:9092,172.20.32.83:9092'


def test_get_client_with_args(group_id):
    """
    测试通过直接传参获取 Kafka 配置
    """
    return get_client(
        brokers='localhost:9092',
        group_id=group_id,
        username='custom_user',
        password='custom_pass',
        producer_config={'acks': 'all'},
        consumer_config={'auto.offset.reset': 'earliest'}
    )


def test_get_client_with_env(group_id):
    """
    测试通过直接传参获取 Kafka 配置
    """
    return get_client(
        group_id=group_id,
    )


if __name__ == '__main__':
    # client = test_get_client_with_args('consumer1')

    print('start producing...')
    client = test_get_client_with_env('consumer-group-hx')

    client.produce_message(topic='test-topic', value={'nihao':'1'})
    # client.produce_messages_in_batch(topic='test-topic', messages=[(f'key{i}', f'value{i}') for i in range(100)])

    time.sleep(5)

    print('start consuming...')
    client.consume_messages(topics=['test-topic'], handle_func=handle_message)
    # client.consume_messages_with_threads(topics=['test-topic'], handle_func=handle_message, num_threads=5)
