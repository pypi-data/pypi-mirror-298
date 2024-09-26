"""
Created on 2016/5/10
@author: lijc210@163.com
Desc: 功能描述。
"""

# -*- coding:utf-8 -*-

import psycopg2
from psycopg2.extras import RealDictCursor


class PgClient:
    def __init__(
        self,
        host="10.10.20.100",
        user="postgres",
        password="postgres",
        database="dw",
        port="5432",
        cursor_factory=None,
    ):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.cursor_factory = cursor_factory

    def Conn(self):
        conn = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
        )
        if self.cursor_factory == "dict":
            cursor = conn.cursor(cursor_factory=RealDictCursor)
        else:
            cursor = conn.cursor()
        return conn, cursor

    # 查询
    def query(self, sql):
        conn, cursor = self.Conn()
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def insertmany(self, sql, sqlDataList):
        # insert into ods_frame_db_com_department_mid(id,breadcrumb) values(%s,%s)
        # test = [[3,'c']]
        conn, cursor = self.Conn()
        cursor.executemany(sql, sqlDataList)
        # lastrowid = self.cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()

    def insert(self, sql):
        conn, cursor = self.Conn()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    def execute(self, sql):
        conn, cursor = self.Conn()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    def execute_isolation(self, sql):
        conn, cursor = self.Conn()
        old_isolation_level = conn.isolation_level
        conn.set_isolation_level(0)
        cursor.execute(sql)
        conn.set_isolation_level(old_isolation_level)
        cursor.close()
        conn.close()


if __name__ == "__main__":
    pg_client = PgClient(host="10.10.23.100", cursor_factory="dict")
    sql = """select ip_num,city from config.conf_ip_city_detail limit 10"""
    print(pg_client.query(sql))
