from azure.storage.blob import BlobClient,ContainerClient,BlobServiceClient,generate_blob_sas,BlobSasPermissions
from azure.identity import DefaultAzureCredential
from datetime import datetime,timezone,timedelta
import tempfile


def BlobDownloadAuthN(host,container,namespace, name,provider,version):
    # blobpath = f'/v1/modules/{namespace}/{name}/{provider}/{version}/local.zip'
    bloburl = f'{host}/{container}/v1/modules/{namespace}/{name}/{provider}/{version}/local.zip'
    token_credential = DefaultAzureCredential()
    blob_client = BlobClient.from_blob_url(bloburl, credential=token_credential)  
    download_stream = blob_client.download_blob()
    return download_stream

def BlobSASUri(host,account,container,namespace, name,provider,version):
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

