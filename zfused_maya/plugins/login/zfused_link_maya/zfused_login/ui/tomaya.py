# coding:utf-8
# --author-- lanhua.zhou

#pyside and pyside2
from qtpy import QtGui, QtWidgets, QtCore, API
if API == "pyside":
    import shiboken as shiboken
elif API == "pyside2":
    import shiboken2 as shiboken

import maya.OpenMayaUI as OpenMayaUI

def GetMayaMainWindowPoint():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(ptr), QtWidgets.QWidget)

def GetMayaLayoutPoint(layoutName):
    ptr = OpenMayaUI.MQtUtil.findLayout(layoutName)
    return shiboken.wrapInstance(long(ptr), QtWidgets.QWidget)
