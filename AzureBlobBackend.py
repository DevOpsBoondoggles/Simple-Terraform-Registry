from azure.storage.blob import BlobServiceClient
from azure.storage.blob import ContainerClient
from azure.identity import DefaultAzureCredential
import json
import re
def BlobVersionsGet(host,container,namespace,name,provider):    
    name_start = f"v1/modules/{namespace}/{name}/{provider}"
    container_client = ContainerClient(host, container, credential=None)
    blobs_list = container_client.list_blobs(name_starts_with=name_start)
    x = '{"modules": [{"versions": []}]}'
    y =  json.loads(x)  #turn string above json python object
    for module in y['modules']:
        for blob in blobs_list:
            ver = (re.search(r'[0-9].[0-9].[0-9]', blob.name).group())
            module['versions'].append({'version' : ver}) #dig in and loop into versions
    return  json.dumps(y)


def BlobVersionsGetAuthN(host,container,namespace,name,provider):   
    token_credential = DefaultAzureCredential()
    name_start = f"v1/modules/{namespace}/{name}/{provider}"
    container_client = ContainerClient(host, container, credential=token_credential)
    blobs_list = container_client.list_blobs(name_starts_with=name_start)
    x = '{"modules": [{"versions": []}]}'
    y =  json.loads(x)  #turn string above json python object
    for module in y['modules']:
        for blob in blobs_list:
            ver = (re.search(r'[0-9].[0-9].[0-9]', blob.name).group())
            module['versions'].append({'version' : ver}) #dig in and loop into versions
    return  json.dumps(y)

# def BlobDownloadAuthN(namespace, name,provider,version,blobpath):

#     token_credential = DefaultAzureCredential()
#     container_client = ContainerClient(host, container, credential=token_credential)
#     blob_client = container_client.get_blob_client(blobpath)
#     with open(DEST_FILE, "wb") as my_blob:
#     download_stream = blob_client.download_blob()
#     my_blob.write(download_stream.readall())


