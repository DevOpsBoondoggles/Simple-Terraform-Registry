from azure.storage.blob import BlobServiceClient
from azure.storage.blob import ContainerClient
import json
import re
uri = "https://terrreggm.blob.core.windows.net/"
container = "terrregistryblob"
namespace = "unittest"
name = "versionget"
provider = "local"
name_start = f"v1/modules/{namespace}/{name}/{provider}"
container_client = ContainerClient(uri, container, credential=None)
blobs_list = container_client.list_blobs(name_starts_with=name_start)
x = '{"modules": [{"versions": []}]}'
y =  json.loads(x)  #turn string above json python object
for module in y['modules']:
    for blob in blobs_list:
        ver = (re.search(r'[0-9].[0-9].[0-9]', blob.name).group())
        module['versions'].append({'version' : ver}) #dig in and loop into versions
print(json.dumps(y))
# return  json.dumps(y)