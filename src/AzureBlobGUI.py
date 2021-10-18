
from flask import Flask,render_template
import os
from flask_misaka import Misaka
from azure.identity import DefaultAzureCredential
from azure.storage.blob import ContainerClient

##### this is the Template jinja stuff for the webpage
app = Flask(__name__, template_folder="views")
### need this line for the Misaka markdown rendering
Misaka(app,fenced_code="true")
azblobaccountname = os.environ.get("AZBLOBACCOUNTNAME") #blobaccount
azblobstoragehost = os.environ.get("AZBLOBSTORAGEHOST") #the full url "https://blobaccount.blob.core.windows.net"
azcontainer = os.environ.get("AZCONTAINER") #container where the modules are

def RootBlobsList(host,container,filepath):   
    token_credential = DefaultAzureCredential()
    container_client = ContainerClient(host, container, credential=token_credential)
    blobs_list = container_client.list_blobs(name_starts_with=filepath) #
    return blobs_list



def GetBlobContent(host,container,filepath):   
    token_credential = DefaultAzureCredential()
    container_client = ContainerClient(host, container, credential=token_credential)
    blob_client = container_client.get_blob_client(filepath)
    stream = blob_client.download_blob()
    return stream.content_as_text()

def NamespaceBlobList(blobs_list,filepath):
    x = []
    start = len(filepath) #get the end of the standard path. start of the module name
    #e.g. 'v1/modules/unittest/versionget/azurerm/1.0.0/local.zip'
    for blob in blobs_list:
        #this whole shenanigans is to loop through the blob names and strip out the part needed
        total = len(blob.name) #blob has multiple attributes so we specify name
        stringback = blob.name[start:total]  #e.g. 'unittest/versionget/azurerm/1.0.0/local.zip'
        end = stringback.index('/') #find first / 'unittest/ <<<<<<'
        word = stringback[0:end] #go from start of stripped string to the first / 'unittest'
        x.append(word) #dig in and loop into versions
    unique = list(dict.fromkeys(x))#this bit basically makes a dictionary to get only unique values and then converts back to a list
    return unique

@app.route('/') # to list all the module namespaces 
def index():
    filepath = f'v1/modules/'
    rootblobs = RootBlobsList(azblobstoragehost,azcontainer,filepath)
    namespaces = NamespaceBlobList(rootblobs,filepath)
    return render_template('index.html',modules=namespaces, filepath=filepath)
    

@app.route('/v1/modules/<namespace>/', methods=['GET']) # list all the modules in a namespace
def modulenamelist(namespace):
    basefilepath = f'v1/modules/'
    filepath = f'{basefilepath}{namespace}/'
    rootblobs = RootBlobsList(azblobstoragehost,azcontainer,filepath)
    namespaces = NamespaceBlobList(rootblobs,filepath)
    return render_template('namespace.html',modules=namespaces, filepath=basefilepath)

@app.route('/v1/modules/<namespace>/<name>/', methods=['GET']) # list all the modules in a namespace
def providerlist(namespace,name):
    basefilepath = f'v1/modules/'
    filepath = f'{basefilepath}{namespace}/{name}/'
    rootblobs = RootBlobsList(azblobstoragehost,azcontainer,filepath)
    namespaces = NamespaceBlobList(rootblobs,filepath)
    return render_template('namespace.html',modules=namespaces, filepath=basefilepath)

@app.route('/v1/modules/<namespace>/<name>/<provider>/', methods=['GET']) # list all the modules in a namespace
def versionlist(namespace,name,provider):
    basefilepath = f'v1/modules/'
    filepath = f'{basefilepath}{namespace}/{name}/{provider}/'
    rootblobs = RootBlobsList(azblobstoragehost,azcontainer,filepath)
    namespaces = NamespaceBlobList(rootblobs,filepath)
    return render_template('namespace.html',modules=namespaces, filepath=basefilepath)

@app.route('/v1/modules/<namespace>/<name>/<provider>/<version>/', methods=['GET'])
def load_readme(namespace, name,provider,version):
    filepath = f'v1/modules/{namespace}/{name}/{provider}/{version}'
    readmecontent = GetBlobContent(azblobstoragehost,azcontainer,f'{filepath}/readme.md')
    # with open(f'{filepath}/readme.md', 'r') as f:
    #     content = f.read()
    return render_template("readme.html",text=readmecontent, title=f'Readme for {namespace}/{name}/{provider}/{version}')
  