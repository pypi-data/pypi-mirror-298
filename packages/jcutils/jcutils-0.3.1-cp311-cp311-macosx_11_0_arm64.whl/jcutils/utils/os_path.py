"""
@Time   : 2018/12/14
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import os


def get_file_path_list(rootdir):
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    file_path_list = []
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isfile(path):
            file_path_list.append(path)
    return file_path_list


if __name__ == "__main__":
    get_file_path_list("/usr/local")
