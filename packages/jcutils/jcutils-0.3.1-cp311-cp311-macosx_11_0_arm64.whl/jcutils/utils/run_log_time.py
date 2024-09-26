"""
@Time   : 2018/8/22
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import json
import time
from functools import wraps

from func_timeout import FunctionTimedOut, func_timeout


def run_time_log(
    thr_time=0.5,
    logger=None,
    message="",
    stop_time=0,
    stop_return=None,
    force_stop=False,
):
    """
    记录函数执行时间到日志
    多线程安全，多进程不安全
    :param thr_time: 超过多长时间记录日志
    :param logger:
    :param message: 传递一些信息
    :param stop_time: 超过多长时间停止执行
    :param stop_return: 超时返回值
    :param force_stop: 超时是否停止执行
    :return:
    """

    def decorator_function(function):
        @wraps(function)
        def wrapped_function(*args, **kwargs):
            t0 = time.time()
            if stop_time and force_stop:
                try:
                    result = func_timeout(stop_time, function, args=args, kwargs=kwargs)
                except FunctionTimedOut:
                    logger.warning(
                        "{}函数未在{}秒内完成，将强制停止".format(function.__name__, stop_time)
                    )
                    return stop_return
            else:
                result = function(*args, **kwargs)
            t1 = time.time()
            cost_time = t1 - t0
            if cost_time > thr_time:  # 大于多少秒的，则记录下来
                # print args,kwargs
                logger.warning(
                    "{}\t{}\n{}\t{}".format(function.__name__, cost_time, args, kwargs)
                )
            return result

        return wrapped_function

    return decorator_function


class Timer:
    def __init__(self, tag, logger, **kwargs):
        from collections import defaultdict

        self.tag = tag
        self.logger = logger
        # func : [111,2222]
        self.data = defaultdict(list)
        self.other = dict(kwargs)
        self.tag_data_dcit = {}
        self.tag_start(self.tag)

    def tag_start(self, title):
        self.data[title].append(time.time())

    def tag_end(self, title):
        self.data[title].append(time.time())

    def tag_data(self, title, value):
        self.tag_data_dcit[title] = value

    def if_time(self, title, t):
        self.tag_end(self.tag)
        s, e = self.data[title]
        cost = e - s
        if cost > t:
            _data = {k: v[1] - v[0] for k, v in self.data.items()}
            self.logger.info(
                "total:{}##{}##{}##{}".format(
                    cost,
                    self.tag,
                    _data,
                    json.dumps(self.tag_data_dcit, ensure_ascii=False),
                )
            )


if __name__ == "__main__":
    #####run_time_log#####
    from utils.logging_ import FileHandler_

    FUNC_LOG_PATH = "func.log"  # 函数日志
    logger = FileHandler_(
        getLogger="api",
        setLevel="logging.INFO",
        filename=FUNC_LOG_PATH,
        mode="w",
        StreamHandler=False,
        formatter=None,
    )

    @run_time_log(
        thr_time=0.5,
        logger=logger,
        stop_time=0.7,
        stop_return=[],
        force_stop=False,
    )
    def aaa(a, b, c=0):
        print("aaaa")
        time.sleep(1)
        return a, b, c

    print(aaa(1, 2, c=3))

    # #####Timer#####
    #
    # def bbb():
    #     TITLE_FUN = "test"
    #     timer = Timer(tag=TITLE_FUN, logger=logger)
    #     # timer.tag_start(TITLE_FUN)
    #     timer.tag_start("aaa")
    #     time.sleep(1)
    #     timer.tag_end("aaa")
    #     timer.tag_start("bbb")
    #     time.sleep(2)
    #     timer.tag_end("bbb")
    #     timer.tag_data("ccccccccc", "value")
    #     # timer.tag_end(TITLE_FUN)
    #     timer.if_time(TITLE_FUN, 1)
    #
    #
    # bbb()
