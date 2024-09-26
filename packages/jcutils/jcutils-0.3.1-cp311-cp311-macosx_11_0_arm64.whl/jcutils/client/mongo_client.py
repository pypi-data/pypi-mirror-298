"""
Created on 2016/5/10
@author: lijc210@163.com
Desc: 功能描述。
"""
import pymongo


class MongoClient:
    def __init__(self, url=None, database=None):
        self.url = url
        self.database = database

    def conn(self, database=True, replicaSet=None):
        if database:
            conn = pymongo.MongoClient(self.url, replicaSet=replicaSet)[self.database]
        else:
            conn = pymongo.MongoClient(self.url, replicaSet=replicaSet)
        return conn

    def find_one(self, collection=None):
        conn = self.conn()[collection]
        results = conn.find_one()
        return results

    def find(self, collection=None, filter=None):
        conn = self.conn()[collection]
        results = conn.find(filter)
        return results

    def insert(self):
        pass

    def insertmany(self):
        pass

    def oplog(self, ts=None):
        """
        from bson.timestamp import Timestamp
        ts = Timestamp(1541660421,3)

        http://api.mongodb.com/python/current/examples/tailable.html

        其中op，可以是如下几种情形之一：
        "i"： insert
        "u"： update
        "d"： delete
        "c"： db cmd
        "db"：声明当前数据库 (其中ns 被设置成为=>数据库名称+ '.')
        "n": no op,即空操作，其会定期执行以确保时效性
        :return:
        """
        conn = self.conn(database=False, replicaSet=None)
        is_master = conn.admin.command("isMaster")
        replicaSet = is_master.get("setName", None)
        if replicaSet:
            conn = self.conn(database=False, replicaSet=replicaSet)
            oplog = conn.local.oplog.rs
            if not ts:
                first = (
                    oplog.find().sort("$natural", pymongo.ASCENDING).limit(-1).next()
                )
                ts = first["ts"]
            cursor = oplog.find({"ts": {"$gt": ts}})
            return cursor
            # for doc in cursor:
            #     ts = doc['ts']
            #     print(ts)


if __name__ == "__main__":
    mongo_client = MongoClient(
        url="mongodb://usvr_bi:W3NmE5xPQiJ5iEvzxZIc@10.10.22.64:27120/",
        database="decoration",
    )
    print(mongo_client.find_one(collection="shop"))
    for adict in mongo_client.find(filter={"shop_id": 213985}, collection="shop"):
        print(adict)
    # mongo_client.oplog()
