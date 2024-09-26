"""
Created on 2017/6/15 0015
@author: lijc210@163.com
Desc: 功能描述。
"""
with open("tmp.log") as f:
    for line in f.readlines():
        line_list = line.strip().split(" ")
        try:
            ms = float(line_list[-1].replace("ms", ""))
            if ms >= 5000:
                print(line.strip())
        except Exception:
            pass
            # print line.strip()
