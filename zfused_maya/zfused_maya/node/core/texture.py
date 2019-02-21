# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

""" 贴图文件操作集合 """

import os
import logging
import shutil
import maya.cmds as cmds

import zfused_maya.core.filefunc as filefunc

logger = logging.getLogger(__file__)


TEXT_NODE = ["file", "imagePlane", "RedshiftNormalMap","RedshiftCameraMap"]
TEXTURE_ATTR_DICT = {
    "file" : "fileTextureName",
    "imagePlane": "imageName",
    "RedshiftNormalMap":"tex0",
    "RedshiftCameraMap":"tex0",
}


def publish_file(files, src, dst):
    """ upload files 

    """
    _texture_files = files
    #if _texture_files:
    #    _path_set = texture.paths(_texture_files)[0]
    #    _intersection_path = max(_path_set)
    for _texture_file in _texture_files:
        #  backup texture file
        _extend_file = _texture_file.split(src)[-1]
        if _extend_file.startswith("/"):
            _extend_file = _extend_file[1::]
        _backup_texture_file = os.path.join(dst, _extend_file)
        #  upload texture file
        logger.info("upload file {} to {}".format(_texture_file, _backup_texture_file))
        _result = filefunc.publish_file(_texture_file, _backup_texture_file)
        #  if has .tx file and will upload
        _except_suffix, _ = os.path.splitext(_texture_file)
        _tx_texture_file = "{}.tx".format(_except_suffix)
        if os.path.isfile(_tx_texture_file):
            _extend_file = _tx_texture_file.split(src)[-1]
            if _extend_file.startswith("/"):
                _extend_file = _extend_file[1::]
            _backup_tx_texture_file = os.path.join(dst, _extend_file)
            #  upload tx file
            _result = filefunc.publish_file(_tx_texture_file, _backup_tx_texture_file)

def local_file(files, src, dst):
    """ local download files 

    """
    _texture_files = files
    #if _texture_files:
    #    _path_set = texture.paths(_texture_files)[0]
    #    _intersection_path = max(_path_set)
    for _texture_file in _texture_files:
        #  backup texture file
        _extend_file = _texture_file.split(src)[-1]
        if _extend_file.startswith("/"):
            _extend_file = _extend_file[1::]
        _local_texture_file = os.path.join(dst, _extend_file)
        #  downlocal texture file
        #_result = filefunc.publish_file(_texture_file, _backup_texture_file)
        _local_texture_dir = os.path.dirname(_local_texture_file)
        if not os.path.isdir(_local_texture_dir):
            os.makedirs(_local_texture_dir)
        _result = shutil.copy(_texture_file, _local_texture_file)
        #  if has .tx file and will local download
        _except_suffix, _ = os.path.splitext(_texture_file)
        _tx_texture_file = "{}.tx".format(_except_suffix)
        if os.path.isfile(_tx_texture_file):
            _extend_file = _tx_texture_file.split(src)[-1]
            if _extend_file.startswith("/"):
                _extend_file = _extend_file[1::]
            _local_tx_texture_file = os.path.join(dst, _extend_file)
            #  download tx file
            #_result = filefunc.publish_file(_tx_texture_file, _local_tx_texture_file)
            _local_tx_texture_dir = os.path.dirname(_local_tx_texture_file)
            if not os.path.dirname(_local_tx_texture_dir):
                os.makedirs(_local_tx_texture_dir)
            _result = shutil.copy(_tx_texture_file, _local_tx_texture_file)

def change_node_path(nodes, src, dst):
    """ change file nodes path

    """
    _file_nodes = nodes
    #if _file_nodes:
    for _file_node in _file_nodes:
        _type = cmds.nodeType(_file_node)
        _ori_file_texture_path = cmds.getAttr("{}.{}".format(_file_node,TEXTURE_ATTR_DICT[_type]))
        _file_texture_path = _ori_file_texture_path
        _extend_file = _file_texture_path.split(src)[-1]
        if _extend_file.startswith("/"):
            _extend_file = _extend_file[1::]
        _new_file_text_path = "%s/%s"%(dst, _extend_file)
        # 锁定节点色彩空间，防止替换贴图时色彩空间设置丢失
        if _type =="file" and not cmds.getAttr("{}.ignoreColorSpaceFileRules".format(_file_node)):
            cmds.setAttr("{}.ignoreColorSpaceFileRules".format(_file_node), 1)
        while True:
            # _file_name = cmds.getAttr("{}.{}".format(_file_node,TEXTURE_ATTR_DICT[_type]))
            cmds.setAttr("{}.{}".format(_file_node,TEXTURE_ATTR_DICT[_type]), _new_file_text_path, type = 'string')
            if cmds.getAttr("{}.{}".format(_file_node,TEXTURE_ATTR_DICT[_type])) == _new_file_text_path:
                break
        # 取消色彩空间锁定
        if _type =="file":
            cmds.setAttr("{}.ignoreColorSpaceFileRules".format(_file_node), 0)

