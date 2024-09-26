from src.api.conn import order_client


def query():
    sql = """
    select shop_code_inner,sum(num) s from gqsh_order t1
    left join gqsh_order_item t2
    on t1.order_no = t2.order_no
    where create_time between '2023-12-09 00:00:00' and '2023-12-10 00:00:00'
    group by shop_code_inner order by s desc
    """
    res = order_client.query(sql)
    print(res)


query()
