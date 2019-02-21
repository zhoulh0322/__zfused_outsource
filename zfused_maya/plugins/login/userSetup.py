# coding:utf-8
#--author-- lanhua.zhou
from __future__ import print_function

import sys
import os
import maya.cmds as cmds
import maya.utils
import maya.mel as mm



def _login():
    import zfused_link_maya.zfused_login as zfused_login
    ui = zfused_login.login.Login()
    ui.show()

try:
    maya.utils.executeDeferred(_login)
except Exception as e:
    print(w)


def main():
    cmds.loadPlugin("mtoa")

    def func():
        mm.eval("setCurrentRenderer arnold;")
        mm.eval("unifiedRenderGlobalsWindow")
        cmds.setAttr("defaultRenderGlobals.byFrameStep", )
        cmds.setAttr("defaultArnoldRenderOptions.shader_searchpath",
                     r"C:\solidangle\mtoadeploy\2016\shaders", type="string")
    cmds.scriptJob(runOnce=1, idleEvent=func)
