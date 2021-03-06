import versiongetter
import json
#from flask import jsonify
data = versiongetter.folderlist("./v1/modules/unittest/versionget/local")
x = '''
{
    "modules": [
       {
            "versions": [
            ]
       }
    ]
}
'''
y =  json.loads(x)  
#data2 = json.dumps(x)
for module in y['modules']:
        for ver in data:
            module['versions'].append({'version' : ver})
print(json.dumps(y,indent=2))
#print(y['modules'])