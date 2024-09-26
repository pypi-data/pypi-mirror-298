"""
@author: lijc210@163.com
@file: built_in_tools.py
@time: 2019/09/25
@desc: 功能描述。
"""
import pickle


def pickleFile(file, item):
    with open(file, "wb") as dbFile:
        pickle.dump(item, dbFile)


def unpickeFile(file):
    with open(file, "rb") as dbFile:
        return pickle.load(dbFile)
