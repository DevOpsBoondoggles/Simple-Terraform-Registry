# TerraformRegistry
First bash at making a Terraform Private Module Registry.
This is written in python by very much a novice.
It is janky and bit annoying.

### However, it works!  
It is the minimal API required to work.

As per:
https://www.terraform.io/docs/internals/module-registry-protocol.html


I have this running in a free tier Azure Web App Service and terraform can download from it with full Registry syntax. 

### Bad Parts
You do have to store the modules on the App Service storage but they're small.
You can SFTP the modules in and redeploying the webapp won't break them.
I have included a couple of sample modules to show the file system setup.


**The zip file with the .tfs HAS to be 'local.zip' at present.**

**This is still a WIP / Barebones / MVP.**

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