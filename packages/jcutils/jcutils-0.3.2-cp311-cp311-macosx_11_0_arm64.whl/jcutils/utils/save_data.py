"""
Created on 2017/11/22 0022 17:31
@author: lijc210@163.com
Desc:
"""
import codecs
import csv


def to_csv(save_file=None, data_list=None):
    with codecs.open(save_file, "wb", "GB18030") as csvfile:
        spamwriter = csv.writer(csvfile, dialect="excel")
        spamwriter.writerows(data_list)


if __name__ == "__main__":
    data_list = [["id", "name"], [1, "张三"], [2, "李四"]]
    to_csv(save_file="test.csv", data_list=data_list)
