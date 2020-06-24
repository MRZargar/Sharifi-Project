import os
import zipfile
import shutil

def zip_move(file_names, path):
    path = path +"/"
    try:
        import zlib
        mode= zipfile.ZIP_DEFLATED
    except:
        mode= zipfile.ZIP_STORED
    for name in file_names:
        name = int(name[:-4])
        try:
            zipfile.ZipFile(str(name) + ".zip", 'w', mode).write(str(name) + ".txt")
            shutil.move(str(name) + ".zip", path + str(name) + ".zip")
            os.remove(str(name) + ".txt")
        except OSError:
            os.remove(str(name) + ".zip")
            print(" Can not create zip file or move or remove %s file"% (str(name) +'.txt')) 

path = 'sent'
## create Zip file
name = ['2110910800.txt', '2110907200.txt']
zip_move(name, path)
