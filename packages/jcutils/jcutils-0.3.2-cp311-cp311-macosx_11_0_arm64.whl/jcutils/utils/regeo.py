# Created on: 2018/3/2 16:03
# Email: lijicong@163.com
# desc  根据坐标获取地址
# -*- coding:utf-8 -*-

import requests

georegeo_url = "https://restapi.amap.com/v3/geocode/regeo"

key = "ec67ff42f93e2088681011e54edf688d"


def api_geocode(location, city=None):
    resp = requests.get(
        georegeo_url,
        params={"key": key, "location": location, "city": city, "batch": "true"},
    )
    print(resp.text)


if __name__ == "__main__":
    api_geocode("116.310003,39.991957|117.310003,39.991957")
