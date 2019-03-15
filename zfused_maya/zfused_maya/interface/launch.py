# coding:utf-8
# --author-- lanhua.zhou

import sys
import logging

from qtpy import QtGui, QtWidgets, QtCore, API
if API == "pyside":
    import shiboken
elif API == "pyside2":
    import shiboken2 as shiboken

import maya.cmds as cmds
import maya.mel as mm
import maya.OpenMayaUI as OpenMayaUI

import zfused_maya.interface.projectinterface.projectguide as projectguide
import zfused_maya.interface.menuinterface.menubar as menubar
import zfused_maya.interface.tomaya as tomaya

from . import plugins

logger = logging.getLogger(__name__)


def repair():
    logger.info("repair zfused maya interface")

    
    if cmds.toolBar("zfused_maya_project", q=True, ex=True):
        cmds.deleteUI("zfused_maya_project")

    
    if cmds.toolBar("zfused_maya_content", q=True, ex=True):
        cmds.deleteUI("zfused_maya_content")
    

    mm.eval("ShowAttributeEditorOrChannelBox;")
    mm.eval("RestoreUIElements;")
    mm.eval("restoreMainWindowComponents;")


def load():
    logger.info("load zfused maya interface")

    
    if cmds.toolBar("zfused_maya_project", q=True, ex=True):
        cmds.deleteUI("zfused_maya_project")
    
    if cmds.toolBar("zfused_maya_content", q=True, ex=True):
        cmds.deleteUI("zfused_maya_content")
    
    mm.eval("ShowAttributeEditorOrChannelBox;")
    mm.eval("RestoreUIElements;")
    mm.eval("restoreMainWindowComponents;")

    _main_window = tomaya.GetMayaMainWindowPoint()
    #tool_win = tool_ui.Ui()

    """
    # content guide
    content_win = contentguide.ContentGuide()
    obj_content = tomaya.BuiltInMaya(content_win)
    allowedAreas = ['left', "right"]
    cmds.toolBar("zfused_maya_content", area = 'right',
                 content = obj_content, allowedArea = allowedAreas, visible = False)
    """

    # project guide
    project_win = projectguide.ProjectGuide()
    obj_project = tomaya.BuiltInMaya(project_win)
    allowedAreas = ['top', "bottom"]
    cmds.toolBar("zfused_maya_project", area = 'top',
                 content = obj_project, allowedArea = allowedAreas)

    
    # reload menu
    menubar.rebuild()

    # load setting
    mm.eval("refreshPauseButtonCmd 0")


    # plugins path
    plugins.set_plugin_path()