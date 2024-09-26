from src.api.conn import opsigenes_client

sql = """replace into upd_dingtalk_process_instances(
                title,
                finishTime,
                originatorUserId,
                originatorDeptId,
                originatorDeptName,
                status,
                approverUserIds,
                ccUserIds,
                result,
                businessId,
                operationRecords,
                tasks,
                bizAction,
                bizData,
                attachedProcessInstanceIds,
                mainProcessInstanceId,
                formComponentValues,
                createTime,
                process_code,
                process_name
    )
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
values = [
    [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "[]",
        "[]",
        "7",
        "8",
        "[]",
        "[]",
        "9",
        "10",
        "[]",
        "11",
        "[]",
        "12",
        "aaa",
        "bbb",
    ]
]

opsigenes_client.executemany(sql, values)
