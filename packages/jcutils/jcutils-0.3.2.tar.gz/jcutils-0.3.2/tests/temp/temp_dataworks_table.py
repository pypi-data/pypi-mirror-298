# coding: utf-8
"""
@File    :   test_dataworks_table.py
@Time    :   2023/10/13 15:56:43
@Author  :   lijc210@163.com
@Desc    :   https://help.aliyun.com/zh/dataworks/developer-reference/api-1/?spm=a2c4g.11186623.0.0.244a36c9WDYRq7
"""

import json

from alibabacloud_dataworks_public20200518 import (
    models as dataworks_public_20200518_models,
)
from alibabacloud_tea_util import models as util_models

from src.api.conn import dataworks_client

runtime = util_models.RuntimeOptions()

get_meta_dbtable_list_request = dataworks_public_20200518_models.GetMetaDBTableListRequest(app_guid="odps.data_kezhi")

res = dataworks_client.get_meta_dbtable_list_with_options(get_meta_dbtable_list_request, runtime)
print(json.dumps(res.body.data))
