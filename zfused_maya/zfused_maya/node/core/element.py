# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

""" 关联操作集合 """

from __future__ import print_function

import os
import sys
import glob
import copy 
import json

import maya.cmds as cmds

import zfused_api
import zfused_maya.core.record as record

from . import attr


__CACHE_DICT = {
    "namespace": "",
    "reference_node": "",
    "link_object": "asset",
    "link_id": 0,
    "task_id": 0,
    "project_step_id": 0,
    "output_attr_id": 0,
    "version": 0,
    "version_id": 0,
    "project_id": 0,
    "type": "reference",
    "is_local": "false"
}


def scene_elements():
    """ get maya file scene elemnets

    :rtype: list
    """
    _scene_elements = []

    _project_id = record.current_project_id()
    if not _project_id:
        return _scene_elements

    # get rendering elements
    _rendering_groups = []
    _groups = cmds.ls(dag = True)
    for _group in _groups:
        if cmds.objExists("{}.redering".format(_group)):
            _is_rendering = cmds.getAttr("{}.redering".format(_group))
            if _is_rendering:
                _rendering_groups.append(_group)
    _all_references = {}
    for _rendering in _rendering_groups:
        if cmds.referenceQuery(_redering, isNodeReferenced = True):
            _node = cmds.referenceQuery(_redering, referenceNode = True)
            if not _all_references.keys().__contains__(_node):
                _all_references[_node] = []
            _all_references[_node].append(obj)
    for _reference in _all_references.keys():
        namespace = cmds.referenceQuery(_reference, namespace = True)
        if namespace.startswith(":"):
            namespace = namespace[1::]
        rfn = cmds.referenceQuery(_reference, rfn = True)
        #get attr
        _node_attr = attr.get_node_attr(rfn)
        if not _node_attr:
            continue
        if _node_attr["project_id"] != _project_id:
            continue
        copy_data = copy.deepcopy(__CACHE_DICT)
        for k in _node_attr.keys():
            if copy_data.keys().__contains__(k):
                copy_data[k] = _node_attr[k]
        copy_data["namespace"] = namespace
        copy_data["reference_node"] = rfn
        _scene_elements.append(copy_data)

    # reference node
    _reference_nodes = cmds.ls(type = "reference")
    #all_references = cmds.ls(type = "reference")
    for _node in _reference_nodes:
        if _node not in _all_references.keys():
            try:
                namespace = cmds.referenceQuery(_node, namespace = True)
            except:
                continue
            if namespace.startswith(":"):
                namespace = namespace[1::]
            _rfn = cmds.referenceQuery(_node, rfn = True)
            #get attr
            # ref_attr = node.GetAttr(_rfn)
            _node_attr = attr.get_node_attr(_rfn)
            if not _node_attr:
                continue
            if _node_attr["project_id"] != _project_id:
                continue
            copy_data = copy.deepcopy(__CACHE_DICT)
            for k in _node_attr.keys():
                if copy_data.keys().__contains__(k):
                    copy_data[k] = _node_attr[k]
            copy_data["namespace"] = namespace
            copy_data["reference_node"] = _rfn
            _scene_elements.append(copy_data)

    return _scene_elements


def replace_by_step(element, project_step_id):
    """ replace file by new project step

    """
    _link_object = element["link_object"]
    _link_id = element["link_id"]
    _reference_node = element["reference_node"]

    _replace_tasks = zfused_api.zFused.get("task", filter = {"Object": _link_object,
                                                            "LinkId": _link_id,
                                                            "ProjectStepId": project_step_id})
    if not _replace_tasks:
        return
    _replace_task = _replace_tasks[0]
    _replace_task_handle = zfused_api.task.Task(_replace_task["Id"])
    _version_id = _replace_task_handle.last_version_id()
    if not _version_id:
        return
    _version_handle = zfused_api.version.Version(_version_id)
    # get replace file
    _step = "file"
    _path = _replace_task_handle.production_path()
    _name = _version_handle.data["FilePath"]
    _file_path = "{}/{}{}".format(_path, _step, _name)

    # 是否要判定下载到本机 。。。
    #   
    cmds.file(_file_path, loadReference = _reference_node)

    #rewrite node info
    cmds.setAttr("%s.link_id"%element["reference_node"], str(_link_id), type = "string")
    cmds.setAttr("%s.task_id"%element["reference_node"], str(_replace_task["Id"]), type = "string")
    #version = versionHandle.data["Index"]
    cmds.setAttr("%s.version_id"%element["reference_node"], str(_version_id), type = "string")

    element["version_id"] = _version_id
    element["link_id"] = _link_id
    element["task_id"] = _replace_task["Id"]
    
    return element