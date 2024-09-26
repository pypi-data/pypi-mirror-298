# coding: utf-8
"""
@File    :   work_weixin_api.py
@Time    :   2024/01/08 14:31:53
@Author  :   lijc210@163.com
@Desc    :   企业微信api，需要企业corpid和corpsecret
corpid，企业ID：
个人专用企业微信：ww72ecd238eb208885，
corpsecret，应用的凭证密钥，每个应用独立：
个人微信报警：Secret(rmP-6p-DHkMRG8FWioqjtal_bOYKypWcdEhd5rMXziw)，AgentId(1000003)
gemini助手：Secret(rmP-6p-DHkMRG8FWioqjtal_bOYKypWcdEhd5rMXziw)，AgentId(1000003)

企业微信管理后台
https://work.weixin.qq.com/wework_admin/loginpage_wx
企业微信消息推送
https://developer.work.weixin.qq.com/document/path/90235
"""

import json
import os
import sys
import time
import traceback
import warnings

import requests

warnings.filterwarnings("ignore")


class WorkWeixinApi:
    """ """

    def __init__(self, corpid, agentid, corpsecret):
        self.url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        self.corpid = corpid
        self.agentid = agentid
        self.corpsecret = corpsecret
        self.expired_time = 7200
        self.token_path = ".qyapi" + str(agentid)

    def get_token(self):
        # 获取当前时间
        current_time = time.time()
        if os.path.exists(self.token_path) and current_time - os.path.getmtime(self.token_path) < self.expired_time:
            with open(self.token_path, "r") as f:
                token = f.read()
        else:
            url = f"{self.url}?corpid={self.corpid}&corpsecret={self.corpsecret}"
            response = requests.get(url, verify=False)
            response_json = response.json()
            if "access_token" in response_json:
                token = response_json["access_token"]
                with open(self.token_path, "w") as f:
                    f.write(token)
            else:
                raise Exception("get token error:{}".format(response_json))
        return token

    def send(self, text="", touser="", toparty=""):
        try:
            token = self.get_token()
            payload = {
                "touser": touser,
                "toparty": self.agentid,
                "msgtype": "text",
                "agentid": self.agentid,
                "text": {"content": str(text)},
                "safe": "0",
            }
            response = requests.post(
                "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + token,
                json=payload,
                verify=False,
            )
            response_json = response.json()
            if response_json["errcode"] != 0:
                print(response_json)
        except Exception:
            traceback.print_exc()

    def media_upload(
        self, path, type, agentid
    ):  ##上传临时素材 媒体文件类型，分别有图片（image）、语音（voice）、视频（video），普通文件（file）
        token = self.get_token()
        media_url = f"https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={token}&type={type}"
        files = {"media": open(path, "rb")}
        r = requests.post(media_url, files=files)
        print(r.text)
        re = json.loads(r.text)
        # print("media_id: " + re['media_id'])
        return re["media_id"]

    def send_pic(self, path="", touser="", toparty=""):
        media_id = self.media_upload(path, "image", agentid)
        token = self.get_token()
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}"
        data = {
            "touser": touser,
            "toparty": toparty,
            "msgtype": "image",
            "agentid": self.agentid,
            "image": {"media_id": media_id},
            "safe": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800,
        }
        response = requests.post(url=url, data=json.dumps(data))
        response_json = response.json()
        if response_json["errcode"] != 0:
            print(response_json)
        return response_json


if __name__ == "__main__":
    if len(sys.argv) == 2:
        content = sys.argv[1]
    else:
        content = "测试"
    corp_id = "ww72ecd238eb208885"
    agentid = 1000003
    secret = "rmP-6p-DHkMRG8FWioqjtal_bOYKypWcdEhd5rMXziw"
    weixin = WorkWeixinApi(corp_id, agentid, secret)

    #  发送消息
    weixin.send(text=content, touser="@all", toparty="1")

    # 发送图片
    # weixin = WorkWeixinApi(corp_id, secret)
    # weixin.send_pic(path="D:\\1.jpg", touser="@all", toparty="1")
