import os
import zipfile
import shutil

path = "sent/"

def zip_move(name):
    try:
        import zlib
        mode= zipfile.ZIP_DEFLATED
    except:
        mode= zipfile.ZIP_STORED
    try:
        name = int(name[:-4])
    except Exception as ex:
        print(">> move_and_zip / error:  Can not convert name file to integer.\n", ex)
    try:
        zipfile.ZipFile(str(name) + ".zip", 'w', mode).write(str(name) + ".txt")
        shutil.move(str(name) + ".zip", path + str(name) + ".zip")
        os.remove(str(name) + ".txt")
    except OSError:
        os.remove(str(name) + ".zip")
        print(">> move_and_zip / error:  Can not create zip file or move or remove %s file"% (str(name) +'.txt')) 


if os.path.isdir(path):
    print(">> move_and_zip / info:  Directory has exist")
else:
    try:
        os.mkdir(path)
    except OSError:
        print (">> move_and_zip / error:  Creation of the directory %s failed" % path)
    else:
        print (">> move_and_zip / info:  Successfully created the directory %s " % path)

## create Zip file and move in sent directory

name = ''  # for example name = '2110910800.txt'
zip_move(name)
