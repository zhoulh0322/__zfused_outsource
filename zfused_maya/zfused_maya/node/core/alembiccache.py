# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

""" alembic缓存文件操作集合 """

import os
import maya.cmds as cmds

import zfused_maya.core.filefunc as filefunc


def publish_file(files, src, dst):
    """ upload files 

    """
    _files = files
    for _file in _files:
        #  alembic cache file
        _extend_file = _file.split(src)[-1]
        if _extend_file.startswith("/"):
            _extend_file = _extend_file[1::]
        _backup_file = os.path.join(dst, _extend_file)
        #  upload alembic cache file
        _result = filefunc.publish_file(_file, _backup_file)

def local_file(files, src, dst):
    """ local download files 

    """
    _files = files
    for _file in _files:
        #  backup texture file
        _extend_file = _file.split(src)[-1]
        if _extend_file.startswith("/"):
            _extend_file = _extend_file[1::]
        _local_file = os.path.join(dst, _extend_file)
        #  downlocal texture file
        #_result = filefunc.publish_file(_texture_file, _backup_texture_file)
        _local_dir = os.path.dirname(_local_file)
        if not os.path.isdir(_local_dir):
            os.makedirs(_local_dir)
        _result = shutil.copy(_file, _local_file)

def change_node_path(nodes, src, dst):
    """ change file nodes path

    """
    _file_nodes = nodes
    for _file_node in _file_nodes:
        _ori_file_texture_path = cmds.getAttr("{}.abc_File".format(_file_node))
        _file_texture_path = _ori_file_texture_path
        _extend_file = _file_texture_path.split(src)[-1]
        if _extend_file.startswith("/"):
            _extend_file = _extend_file[1::]
        _new_file_text_path = "%s/%s"%(dst, _extend_file)
        while True:
            cmds.setAttr("{}.abc_File".format(_file_node), _new_file_text_path, type = 'string')
            if cmds.getAttr("{}.abc_File".format(_file_node)) == _new_file_text_path:
                break

def nodes():
    """ 获取alembic cache节点

    :rtype: list
    """
    _file_nodes = cmds.ls(type = "AlembicNode")
    _result_nodes = []
    for _file_node in _file_nodes:
        _is_reference = cmds.referenceQuery(_file_node, isNodeReferenced = True)
        _is_lock = cmds.getAttr("{}.abc_File".format(_file_node), l = True)
        if _is_reference and _is_lock:
            continue
        _result_nodes.append(_file_node)
    return _result_nodes

def files():
    """get alembic cache file
    
    :rtype: list
    """
    _all_files = cmds.file(query=1, list=1, withoutCopyNumber=1)
    _all_files_dict = {}
    for _file in _all_files:
        _file_dir_name = os.path.dirname(_file)
        _, _file_suffix = os.path.splitext(_file)
        _all_files_dict[_file] = [_file_dir_name, _file_suffix]
    _file_nodes = cmds.ls(type = "AlembicNode")
    _alembic_files = []
    for _file_node in _file_nodes:
        _is_reference = cmds.referenceQuery(_file_node, isNodeReferenced = True)
        _is_lock = cmds.getAttr("{}.abc_File".format(_file_node), l = True)
        if _is_reference and _is_lock:
            continue
        _file_name = cmds.getAttr("{}.abc_File".format(_file_node))
        _node_dir_name = os.path.dirname(_file_name)
        _, _node_suffix = os.path.splitext(_file_name)
        
        for _file in _all_files:
            _file_dir_name,_file_suffix = _all_files_dict[_file]
            if _node_dir_name == _file_dir_name and _node_suffix == _file_suffix:
                _alembic_files.append(_file)
    return _alembic_files


def paths(alembic_files):
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

    _set_list = _get_file_set_list(alembic_files)
    if not _set_list:
        return []
    _value = []
    _set(_set_list, _value)  

    return _value