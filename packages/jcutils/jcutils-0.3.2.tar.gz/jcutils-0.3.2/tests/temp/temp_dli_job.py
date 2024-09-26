import urllib3
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.http.http_config import HttpConfig
from huaweicloudsdkdli.v1.dli_client import DliClient
from huaweicloudsdkdli.v1.model import ListFlinkJobsRequest, ShowFlinkJobRequest
from urllib3.exceptions import InsecureRequestWarning

from src.api.settings import config

urllib3.disable_warnings(InsecureRequestWarning)

http_config = HttpConfig.get_default_config()
http_config.ignore_ssl_verification = True
credentials = BasicCredentials(config.credentials.dli_ak, config.credentials.dli_sk, config.credentials.dli_project_id)

dli_client = (
    DliClient.new_builder()
    .with_http_config(http_config)
    .with_credentials(credentials)
    .with_endpoint(config.credentials.dli_endpoint)
    .build()
)

request = ListFlinkJobsRequest(limit=100)
flink_jobs = dli_client.list_flink_jobs(request)
text = ""
for adict in flink_jobs.job_list.jobs:
    # print(adict.job_id, adict.name)
    request = ShowFlinkJobRequest(job_id=adict.job_id)
    flink_job = dli_client.show_flink_job(request)
    if "ads_pay_card_account" in flink_job.job_detail.sql_body:
        print("aaaaaaaaaa", adict.name)

if __name__ == "__main__":
    pass
