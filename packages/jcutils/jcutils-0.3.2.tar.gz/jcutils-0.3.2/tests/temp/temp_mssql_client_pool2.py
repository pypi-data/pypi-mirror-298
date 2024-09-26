from src.api.conn_pool import mssql_client_pool

sql = "select count(1) as total from dbo.t_sal_outstock where FCREATEDATE between '2024-07-31 00:00:00' and '2024-08-01 00:00:00'"
print(mssql_client_pool.query(sql))
