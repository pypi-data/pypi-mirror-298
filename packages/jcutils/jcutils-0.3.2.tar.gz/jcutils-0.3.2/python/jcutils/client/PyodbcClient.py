import pyodbc


class PyodbcClient:
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.connection = self._connect()

    def _connect(self):
        conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}"
        return pyodbc.connect(conn_str)

    def execute_query(self, sql_query):
        cursor = self.connection.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def execute_update(self, sql_query):
        cursor = self.connection.cursor()
        cursor.execute(sql_query)
        cursor.commit()
        cursor.close()

    def close_connection(self):
        self.connection.close()


# 示例用法
client = PyodbcClient(
    server="47.94.219.54",
    database="AIS20201114183546",
    username="BIRead",
    password="your_password",
)

# 查询示例
result = client.execute_query("SELECT top 10 * FROM dbo.T_SAL_OUTSTOCK")
print(result)

# 关闭连接
client.close_connection()
