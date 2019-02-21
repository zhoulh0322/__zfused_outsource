# coding:utf-8
#--author-- lanhua.zhou
from __future__ import print_function

import os
import glob
import shutil
import py_compile 

localPath = os.path.dirname(os.path.dirname(__file__))
serverPath = r"//td/zfused/zfused_outsource/zfused_maya"

def bianli(path):
    _file_list = os.listdir(path)
    for i in _file_list:
        print(i)
        path_new = os.path.join(path,i)
        if os.path.isfile(path_new):
            print(path_new)
            #copy file
            if path_new.endswith(".py"):
                py_compile.compile(path_new)
                ser_path = path_new.replace(localPath,serverPath).replace(".py",".pyc")
                if not os.path.isdir(os.path.dirname(ser_path)):
                    #print os.path.dirname(ser_path)
                    os.makedirs(os.path.dirname(ser_path))
                try:
                    shutil.copy(path_new, ser_path)
                except:
                    pass
            elif path_new.endswith(".svn") or path_new.endswith(".svn-base"):
                pass
            else:
                #copy
                ser_path = path_new.replace(localPath,serverPath)
                if not os.path.isdir(os.path.dirname(ser_path)):
                    #print os.path.dirname(ser_path)
                    os.makedirs(os.path.dirname(ser_path))
                try:
                    shutil.copy(path_new, ser_path)
                except:
                    pass
        if os.path.isdir(path_new):
            if path_new.endswith("__pycache__"):
                #os.removedirs(path_new)
                #import shutil
                shutil.rmtree(path_new)
            else:
                bianli(path_new)
    
bianli(localPath)