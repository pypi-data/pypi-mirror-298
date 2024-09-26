# coding: utf-8
"""
@File    :   test_maxcompute_table.py
@Time    :   2023/10/13 15:56:43
@Author  :   lijc210@163.com
@Desc    :   https://help.aliyun.com/zh/maxcompute/user-guide/api-reference/
"""

from alibabacloud_maxcompute20220104 import models as max_compute_20220104_models
from alibabacloud_tea_util import models as util_models

from src.api.conn import maxcompute_client

runtime = util_models.RuntimeOptions()
headers = {}

list_tables_request = max_compute_20220104_models.ListTablesRequest(max_item=100)

res = maxcompute_client.list_tables_with_options("data_kezhi", list_tables_request, headers, runtime)
# print(json.dumps(res, ensure_ascii=False))
# print(res.body.data)
print(len(res.body.data.tables))
# for node in res.body.data.tables:
#     print(node.display_name)
#     # print(node)
