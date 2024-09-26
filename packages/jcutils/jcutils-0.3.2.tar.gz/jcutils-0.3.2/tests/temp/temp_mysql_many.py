import json
import time
from concurrent import futures

from src.api.conn_pool import apocalypse_client

with open("tests/up.json") as f:
    data_list_up = json.loads(f.read())

sql2 = "update upd_dim_jd_erp_shop set gs_province=%s,gs_province_leader=%s, \
    area=%s,area_manager=%s,mf_urban_zoning=%s,mf_urban_zoning_ma=%s,mf_regional_supervision=%s,\
    operation_region=%s,operation_region_leader=%s \
    where store_shop_code=%s"


def update(alist):
    t1 = time.time()
    apocalypse_client.executemany(sql2, alist)
    print(time.time() - t1)


def chunks(data, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(data), n):
        yield data[i : i + n]


t2 = time.time()
all_list = []
with futures.ThreadPoolExecutor(10) as executor:
    res = executor.map(update, chunks(data_list_up, 100))
print("aaaaaaa", time.time() - t2)

# for alist in chunks(data_list_up, 100):
#     print(len(alist))
