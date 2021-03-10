import json
import versiongetter
from AzureBlobBackend import BlobVersionsGet
from flask import Flask, abort,current_app, flash, jsonify, make_response, send_file#, redirect, request, url_for
from os import path

app = Flask(__name__)
azblobstoragehost = "https://terrreggm.blob.core.windows.net/"
azcontainer = "terrregistryblob"
#Service Discovery
@app.route('/.well-known/terraform.json', methods=['GET'])
def discovery():
    return {"modules.v1": "/v1/modules/"}

#Get Versions
@app.route('/v1/modules/<namespace>/<name>/<provider>/versions', methods=['GET'])
def versions(namespace, name,provider):
    filepath = './v1/modules/' + namespace + "/" + name + "/" + provider + "/"
    if not path.exists(filepath):
        abort(404)
    return BlobVersionsGet(azblobstoragehost,azcontainer,namespace,name,provider)

#need to actually send the file
@app.route('/v1/modules/<namespace>/<name>/<provider>/<version>/local.zip', methods=['GET'])
def downloadfile(namespace, name,provider,version):
    filepath = f'{azblobstoragehost}/{azcontainer}/v1/modules/{namespace}/{name}/{provider}/{version}/local.zip'
    if not path.exists(filepath):
        abort(404)
    return send_file(filepath)