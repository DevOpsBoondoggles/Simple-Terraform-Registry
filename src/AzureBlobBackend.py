from azure.identity import DefaultAzureCredential
from azure.storage.blob import ContainerClient,BlobServiceClient,generate_blob_sas,BlobSasPermissions
from flask import Flask,current_app, make_response
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


def ListNamespaces(host,container,namespace,name,provider):   
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


def DownloadFile(host,account,container,namespace, name,provider,version):
    blob = f'v1/modules/{namespace}/{name}/{provider}/{version}/local.zip'
    host = host.rstrip('/') #in case the output has a / already
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




