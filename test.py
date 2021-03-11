from azure.storage.blob import BlobClient
from azure.storage.blob import ContainerClient
from azure.identity import DefaultAzureCredential
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
# azblobstoragehost = "https://terrreggm.blob.core.windows.net"
# azcontainer = "terrregistryblob"
# BlobDownloadAuthN(azblobstoragehost,azcontainer,'unittest','versionget','azurerm','1.0.0')