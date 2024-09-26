"""
@author: lijc210@163.com
@file: 14.py
@time: 2020/07/14
@desc: 节假日数据
https://www.tianapi.com/apiview/139#apicode
"""
import http.client
import json
import sys
import time
import urllib
from datetime import datetime, timedelta

import requests


def day_ops(days=0, outfmt="%Y-%m-%d %H:%M:%S"):
    """
    当前时间加减天
    :param days:
    :param outfmt:
    :return:
    """
    return (datetime.now() + timedelta(days=days)).strftime(outfmt)


def get_day_range(dt1=None, dt2=None, infmt="%Y-%m-%d %H:%M:%S", outfmt="%Y-%m-%d"):
    """
    获取获取两个日期之间的所有日期
    :return:
    """
    dt1 = datetime.strptime(dt1, infmt)
    dt2 = datetime.strptime(dt2, infmt)
    delta = dt2 - dt1
    date_range = []
    for i in range(delta.days + 1):
        dt = (dt1 + timedelta(i)).strftime(outfmt)
        date_range.append(dt)
    return date_range


def get_holiday_old(year):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36",
        "Referer": "https://ad.toutiao.com",
    }
    url = "http://timor.tech/api/holiday/year/{year}/".format(year=year)
    r = requests.get(url, headers=headers, timeout=10)
    print(r.text)
    res_dict = r.json()
    res_holiday = res_dict["holiday"]
    holiday_dict = {year + "-" + k: v for k, v in res_holiday.items()}
    return holiday_dict


def get_holiday(year):
    conn = http.client.HTTPSConnection("apis.tianapi.com")  # 接口域名
    params = urllib.parse.urlencode(
        {"key": "28dae677dc4e9eff8e88251cca67bb8b", "date": year, "type": "1"}
    )
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    conn.request("POST", "/jiejiari/index", params, headers)
    tianapi = conn.getresponse()
    result = tianapi.read()
    data = result.decode("utf-8")
    # print(data)
    dict_data = json.loads(data)
    holiday_dict = {}
    code = dict_data["code"]
    if code == 200:
        res_list = dict_data["result"].get("list")
        if res_list:
            for adict in res_list:
                name = adict["name"]
                vacation = adict["vacation"]  # 节假日数组
                remark = adict["remark"]  # 调休日数组
                # print(name,vacation,"########",remark)
                if vacation:
                    for vacation_day in vacation.split("|"):
                        holiday_dict[vacation_day] = {
                            "holiday": True,
                            "name": name,
                            "after": None,
                            "target": None,
                        }
                if remark:
                    for remark_day in remark.split("|"):
                        holiday_dict[remark_day] = {
                            "holiday": False,
                            "name": name + "补班",
                            "after": None,
                            "target": None,
                        }
    # print(json.dumps(holiday_dict,ensure_ascii=False))
    return holiday_dict


def get_data_list(
    year,
):
    data_list = []
    if year < "2020":
        holiday_dict = get_holiday_old(year)
    else:
        holiday_dict = get_holiday(year)
    date_range = get_day_range(
        year + "-01-01", year + "-12-31", infmt="%Y-%m-%d", outfmt="%Y-%m-%d"
    )
    for day2 in date_range:
        day1 = day2.replace("-", "")
        week = datetime.strptime(day2, "%Y-%m-%d").weekday()  # 表示星期几，0-6表示星期一到星期天
        holiday_one_dict = holiday_dict.get(day2)
        if holiday_one_dict:
            holiday = holiday_one_dict["holiday"]  # true表示是节假日，false表示是调休
            # 节假日的中文名。如果是调休，则是调休的中文名，例如'国庆前调休'
            name = holiday_one_dict["name"]
            # 只在调休下有该字段。true表示放完假后调休，false表示先调休再放假
            after = holiday_one_dict.get("after")
            target = holiday_one_dict.get("target")  # 只在调休下有该字段。表示调休的节假日
            if holiday:
                type = "法定节假日"
            else:
                type = "补假的工作日"
        else:
            if week in (5, 6):
                type = "正常周末"
            else:
                type = "正常工作日"
            holiday, name, after, target = "common", None, None, None
        alist = [day1, day2, holiday, name, after, target, week, year, type]
        data_list.append(alist)
    return data_list


def main():
    # 每月1号执行，避免过多调用接口
    time.strftime("%d", time.localtime(time.time()))
    # if today != '01':
    #     return

    if len(sys.argv) == 2 and len(sys.argv[1]) == 4:
        year = sys.argv[1]
    else:
        year = time.strftime("%Y", time.localtime(time.time()))  # 当前年
    print(f"业务日期{year}")
    # print(year)
    get_data_list(str(year))
    # print(json.dumps(data_list,ensure_ascii=False))


if __name__ == "__main__":
    main()
