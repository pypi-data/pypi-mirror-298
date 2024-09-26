from src.api.conn import ck1_client

sql = "desc ads.ads_ws_daily_weekly_summary"
res = ck1_client.query(sql)

# alist = []
# for row in res:
#     adict =     {
#         "fieldCode":row[0],
#         "fieldName":row[4],
#         "desc":row[1],
#         "fieldType":""
#     }
#     print(row)
#     alist.append(adict)

for i, row in enumerate(res, 1):
    fieldCode = row[0]
    fieldName = row[4]
    desc = row[1]
    fieldType = 4
    a = f"""
        parms{i}.put("fieldCode", "{fieldCode}");
        parms{i}.put("fieldName", "{fieldName}");
        parms{i}.put("desc", "{desc}");
        parms{i}.put("fieldType", {fieldType});
    """
    print(a)

# print(json.dumps(alist,ensure_ascii=False))
