import json
import os
from flask import Flask, redirect
from os import path
from flask_misaka import Misaka

##### this is the Template jinja stuff for the webpage
app = Flask(__name__, template_folder="views")
### need this line for the Misaka markdown rendering
Misaka(app,fenced_code="true")



#set your backend using environment variables
modulebackend = os.environ.get("MODULEBACKEND") #azureblob or blank

#check and import pieces for azure blob storage
if modulebackend == 'azureblob':
    #These need set if you're using azure backend
    azblobaccountname = os.environ.get("AZBLOBACCOUNTNAME") #blobaccount
    azblobstoragehost = os.environ.get("AZBLOBSTORAGEHOST") #the full url "https://blobaccount.blob.core.windows.net"
    azcontainer = os.environ.get("AZCONTAINER") #container where the modules are
    from azure.storage.blob import BlobClient,ContainerClient
    from azure.identity import DefaultAzureCredential
    from AzureBlobBackend import VersionGet,DownloadFile,XHeader
    from AzureBlobGUI import *
    az_env_variables = [azblobstoragehost,azblobaccountname,azcontainer]
    for envvar in az_env_variables:
        if not envvar:
            raise ValueError(f'missing Azure environment variable')
else:
    from LocalStorageBackend import VersionGet,DownloadFile,XHeader
    from LocalStorageGUI import *




#Service Discovery
@app.route('/.well-known/terraform.json', methods=['GET'])
def discovery():
    return {"modules.v1": "/v1/modules/"}

#Get Versions
@app.route('/v1/modules/<namespace>/<name>/<provider>/versions', methods=['GET'])
def get_versions(namespace, name,provider):
    if modulebackend == 'azureblob':
        response = VersionGet(azblobstoragehost,azcontainer,namespace,name,provider)
    else:
        response = VersionGet(namespace,name,provider)
    return f'{response}'

#Download Specific Version :namespace/:name/:provider/:version/download
@app.route('/v1/modules/<namespace>/<name>/<provider>/<version>/download', methods=['GET'])
def download_version(namespace, name,provider,version):
    return XHeader(namespace, name,provider,version)

#need to actually send the file
@app.route('/v1/modules/<namespace>/<name>/<provider>/<version>/local.zip', methods=['GET'])
def download_file(namespace, name,provider,version):
    if modulebackend == 'azureblob':
        return redirect(DownloadFile(azblobstoragehost,azblobaccountname,azcontainer, namespace,name,provider,version))
    else:
        return DownloadFile(namespace, name,provider,version)

if os.environ.get("ISCONTAINER"):
    app.run(host='0.0.0.0', port=80)
else:
    if __name__ == "__main__":
        app.run()
