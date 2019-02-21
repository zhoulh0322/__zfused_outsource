# coding:utf-8
# --author-- lanhua.zhou

#pyside and pyside2
from qtpy import QtGui, QtWidgets, QtCore, API
if API == "pyside":
    import shiboken as shiboken
elif API == "pyside2":
    import shiboken2 as shiboken

import maya.cmds as cmds
import maya.OpenMayaUI as OpenMayaUI

def GetMayaMainWindowPoint():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(ptr), QtWidgets.QWidget)

def GetMayaLayoutPoint(layoutName):
    ptr = OpenMayaUI.MQtUtil.findLayout(layoutName)
    return shiboken.wrapInstance(long(ptr), QtWidgets.QWidget)

def GetMayaPoint(mayaName):
    """
    Convert a Maya ui path to a Qt object
    @param mayaName: Maya UI Path to convert (Ex: "scriptEditorPanel1Window|TearOffPane|scriptEditorPanel1|testButton" )
    @return: PyQt representation of that object
    """
    ptr = OpenMayaUI.MQtUtil.findControl(mayaName)
    if ptr is None:
        ptr = OpenMayaUI.MQtUtil.findLayout(mayaName)
    if ptr is None:
        ptr = OpenMayaUI.MQtUtil.findMenuItem(mayaName)
    if ptr is not None:
        return shiboken.wrapInstance(long(ptr), QtCore.QObject)

def BuiltInMaya(qt_widget):
    layout = cmds.formLayout()
    qtobj = shiboken.wrapInstance(long(OpenMayaUI.MQtUtil.findLayout(layout)), QtCore.QObject)
    qtobj.children()[0].layout().addWidget(qt_widget)
    child = cmds.formLayout(layout, q = True, childArray =True)
    cmds.formLayout(layout, edit=True, attachForm=[(child[0], 'right', 0), (child[0], 'left', 0),(child[0], 'top', 0),(child[0], 'bottom', 0)])
    cmds.setParent('..')
    return layout


'''
# -----------------------------------------------
import menuinterface
import contentinterface
import projectinterface
import userinterface


def content_interface():
    _ptr = OpenMayaUI.MQtUtil.findControl("zfused_maya_content_interface")
    _interface = shiboken.wrapInstance(long(_ptr), contentinterface.contentguide.ContentGuide)
    return _interface

'''