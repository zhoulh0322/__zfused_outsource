# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

""" 关联操作集合 """

from __future__ import print_function

import os
import sys
import glob
import copy 
import json

import zfused_api
import zfused_maya.core.record as record

from . import attr
from . import element

import maya.cmds as cmds

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


def create_relatives():
    """ 创建当前关联信息

    """
    # get current task id
    _task_id = record.current_task_id()
    if not _task_id:
        return 

    _task_handle = zfused_api.task.Task(_task_id)
    _link_object = _task_handle.data["Object"]
    _link_id = _task_handle.data["LinkId"]

    _task_ids = []
    # get task input task
    _input_task_dict = _task_handle.input_tasks()
    if _input_task_dict:
        for _, _task_list in _input_task_dict.items():
            for _task in _task_list:
                _task_ids.append(_task["Id"])
    # get elements
    _element_list = element.scene_elements()
    if _element_list:
        _task_ids += [_element["task_id"] for _element in _element_list]
    _task_ids = list(set(_task_ids))

    # 上一级version版本
    _version_id = _task_handle.last_version_id()
    if _version_id:
        print(_version_id)
        _version_relatives = zfused_api.zFused.get("relative", filter = {"TargetObject": "version", "TargetId": _version_id})
        if not _version_relatives:
            _task_relatives = zfused_api.zFused.get("relative", filter = {"TargetObject": "task", "TargetId": _task_id, "SourceObject": "version"})
            if _task_relatives:
                for _re in _task_relatives:
                    zfused_api.relative.create_relatives("version", _re["SourceId"], "version", _version_id)

    # clear ori relatives
    zfused_api.relative.clear_relatives("task", _task_id)
    zfused_api.relative.clear_relatives(_link_object, _link_id)
    #zfused_api.relative.clear_relatives("version", 0)

    # create relatives
    for _id in _task_ids:
        # create task relatives
        zfused_api.relative.create_relatives("task", _id, "task", _task_id)
           
        # create object relatives
        _handle = zfused_api.task.Task(_id)
        zfused_api.relative.create_relatives(_handle.data["Object"], _handle.data["LinkId"], _link_object, _link_id)

    for _element in _element_list:
        # create version relatives
        zfused_api.relative.create_relatives("version", _element["version_id"], "task", _task_id)