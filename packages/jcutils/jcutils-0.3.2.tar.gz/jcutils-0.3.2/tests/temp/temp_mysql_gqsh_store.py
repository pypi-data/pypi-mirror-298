from src.api.conn import store_client


def query():
    res = store_client.query(
        "select count(1) from store_stock_activity where activity_id in (153) and type = 2 and is_deleted = 0 "
    )
    print(res)


query()
