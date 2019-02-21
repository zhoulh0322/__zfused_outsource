# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

""" 材质文件操作集合 """

import os

import maya.cmds as cmds
import maya.mel as mel


def delete_unused():
    #import maya.mel as mel
    mel.eval('MLdeleteUnused;')

def get_connection():
    """ material connection

    :rtype: dict
    """
    matDict = {}
    MaterialList = cmds.ls(materials = True)
    matDict = {}
    for MaterialName in MaterialList: #loop all mats
        if MaterialName in ['lambert1','particleCloud1']:
            continue
        if cmds.objExists(MaterialName + '.outColor') == True:
            ModelList = []
            NodeList = cmds.listConnections(MaterialName + '.outColor', s=0, d=1, type='shadingEngine')
            if NodeList != None:
                for NodeName in NodeList:
                    #if cmds.objectType(NodeName) ==    'shadingEngine': #already filtered
                    #~ print '\n\n\n',111,MaterialName,NodeName
                    PlugList = cmds.listConnections(NodeName, d=0,s=1, plugs=True, shapes=True)
                    #~ print 112,PlugList
                    for PlugName in PlugList:
                        PlugSplit = PlugName.split('.')
                        #~ if 'instObjGroups' in PlugSplit.split('[')[0]:
                        #~ if MaterialName == 'tou':
                            #~ print 1111,PlugName
                        for tmp in PlugSplit:
                            PlugSplit2 = tmp.split('[')[0]
                            if 'instObjGroups' in PlugSplit2:
                                #~ if MaterialName == 'tou':
                                    #~ print 222,PlugSplit2
                                ReturnedList = []
                                if cmds.objExists(PlugName + '.objectGrpCompList') == True:
                                    ReturnedList = cmds.getAttr(PlugName + '.objectGrpCompList')
                                if len(ReturnedList) == 0:
                                    ModelList.append(PlugSplit[0])
                                elif ReturnedList == [u'vtx[*]']:# todo: problem is about here or next else
                                    ModelList.append(PlugSplit[0])
                                else:
                                    FaceList = ReturnedList
                                    for FaceName in FaceList:
                                        ModelList.append(PlugSplit[0] + '.' + FaceName)
                                break
            matDict[MaterialName] = ModelList
    return matDict

def record():
    matDict = get_connection()        
    # tmpFile = cmds.file(q=1,sceneName=1)
    # cmds.file(save=1) #用于编辑材质文件后重回到模型文件
    for MaterialName in matDict:
        ModelList = matDict[MaterialName]
        if len(ModelList) != 0:
            if cmds.objExists(MaterialName + '.model') == False:
                cmds.addAttr(MaterialName,longName = 'model',dataType = 'string')
            cmds.setAttr(MaterialName + '.model',','.join(ModelList),type = 'string')