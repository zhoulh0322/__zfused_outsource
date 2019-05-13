# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import sys
import os
import logging
import json

import maya.cmds as cmds
import maya.api.OpenMaya as om

import zfused_api
import zfused_maya.core.record as record
import zfused_maya.core.filefunc as filefunc

import zfused_maya.node.core.assembly as assembly

__all__ = ["publish_structure"]

logger = logging.getLogger(__name__)


def publish_structure():
    """ 上传任务模型结构
    
    """
    _attr_code = "structure"
    _file_suffix = "json"
    _file_format = "json"

    _current_file = cmds.file(q = True, sn = True)
    # path 
    _link = record.current_link() 
    _project_step_id = record.current_project_step_id()
    _project_step_handle = zfused_api.step.ProjectStep(_project_step_id)
    _step_code = _project_step_handle.code()
    _software_code = zfused_api.software.Software(_project_step_handle.data["SoftwareId"]).code()
    _object_handle = zfused_api.objects.Objects(_link[0], _link[1])
    _link_production_path = _object_handle.production_path()
    _link_publish_path = _object_handle.publish_path()
    _file_code = _object_handle.file_code()
    _production_path = "{}/{}/{}/{}".format(_link_production_path, _step_code, _software_code, _attr_code)
    _publish_path = "{}/{}/{}/{}".format(_link_publish_path, _step_code, _software_code, _attr_code)
    # file
    _cover_file = "%s/%s.%s"%(_production_path, _file_code, _file_suffix)
    _publish_file = "%s/%s.%s"%(_publish_path, _file_code, _file_suffix)
    _publish_file_dir = os.path.dirname(_publish_file)
    if not os.path.isdir(_publish_path):
        os.makedirs(_publish_file_dir)

    try:        
        _structure_data = assembly.scene_assemblys()
        with open(_publish_file, "w") as handle:
            handle.write( json.dumps(_structure_data, indent = 4, separators=(',',':')) )
        _result = filefunc.publish_file( _publish_file, _cover_file )
    except Exception as e:
        logger.error(e)
        return False

    # open orignal file
    # cmds.file(_current_file, o = True, f = True, pmt = True)
    return True
