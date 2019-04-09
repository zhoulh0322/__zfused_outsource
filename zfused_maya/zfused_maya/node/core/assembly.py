# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

""" 场景集合操作函数集 """

from __future__ import print_function

import maya.cmds as cmds

import logging

# load gpu plugin
_is_load = cmds.pluginInfo("sceneAssembly", query=True, loaded = True)
if not _is_load:
    try:
        logger.info("load scene assembly plugin")
        cmds.loadPlugin("sceneAssembly")
    except Exception as e:
        logger.error(e)
        sys.exit()

class Assembly(object):
    def __init__(self, name):
        self._assembly_name = name

    def create_representation(self, name, retype, infile):
        _ad = cmds.assembly(self._assembly_name, edit = True, 
                                                repName = name,
                                                repLabel = name,
                                                createRepresentation = retype,
                                                input = infile)
        _lr = cmds.assembly(self._assembly_name, q = True, lr = True)
        cmds.setAttr("{}.representations[{}].repLabel".format(self._assembly_name, _lr.index(_ad)), name, type = "string")
        
    def set_active(self, active_string):
        cmds.assembly(self._assembly_name, e = True, active = active_string)

def create_assembly_definition(name):
    """ 创建资产集合节点

    :type: zfused_maya.node.core.assembly.Assembly
    """
    _name = cmds.assembly(name='{}_assemblyDefinition_0001'.format(name))
    return Assembly(_name)

def create_assembly_reference(name, reference_file = None):
    """ 创建资产集合节点

    :type: zfused_maya.node.core.assembly.Assembly
    """
    _name = cmds.assembly(name='{}_assemblyReference_0001'.format(name), type = "assemblyReference")
    #return AssemblyDefinition(_name)
    if reference_file:
        cmds.setAttr('{}.definition'.format(_name), reference_file, type = "string" )

    return Assembly(_name)