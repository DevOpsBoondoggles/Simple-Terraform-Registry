import os

def folderlist(filepath):
    dirList = os.listdir(filepath) # current directory
    dirOnly = []
    for dir in dirList:
        dirPath = f'{filepath}/{dir}'
        if os.path.isdir(dirPath) == True:
            if not dir.startswith("."): 
                dirOnly.append(dir)
    return dirOnly


