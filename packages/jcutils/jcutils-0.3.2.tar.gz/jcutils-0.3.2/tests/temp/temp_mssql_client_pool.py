from src.api.conn_pool import mssql_client_pool

sql = "select top 10 * from dbo.T_SAL_ORDER with(nolock) where FCREATEDATE>='2024-08-01 13:58:52'"
print(mssql_client_pool.query(sql))
