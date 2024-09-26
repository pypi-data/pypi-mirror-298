import requests

from src.api.settings import config
from src.api.utils.tools import user_token

databi_url = config.urls.databi_url

adict = {
    "token": user_token,
    "userGroups": [{"name": "店驰公司绩效", "externalGroupId": "exta240866b7742c6b87b6cc"}],
}
response = requests.post(f"{databi_url}/public-api/user-groups/add", json=adict)
print(response.text)

if __name__ == "__main__":
    pass
