# coding:utf-8
# --author-- binglu.wang
from __future__ import print_function

import os
import json
import logging

import maya.cmds as cmds

import zfused_api
import zfused_maya.node.core.element as element
import zfused_maya.node.core.yeticache as yeticache

__all__ = ["import_yeti_cache"]
logger = logging.getLogger(__name__)

_is_load = cmds.pluginInfo("pgYetiMaya", query=True, loaded = True)
if not _is_load:
    try:
        logger.info("try load pgYetiMaya plugin")
        cmds.loadPlugin("pgYetiMaya")
    except Exception as e:
        logger.error(e)
        sys.exit()

def get_cache_info(cache_file):
    '''load json info
    '''
    with open(cache_file, 'r') as info:
        dataInfo = json.load(info)
        info.close()
    return dataInfo

def arrange_info(info,_dict = {}):
    for _i in info:
        _asset,_ns,_node,_path = _i
        if _asset not in _dict:
            _dict[_asset] = {}
        if _ns not in _dict[_asset]:
            _dict[_asset][_ns] = []
        _dict[_asset][_ns].append(_node)
        _dict[_asset][_ns].append(_path)
    return _dict

def import_yeti_cache(output_link_object, output_link_id,  output_attr_id, input_link_object, input_link_id, input_attr_id):
    # 思路：
    # 镜头打开后查询json信息，如果有，根据json信息对比文件中的元素领取yeti材质文件，然后附缓存
    _file_title = "fur/yeti"

    _output_attr_handle = zfused_api.outputattr.OutputAttr(output_attr_id)
    _project_step_id = _output_attr_handle.data["ProjectStepId"]
    _project_step_handle = zfused_api.step.ProjectStep(_project_step_id)
    _step_code = _project_step_handle.code()
    _software_code = zfused_api.software.Software(_project_step_handle.data["SoftwareId"]).code()

    _output_link_handle = zfused_api.objects.Objects(output_link_object, output_link_id)
    _output_link_production_path = _output_link_handle.production_path()
    _output_link_publish_path = _output_link_handle.publish_path()
    _file_code = _output_link_handle.file_code()
    _suffix = _output_attr_handle.suffix()
    _attr_code = _output_attr_handle.code()
    _output_link_production_file = "{}/{}/{}/{}/{}{}".format( _output_link_production_path, _step_code, _software_code, _attr_code, _file_code, _suffix )

    if not os.path.exists(_output_link_production_file):
        return False
    # get shot info
    # _elements = element.scene_elements()
    # _asset_dict = element.get_asset(_elements,_file_title)
    _jsoninfo = get_cache_info(_output_link_production_file)
    if not _jsoninfo:
        return
    _asset_dict,_realinfo = yeticache.load_asset(_jsoninfo,_file_title)
    if not _asset_dict:
        return
    _info = arrange_info(_realinfo)

    # merge yeti cache
    for _asset in _info:
        for item in _info[_asset].values():
            if _asset in _asset_dict and _asset_dict[_asset]["namespace"]:
                _tex_ns = _asset_dict[_asset]["namespace"][0]
                try:
                    _nodes = item[::2]
                    _paths = item[1::2]
                    for _node,_path in zip(_nodes,_paths):
                        logger.info("load yeticache:{}".format(_path))
                        yeticache.import_cache(_path,"{}:{}".format(_tex_ns,_node))
                except:
                    logger.warning("wrong load yeti cache:{}".format(_path))
                _asset_dict[_asset]["namespace"].pop(0)
    return True

if __name__ == '__main__':
    import_yeti_cache()