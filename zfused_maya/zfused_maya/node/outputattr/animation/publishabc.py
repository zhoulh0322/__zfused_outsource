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
import zfused_maya.node.core.alembiccache as alembiccache
import zfused_maya.node.core.fixmeshname as fixmeshname
import zfused_maya.node.core.renderinggroup as renderinggroup
import zfused_maya.node.core.yeticache as yeticache
import zfused_maya.node.core.displaylayer as displaylayer


__all__ = ["publish_abc"]
logger = logging.getLogger(__name__)

PREPFRAME = 8
EXPORTATTR = ["worldSpace", "writeVisibility"]

# load abc plugin
_is_load = cmds.pluginInfo("AbcExport", query=True, loaded = True)
if not _is_load:
    try:
        logger.info("try load pgYetiMaya plugin")
        cmds.loadPlugin("AbcExport")
    except Exception as e:
        logger.error(e)
        sys.exit()

# @core.viewportOff
def publish_abc():
    """ publish alembiccache
    
    """
    def get_cam_info(abcSuffix,fileCode,startFrame,endFrame,_job = [],_json = [],_dict = {}):
        # _alljob = []
        _cams = cmds.ls("{}*".format(fileCode),fl = 1,type = "camera")
        if not _cams:
            return
        for _cam in _cams:
            _cam_trans = cmds.listRelatives(_cam,p = 1)[0]
            _production_file = "{}/{}.{}".format(_production_path,_cam_trans,abcSuffix)
            _publish_file = "{}/{}.{}".format(_publish_path,_cam_trans,abcSuffix)
            _joborder = alembiccache.create_frame_cache(_publish_file,startFrame,endFrame,_cam_trans,*EXPORTATTR)
            _job.append(_joborder)
            _json.append(["",_cam_trans,"",_production_file])
            _dict[_publish_file] = _production_file

    def get_asset_info(renderdag,abcSuffix,fileCode,startFrame,endFrame,_job = [],_json = [],_dict = {}):
        # _alljob = []
        _assets = yeticache.get_asset_list()
        fixmeshname.fix_deformed_mesh_name("_rendering", renderdag)
        for _dag in renderdag:
            _ns = cmds.referenceQuery(_dag,ns = 1,shn = 1)
            if _ns in _assets:
                _production_file = "{}/{}.{}".format(_production_path,_ns,abcSuffix)
                _publish_file = "{}/{}.{}".format(_publish_path,_ns,abcSuffix)
                _joborder = alembiccache.create_frame_cache(_publish_file,startFrame,endFrame,_dag,*EXPORTATTR)
                _job.append(_joborder)
                _json.append([_assets[_ns],_ns,_dag.split(":")[-1],_production_file])# 依次是：assetname,namespace,nodename,cachepath
                _dict[_publish_file] = _production_file

    # _attr_code = "cache/anicache"
    _attr_code = "cache/alembiccache"
    _file_suffix = "json"
    _abc_suffix = "abc"

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

    _production_json_file = "{}/{}.{}".format(_production_path,_file_code,_file_suffix)
    _publish_json_file = "{}/{}.{}".format(_publish_path,_file_code,_file_suffix)
    # _start_frame = _object_handle.start_frame()-PREPFRAME
    # _end_frame = _object_handle.end_frame()+PREPFRAME
    _start_frame = int(cmds.playbackOptions(q = True,min = True))-PREPFRAME
    _end_frame = int(cmds.playbackOptions(q = True,max = True))+PREPFRAME

    # 单独发布接口，返回空发布全部
    renderdag = []
    if not renderdag:
        renderdag = renderinggroup.nodes()
    # enable norender attributes
    _norenders = displaylayer.norender_info(displaylayer.nodes())
    if _norenders:
        for i in _norenders:
            _attr = "{}.v".format(i)
            if cmds.objExists(_attr) and cmds.getAttr(_attr) != 0:
                cmds.setAttr(_attr,0)

    # get info
    _alljob = []
    _json_info = []
    upload_dict = {}
    get_cam_info(_abc_suffix,_file_code,_start_frame,_end_frame,_alljob,_json_info,upload_dict)
    get_asset_info(renderdag,_abc_suffix,_file_code,_start_frame,_end_frame,_alljob,_json_info,upload_dict)

    if not os.path.isdir(_publish_path):
        logger.info("create publish dir {}".format(_publish_path))
        os.makedirs(_publish_path)
    try:
        with open(_publish_json_file,"w") as info:
            json.dump(_json_info, info,indent = 4,separators=(',',':'))
        _result = filefunc.publish_file(_publish_json_file,_production_json_file,True)
        cmds.AbcExport(j = _alljob)
        for _k,_v in upload_dict.items():
            _result = filefunc.publish_file(_k,_v,True)
    except Exception as e:
        logger.error(e)
        return False
    return True

if __name__ == '__main__':
    publish_abc()
