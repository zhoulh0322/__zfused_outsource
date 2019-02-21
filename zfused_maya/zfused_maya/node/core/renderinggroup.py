# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

""" 场景集合操作函数集 """
from __future__ import print_function

import maya.cmds as cmds

import logging

logger = logging.getLogger(__name__)



def set_node_attr(node):
    """ set node rendering attr

    """
    if not cmds.objExists("{}.rendering".format(node)):
        cmds.addAttr(node, longName = "rendering",at = 'bool')
        cmds.setAttr("{}.rendering".format(node), True)

def nodes():
    """ get rendering node

    :rtype: list
    """      
    _is_rendering = []
    _all_dags = cmds.ls(dag = True)
    for _dag in _all_dags:
        #print dag
        #get 
        if cmds.objExists("%s.rendering"%_dag):
            value = cmds.getAttr("%s.rendering"%_dag)
            if value:
                _is_rendering.append(_dag)
    return _is_rendering