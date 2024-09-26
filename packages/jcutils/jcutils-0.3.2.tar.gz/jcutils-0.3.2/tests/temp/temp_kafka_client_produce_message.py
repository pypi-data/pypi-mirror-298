from src.api.settings import config
from src.api.utils.kafka_client import KafkaClient

kafka_client = KafkaClient(bootstrap_servers=config.kafka.bootstrap_servers)

topic_name = "test"

# 发送消息
for i in range(5):
    kafka_client.produce_message(topic_name, f"Hello test {i}".encode())
