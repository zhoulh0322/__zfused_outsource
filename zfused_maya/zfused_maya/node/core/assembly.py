# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

""" 场景集合操作函数集 """

from __future__ import print_function

import maya.cmds as cmds
import pymel.core as pm

import zfused_maya.node as node

import logging

logger = logging.getLogger(__name__) 

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

    def name(self):
        """ get assembly name
        """
        return self._assembly_name

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

def scene_assemblys():        
    def _get_data(_node):
        _py_node = pm.PyNode(_node._node)
        _node_data = {}
        #
        _name = _node._node.split(":")[-1].split("_assemblyReference_")[0]
        _node_data["name"] = _name
        _node_data["namespace"] = _py_node.namespace()
        _node_data["node_type"] = _py_node.type()
        _node_data["attr"] = _node.get_attr()
        _node_data["child"] = []

        _childs = cmds.listRelatives(_node._node, c = True, typ = ["assemblyReference", "transform"], f = True)
        # get child
        if _childs:
            for _child in _childs:
                _child_node = node.Node(_child)
                _child_data = _get_data(_child_node)
                _node_data["child"].append(_child_data)
        return _node_data

    # 
    # get root name
    _assembly_root = []
    _assemblys = pm.ls(type = "assembly", ap = True, )
    for _assembly in _assemblys:
        _root = _assembly.root()
        if _root not in _assembly_root:
            _assembly_root.append(_root)

    #
    # get data
    _assembly_node = []
    for _root in _assembly_root:
        _root_node = node.Node(_root.name())
        _root_data = _get_data(_root_node)
        _assembly_node.append(_root_data)  

    return _assembly_node


def _test():
    import os
    import maya.api.OpenMaya as OpenMaya


    _assembly_references = cmds.ls(type = "assemblyReference", ap = True)

    _copys = []
    _num_dict = {}
    for _assembly_reference in _assembly_references:
        # old
        # _parents = cmds.listRelatives(_assembly_reference, p = True, ad = True)
        # if len(_parents) > 1:
        #     continue
        selectionList = OpenMaya.MSelectionList()
        selectionList.add(_assembly_reference)
        nodeDagPath = selectionList.getDagPath(0)
        if not nodeDagPath.isInstanced():
            _file_name = cmds.getAttr("{}.definition".format( _assembly_reference ))
            if _file_name not in _num_dict.keys():
                _num_dict[_file_name] = []
            _num_dict[_file_name].append(_assembly_reference)

    for _assembly_references in _num_dict.values():
        if len(_assembly_references) > 1:
            _copys += _assembly_references
    # instance group
    _instance_group = "_instance_grp"
    if not cmds.objExists( _instance_group ):
        cmds.createNode("transform", name = _instance_group)

    _will_instances = []
    for _copy in _copys:
        if cmds.listRelatives(_copy, p = True):
            _p_name = cmds.parent(_copy, w = True)
            _new_names = cmds.parent( _p_name, _instance_group )
        else:
            _new_names = cmds.parent( _copy, _instance_group )
        _will_instances += _new_names

    _instances = {}
    for _will_instance in _will_instances:
        _file_name = cmds.getAttr("{}.definition".format( _will_instance ))
        _base_name = os.path.basename(_file_name)
        _code = os.path.splitext( _base_name )[0]
        if _code not in _instances.keys():
            _ins_grp = cmds.createNode("transform", name = "{}_instance".format(_code))
            # create assembly node
            _name = cmds.assembly(name='{}_assemblyReference_0001'.format(_code), type = "assemblyReference")
            cmds.setAttr('{}.definition'.format(_name), _file_name, type = "string" )
            _lrs = cmds.assembly(_name, q = True, lr = True)
            cmds.assembly(_name, e = True, active = _lrs[0])
            cmds.parent(_name, _ins_grp)
            _instances[_code] = _ins_grp
        _ins_name = _instances[_code]
        # instance copy
        _new_ins_name = cmds.instance(_ins_name)[0]

        # get parent rotate scale and vis 
        _tanslate = cmds.getAttr("{}.translate".format(_will_instance) )
        cmds.setAttr("{}.translate".format(_new_ins_name), _tanslate[0][0], _tanslate[0][1], _tanslate[0][2])
        _rotate = cmds.getAttr("{}.rotate".format(_will_instance) )
        cmds.setAttr("{}.rotate".format(_new_ins_name), _rotate[0][0], _rotate[0][1], _rotate[0][2])
        _scale = cmds.getAttr("{}.scale".format(_will_instance) )
        cmds.setAttr("{}.scale".format(_new_ins_name), _scale[0][0], _scale[0][1], _scale[0][2])
        _vis = cmds.getAttr("{}.visibility".format(_will_instance) )
        cmds.setAttr("{}.visibility".format(_new_ins_name), _vis)

    # remove instance
    cmds.delete(_instances.values())
    # remove instance grp
    cmds.delete(_instance_group)
    