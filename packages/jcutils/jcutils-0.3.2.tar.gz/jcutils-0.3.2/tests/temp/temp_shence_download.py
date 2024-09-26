import os

import requests

from src.api.settings import config
from src.api.utils.datetime_ import day_now, day_ops

token = config.credentials.shence_api_secret

start_time = day_ops(days=-1, outfmt="%Y-%m-%d 00:00:00")
end_time = day_now(outfmt="%Y-%m-%d 00:00:00")

# 上传的
data = {
    "q": """select
            first_id,
            from_unixtime(cast(register_time/1000 as int) , 'yyyy-MM-dd') as register_time,
            from_unixtime(cast(siyu_add_time/1000 as int) , 'yyyy-MM-dd') as siyu_add_time,
            from_unixtime(cast(first_consume_date/1000 as int) , 'yyyy-MM-dd') as first_consume_date
            from users
            where register_time between 1700236800000 and 1703001600000  /*MAX_QUERY_EXECUTION_TIME=1800*/"""
}
print(data)
r = requests.post(config.urls.shence_url + f"/api/sql/query?token={token}&project=production", data=data)
file_path = os.path.join(config.dirs.temp_path, "shence.xlsx")
print(file_path)
with open(file_path, "w") as f:
    f.write(r.text)
