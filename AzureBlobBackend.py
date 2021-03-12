from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient,ContainerClient,BlobServiceClient,generate_blob_sas,BlobSasPermissions
from flask import Flask, abort,current_app, flash, jsonify, make_response, send_file, redirect
from datetime import datetime,timezone,timedelta
import json
import re

def VersionGet(host,container,namespace,name,provider):   
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

def XHeader(namespace, name,provider,version):
    blobpath = f'/v1/modules/{namespace}/{name}/{provider}/{version}/local.zip'
    response = make_response('', 204 )
    response.mimetype = current_app.config['JSONIFY_MIMETYPE']
    response.headers['X-Terraform-Get'] = blobpath
    return response

# def DownloadFile(host,container,namespace, name,provider,version):
#     # blobpath = f'/v1/modules/{namespace}/{name}/{provider}/{version}/local.zip'
#     bloburl = f'{host}/{container}/v1/modules/{namespace}/{name}/{provider}/{version}/local.zip'
#     token_credential = DefaultAzureCredential()
#     blob_client = BlobClient.from_blob_url(bloburl, credential=token_credential)  
#     download_stream = blob_client.download_blob()
#     return download_stream

def DownloadFile(host,account,container,namespace, name,provider,version):
    blob = f'v1/modules/{namespace}/{name}/{provider}/{version}/local.zip'
    bloburl = f'{host}/{container}/{blob}'
    azblobaccount = '' #need a way to pull this from the host
    token_credential = DefaultAzureCredential()
    #create a blob service with either the local dev environment variables or system managed identity
    blob_service = BlobServiceClient(host, credential=token_credential) 
    start_utc = datetime.now(timezone.utc) - timedelta(minutes=3)
    end_utc = datetime.now(timezone.utc) + timedelta(minutes=3)
    u_d_key= blob_service.get_user_delegation_key(start_utc, end_utc,timeout = 20)
    sasPerm = BlobSasPermissions(read=True,tag=False)
    blobsas = generate_blob_sas(account, container, blob, user_delegation_key=u_d_key, permission=sasPerm, expiry=end_utc, start=start_utc)
    return f'{bloburl}?{blobsas}'


# def BlobVersionsGet(host,container,namespace,name,provider):    
#     name_start = f"v1/modules/{namespace}/{name}/{provider}"
#     container_client = ContainerClient(host, container, credential=None)
#     blobs_list = container_client.list_blobs(name_starts_with=name_start)
#     x = '{"modules": [{"versions": []}]}'
#     y =  json.loads(x)  #turn string above json python object
#     for module in y['modules']:
#         for blob in blobs_list:
#             ver = (re.search(r'[0-9].[0-9].[0-9]', blob.name).group())
#             module['versions'].append({'version' : ver}) #dig in and loop into versions
#     return  json.dumps(y)




# def BlobDownloadAuthN(namespace, name,provider,version,blobpath):

#     token_credential = DefaultAzureCredential()
#     container_client = ContainerClient(host, container, credential=token_credential)
#     blob_client = container_client.get_blob_client(blobpath)
#     with open(DEST_FILE, "wb") as my_blob:
#     download_stream = blob_client.download_blob()
#     my_blob.write(download_stream.readall())


