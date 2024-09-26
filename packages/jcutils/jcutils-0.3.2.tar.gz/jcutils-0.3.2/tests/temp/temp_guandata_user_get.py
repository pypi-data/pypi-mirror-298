import requests

from src.api.settings import config
from src.api.utils.tools import user_token

databi_url = config.urls.databi_url

# 获取用户组列表
bdict = {"token": user_token, "loginId": "oss254TEST"}
response = requests.post(f"{databi_url}/public-api/user/info", json=bdict)
print(response.text)

if __name__ == "__main__":
    pass
