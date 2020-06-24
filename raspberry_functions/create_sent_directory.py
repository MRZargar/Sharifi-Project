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
