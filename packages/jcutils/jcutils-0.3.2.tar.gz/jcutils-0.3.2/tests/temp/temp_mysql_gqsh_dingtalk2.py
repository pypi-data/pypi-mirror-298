import re
from io import BytesIO

import pandas as pd

from src.api.conn import dingtalk_client

pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"


res = dingtalk_client.query(
    """select * from process_instances
where process_code = 'PROC-5495D970-69A5-400D-855D-5F855DC49BC5'
and result ='agree' and status = 'COMPLETED'
and businessId = '202407301038000531748'
limit 1000
"""
)
# print(res)

for row in res:
    businessid = row["businessId"]
    attachment_data = row["attachment_data"]
    if attachment_data:
        file_stream = BytesIO(attachment_data)
        df = pd.read_excel(file_stream, sheet_name=0, keep_default_na=False, engine="openpyxl")
        df_filled = df.fillna(0)
        # 将数据转换为列表，并将 NaN 转换为 None
        attachment_data_list = df_filled.values.tolist()
        for n, data_array in enumerate(attachment_data_list, 1):
            print(n, businessid, str(data_array[0]), data_array)
            # 使用 re.match 检查字符串是否符合正则表达式
            if re.match(pattern, str(data_array[0])):
                settlement_date_excel = str(data_array[0])
            else:
                print(f"日期格式错误，为：{data_array[0]}")
                # raise ValueError(f"日期格式错误，为：{data_array[0]}")
            print(settlement_date_excel)