def error_nodes():
    """get error file node
       判断file节点是否错误,填入错误贴图地址
    
    :rtype: list
    """
    _all_files = cmds.file(query=1, list=1, withoutCopyNumber=1)
    _all_files_dict = {}
    for _file in _all_files:
        _file_dir_name = os.path.dirname(_file)
        _, _file_suffix = os.path.splitext(_file)
        _all_files_dict[_file] = [_file_dir_name, _file_suffix]
    _file_nodes = cmds.ls(type = TEXT_NODE)
    _error_nodes = []
    for _file_node in _file_nodes:
        _type = cmds.nodeType(_file_node)
        _is_reference = cmds.referenceQuery(_file_node, isNodeReferenced = True)
        _is_lock = cmds.getAttr("{}.{}".format(_file_node,TEXTURE_ATTR_DICT[_type]), l = True)
        if _is_reference and _is_lock:
            continue
        _file_name = cmds.getAttr("{}.{}".format(_file_node,TEXTURE_ATTR_DICT[_type]))
        _node_dir_name = os.path.dirname(_file_name)
        _, _node_suffix = os.path.splitext(_file_name)
        _is_error = True
        for _file in _all_files:
            _file_dir_name,_file_suffix = _all_files_dict[_file]
            if _node_dir_name == _file_dir_name and _node_suffix == _file_suffix:
                _is_error = False
        if _is_error:
            _error_nodes.append(_file_node)
    return _error_nodes

def nodes():
    """ 获取file节点

    :rtype: list
    """
    _file_nodes = cmds.ls(type = TEXT_NODE)
    _result_nodes = []
    for _file_node in _file_nodes:
        _type = cmds.nodeType(_file_node)
        _is_reference = cmds.referenceQuery(_file_node, isNodeReferenced = True)
        _is_lock = cmds.getAttr("{}.{}".format(_file_node,TEXTURE_ATTR_DICT[_type]), l = True)
        if _is_reference and _is_lock:
            continue
        _result_nodes.append(_file_node)
    return _result_nodes

def files():
    """ get texture file
    
    :rtype: list
    """
    _all_files = cmds.file(query=1, list=1, withoutCopyNumber=1)
    _all_files_dict = {}
    for _file in _all_files:
        _file_dir_name = os.path.dirname(_file)
        _, _file_suffix = os.path.splitext(_file)
        _all_files_dict[_file] = [_file_dir_name, _file_suffix]
    _file_nodes = cmds.ls(type = TEXT_NODE)
    _texture_files = []
    for _file_node in _file_nodes: 
        _type = cmds.nodeType(_file_node)
        _is_reference = cmds.referenceQuery(_file_node, isNodeReferenced = True)
        _is_lock = cmds.getAttr("{}.{}".format(_file_node,TEXTURE_ATTR_DICT[_type]), l = True)
        if _is_reference and _is_lock:
            continue
        _file_name = cmds.getAttr("{}.{}".format(_file_node,TEXTURE_ATTR_DICT[_type]))
        # print _file_node,_file_name
        _node_dir_name = os.path.dirname(_file_name)
        _, _node_suffix = os.path.splitext(_file_name)
        if _file_name in _all_files_dict:
            for _file in _all_files:
                # _file_dir_name = os.path.dirname(_file)
                # _, _file_suffix = os.path.splitext(_file)
                _file_dir_name,_file_suffix = _all_files_dict[_file]
                if _node_dir_name == _file_dir_name and _node_suffix == _file_suffix:
                    if _file not in _texture_files:
                        _texture_files.append(_file)
        else:
            _texture_files.append(_file_name)
    return _texture_files

# def node_files():
#     """ get node-file
#     """

#     _node_files = {}

