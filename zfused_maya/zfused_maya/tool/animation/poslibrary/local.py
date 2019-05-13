#coding:utf-8
#表情库本地版 0.4

from pymel.core import *
import os
import zfused_maya.tool.animation.studiolibrary as studiolibrary
import zfused_maya.core.resource as resource

qtUIFile = resource.get('uis/animation/poslibrary', 'local.ui')
#character_list_path = 'P:/HQ/asset/char'
character_list_path = 'X:/BKM2/asset/char'
global face_lib_path

def refresh_characters_list(*args):
    global face_lib_path
    face_lib_path = textField('localPath_lineEdit', q=True, text=True)
    
    character_names = []
    try:
        for dirname in os.listdir(character_list_path):
            character_names.append(dirname)
		# print character_names
    except:
        print u'服务器丢了QAQ'

    textScrollList('scene_characters_textScrollList', edit=True, removeAll=True)
    for name in character_names:
        if namespace(exists=name) == True:
            #print name
            textScrollList('scene_characters_textScrollList', edit=True, append=name)

    textScrollList('local_characters_textScrollList', edit=True, removeAll=True)
    for dirname in os.listdir(face_lib_path):
        if dirname in character_names:
            textScrollList('local_characters_textScrollList', edit=True, append=dirname)

def open_lib(name):
    lock = checkBox('readonly_local_checkBox', q=True, value=True)
    # print name
    # print lock
    if os.path.exists(face_lib_path + '\\' + name) == True:
        studiolibrary.main(name=name, path=face_lib_path + '\\' + name, lock=lock)
    else:
        print u'没有' + name + u'的表情库'

def open_lib_scene(*args):
    name = textScrollList('scene_characters_textScrollList', q=True, selectItem=True)
    name = name[0]
    open_lib(name)

def open_lib_local(*args):
    name = textScrollList('local_characters_textScrollList', q=True, selectItem=True)
    name = name[0]
    open_lib(name)

def open_lib_local_root(*args):
    global face_lib_path
    face_lib_path = textField('localPath_lineEdit', q=True, text=True)
    lock = checkBox('readonly_local_checkBox', q=True, value=True)
    if os.path.exists(face_lib_path) == True:
        studiolibrary.main(name=u'本地根目录', path=face_lib_path, lock=lock)
    else:
        os.mkdir(face_lib_path)
        print u'创建了根目录'
        '''
        try:
            for dirname in os.listdir(character_list_path):
                os.mkdir(face_lib_path + '\\' + dirname)
    	        print u'创建了' + face_lib_path + u'\\' + dirname
        except:
            print u'服务器丢了QAQ'
        '''

def Ui():
    try:
        dialog_face_lib_local
    except:
        print 'create window'
    else:
        if control(dialog_face_lib_local, exists=1):
            deleteUI(dialog_face_lib_local)
    if window('window_face_lib_local', exists=1):
        deleteUI('window_face_lib_local')


    window_face_lib_local = window('window_face_lib_local', title=u'本地表情库', widthHeight=(340, 400))
    paneLayout('layout_face_lib_local', configuration = 'single')
    dialog_face_lib_local = loadUI(verbose=1, uiFile=qtUIFile)
    control(dialog_face_lib_local, edit=True, parent='layout_face_lib_local')
    showWindow(window_face_lib_local)


    button('refresh_button', edit=True, command=refresh_characters_list)
    button('lib_local_root_button', edit=True, command=open_lib_local_root)
    textScrollList('scene_characters_textScrollList', edit=True, selectCommand=open_lib_scene)
    textScrollList('local_characters_textScrollList', edit=True, selectCommand=open_lib_local, preventOverride = True)
	
    #global face_lib_path
    #face_lib_path = textField('localPath_lineEdit', q=True, text=True)

    refresh_characters_list()

#Ui()