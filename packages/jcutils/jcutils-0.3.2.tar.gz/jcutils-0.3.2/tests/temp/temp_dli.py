from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.http.http_config import HttpConfig
from huaweicloudsdkdli.v1.dli_client import DliClient
from huaweicloudsdkdli.v1.model import ListFlinkJobsRequest, ListQueuesRequest

from src.api.settings import config

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

request = ListQueuesRequest()
print(dli_client.list_queues(request))
print(dir(dli_client))

request = ListFlinkJobsRequest(limit=100)
flink_jobs = dli_client.list_flink_jobs(request)
print(flink_jobs)

# request = RunFlinkJobRequest()
# request.body = {
#     "job_ids": [235695],
#     "resume_savepoint": False
# }
# flink_job = dli_client.run_flink_job(request)
# print(flink_job)

# request = ShowFlinkJobRequest(job_id=235695)
# flink_job = dli_client.show_flink_job(request)
# print(flink_job)

if __name__ == "__main__":
    pass
