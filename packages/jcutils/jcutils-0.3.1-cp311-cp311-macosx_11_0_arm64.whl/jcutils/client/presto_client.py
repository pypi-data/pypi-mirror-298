"""
Created on 2016/8/5
@author: lijc210@163.com
Desc: python2.7 下远程查询presto
"""

from pyhive import presto


class PrestoClient:
    def __init__(self):
        pass

    def Conn(self):
        conn = presto.connect(host="10.10.23.11", port=8444, username="lijicong")
        cursor = conn.cursor()
        return conn, cursor

    def query(self, sql):
        conn, cursor = self.Conn()
        cursor.execute(sql)
        results = cursor.fetchall()
        # print(cursor.description)
        cursor.close()
        conn.close()
        return results

    def queryDict(self, sql):
        conn, cursor = self.Conn()
        cursor.execute(sql)
        results = cursor.fetchall()
        desc = []
        if cursor.description:
            desc = [field[0] for field in cursor.description]
        res_list = [dict(zip(desc, row, strict=True)) for row in results]
        cursor.close()
        conn.close()
        return res_list


if __name__ == "__main__":
    presto_client = PrestoClient()
    sql = "select * from dw.ol_cms_display_amount limit 10"
    print(presto_client.query(sql))
