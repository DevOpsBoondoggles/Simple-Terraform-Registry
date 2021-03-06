import json
from flask import Flask, abort,current_app, flash, jsonify, make_response#, redirect, request, url_for
from os import path


app = Flask(__name__)
#Service Discovery
@app.route('/.well-known/terraform.json', methods=['GET'])
def discovery():
    return {"modules.v1": "/v1/modules/"}

#Get Versions
@app.route('/v1/modules/<namespace>/<name>/<provider>/versions', methods=['GET'])
def versions(namespace, name,provider):
    filepath = 'module/' + namespace + "/" + name + "/" + provider + ".json"

    if not path.exists(filepath):
        abort(404)

    with open(filepath) as reader:
        data = json.load(reader)
   # response = { "modules" : [] }
    # for elem in data["modules"]:
    #     versions = {"version": elem["version"], "protocols": elem["protocols"], "platforms": []}
    #     # for platform in elem["platforms"]:
    #     #     version["platforms"].append({"os": platform["os"], "arch": platform["arch"]})
    #    # response["versions"].append(version)
    return data

#Download Specific Version :namespace/:name/:provider/:version/download
@app.route('/v1/modules/<namespace>/<name>/<provider>/<version>/download', methods=['GET'])
def downloadversion(namespace, name,provider,version):
    filepath = 'module/' + namespace + "/" + name + "/" + provider + "/" + version  + "/" + provider + ".zip"

    if not path.exists(filepath):
        abort(404)

    # with open(filepath) as reader:
    #     data = json.load(reader)
    response = make_response('', 204 )
    response.mimetype = current_app.config['JSONIFY_MIMETYPE']
    response.headers['X-Terraform-Get'] = filepath
    return response