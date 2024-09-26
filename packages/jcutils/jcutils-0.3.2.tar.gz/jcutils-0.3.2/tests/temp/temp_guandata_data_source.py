import json

import requests

from src.api.settings import config


def data_source():
    url = "https://databi.zzgqsh.com/public-api/data-source/list"
    adict = {"token": config.credentials.guanyuan_user_token}
    r = requests.post(url, json=adict)

    for adict in r.json()["response"]:
        atext = json.dumps(adict, ensure_ascii=False)
        if "ads_order_sales" in atext and "ads_order_item_sales" in atext:
            # print (json.dumps(adict,ensure_ascii=False))
            print(adict["name"])


def task():
    url = "https://databi.zzgqsh.com/api/task/guandata/history?startTime=2023-03-29%2015%3A58%3A34&endTime=2023-03-29%2018%3A58%3A34"
    adict = {"token": config.credentials.guanyuan_user_token}
    r = requests.post(url, json=adict)

    print(r.text)
    # for adict in r.json()["response"]:
    #     print (adict["name"])


if __name__ == "__main__":
    # data_source()
    # task()
    pass
