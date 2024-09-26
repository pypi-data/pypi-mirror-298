import logging
import platform
import signal
from contextlib import contextmanager
from functools import wraps
from logging.handlers import TimedRotatingFileHandler


def retry(num=0, ex=BaseException, is_raise=True, ex_def=None):
    """
    报错自动重试
    :param is_raise: 是否抛出 异常
    :param ex_def: 重试 指定次数 后 还是 异常 的默认值
    :param ex: 指定 异常 重试
    :param num:  重试次数
    :return: 返回 被 注解 函数的返回值,或者 ed_def
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _i in range(0, num + 1):
                try:
                    result = func(*args, **kwargs)
                except BaseException as e:
                    result = e
                if not isinstance(result, ex):
                    break

            if isinstance(result, BaseException):
                if is_raise:
                    raise result
                else:
                    return ex_def
            else:
                return result

        return wrapper

    return decorator


def use_platform():
    sysstr = platform.system()
    if sysstr == "Windows":
        return "win"
    elif sysstr == "Linux":
        return "linux"
    else:
        return "other"


class CheloExtendedLogger(logging.Logger):
    """
    Custom logger class with additional levels and methods
    """

    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s [%(filename)s,%(lineno)d] %(message)s"
        )
        platform_sys = use_platform()
        if platform_sys == "win":
            log_path = r"D:\weibo\log\%s.log" % name
        else:
            log_path = "/var/log/%s.log" % name
        fh = TimedRotatingFileHandler(
            log_path, when="midnight", encoding="utf-8"
        )  # 用于输出到文件
        fh.setFormatter(formatter)
        self.addHandler(fh)  # 用于输出到文件

        hdr = logging.StreamHandler()  # 用于输出到控制台
        hdr.setFormatter(formatter)
        self.addHandler(hdr)  # 用于输出到控制台
        return


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
