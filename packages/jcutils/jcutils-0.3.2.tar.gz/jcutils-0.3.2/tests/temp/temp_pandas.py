import os
from datetime import datetime

import pandas as pd

from src.api.settings import config


def datetime_converter(o):
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")


fileName = "补贴导入模板.xlsx"
file_path = os.path.join(config.dirs.temp_path, fileName)
df = pd.read_excel(file_path, sheet_name=0, keep_default_na=False, engine="openpyxl")
# 将数据转换为列表，并将 NaN 转换为 None
data_list = df.values.tolist()
print(data_list)
