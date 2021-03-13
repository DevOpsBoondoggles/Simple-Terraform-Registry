# Simple Terraform Registry
First bash at making a Terraform Private Module Registry with either local or Azure Blob Storage backend.

This is written in Python by very much a novice.
It's not perfect but my aim is to eventually have a very simple to deploy terraform registry, deployed via terraform and all automatic testing etc.
I wrote this because I couldn't find an opensource registry written in Python that let you have an Azure Blob backend.

### However, it works!  
It is the minimal API required to work.
As per:
https://www.terraform.io/docs/internals/module-registry-protocol.html


I have this running in a free tier Azure Web App Service and terraform can download from it with full Registry syntax. 

Like so:

![image](https://user-images.githubusercontent.com/25871665/111051557-d7a10600-844b-11eb-8355-4fb2043e7c6d.png)

### Bad Parts
I haven't configured any choice in how to setup the folder structure.
It **must** be:

```
V1/Modules/Namespace/Name/Provider/x.x.x/local.zip 
```
with x.x.x being semantic versioning. 

I have included a couple of empty sample modules to show the file system setup.

**The zip file with the .tfs HAS to be 'local.zip' at present.**

I do want to add extra backends eventually and more fluidity in names / zip format. 

Inside the host of the files the path needs to be like the below for modules.

```
Examples:
unittest = namespace
versionget = name
azurerm / local = providers 
1.0.0 = version
```
filepaths like so: 
```
<host>/v1/modules/unittest/versionget/azurerm/1.1.0/local.zip
<host>/v1/modules/unittest/versionget/azurerm/1.0.0/local.zip
<host>/v1/modules/unittest/versionget/local/1.0.0/local.zip
```

So if you were on a linux webapp in Azure:
```
/home/site/wwwroot - host
```
so files have to be
```
/home/site/wwwroot/v1/modules/unittest/versionget/azurerm/1.1.0/local.zip
```

If you're using Azure blob storage backend:

```
files will be in a container and then the same file path so:

https://blobaccount.blob.core.windows.net/azcontainer/v1/modules/unittest/versionget/azurerm/1.1.0/local.zip
```

You also need to set the environment variables:

```
#set your backend
modulebackend = os.environ.get("MODULEBACKEND") #azureblob or blank

#check and import pieces for azure blob storage
if modulebackend == 'azureblob':
    #These need set if you're using azure backend 
    azblobaccountname = os.environ.get("AZBLOBACCOUNTNAME") #blobaccount
    azblobstoragehost = os.environ.get("AZBLOBSTORAGEHOST") #the full url "https://blobaccount.blob.core.windows.net"
    azcontainer = os.environ.get("AZCONTAINER") #container where the modules are
```

You can then set these in your app config for a web app host.

![image](https://user-images.githubusercontent.com/25871665/111051740-5185bf00-844d-11eb-8b39-f65a6933a5c9.png)


### Backend Options

If you're going local, no problem, deploy the above to a webapp (you can fork and then use Deployment Centre as the maximum easy mode!).

![image](https://user-images.githubusercontent.com/25871665/111052022-49c71a00-844f-11eb-821c-72e5fc9135ab.png)


If you're doing Blob Storage as backend, as well as doing the environment variable options above, you need to give your Web App a system assigned managed identity and also give it (and yourself!) the role of Storage Blob Data Reader on the storage account you want to host the files in and make sure that it's set to Azure AD auth. 
See the following pictures. 

I use AzureDefaultCredential for the auth, so when it's running on a system managed identity it uses that, when you run locally it uses either an SP you set into environment variables or other options as per:
https://docs.microsoft.com/en-us/python/api/azure-identity/azure.identity.defaultazurecredential?view=azure-python

Remember if you're running it locally via python -m Flask run, it's only http, Terraform REQUIRES https, so use ngrok or something to get an HTTPS. 
Hopefully you won't need to and this will all work though. 

![image](https://user-images.githubusercontent.com/25871665/111052032-65322500-844f-11eb-856d-0afbc9dee413.png)

![image](https://user-images.githubusercontent.com/25871665/111052067-ae827480-844f-11eb-82e2-e4d352bc033d.png)

![image](https://user-images.githubusercontent.com/25871665/111052093-edb0c580-844f-11eb-901a-7e3274ae39fa.png)


