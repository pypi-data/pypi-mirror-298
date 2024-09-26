from src.api.conn_pool import apocalypse_client_pool

res = apocalypse_client_pool.query("select * from flink_hw_source limit 10")
print(res)

# sql = "insert into flink_hw_source(id,name,age,status) values(5, 'a', 20, 1)"
# apocalypse_client_pool.execute(sql)

sql = "insert into flink_hw_source(id,name,age,status) values(%s,%s,%s,%s)"
data_list1 = [[5, "a", 20, 1], [6, "b", 20, 1]]
lastrowid = apocalypse_client_pool.executemany(sql, data_list1)
print(lastrowid)

data_list2 = [[7, "a", 20, 1], [8, "b", 20, 1]]
apocalypse_client_pool.executemany(sql, data_list2)
