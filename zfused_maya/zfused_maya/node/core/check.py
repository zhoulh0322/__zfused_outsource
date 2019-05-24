# coding:utf-8
# --author-- lanhua.zhou

""" zfused maya 检查机制 """

from __future__ import print_function

import os
import logging
import maya.cmds as cmds

import zfused_api 
import zfused_maya.core.record as record 

import texture

class Check(object):
    """ check base object
    """
    value = False

def camera_name():
    info = u"当前摄像机名称与任务名不匹配\n"
    _task_id = record.current_task_id()
    if not _task_id:
        return False, info
    _task_handle = zfused_api.task.Task(_task_id)
    _obj_handle = zfused_api.objects.Objects(_task_handle.data["Object"], _task_handle.data["LinkId"])
    _name = _obj_handle.file_code()

    if not cmds.ls("*%s*"%_name, type = "camera"):
        return False,info    
    return True,None

def file_name():
    _info = u"当前文件名称与任务名不匹配\n"
    _task_id = record.current_task_id()
    if not _task_id:
        return False, _info
    _task_handle = zfused_api.task.Task(_task_id)
    _obj_handle = zfused_api.objects.Objects(_task_handle.data["Object"], _task_handle.data["LinkId"])
    _name = _obj_handle.file_code()
    _file_name = cmds.file(q = True, sn = True)
    if not os.path.basename(_file_name).startswith(_name):
        return False,_info    
    return True,None

def file_node():
    """ check file node is not null

    """
    _file_nodes = texture.error_nodes()        
    if len(_file_nodes) > 1:
        info = u"file节点存在错误贴图路径,请用贴图管理工具检查\n"
        for _file_node in _file_nodes:
            info += "{}\n".format(_file_node)
        return False, info
    return True, None

def reference_file_node():
    """ check reference file

    """
    pass

def texture_path():
    """ check texture file path

    """
    _info = ""
    _files = texture.files()
    if not _files:
        return True, None
    _paths = texture.paths(_files)
    if len(_paths) > 1:
        info = u"贴图存在不同路径下,请用贴图管理工具检查\n"
        for _path in _paths:
            info += "{}\n".format(max(_path))
        return False, info
    return True, None

def animation_layer():
    """ check animation layer

    """
    _lays = cmds.ls(type = "animLayer")
    if len(_lays) > 0:
        info = u"场景存在多余动画层\n"
        for _layer in _lays:
            info += "{}\n".format(_layer)
        return False, info
    return True, None

def unknown_node():
    """ check unknown nodes

    """
    _nodes = cmds.ls(type = "unknown")
    if len(_nodes) > 0:
        info = "场景存在未知节点\n"
        for _node in _nodes:
            info += "{}\n".format(_node)
        return False,info
    return True, None

def camera():
    """ check camera

    """
    _extra_camera = ["facial_cam"]
    _cameras = cmds.ls(type = "camera")
    _left_cameras = list(set(_cameras) - set(["frontShape","topShape","perspShape","sideShape"]))
    if _left_cameras:
        info = "场景存在多余摄像机\n"
        for _camera in _left_cameras:
            _is_extra = False
            for _cam in _extra_camera:
                if _cam in _camera:
                    _is_extra = True
            if _is_extra:
                continue
            info += "{}\n".format(_camera)
        return False,info
    return True,None

def reference():
    """ check reference file

    """
    _references = cmds.ls(type = "reference")
    if _references:
        info = "场景存在参考文件\n"
        for _reference in _references:
            info += "{}\n".format(_reference)
        return False,info
    return True,None

def light():
    """ check light

    """
    _lights = cmds.ls(type = cmds.listNodeTypes("light"))
    
    if _lights:
        info = "场景存在多余灯光节点\n"
        for _light in _lights:
            info += "{}\n".format(_light)
        return False,info
    return True, None

def anim_curve():
    """ check anim curves

    """
    _cures = cmds.ls(type = 'animCurve')
    if _cures:
        info = "场景存在动画曲线\n"
        for _cure in _cures:
            info += "{}\n".format(_cure)
        return False,info
    return True, None

def display_layer():
    """ check display layer

    """
    import pymel.core as core
    _layers = [Layer for Layer in core.ls(type = 'displayLayer') if not core.referenceQuery(Layer, isNodeReferenced = True) and Layer.name() != 'defaultLayer' and cmds.getAttr("%s.identification"%Layer) != 0]
    if _layers:
        info = "场景存在显示层\n"
        for _layer in _layers:
            info += "{}\n".format(_layer)
        return False,info
    return True, None

def render_layer():
    """ check render layer

    """
    import pymel.core as core
    _layers = [Layer for Layer in core.ls(type = 'renderLayer') if not core.referenceQuery(Layer, isNodeReferenced = True) and Layer.name() != 'defaultRenderLayer']
    if _layers:
        info = "场景存在渲染层\n"
        for _layer in _layers:
            info += "{}\n".format(_layer)
        return False,info
    return True, None

def namespace():
    """ check namespace

    """
    _namespaces = cmds.namespaceInfo(recurse = True, listOnlyNamespaces = True)
    _namespaces = list(set(_namespaces) - set(["shared","UI"]))
    if _namespaces:
        info = "场景中存在命名空间\n"
        for _namespace in _namespaces:
            info += "{}\n".format(_namespace)
        return False,info
    return True, None

def repeat(node_type = "mesh"):
    """ 检查重命名

    """
    _is_repeat = False
    _lists = cmds.ls(noIntermediate = 1, type = node_type)
    info = "场景存在重复命名节点\n"
    for _name in _lists:
        if len(_name.split('|')) != 1:
            _is_repeat = True
            info += "{}\n".format(_name)
    if _is_repeat:
        return False, info
    else:
        return True, None



def trans_in_mesh():
    """ check mesh in mesh

    """
    _list = []
    _meshGrp = [x for x in cmds.ls(type='transform') if ('_model_GRP' in x) and cmds.objExists(x+'.treeName')]
    if _meshGrp:
        _all_meshs = cmds.listRelatives(_meshGrp[0],type = "mesh",ad = 1,f = 1)
        _all_trans = cmds.listRelatives(_all_meshs,p = 1,f = 1)
        if _all_trans:
            for i in _all_trans:
                wrongtrans = cmds.listRelatives(i,ad = 1,type = "transform")
                # print wrongtrans
                if wrongtrans:
                    _list.extend(wrongtrans)
    # print (_list)
    if _list:
        info = "场景存在嵌套模型\n{}".format("\n".join(_list))
        # print (info)
        return False, info
    else:
        return True, None

def isshow(node):
    _value = True
    if cmds.getAttr("%s.v"%node) == 0:
        _value = False
    while True:
        node = cmds.listRelatives(node, p = 1, f = True)
        if not node:
            break
        else:
            node = node[0]
            if cmds.getAttr("%s.v"%node) == 0:
                _value = False
                break
    return _value

def color_set():
    '''顶点着色
    '''
    _color_set = []
    _dags = cmds.ls(dag = 1)
    if not _dags:
        return True, None
    for _dag in _dags:
        _set = cmds.polyColorSet(_dag,q = 1,acs = 1)
        if _set:
            _color_set.extend(_set)
    if _color_set:
        info = "场景存在顶点着色\n{}".format("\n".join(_color_set))
        return False ,info
    else:
        return True, None

def intermediate_shape():
    sel = cmds.ls(io = 1,type = "mesh")
    if sel:
        info = "场景存在转换的中间模型\n{}".format("\n".join(sel))
        return False ,info
    else:
        return True, None