from src.api.conn import ck1_client

sql = """
SELECT count()
FROM system.tables
WHERE database = 'ads'
"""


res = ck1_client.query(sql)
print(res)
