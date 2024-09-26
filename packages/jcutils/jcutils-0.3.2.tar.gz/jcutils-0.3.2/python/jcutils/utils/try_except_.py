"""
@Time   : 2018/9/5
@author : lijc210@163.com
@Desc:  : 函数异常，发送通知
"""
import sys
import time
import traceback

from utils.mail import Mail
from utils.work_weixin_send import Weixin


def try_except(fun):
    def notice(*args, **kwargs):
        try:
            res = fun(*args, **kwargs)
        except Exception:
            res = None
            traceback.print_exc()

            fun_name = fun.__name__
            error_content = traceback.format_exc()
            datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            subject = fun_name + str(datetime) + "出错"
            content = error_content
            # 邮件通知
            mail_to = [
                "lijicong1@qeeka.com",
                "henry.xiao@qeeka.com",
                "lingkangfu@qeeka.com",
            ]
            mail_cc = [
                "lijicong1@qeeka.com",
                "henry.xiao@qeeka.com",
                "lingkangfu@qeeka.com",
            ]
            mail = Mail(mail_to, mail_cc)
            mail.send(subject, content)
            # 微信通知
            weixin = Weixin()
            weixin.send(agentid=1000012, text=subject)
            sys.exit(1)
        return res

    return notice


if __name__ == "__main__":

    @try_except
    def func():
        print("aaaa")
        raise ValueError("aaaa")

    func()
