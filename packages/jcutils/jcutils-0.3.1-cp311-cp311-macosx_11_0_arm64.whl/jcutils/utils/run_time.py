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


def run_time_log(thr_time=0.5, logger=None, message=""):
    """
    记录函数执行时间到日志
    多线程安全，多进程不安全
    :param thr_time:
    :param log_path:
    :return:
    """

    def decorator_function(function):
        @wraps(function)
        def wrapped_function(*args, **kwargs):
            t0 = time.time()
            result = function(*args, **kwargs)
            t1 = time.time()
            cost_time = t1 - t0
            if cost_time > thr_time:  # 大于多少秒的，则记录下来
                # print args,kwargs
                logger.warning(
                    "{}\t{}\t{}".format(function.__name__, cost_time, message)
                )
            return result

        return wrapped_function

    return decorator_function


if __name__ == "__main__":

    @run_time
    def aaa():
        print("aaaa")

    aaa()
