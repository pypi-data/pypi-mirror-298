"""
@File    :   upd_dingtalk_process_instances.py
@Time    :   2021/02/02 09:19:09
@Author  :   lijc210@163.com
@Desc    :   拉取钉钉审批实例详情数据
"""

import json
import sys

from src.api.app.dingtalk_process import get_process_code_dict, query_data, save_data, save_one_item
from src.api.utils.datetime_ import day_now, day_ops, dt2ts, ts2dt

target_dict = {
    "PROC-F7082ECE-7F5A-42E9-B4F9-4790D18477F6": {
        "process_name": "ROI测试流程-付款申请(非资产类第三方)",
        "parsing_mode": "付款",
        "form_amount_id": "CalculateField_151INXSYWCG00",
        "form_amount_name": "申请付款金额",
    },
    "PROC-5D23C981-E060-454B-8EEF-D63E58B394E7": {"process_name": "测试240410 通用事前审批"},
    "PROC-5495D970-69A5-400D-855D-5F855DC49BC5": {"process_name": "云豆补贴充值\\核销申请"},
    "PROC-402B99D4-FCAF-40A6-9276-1F0AB6D2CCB6": {
        "process_name": "ROI测试-云豆补贴充值\\核销申请",
        "parsing_mode": "云豆",
        "form_amount_id": "MoneyField_143HYWS4LXJ40",
        "form_amount_name": "补贴金额（元）",
    },
    "PROC-E5B52DC0-A2EC-4628-85E8-D57D2C36BABA": {
        "process_name": "ROI测试-费用报销",
        "parsing_mode": "报销",
        "form_amount_id": "CalculateField_151INXSYWCG00",
        "form_amount_name": "报销总额",
    },
}


def process():
    if sys.argv[1:]:
        dt = sys.argv[1]
        print(f"接收参数：{sys.argv[1]}")
        start_time = int(dt2ts(dt, infmt="%Y-%m-%d") * 1000)
        end_time = int(dt2ts(dt, infmt="%Y-%m-%d") * 1000) + 24 * 60 * 60 * 1000
    else:
        start_time = int(dt2ts(day_ops(days=-1, outfmt="%Y-%m-%d"), infmt="%Y-%m-%d") * 1000)
        end_time = int(dt2ts(day_now()) * 1000)

    print("start_time:", ts2dt(start_time))
    print("end_time:", ts2dt(end_time))
    process_name_code_dict = get_process_code_dict()
    print(json.dumps(process_name_code_dict, indent=4, ensure_ascii=False))

    for process_name, adict in target_dict.items():
        process_code = process_name_code_dict.get(process_name, "")
        if not process_code:
            print("正在处理:", f"未找到{process_name}的process_code")
            continue
        print("正在处理:", process_name, process_code)
        items = query_data(start_time, end_time, process_code)
        print(f"共获取到{len(items)}条数据")
        save_data(process_code, process_name, items)


def main():
    process()


def test():
    save_one_item(
        process_code="PROC-E5B52DC0-A2EC-4628-85E8-D57D2C36BABA",
        process_name="ROI测试-费用报销",
        processinstance_id="vD3z0yKGTIWii0e8pdeDnQ08261723691484",
    )


if __name__ == "__main__":
    # main()
    test()
