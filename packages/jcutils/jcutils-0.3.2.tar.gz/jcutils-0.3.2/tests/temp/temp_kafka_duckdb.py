from src.api.settings import config
from src.api.utils.kafka_client import KafkaClient

kafka_client = KafkaClient(bootstrap_servers=config.kafka.bootstrap_servers)

topic_name = "test"
group_id = "my_group" + "_" + topic_name + "_tmp6"

# # 列出主题
# topics = kafka_client.list_topics()
# print(json.dumps(topics, ensure_ascii=False))

# # 查看主题信息
# partitions = kafka_client.describe_topic(topic_name)
# print(json.dumps(partitions, ensure_ascii=False))


# # 发送消息
# kafka_client.produce_message(topic_name, b"Hello Kafka")

# # 消费消息（从最早的偏移量开始）
# for message in kafka_client.consume_messages(topic_name, group_id=group_id, auto_offset_reset="earliest"):
#     print(message)

# # 消费消息（从最新的偏移量开始）
# for message in kafka_client.consume_messages(topic_name, group_id=group_id, auto_offset_reset="latest"):
#     print(message)

# 消费消息（从指定的偏移量开始）有bug,只有第一个分区的 ofset 生效了
# for message in kafka_client.consume_messages(topic_name, group_id=group_id, offset=5):
#     print(message)

# # 消费消息（从指定的时间戳开始）
# for message in kafka_client.consume_messages(topic_name, group_id=group_id, dtime="2024-08-16 13:50:00"):
#     print(message)

# # 关闭连接
# kafka_client.close()
