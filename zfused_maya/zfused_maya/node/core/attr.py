# coding:utf-8
# --author-- lanhua.zhou

""" zfused maya 内部操作数据记录信息 """

from __future__ import print_function

import zfused_api

import maya.cmds as cmds

import logging


ATTRIBUTES = ["project_id", "link_object", "link_id", "project_step_id", "task_id", "output_attr_id", "version", "version_id", "is_local"]


def set_node_attr(node, output_attr_id, version_id, is_local = "false"):
    """ set node version attr 
    
    """
    _is_lock = False
    if cmds.lockNode(node, q = True)[0]:
        islock = True
        # unlock node
        cmds.lockNode(node, l = False)
    for _attr in ATTRIBUTES:
        if not cmds.objExists("%s.%s" % (node, _attr)):
            cmds.addAttr(node, ln = _attr, dt = "string")
            cmds.setAttr("%s.%s" % (node, _attr), e = True, keyable = True)
    if islock:
        cmds.lockNode(node, l=True)

    _version_handle = zfused_api.version.Version(version_id)
    _task_handle = zfused_api.task.Task(_version_handle.data["TaskId"])

    cmds.setAttr("{}.project_id".format(node), 
                 str(_version_handle.data["ProjectId"]), 
                 type="string")
    cmds.setAttr("{}.link_object".format(node), 
                 str(_version_handle.data["Object"]), 
                 type="string")
    cmds.setAttr("{}.link_id".format(node), 
                 str(_version_handle.data["LinkId"]), 
                 type="string")
    cmds.setAttr("{}.project_step_id".format(node), 
                 str(_task_handle.data["ProjectStepId"]), 
                 type="string")
    cmds.setAttr("{}.output_attr_id".format(node), str(output_attr_id), type = "string")
    cmds.setAttr("{}.task_id".format(node), 
                 str(_version_handle.data["TaskId"]), 
                 type="string")
    cmds.setAttr("{}.version".format(node), str(_version_handle.index()), type = "string")
    cmds.setAttr("{}.version_id".format(node), 
                 str(_version_handle.data["Id"]), 
                 type="string")
    #is_local = "false"
    cmds.setAttr("{}.is_local".format(node), 
                 str(is_local), 
                 type="string")


def get_node_attr(node):
    """ get not attr data

    """
    _attr_data = {}
    if not cmds.objExists("{}.project_id".format(node)):
        return _attr_data
    _attr_data["project_id"] = int(cmds.getAttr("%s.project_id" % node))
    _attr_data["project_step_id"] = int(cmds.getAttr("%s.project_step_id" % node))
    _attr_data["task_id"] = int(cmds.getAttr("%s.task_id" % node))
    if cmds.objExists("{}.output_attr_id".format(node)):
        _attr_data["output_attr_id"] = int(cmds.getAttr("{}.output_attr_id".format(node)))
    if cmds.objExists("%s.is_local" % node):
        _attr_data["is_local"] = cmds.getAttr("%s.is_local" % node)
    else:
        _attr_data["is_local"] = "false"
    if cmds.objExists("%s.link_object" % node):
        _attr_data["link_object"] = cmds.getAttr("%s.link_object" % node)
    else:
        _attr_data["link_object"] = cmds.getAttr("%s.object" % node)
    if cmds.objExists("%s.link_id" % node):
        _attr_data["link_id"] = int(cmds.getAttr("%s.link_id" % node))
    else:
        _attr_data["link_id"] = int(cmds.getAttr("%s.id" % node))
    if cmds.objExists("%s.version_id" % node):
        _attr_data["version_id"] = int(cmds.getAttr("%s.version_id" % node))
    else:
        # get version id
        _version_index = int(cmds.getAttr("%s.version" % node))
        _version_data = zfused_api.zFused.get("version", filter = {"TaskId": _attr_data["task_id"], "Index": _version_index})[0]
        _attr_data["version_id"] = int(_version_data["Id"])
    if cmds.objExists("{}.version".format(node)):
        _attr_data["version"] = int(cmds.getAttr("%s.version" % node))
    else:
        _version_handle = zfused_api.version.Version(_attr_data["version_id"])
        _attr_data["version"] = _version_handle.index()

    return _attr_data