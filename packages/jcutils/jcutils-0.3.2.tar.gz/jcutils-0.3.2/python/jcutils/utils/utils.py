"""
@Time   : 2019/5/28
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import json
import random
import re
import time
import xml.dom.minidom

import requests

BASE_URL = "https://login.weixin.qq.com"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
TIMEOUT = (10, 60)
s = requests.Session()


def get_msg(loginInfo):
    """
    获取消息
    :param loginInfo:
    :return:
    """
    url = "{}/webwxsync?sid={}&skey={}&pass_ticket={}".format(
        loginInfo["url"],
        loginInfo["wxsid"],
        loginInfo["skey"],
        loginInfo["pass_ticket"],
    )
    data = {
        "BaseRequest": loginInfo["BaseRequest"],
        "SyncKey": loginInfo["SyncKey"],
        "rr": ~int(time.time()),
    }
    headers = {
        "ContentType": "application/json; charset=UTF-8",
        "User-Agent": USER_AGENT,
    }
    r = s.post(url, data=json.dumps(data), headers=headers, timeout=TIMEOUT)
    # print("aaa",r.text)
    r = s.post(url, data=json.dumps(data), headers=headers, timeout=TIMEOUT)
    # print("bbb",r.text)
    dic = json.loads(r.content.decode("utf-8", "replace"))
    if dic["BaseResponse"]["Ret"] != 0:
        return None, None
    loginInfo["SyncKey"] = dic["SyncCheckKey"]
    loginInfo["synckey"] = "|".join(
        [
            "{}_{}".format(item["Key"], item["Val"])
            for item in dic["SyncCheckKey"]["List"]
        ]
    )
    return dic["AddMsgList"], dic["ModContactList"]


def process_login_info(loginContent):
    """
    获取登录信息
    :param loginContent:
    :return:
    """
    """ when finish login (scanning qrcode)
     * syncUrl and fileUploadingUrl will be fetched
     * deviceid and msgid will be generated
     * skey, wxsid, wxuin, pass_ticket will be fetched
    """
    loginInfo = {}
    regx = r'window.redirect_uri="(\S+)";'
    loginInfo["url"] = re.search(regx, loginContent).group(1)
    headers = {"User-Agent": USER_AGENT}
    r = s.get(loginInfo["url"], headers=headers, allow_redirects=False)
    print("eeeeeeeeeee", loginInfo["url"], r.text)
    loginInfo["url"] = loginInfo["url"][: loginInfo["url"].rfind("/")]
    for indexUrl, detailedUrl in (
        ("wx2.qq.com", ("file.wx2.qq.com", "webpush.wx2.qq.com")),
        ("wx8.qq.com", ("file.wx8.qq.com", "webpush.wx8.qq.com")),
        ("qq.com", ("file.wx.qq.com", "webpush.wx.qq.com")),
        ("web2.wechat.com", ("file.web2.wechat.com", "webpush.web2.wechat.com")),
        ("wechat.com", ("file.web.wechat.com", "webpush.web.wechat.com")),
    ):
        fileUrl, syncUrl = (
            "https://%s/cgi-bin/mmwebwx-bin" % url for url in detailedUrl
        )
        if indexUrl in loginInfo["url"]:
            loginInfo["fileUrl"], loginInfo["syncUrl"] = fileUrl, syncUrl
            break
    else:
        loginInfo["fileUrl"] = loginInfo["syncUrl"] = loginInfo["url"]
    loginInfo["deviceid"] = "e" + repr(random.random())[2:17]
    loginInfo["BaseRequest"] = {}
    for node in xml.dom.minidom.parseString(r.text).documentElement.childNodes:
        print(node)
        if node.nodeName == "skey":
            loginInfo["skey"] = loginInfo["BaseRequest"]["Skey"] = node.childNodes[
                0
            ].data
        elif node.nodeName == "wxsid":
            loginInfo["wxsid"] = loginInfo["BaseRequest"]["Sid"] = node.childNodes[
                0
            ].data
        elif node.nodeName == "wxuin":
            loginInfo["wxuin"] = loginInfo["BaseRequest"]["Uin"] = node.childNodes[
                0
            ].data
        elif node.nodeName == "pass_ticket":
            loginInfo["pass_ticket"] = loginInfo["BaseRequest"][
                "DeviceID"
            ] = node.childNodes[0].data
    if not all(key in loginInfo for key in ("skey", "wxsid", "wxuin", "pass_ticket")):
        print(
            "Your wechat account may be LIMITED to log in WEB wechat, error info:\n%s"
            % r.text
        )
        return False, loginInfo
    return True, loginInfo


def web_init(loginInfo):
    url = "%s/webwxinit" % loginInfo["url"]
    params = {
        "r": int(-time.time() / 1579),
        "pass_ticket": loginInfo["pass_ticket"],
    }
    data = {
        "BaseRequest": loginInfo["BaseRequest"],
    }
    headers = {
        "ContentType": "application/json; charset=UTF-8",
        "User-Agent": USER_AGENT,
    }
    r = s.post(url, params=params, data=json.dumps(data), headers=headers)
    dic = json.loads(r.content.decode("utf-8", "replace"))
    print(dic)
    return dic


def check_login(self, uuid=None):
    uuid = uuid or self.uuid
    url = "%s/cgi-bin/mmwebwx-bin/login" % BASE_URL
    localTime = int(time.time())
    params = "loginicon=true&uuid={}&tip=1&r={}&_={}".format(
        uuid,
        int(-localTime / 1579),
        localTime,
    )
    headers = {"User-Agent": USER_AGENT}
    r = self.s.get(url, params=params, headers=headers)
    regx = r"window.code=(\d+)"
    data = re.search(regx, r.text)
    if data and data.group(1) == "200":
        if process_login_info(self, r.text):
            return "200"
        else:
            return "400"
    elif data:
        return data.group(1)
    else:
        return "400"


def get_contact(loginInfo, seq=0):
    url = "{}/webwxgetcontact?r={}&seq={}&skey={}".format(
        loginInfo["url"],
        int(time.time()),
        seq,
        loginInfo["skey"],
    )
    headers = {
        "ContentType": "application/json; charset=UTF-8",
        "User-Agent": USER_AGENT,
    }

    r = s.get(url, headers=headers)
    print("cccccccccccc", r.text)
