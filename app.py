import json
import requests
import versiongetter
import shutil
import os
import tempfile #1
from test import BlobDownloadAuthN
from azure.storage.blob import BlobClient
from azure.storage.blob import ContainerClient
from azure.identity import DefaultAzureCredential
from AzureBlobBackend import BlobVersionsGet,BlobVersionsGetAuthN
from flask import Flask, abort,current_app, flash, jsonify, make_response, send_file, redirect#, request, url_for
from os import path


app = Flask(__name__)
azblobstoragehost = "https://terrreggm.blob.core.windows.net"
azcontainer = "terrregistryblob"
#Service Discovery
@app.route('/.well-known/terraform.json', methods=['GET'])
def discovery():
    return {"modules.v1": "/v1/modules/"}

#Get Versions
@app.route('/v1/modules/<namespace>/<name>/<provider>/versions', methods=['GET'])
def versions(namespace, name,provider):
    # filepath = './v1/modules/' + namespace + "/" + name + "/" + provider + "/"
    # if not path.exists(filepath):
    #     abort(404)
    response = BlobVersionsGetAuthN(azblobstoragehost,azcontainer,namespace,name,provider)
    return f'{response}'

#Download Specific Version :namespace/:name/:provider/:version/download
@app.route('/v1/modules/<namespace>/<name>/<provider>/<version>/download', methods=['GET'])
def downloadversion(namespace, name,provider,version):
    blobpath = f'/v1/modules/{namespace}/{name}/{provider}/{version}/local.zip'
    response = make_response('', 204 )
    response.mimetype = current_app.config['JSONIFY_MIMETYPE']
    response.headers['X-Terraform-Get'] = blobpath
    return response
    
#need to actually send the file
@app.route('/v1/modules/<namespace>/<name>/<provider>/<version>/local.zip', methods=['GET'])
def downloadfile(namespace, name,provider,version):
    bloburl = f'{azblobstoragehost}/{azcontainer}/v1/modules/{namespace}/{name}/{provider}/{version}/local.zip'
    token_credential = DefaultAzureCredential()
    blob_client = BlobClient.from_blob_url(bloburl, credential=token_credential)  
    download_stream = blob_client.download_blob()
    # create a temporary directory using the context manager
    f = tempfile.TemporaryDirectory(dir = "temp")
    #f = tempfile.mkdtemp(dir = "temp") #this one works
    with open(f'{f}/local.zip', "wb") as my_blob:
        download_stream = blob_client.download_blob()
        my_blob.write(download_stream.readall())
    return send_file(f'{my_blob.name}')
     

# #Get Versions
# @app.route('/v1/modules/cleartemp', methods=['GET'])
# def cleartemp():
#     dir = 'temp'
#     shutil.rmtree(dir)
#     os.makedirs(dir)
#     open(f'{dir}/placeholder.txt',"w+")
#     return f'cleared temp'