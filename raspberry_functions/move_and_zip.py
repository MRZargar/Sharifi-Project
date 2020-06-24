import os
import zipfile
import shutil

def zip_move(name):
    path = "sent/"
    try:
        import zlib
        mode= zipfile.ZIP_DEFLATED
    except:
        mode= zipfile.ZIP_STORED
    try:
        name = int(name[:-4])
    except Exception as ex:
        print(ex)
    try:
        zipfile.ZipFile(str(name) + ".zip", 'w', mode).write(str(name) + ".txt")
        shutil.move(str(name) + ".zip", path + str(name) + ".zip")
        os.remove(str(name) + ".txt")
    except OSError:
        os.remove(str(name) + ".zip")
        print(" Can not create zip file or move or remove %s file"% (str(name) +'.txt')) 


import os
## make directory sented
path = "sent"

if os.path.isdir("sent"):
    print("directory has exist")

else:
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

## create Zip file and move in sent directory

name = ''  # for example name = '2110910800.txt'
zip_move(name)