#     """
#     _all_files = cmds.file(query=1, list=1, withoutCopyNumber=1)
#     _all_files_dict = {}
#     for _file in _all_files:
#         _file_dir_name = os.path.dirname(_file)
#         _, _file_suffix = os.path.splitext(_file)
#         _all_files_dict[_file] = [_file_dir_name, _file_suffix]
#     _file_nodes = cmds.ls(type = "file")

#     for _file_node in _file_nodes:
#         _texture_files = []
#         _is_reference = cmds.referenceQuery(_file_node, isNodeReferenced = True)
#         _is_lock = cmds.getAttr("{}.fileTextureName".format(_file_node), l = True)
#         if _is_reference and _is_lock:
#             continue
#         _file_name = cmds.getAttr("{}.fileTextureName".format(_file_node))
#         _node_dir_name = os.path.dirname(_file_name)
#         _, _node_suffix = os.path.splitext(_file_name)
        
#         for _file in _all_files:
#             # _file_dir_name = os.path.dirname(_file)
#             # _, _file_suffix = os.path.splitext(_file)
#             _file_dir_name, _file_suffix = _all_files_dict[_file]
#             if _node_dir_name == _file_dir_name and _node_suffix == _file_suffix:
#                 if _file not in _texture_files:
#                     _texture_files.append(_file)
        
#         _node_files[_file_node] = _texture_files 
#     """
#     import glob

#     files = cmds.ls(type=["file", "imagePlane"])

#     for i in files:
#         result = []
#         if cmds.objectType(i) == "file":
#             #animated ?
#             testAnimated = cmds.getAttr("{0}.useFrameExtension".format(i))
#             is_udim = cmds.getAttr("{}.uvTilingMode".format(i))
#             if testAnimated or is_udim != 0:
#                 # Find the path
#                 fullpath= cmds.getAttr("{0}.fileTextureName".format(i))

#                 # Replace /path/img.padding.ext by /path/img.*.ext
#                 image = fullpath.split("/")[-1]
#                 imagePattern = image.split(".")
#                 imagePattern[1] = "*"
#                 imagePattern = ".".join(imagePattern)

#                 # You could have done a REGEX with re module with a pattern name.padding.ext
#                 # We join the path with \\ in order to be Linux/Windows/Apple format
#                 folderPath = "\\".join(fullpath.split("/")[:-1] + [imagePattern])

#                 # Find all image on disk
#                 result+=(glob.glob(folderPath))
#             else:
#                 result.append(cmds.getAttr("{0}.fileTextureName".format(i)))

#         elif cmds.objectType(i) == "imagePlane":
#             #animated ?
#             testAnimated = cmds.getAttr("{0}.useFrameExtension".format(i))
#             if testAnimated:
#                 # Find the path
#                 fullpath= cmds.getAttr("{0}.imageName".format(i))
#                 # Replace /path/img.padding.ext by /path/img.*.ext
#                 image = fullpath.split("/")[-1]
#                 imagePattern = image.split(".")
#                 imagePattern[1] = "*"
#                 imagePattern = ".".join(imagePattern)

#                 # You could have done a REGEX with re module with a pattern name.padding.ext
#                 # We join the path with \\ in order to be Linux/Windows/Apple format
#                 folderPath = "\\".join(fullpath.split("/")[:-1] + [imagePattern])

#                 # Find all image on disk
#                 result+=(glob.glob(folderPath))
#             else:
#                 result.append(cmds.getAttr("{0}.imageName".format(i)))

#         _node_files[i] = result

#     return _node_files

def paths(text_files):
    """ 获取文件路径交集

    :rtype: list
    """
    #get texture sets
    def _get_set(path):
        # 获取文件路径集合
        _list = []
        def _get_path(_path, _list):
            _path_new = os.path.dirname(_path)
            if _path_new != _path:
                _list.append(_path_new)
                _get_path(_path_new, _list)
        _get_path(path, _list)
        return _list

    def _get_file_set_list(_files):
        _files_set_dict = {}
        _set_list = []
        for _f in _files:
            _set = set(_get_set(_f))
            _set_list.append(_set)
        return _set_list

    def _set(set_list,value):
        _frist = set_list[0]
        value.append(_frist)
        _left_list = []
        for i in set_list:
            _com = _frist & i
            if not _com:
                _left_list.append(i)
                continue
            value[len(value)-1] = _com
        if _left_list:
            _set(_left_list, value)

    _set_list = _get_file_set_list(text_files)
    if not _set_list:
        return []
    _value = []
    _set(_set_list, _value)  

    return _value


