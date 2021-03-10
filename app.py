import json
import requests
import versiongetter
from AzureBlobBackend import BlobVersionsGet
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
    response = BlobVersionsGet(azblobstoragehost,azcontainer,namespace,name,provider)
    return f'{response}'

#Download Specific Version :namespace/:name/:provider/:version/download
@app.route('/v1/modules/<namespace>/<name>/<provider>/<version>/download', methods=['GET'])
def downloadversion(namespace, name,provider,version):
    blobpath = f'{azblobstoragehost}/{azcontainer}/v1/modules/{namespace}/{name}/{provider}/{version}/local.zip'
    # request = requests.get(blobpath)
    # if request.status_code >= 400:
    #     abort(404)
    response = make_response('', 204 )
    response.mimetype = current_app.config['JSONIFY_MIMETYPE']
    response.headers['X-Terraform-Get'] = blobpath
    return f'{blobpath}'
    
#need to actually send the file
@app.route('/v1/modules/<namespace>/<name>/<provider>/<version>/local.zip', methods=['GET'])
def downloadfile(namespace, name,provider,version):
    filepath = f'{azblobstoragehost}/{azcontainer}/v1/modules/{namespace}/{name}/{provider}/{version}/local.zip'
    request = requests.get(filepath)
    if request.status_code >= 400:
        abort(404)
    return redirect(filepath)