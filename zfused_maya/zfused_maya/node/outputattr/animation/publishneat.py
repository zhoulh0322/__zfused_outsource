# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os
import logging

import maya.cmds as cmds

import zfused_api
import zfused_maya.core.record as record
import zfused_maya.core.filefunc as filefunc

import zfused_maya.node.core.alembiccache as alembiccache
import zfused_maya.node.core.texture as texture
import zfused_maya.node.core.material as material
import zfused_maya.node.core.fixmeshname as fixmeshname
import zfused_maya.node.core.renderinggroup as renderinggroup
import zfused_maya.node.core.referencefile as referencefile

__all__ = ["publish_neat"]

logger = logging.getLogger(__name__)

# test
def publish_neat():
    """ 上传动画文件
    
    """
    _attr_code = "neat"
    _file_suffix = "ma"
    _file_format = "mayaAscii"

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
    if not os.path.isdir(_publish_file_dir):
        os.makedirs(_publish_file_dir)

    try:
        # save publish file
        cmds.file(rename = _publish_file)
        cmds.file(save = True, type = _file_format, f = True)

        import pymel.core as pm
        # get root name
        _assembly_root = []
        _assemblys = pm.ls(type = "assembly", ap = True, )
        for _assembly in _assemblys:
            _root = _assembly.root()
            if _root not in _assembly_root:
                _assembly_root.append(_root)
        pm.delete(_assembly_root)
        cmds.file(save = True, type = _file_format, f = True)

        # publish file
        _result = filefunc.publish_file(_publish_file, _cover_file)

    except Exception as e:
        logger.error(e)
        return False

    # open orignal file
    # cmds.file(_current_file, o = True, f = True, pmt = True)
    return True