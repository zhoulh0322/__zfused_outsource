#coding:utf-8
#表情库服务器版 0.4

import os
from pymel.core import *
import studiolibrary
import zfused_maya.core.resource as resource



qtUIFile = resource.get('uis/animation/poslibrary', 'server.ui')
#qtUIFile = 'C:/Users/ning.qin/Documents/maya/2016/scripts/face_lib/face_lib_server.ui'
#character_list_path = 'P:/HQ/asset/char'
character_list_path = 'X:/BKM2/asset/char'
global face_lib_path_server



def refresh_characters_list(*args):

    character_names = []
    
    try:
        for dirname in os.listdir(character_list_path):
            #print dirname
            character_names.append(dirname)
            #print character_names
    except:
        print '服务器丢了QAQ'
    
    
    textScrollList('scene_server_characters_textScrollList', edit = True, removeAll = True)
    for name in character_names:
        if namespace( exists = name) == True:
            print name
            textScrollList('scene_server_characters_textScrollList', edit = True, append = name)
    
    textScrollList('server_characters_textScrollList', edit = True, removeAll = True)
    face_lib_path_server = textField('serverPath_lineEdit', q=True, text=True)
    for dirname in os.listdir(face_lib_path_server):
        #textScrollList('server_characters_textScrollList', edit = True, append = dirname)
        if dirname in character_names:
            textScrollList('server_characters_textScrollList', edit = True, append = dirname)

def open_lib(name):
    lock = checkBox('readonly_server_checkBox', q = True, value = True)
    face_lib_path_server = textField('serverPath_lineEdit', q=True, text=True)
    if os.path.exists(face_lib_path_server + '\\' + name) == True:
        studiolibrary.main(name = name, path = face_lib_path_server + '\\' + name, lock = lock)
    else:
        print u'没有' + name + u'的表情库'

def open_lib_scene(*args):
    
    name = textScrollList( 'scene_server_characters_textScrollList', q=True, selectItem = True )
    name = name[0]
    open_lib(name)

def open_lib_server(*args):
    
    name = textScrollList( 'server_characters_textScrollList', q=True, selectItem = True )
    name = name[0]
    open_lib(name)

def open_lib_server_root(*args):
    global face_lib_path_server
    face_lib_path_server = textField('serverPath_lineEdit', q=True, text=True)
    lock = checkBox('readonly_server_checkBox', q=True, value=True)
    if os.path.exists(face_lib_path_server) == True:
        studiolibrary.main(name=u'服务器根目录', path=face_lib_path_server, lock=lock)
    else:
        print '服务器根目录丢了QAQ'
        #os.mkdir(face_lib_path_server)
        #print u'创建了根目录'

def Ui():
    try:
        dialog_face_lib_server
    except:
        print 'create window'
    else:
        if control(dialog_face_lib_server, exists=1):
            deleteUI(dialog_face_lib_server)
    if window('window_face_lib_server', exists=1):
        deleteUI('window_face_lib_server')
    
    window_face_lib_server = window('window_face_lib_server', title=u'服务器表情库', widthHeight=(340, 400) )
    paneLayout('layout_face_lib_server', configuration = 'single')
    dialog_face_lib_server = loadUI(verbose = 1, uiFile = qtUIFile)
    control(dialog_face_lib_server, edit=True, parent='layout_face_lib_server')
    showWindow( 'window_face_lib_server' )
    
    button('refresh_server_button', edit=True, command = refresh_characters_list)
    button('lib_server_root_button', edit=True, command=open_lib_server_root)
    textScrollList( 'scene_server_characters_textScrollList', edit=True, selectCommand = open_lib_scene )
    textScrollList( 'server_characters_textScrollList', edit=True, selectCommand = open_lib_server )
    control('server_Form', edit=True, backgroundColor = [0.2,0.3,0.4])
    
    
    #checkBox('readonly_server_checkBox', edit = True, value = lock, enable = not lock)
    
    
    global face_lib_path_server
    face_lib_path_server = textField('serverPath_lineEdit', q=True, text=True)
    
    refresh_characters_list()

#Ui()