from src.api.conn import apocalypse_client


def update():
    res = apocalypse_client.execute(
        "update  upd_dianchi_users " + "set nick_name='马文龙',user_name='yunpu3126' where user_name = '马文龙'"
    )
    print(res)


def query():
    res = apocalypse_client.query("select * from upd_dianchi_users where user_name = 'yunpu3126'")
    print(res)


update()
query()
