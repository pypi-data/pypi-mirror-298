import datetime

since_array = (
    (31536000, "年"),  # 60 * 60 * 24 * 365
    (2592000, "月"),
    (604800, "周"),
    (86400, "天"),
    (3600, "小时"),
    (60, "分钟"),
    (1, "秒"),
)


def relative_time(start_time, end_time):
    since = int((end_time - start_time).total_seconds())
    for k, v in since_array:
        if since >= k:
            return "{}{}前".format(since / k, v)
    return "刚刚"


if __name__ == "__main__":
    # 刚刚
    print(
        relative_time(
            datetime.datetime(2018, 0o5, 25, 19, 19, 29),
            datetime.datetime(2018, 0o5, 25, 19, 19, 29),
        )
    )
    # 10秒前
    print(
        relative_time(
            datetime.datetime(2018, 0o5, 25, 19, 19, 19),
            datetime.datetime(2018, 0o5, 25, 19, 19, 29),
        )
    )
    # 4分钟前
    print(
        relative_time(
            datetime.datetime(2018, 0o5, 25, 19, 15, 19),
            datetime.datetime(2018, 0o5, 25, 19, 19, 29),
        )
    )
    # 4小时前
    print(
        relative_time(
            datetime.datetime(2018, 0o5, 25, 15, 15, 19),
            datetime.datetime(2018, 0o5, 25, 19, 19, 29),
        )
    )
    # 5天前
    print(
        relative_time(
            datetime.datetime(2018, 0o5, 20, 15, 15, 19),
            datetime.datetime(2018, 0o5, 25, 19, 19, 29),
        )
    )
    # 1周前
    print(
        relative_time(
            datetime.datetime(2018, 0o5, 15, 15, 15, 19),
            datetime.datetime(2018, 0o5, 25, 19, 19, 29),
        )
    )
    # 1月前
    print(
        relative_time(
            datetime.datetime(2018, 0o5, 15, 15, 15, 19),
            datetime.datetime(2018, 0o5, 25, 19, 19, 29),
        )
    )
    # 1年前
    print(
        relative_time(
            datetime.datetime(2017, 0o5, 15, 15, 15, 19),
            datetime.datetime(2018, 0o5, 25, 19, 19, 29),
        )
    )
