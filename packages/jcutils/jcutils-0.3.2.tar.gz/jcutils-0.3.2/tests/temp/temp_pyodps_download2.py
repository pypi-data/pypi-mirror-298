"""
@File    :   test_pyodps.py
@Time    :   2021/02/02 10:35:06
@Author  :   lijc210@163.com
@Desc    :   None
"""

import csv
import os

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
select  jd_stock_no as 仓库编码
        ,jd_stock_name as 仓库名称
        ,wl_fnumber as 产品编码
        ,wl_name as 产品名称
        ,wl_category1 as 一级分类
        ,wl_category2 as 二级分类
        ,wl_category3 as 三级分类
        ,wl_category4 as 四级分类
        ,round(on_sale_rate * 100,2) as 上架率
from    data_kezhi.ads_wk_stock_base_wide
where   dt = '20240820'
-- limit 10
"""

file_path = os.path.join(config.dirs.temp_path, "ads_wk_stock_base_wide.csv")
print(file_path)

with open(file_path, "w", newline="") as csvfile:
    spamwriter = csv.writer(csvfile)
    # spamwriter.writerows(date_list)
    with odps.execute_sql(sql).open_reader() as reader:
        for record in reader:
            row = [v for k, v in record]
            # print(record)
            spamwriter.writerow(row)
