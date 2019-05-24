# coding:utf-8
# --author-- binglu.wang
from __future__ import print_function

import os
import json
import logging

import maya.cmds as cmds

import zfused_api
import zfused_maya.core.record as record
import zfused_maya.core.filefunc as filefunc
import zfused_maya.node.core as core
import zfused_maya.node.core.yeti as yeti
import zfused_maya.node.core.yeticache as yeticache

__all__ = ["publish_cache"]

logger = logging.getLogger(__name__)

PREPFRAME = 8

# load yeti plugin
_is_load = cmds.pluginInfo("pgYetiMaya", query=True, loaded = True)
if not _is_load:
    try:
        logger.info("try load pgYetiMaya plugin")
        cmds.loadPlugin("pgYetiMaya")
    except Exception as e:
        logger.error(e)
        sys.exit()

# @core.viewportOff
def publish_cache():
    """ publish yeticache

    :rtype: bool
    """
    _attr_code = "cache/yeticache"
    _file_suffix = "json"

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
    
    _production_json_file = "{}/{}.{}".format(_production_path,_file_code,_file_suffix)
    _publish_json_file = "{}/{}.{}".format(_publish_path,_file_code,_file_suffix)
    _publish_file_dir = os.path.dirname(_publish_json_file)
    if not os.path.isdir(_publish_path):
        os.makedirs(_publish_file_dir)

    # _start_frame = _object_handle.start_frame()-PREPFRAME
    # _end_frame = _object_handle.end_frame()+PREPFRAME
    _start_frame = int(cmds.playbackOptions(q = True,min = True))-PREPFRAME
    _end_frame = int(cmds.playbackOptions(q = True,max = True))+PREPFRAME

    if not os.path.isdir(_publish_path):
        os.makedirs(_publish_path)
    try:
        _pgnodes = yeticache.nodes()
        _info,_batch = yeticache.get_upload_info(_pgnodes, 4, _production_path, _publish_path)
        _publish_dict = {}
        for _k,_v in _batch.items():
            _publish_dict[_v[0]] = _v[1]
            logger.info("export cache: {}".format(_v[0]))
            yeticache.create_cache(_k,_v[0],_start_frame,_end_frame,3)
        with open(_publish_json_file,"w") as info:
            json.dump( _info, info,indent = 4,separators=(',',':') )
        _result = filefunc.publish_file( _publish_json_file, _production_json_file, True )
        for _k1,_v1 in _publish_dict.items():
            _local_path = os.path.dirname(_k1)
            for _file in os.listdir(_local_path):
                _production_file = "{}/{}".format(os.path.dirname(_v1),_file)
                _publish_file = "{}/{}".format(_local_path,_file)
                _result = filefunc.publish_file(_publish_file, _production_file,True)
    except Exception as e:
        logger.error(e)
        return False
    return True

if __name__ == '__main__':
    publish_cache()
