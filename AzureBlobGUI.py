from flask import Flask,render_template
import os
import json
from flask_misaka import markdown,Misaka
from azure.identity import DefaultAzureCredential
from azure.storage.blob import ContainerClient

##### this is the Template jinja stuff for the webpage
app = Flask(__name__, template_folder="views")
### need this line for the Misaka markdown rendering
Misaka(app,fenced_code="true")
azblobaccountname = os.environ.get("AZBLOBACCOUNTNAME") #blobaccount
azblobstoragehost = os.environ.get("AZBLOBSTORAGEHOST") #the full url "https://blobaccount.blob.core.windows.net"
azcontainer = os.environ.get("AZCONTAINER") #container where the modules are

def ModuleslistGui(host,container):   
    token_credential = DefaultAzureCredential()
    filepath = f"v1/modules/"
    container_client = ContainerClient(host, container, credential=token_credential)
    blobs_list = container_client.list_blobs(name_starts_with=filepath) #
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
    return render_template('index.html',modules=unique, filepath=filepath)


@app.route('/') # to list all the module namespaces 
def index():
   # filepath = f'./v1/modules/'
    namespaces = ModuleslistGui(azblobstoragehost,azcontainer)
    return f'{namespaces}'