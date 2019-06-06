# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os
import json
import logging

import maya.cmds as cmds

import zfused_api

import zfused_maya.core.record as record

import zfused_maya.node.core.element as element
import zfused_maya.node.core.alembiccache as alembiccache
import zfused_maya.node.core.proxycontainer as proxycontainer
import zfused_maya.node.core.assembly as assembly


def read_json_file(file_path):
    with open(os.path.abspath(file_path), "r") as json_file:
        json_dict = json.load(json_file)
    return json_dict if json_dict else {}

def write_json_file(json_dict, file_path):
    with open(file_path,"w") as json_file:
        json_file.write(json.dumps(json_dict, indent = 4, separators=(',',':')))
        json_file.close()

def get_assets():
    import zfused_maya.core.record as record
    _assets = {}
    _project_id = record.current_project_id()
    _project_assets = zfused_api.asset.project_assets([_project_id])
    # print _project_assets
    for _asset in _project_assets:
        asset = zfused_api.asset.Asset(_asset["Id"])
        _assets[asset.code()] = asset.production_path()
    return _assets

def build_structure(parent_node_list, parent):
    _parent_name = parent
    _current_project_id = record.current_project_id()
    _assets = get_assets()
    for parent_node in parent_node_list:
        node_type = parent_node['node_type']
        child     = parent_node['child']
        namespace = parent_node['namespace']
        name      = parent_node['name']
        attr      = parent_node['attr']
        name = name.split("|")[-1]
        #if namespace != '':
        #    name = namespace + ':' + name
        if node_type == "assemblyReference":
            # _assets = zfused_api.zFused.get("asset", filter = {"Code": name, "ProjectId":_current_project_id})
            if not name in _assets:
                node_type = "transform"
            else:
                node_type = "assemblyReference"
                # _asset_handle = zfused_api.asset.Asset(_assets[0]["Id"])
                _production_path = _assets[name]
                # _proxy_file = "{}/shader/redshift/maya2017/proxy/{}.rs".format(_production_path, name)
                # _gpu_file = "{}/shader/redshift/maya2017/gpu/{}.abc".format(_production_path, name)
                _proxy_file = "{}/model/maya2017/assemblyDefinition/{}.mb".format(_production_path, name)
                print(_proxy_file)
        if _parent_name == '':
            if node_type == "assemblyReference":
                #cmds.file(_proxy_file, i = True)
                _assembly = assembly.create_assembly_reference(name, _proxy_file)
                _node_name = _assembly.name()
            else:
                _node_name = cmds.createNode(node_type, name = name, parent = "")
        else:
            if node_type == "assemblyReference":
                _assembly = assembly.create_assembly_reference(name, _proxy_file)
                _node_name = _assembly.name()
                _node_name = cmds.parent(_node_name, _parent_name)[0]               
            else:
                #  --------------------------------------------------------------------------
                if name == _parent_name:
                    name = "{}_dup_01".format(name)
                _node_name = cmds.createNode(node_type, name = name, parent = _parent_name)
            #_node_name = cmds.createNode(node_type, name = name, parent = parent)
        # _node_name = 
        for attr_name, attr_info in attr.items():
            attr_value = attr_info['static_data']
            if node_type == "assemblyReference":
                if attr_name in ["rpx", "rpy", "rpz", "spx", "spy", "spz"]:
                    continue
            cmds.setAttr(_node_name + '.' + attr_name, attr_value)
        if child:
            build_structure(child, _node_name)

def import_structure(output_link_object, output_link_id,  output_attr_id, input_link_object, input_link_id, input_attr_id):
    """ 导入场景结构
    """
    # _file_title = "fur/yeti"
    print(output_link_object, output_link_id,  output_attr_id, input_link_object, input_link_id, input_attr_id)
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

    print(_output_link_production_file)
    _datas = read_json_file(_output_link_production_file)
    print(_datas)
    build_structure(_datas, "")

    return
    # get shot info
    _elements = element.scene_elements()
    _asset_dict = element.get_asset(_elements, _file_title)
    _info = get_cache_info(_attr_file)
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