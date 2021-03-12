import json
import versiongetter
from flask import Flask, abort,current_app, flash, jsonify, make_response, send_file#, redirect, request, url_for
from os import path
import os

def folderlist(filepath):
    dirList = os.listdir(filepath) # current directory
    dirOnly = []
    for dir in dirList:
        dirPath = f'{filepath}/{dir}'
        if path.isdir(dirPath) == True:
            if not dir.startswith("."): 
                dirOnly.append(dir)
    return dirOnly

def VersionGet(namespace,name,provider): 
    filepath = './v1/modules/' + namespace + "/" + name + "/" + provider + "/"
    if not path.exists(filepath):
        abort(404)
    x = '{"modules": [{"versions": []}]}'
    y =  json.loads(x)  #turn string above json python object
    data = folderlist(filepath) #get all the directories (the version folders)
    for module in y['modules']:
            for ver in data:
                module['versions'].append({'version' : ver}) #dig in and loop into versions
    return  json.dumps(y)

def XHeader(namespace, name,provider,version):
    filepath = './v1/modules/' + namespace + "/" + name + "/" + provider + "/" + version  + "/" + "local.zip"
    file = f'./local.zip'
    response = make_response('', 204 )
    response.mimetype = current_app.config['JSONIFY_MIMETYPE']
    response.headers['X-Terraform-Get'] = file
    return response

#need to actually download the file when called by Terraform.
def DownloadFile(namespace, name,provider,version):
    filepath = './v1/modules/' + namespace + "/" + name + "/" + provider + "/" + version  + "/" + "local.zip"
    if not path.exists(filepath):
        abort(404)
    return send_file(filepath)