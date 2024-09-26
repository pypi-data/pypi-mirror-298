# coding: utf-8
"""
@File    :   test_dataworks_project.py
@Time    :   2023/10/13 15:56:43
@Author  :   lijc210@163.com
@Desc    :   https://help.aliyun.com/zh/dataworks/developer-reference/api-1/?spm=a2c4g.11186623.0.0.244a36c9WDYRq7
"""

from alibabacloud_dataworks_public20200518 import (
    models as dataworks_public_20200518_models,
)
from alibabacloud_tea_util import models as util_models

from src.api.conn import dataworks_client

runtime = util_models.RuntimeOptions()

list_projects_request = dataworks_public_20200518_models.ListProjectsRequest(page_number=1, page_size=100)

# res = dataworks_client.list_projects_with_options(list_projects_request, runtime)
# print(res.body.page_result.total_count)
# for node in res.body.page_result.project_list:
#     print(node)

list_nodes_request = dataworks_public_20200518_models.ListNodesRequest(project_env="PROD", project_id=70784)

res = dataworks_client.list_nodes_with_options(list_nodes_request, runtime)
print(res.body.data.total_count)
for node in res.body.data.nodes:
    print(node.node_name, node)
