"""
@author: lijc210@163.com
@file: 14.py
@time: 2020/07/14
@desc: 节假日数据
"""
import time
import traceback
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


def get_holiday(year):
    url = "http://timor.tech/api/holiday/year/{year}/".format(year=year)
    data_list = []
    try:
        res_dict = requests.get(url, timeout=10).json()
    except Exception:
        traceback.print_exc()
        print(traceback.format())
    else:
        code = res_dict["code"]
        date_range = get_day_range(
            year + "-01-01", year + "-12-31", infmt="%Y-%m-%d", outfmt="%Y-%m-%d"
        )
        if code == 0:
            res_holiday = res_dict["holiday"]
            holiday_dict = {year + "-" + k: v for k, v in res_holiday.items()}
            for day2 in date_range:
                day1 = day2.replace("-", "")
                week = datetime.strptime(
                    day2, "%Y-%m-%d"
                ).weekday()  # 表示星期几，0-6表示星期一到星期天
                holiday_one_dict = holiday_dict.get(day2)
                if holiday_one_dict:
                    holiday = holiday_one_dict["holiday"]  # true表示是节假日，false表示是调休
                    # 节假日的中文名。如果是调休，则是调休的中文名，例如'国庆前调休'
                    name = holiday_one_dict["name"]
                    # 只在调休下有该字段。true表示放完假后调休，false表示先调休再放假
                    after = holiday_one_dict.get("after")
                    target = holiday_one_dict.get("target")  # 只在调休下有该字段。表示调休的节假日
                else:
                    holiday, name, after, target = None, None, None, None
                alist = [day1, day2, holiday, name, after, target, week, year]
                data_list.append(alist)
        if not data_list:
            for day2 in date_range:
                day1 = day2.replace("-", "")
                week = datetime.strptime(
                    day2, "%Y-%m-%d"
                ).weekday()  # 表示星期几，0-6表示星期一到星期天
                alist = [day1, day2, None, None, None, None, week, year]
    return data_list


def main():
    # 每月1号执行，避免过多调用接口
    time.strftime("%d", time.localtime(time.time()))
    # if today != '01':
    #     return

    # year = time.strftime("%Y",time.localtime(time.time())) # 当前年
    start_year = "2016"
    end_year = day_ops(days=365 * 2, outfmt="%Y")
    data_list = []
    for year in range(int(start_year), int(end_year) + 1):
        print(year)
        year_date = get_holiday(str(year))
        data_list.extend(year_date)


if __name__ == "__main__":
    main()
