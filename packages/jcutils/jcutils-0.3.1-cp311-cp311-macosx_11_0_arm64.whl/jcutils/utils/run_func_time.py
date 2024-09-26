"""
@Time   : 2018/8/22
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import time
from functools import wraps


def run_time(function):
    """
    打印函数执行时间装饰器
    :param function:
    :return:
    """

    @wraps(function)
    def wrapped_function(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print("{}: {} seconds".format(function.__name__, str(t1 - t0)))
        return result

    return wrapped_function


if __name__ == "__main__":

    @run_time
    def aaa():
        print("aaaa")

    aaa()
