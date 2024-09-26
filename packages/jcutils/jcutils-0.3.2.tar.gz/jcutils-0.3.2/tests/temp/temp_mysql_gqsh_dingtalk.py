from io import BytesIO

import pandas as pd

from src.api.conn import dingtalk_client

print(pd.__version__)


res = dingtalk_client.query(
    """select * from process_instances
where businessid = '202407301038000531748'
"""
)
# print(res)

for row in res:
    businessid = row["businessId"]
    processinstance_id = row["processinstance_id"]
    print(businessid, processinstance_id)
    attachment_data = row["attachment_data"]
    file_stream = BytesIO(attachment_data)
    df = pd.read_excel(file_stream, sheet_name=0, keep_default_na=False, engine="openpyxl")
    df_filled = df.fillna(0)
    # 将数据转换为列表，并将 NaN 转换为 None
    attachment_data_list = df_filled.values.tolist()
    print(attachment_data_list)
