from src.api.conn import pg_client

res = pg_client.query("select * from pg_views where viewowner = 'birw'")
# print(res)
for row in res:
    viewname = row["viewname"]
    definition = row["definition"]
    # print(definition)
    if "ads_order_item_combo_sales" in definition:
        print(viewname)
    # print(row)
