from azure.storage.blob import BlobClient,ContainerClient,BlobServiceClient,generate_blob_sas,BlobSasPermissions
from azure.identity import DefaultAzureCredential
from datetime import datetime,timezone,timedelta

import tempfile
import os
import shutil

def BlobDownloadAuthN(host,container,namespace, name,provider,version):
    # blobpath = f'/v1/modules/{namespace}/{name}/{provider}/{version}/local.zip'
    bloburl = f'{host}/{container}/v1/modules/{namespace}/{name}/{provider}/{version}/local.zip'
    token_credential = DefaultAzureCredential()
    blob_client = BlobClient.from_blob_url(bloburl, credential=token_credential)  
    download_stream = blob_client.download_blob()
    return download_stream
#remove the temp dir
azblobstoragehost = "https://terrreggm.blob.core.windows.net"
azblobaccount = 'terrreggm'
azcontainer = "terrregistryblob"
# BlobDownloadAuthN(azblobstoragehost,azcontainer,'unittest','versionget','azurerm','1.0.0')
token_credential = DefaultAzureCredential()
blob_service = BlobServiceClient(azblobstoragehost, credential=token_credential)
start_utc = datetime.now(timezone.utc) - timedelta(hours=1)
end_utc = datetime.now(timezone.utc) + timedelta(hours=1)
u_d_key= blob_service.get_user_delegation_key(start_utc, end_utc,timeout = 20)
#blob = f'local.zip'
blob = r'v1/modules/unittest/versionget/azurerm/1.2.5/local.zip'
bloburl = f'{azblobstoragehost}/{azcontainer}/{blob}'


sasPerm = BlobSasPermissions(read=True,tag=False)
blobsas = generate_blob_sas(azblobaccount, azcontainer, blob, user_delegation_key=u_d_key, permission=sasPerm, expiry=end_utc, start=start_utc)
print(f'{bloburl}?{blobsas}')