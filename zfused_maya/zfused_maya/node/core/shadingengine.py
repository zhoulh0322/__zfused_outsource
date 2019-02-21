# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

""" 材质引擎操作集合 """

from qtpy import QtGui
import maya.cmds as cmds


def nodes():
    """ get all shading engines

    :rtype: list
    """
    _default_shading_engine = ["initialShadingGroup", "initialParticleSE"]
    _all_shading_engines = cmds.ls(type="shadingEngine")
    _all_shading_engines = list(set(_all_shading_engines)
                                - set(_default_shading_engine))
    return _all_shading_engines

def get_shading_engines():
    """ get all shading engine

    :rtype: list
    """
    _default_shading_engine = ["initialShadingGroup", "initialParticleSE"]
    _all_shading_engines = cmds.ls(type="shadingEngine")
    _all_shading_engines = list(set(_all_shading_engines) - set(_default_shading_engine))
    return _all_shading_engines

def switch_color_shader(engines):
    for _engine in engines:
        # get engine color
        _color = get_node_shading_color(_engine)
        if not _color:
            continue
        _qtcolor = QtGui.QColor(_color)
        r,g,b,_ = _qtcolor.getRgb()
        # new lambert color
        _shader = cmds.shadingNode("lambert", name = "zfused_shading_color_0000",asShader = True)
        cmds.setAttr("{}.color".format(_shader), r/255.0, g/255.0, b/255.0 ,type = "double3")
        # connect
        cmds.connectAttr("{}.outColor".format(_shader), "{}.surfaceShader".format(_engine), f = True)

def switch_orignail_shader(engines):
    for _engine in engines:
        # get orignail engine
        if not cmds.objExists("{}.surfacematerial".format(_engine)):
            continue
        _ori_shader = cmds.getAttr("{}.surfacematerial".format(_engine))
        _node_type = cmds.nodeType(_ori_shader)
        try:
            if _node_type.startswith("ai"):
                cmds.connectAttr("{}.out".format(_ori_shader), "{}.surfaceShader".format(_engine), f = True)
            elif _node_type.startswith("Redshift"):
                cmds.connectAttr("{}.outColor".format(_ori_shader), "{}.surfaceShader".format(_engine), f = True)
            else:
                cmds.connectAttr("{}.outColor".format(_ori_shader), "{}.surfaceShader".format(_engine), f = True)
        except:
            pass

def set_node_shading_color(node, shading_color):
    """ set shading node color attr

    :rtype: bool
    """
    if not cmds.objExists("{}.shadingcolor".format(node)):
        cmds.addAttr(node, ln="shadingcolor", dt="string")
    cmds.setAttr("{}.shadingcolor".format(node), shading_color, type="string")
    if cmds.nodeType(node) == "shadingEngine":
        # set original material
        _ori_material = cmds.listConnections("{}.surfaceShader".format(node), s=True)[0]
        if not cmds.objExists("{}.surfacematerial".format(node)):
            cmds.addAttr(node, ln = "surfacematerial", dt="string")
        if not _ori_material.startswith("zfused_shading_color_"):
            cmds.setAttr("{}.surfacematerial".format(node), _ori_material, type="string")
    return True

def get_node_shading_color(node):
    """ get shading node color attr

    :rtype: str
    """
    if not cmds.objExists("{}.shadingcolor".format(node)):
        return None
    _color = cmds.getAttr("{}.shadingcolor".format(node))
    return _color