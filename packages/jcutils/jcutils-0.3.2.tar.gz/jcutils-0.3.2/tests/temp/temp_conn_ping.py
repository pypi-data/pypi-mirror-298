from src.api.conn import (
    activity_client,
    apocalypse_client,
    ecology_client,
    frame_client,
    gqshtp_client,
    order_client,
    receive_client,
    spider_client,
    store_client,
)

print(order_client.ping())
print(store_client.ping())
print(receive_client.ping())
print(frame_client.ping())
print(apocalypse_client.ping())
print(spider_client.ping())
print(ecology_client.ping())
print(gqshtp_client.ping())
print(activity_client.ping())
