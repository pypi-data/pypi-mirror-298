from src.jcutils.client.mysql_client import MySqlClient
from src.jcutils.settings import config


def test_mysql_client():
    client = MySqlClient(config.databases.apocalypse_db.dict())
    sql = "select * from upd_api_request_data limit 10"
    res = client.query(sql)
    print(res)


if __name__ == "__main__":
    test_mysql_client()
