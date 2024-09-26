import requests

from src.api.settings import config


def data_source():
    url = "https://databi.zzgqsh.com/public-api/data-source/list"
    adict = {"token": config.credentials.guanyuan_user_token}
    r = requests.post(url, json=adict)
    # print(r.text)
    response = r.json()["response"]
    print(len(response))
    for adict in r.json()["response"]:
        # print(json.dumps(adict, ensure_ascii=False))
        displayType = adict["displayType"]
        name = adict["name"]
        config1 = adict["config"]
        if displayType == "GAUSSDB":
            query = config1["tableQuery"]["query"]
            # print(name, query)
            # if "1线上2线下" in query or "销售渠道分组" in query or "销售渠道" in query or "`渠道`" in query:
            #     print(name)
            # if "return_amount" in query and "return_amount_new" not in query and "ads_order_sales_center_view" in query:
            #     print(name)
            # if "ads_order_sales" in query and "view" not in query:
            #     print(name)
            # if "ads_order_item_sales" in query and "view" not in query:
            #     print(name)
            # if "ads_order_sales_center_view" in query and "ads_order_sales_center_view_tmp" not in query:
            #     print(name)
            # if "view_tmp" in query:
            #     print(name)
        elif displayType == "CLICKHOUSE":
            query = config["tableQuery"]["query"]
            # print(name, query)
            if (
                "ads_sales_shop_total" in query and "SUM(amount_receivable)/SUM(target_amount) AS `完成率`" in query
                # and "dim_jd_erp_shop" in query
            ):
                print(name)


def task():
    url = "https://databi.zzgqsh.com/api/task/guandata/history?startTime=2023-03-29%2015%3A58%3A34&endTime=2023-03-29%2018%3A58%3A34"
    adict = {"token": config.credentials.guanyuan_user_token}
    r = requests.post(url, json=adict)

    print(r.text)
    # for adict in r.json()["response"]:
    #     print (adict["name"])


if __name__ == "__main__":
    data_source()
    # task()
    pass
