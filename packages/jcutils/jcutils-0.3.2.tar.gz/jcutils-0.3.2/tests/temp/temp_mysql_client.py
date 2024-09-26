from src.api.settings import config
from src.api.utils.mysql_client import MySqlClient

apocalypse_client = MySqlClient(conn_dict=config.databases.apocalypse_db.dict(), cursorclass="dict")


def query():
    res = apocalypse_client.query("select * from upd_auto_screen_component limit 10")
    print(res)


query()
