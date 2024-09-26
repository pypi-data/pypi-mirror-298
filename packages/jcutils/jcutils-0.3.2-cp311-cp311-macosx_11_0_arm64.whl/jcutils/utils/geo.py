# Created on: 2018/3/2 16:03
# Email: lijicong@163.com
# desc   根据地址获取省市区，坐标
# -*- coding:utf-8 -*-

import sys

import requests

georegeo_url = "https://restapi.amap.com/v3/geocode/geo?parameters"

key = "ec67ff42f93e2088681011e54edf688d"


def api_geocode(address, city=None):
    try:
        resp = requests.get(
            georegeo_url, params={"key": key, "address": address, "city": city}
        )
        assert resp.status_code == 200
        rel_json = resp.json()
        print(rel_json)
        assert rel_json["status"] == "1" and rel_json["info"] == "OK"
        rel_array = rel_json["geocodes"]
        assert len(rel_array) > 0
        rel = rel_array[0]
        rel["status"] = 1
        return rel
    except Exception:
        # traceback.print_exc()
        return None


def req_gaode(address, city=None):
    try:
        resp_rel = api_geocode(city=city, address=address) or {}

        location = resp_rel.get("location")
        lng, lat = (
            location
            and len(location.split(",")) == 2
            and [float(it) for it in location.split(",")]
            or [-1, -1]
        )

        return str(lng), str(lat)
    except Exception:
        return ["-1", "-1"]


def read_input(file):
    for line in file:
        if line and line.strip():  # 略过空行
            yield line.rstrip().split("\t")


def main():
    data = read_input(sys.stdin)
    for line in data:
        address = line[0]
        print("\001".join(req_gaode(address)))


if __name__ == "__main__":
    # main()
    print(req_gaode("文昌市白龙白龙建材城"))
