"""
Created on 2016/5/10
@author: lijc210@163.com
Desc:

-- 创建一个触发器，在更新时自动更新 update_time 字段
CREATE TRIGGER IF NOT EXISTS update_news
AFTER UPDATE ON news
FOR EACH ROW
BEGIN
    UPDATE news SET update_time = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

"""

import logging
import sqlite3


class Sqlite3Client:
    def __init__(self, db=None, cursorclass=None):
        self.db = db
        self.cursorclass = cursorclass
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def __enter__(self):
        return self.conn()

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    @staticmethod
    def dict_factory(cursor, row):
        return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

    def conn(self):
        conn = sqlite3.connect(self.db)
        if self.cursorclass == "dict":
            conn.row_factory = self.dict_factory
        cursor = conn.cursor()
        return conn, cursor

    def query(self, sql):
        conn, cursor = self.conn()
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except sqlite3.Error as e:
            self.logger.error(f"Error executing SQL: {e}")
            raise e
        finally:
            cursor.close()
            conn.close()

    def execute(self, sql, params=()):
        conn, cursor = self.conn()
        try:
            cursor.execute(sql, params)
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
            self.logger.error(f"Error executing SQL: {e}")
            raise e
        finally:
            cursor.close()
            conn.close()

    def executemany(self, sql, sqlDataList):
        conn, cursor = self.conn()
        try:
            cursor.executemany(sql, sqlDataList)
            lastrowid = cursor.lastrowid
            conn.commit()
            return lastrowid
        except sqlite3.Error as e:
            conn.rollback()
            self.logger.error(f"Error executemany SQL: {e}")
            raise e
        finally:
            cursor.close()
            conn.close()

    def transaction(self, sql_list):
        conn, cursor = self.conn()
        try:
            for sql in sql_list:
                cursor.execute(sql)
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
            self.logger.error(f"Transaction failed: {e}")
            raise e
        finally:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    sqlite3_client = Sqlite3Client("tests.db")

    # 查询示例
    sql_query = "SELECT * FROM COMPANY"
    results = sqlite3_client.query(sql_query)
    print(results)

    # 插入示例
    sql_insert = (
        "INSERT INTO COMPANY (ID, NAME, AGE, ADDRESS, SALARY) VALUES (?, ?, ?, ?, ?)"
    )
    params = (1, "Paul", 32, "California", 20000.00)
    sqlite3_client.insert(sql_insert, params=params)
