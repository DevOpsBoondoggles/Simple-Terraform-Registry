import json
import versiongetter
from flask import Flask, abort,current_app, flash, jsonify, make_response, send_file#, redirect, request, url_for
from os import path


app = Flask(__name__)
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
    x = '{"modules": [{"versions": []}]}'
    y =  json.loads(x)  #turn string above json python object
    data = versiongetter.folderlist(filepath) #get all the directories (the version folders)
    for module in y['modules']:
            for ver in data:
                module['versions'].append({'version' : ver}) #dig in and loop into versions
    return  json.dumps(y)

#Download Specific Version :namespace/:name/:provider/:version/download
@app.route('/v1/modules/<namespace>/<name>/<provider>/<version>/download', methods=['GET'])
def downloadversion(namespace, name,provider,version):
    filepath = './v1/modules/' + namespace + "/" + name + "/" + provider + "/" + version  + "/" + "local.zip"
    file = f'./local.zip'
    if not path.exists(filepath):
        abort(404)
    response = make_response('', 204 )
    response.mimetype = current_app.config['JSONIFY_MIMETYPE']
    response.headers['X-Terraform-Get'] = file
    return response

#need to actually download the file when called by Terraform.
@app.route('/v1/modules/<namespace>/<name>/<provider>/<version>/local.zip', methods=['GET'])
def downloadfile(namespace, name,provider,version):
    filepath = './v1/modules/' + namespace + "/" + name + "/" + provider + "/" + version  + "/" + "local.zip"
    if not path.exists(filepath):
        abort(404)
    return send_file(filepath)