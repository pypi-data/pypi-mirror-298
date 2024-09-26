"""
@author: lijc210@163.com
@file: tool_threading.py
@time: 2020/03/11
@desc: 多线程类
"""

from threading import Thread


class MyThread(Thread):
    def __init__(self, func, args):
        super().__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


if __name__ == "__main__":
    import time

    def a(n):
        time.sleep(n)
        return n

    t1 = MyThread(a, args=(1,))
    t2 = MyThread(a, args=(3,))
    t1.start()
    t2.start()

    start = time.time()
    t1.join()
    t2.join()
    res1 = t1.get_result()
    res2 = t2.get_result()
    print(res1)
    print(res2)

    print(time.time() - start)
