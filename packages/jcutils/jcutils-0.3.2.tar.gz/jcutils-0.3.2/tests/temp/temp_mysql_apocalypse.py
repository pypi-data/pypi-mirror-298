from src.api.conn import apocalypse_client


def query():
    res = apocalypse_client.query("select * from upd_api_request_data limit 10")
    # print(res)
    import json

    for row in res:
        data = row["data"]
        print(json.loads(data))


def update():
    res = apocalypse_client.execute("update  mail_subscription " + "set process_status='未处理' where id in (392644)")
    print(res)


def delete():
    res = apocalypse_client.execute(
        "delete from mail_subscription " + "where create_time > '2023-11-20 08:00:00' and process_status ='未处理'"
    )
    print(res)


def alter():
    # res = apocalypse_client.execute("ALTER TABLE apocalypse.mail_subscription ADD msg_pick LONGBLOB NULL")
    # res = apocalypse_client.execute("ALTER TABLE apocalypse.mail_subscription CHANGE msg_pick msg_pick mediumblob NULL AFTER msg_path")
    res = apocalypse_client.execute("ALTER TABLE apocalypse.mail_subscription MODIFY COLUMN msg_pick LONGBLOB NULL")
    print(res)


query()
# update()
# alter()
# delete()
