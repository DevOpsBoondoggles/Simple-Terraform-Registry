import os

def folderlist(filepath):
    dirList = os.listdir(filepath) # current directory
    for dir in dirList:
        dirPath = f'{filepath}/{dir}'
        if os.path.isdir(dirPath) == True:
            if not dir.startswith("."):
               print(dir)

folderlist("./module/unittest/versionget/local")

    #  else:
    # I got file and i can regexp if it is .htm|html