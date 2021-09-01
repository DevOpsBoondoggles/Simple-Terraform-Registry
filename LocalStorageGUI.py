from flask import Flask,render_template
from os import path
from flask_misaka import markdown,Misaka
from LocalStorageBackend import folderlist

##### this is the Template jinja stuff for the webpage
app = Flask(__name__, template_folder="views")
### need this line for the Misaka markdown rendering
Misaka(app,fenced_code="true")

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

