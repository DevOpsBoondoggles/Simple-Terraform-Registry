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
    blobs_list = container_client.list_blobs() #name_starts_with=filepath
    x = []
    for blob in blobs_list:
        x.append(blob.name) #dig in and loop into versions
    return  x


@app.route('/') # to list all the module namespaces 
def index():
   # filepath = f'./v1/modules/'
    namespaces = ModuleslistGui(azblobstoragehost,azcontainer)
    return f'{namespaces}'
    #return render_template('index.html',modules=namespaces, filepath=filepath)