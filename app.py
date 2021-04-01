import json
import os
from flask import Flask, abort,current_app, flash, jsonify, make_response, send_file, redirect,render_template
from os import path
from flask_misaka import markdown,Misaka

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
    az_env_variables = [azblobstoragehost,azblobaccountname,azcontainer]
    for envvar in az_env_variables:
        if not envvar:
            raise ValueError(f'missing Azure environment variable')
else:
    from LocalStorageBackend import VersionGet,DownloadFile,XHeader,folderlist


def get_namespaceslocal(filepath):
    content = list(((folderlist(filepath))))
    return content


@app.route('/') # to list all the module namespaces 
def index():
    filepath = f'./v1/modules/'
    namespaces = get_namespaceslocal(filepath)
    return render_template('index.html',modules=namespaces, filepath=filepath)

@app.route('/v1/modules/<namespace>/', methods=['GET']) # list all the modules in a namespace
def namespaceselect(namespace):
    filepath = f'./v1/modules/{namespace}'
    namespaces = get_namespaceslocal(filepath)
    return render_template('namespace.html',modules=namespaces, filepath=filepath)

@app.route('/v1/modules/<namespace>/<name>/', methods=['GET']) # list the providers of a particular module
def moduleselect(namespace,name):
    filepath = f'./v1/modules/{namespace}/{name}'
    namespaces = get_namespaceslocal(filepath)
    return render_template('modules.html',modules=namespaces, filepath=filepath)

@app.route('/v1/modules/<namespace>/<name>/<provider>/', methods=['GET']) # list the versions of a module for a given provider
def providerselect(namespace,name,provider):
    filepath = f'./v1/modules/{namespace}/{name}/{provider}'
    namespaces = get_namespaceslocal(filepath)
    return render_template('provider.html',modules=namespaces, filepath=filepath)

#Renders the Readme.md from the verion folder
@app.route('/v1/modules/<namespace>/<name>/<provider>/<version>/', methods=['GET'])
def load_readme(namespace, name,provider,version):
    filepath = f'./v1/modules/{namespace}/{name}/{provider}/{version}'
    with open(f'{filepath}/readme.md', 'r') as f:
        content = f.read()
    return render_template("readme.html",text=content, title=f'Readme for {namespace}/{name}/{provider}/{version}')

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