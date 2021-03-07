import requests
import json
import xml.etree.ElementTree as ET
uri = 'https://terrreggm.blob.core.windows.net/terrregistryblob/?comp=list'
#downloaduri = 'https://terrreggm.blob.core.windows.net/terrregistryblob/v1/modules/unittest/versionget/azurerm/1.0.0/local.zip'
response = requests.get(uri)
tree = ET.parse(response.content)
root = tree.getroot()
for child in root:
    print(child.tag, child.attrib)
