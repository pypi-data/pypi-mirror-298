"""
@File    :   test_pyodps.py
@Time    :   2021/02/02 10:35:06
@Author  :   lijc210@163.com
@Desc    :   None
"""

from odps import ODPS

from src.api.settings import config

# lijicong
# odps = ODPS(config.credentials.access_id, config.credentials.access_key,
#  'Data_Kezhi',endpoint='http://service.cn-beijing.maxcompute.aliyun.com/api')

# dataworks
odps = ODPS(
    config.credentials.access_id,
    config.credentials.access_key,
    "Data_Kezhi",
    endpoint="http://service.cn-beijing.maxcompute.aliyun.com/api",
)

sql = """
select * from data_kezhi.ads_order_item_sales_agg_dt_517 where dt='20240514'
"""
with odps.execute_sql(sql).open_reader() as reader:
    i = 0
    for record in reader:
        print(record[0])
        i += 1
    print(i)
