# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

""" 贴图文件操作集合 """

import os
import re
import logging
import shutil
import maya.cmds as cmds

import zfused_maya.core.filefunc as filefunc

logger = logging.getLogger(__file__)

TEXT_NODE = ["file"]

TEXTURE_ATTR_DICT = {
    "file" : "fileTextureName",
    "imagePlane": "imageName",
    "RedshiftNormalMap":"tex0",
    "RedshiftCameraMap":"tex0",
    "RedshiftSprite":"tex0",
    "RedshiftEnvironment":"tex0",
    "RedshiftLensDistortion":"tex0",
    "RedshiftDomeLight":"tex0",
    "RedshiftIESLight":"tex0",
    "RedshiftLightGobo":"tex0"
}

TEX_SUFFIX = ['.als',
              '.avi',
              '.bmp',
              '.cin',
              '.dds',
              '.eps',
              '.exr',
              '.gif',
              '.iff',
              '.jpeg',
              '.jpg',
              '.pic',
              '.pict',
              '.png',
              '.pntg',
              '.psd',
              '.qt',
              '.qtif',
              '.rla',
              '.sgi',
              '.svg',
              '.swf',
              '.swft',
              '.tga',
              '.tif',
              '.yuv']









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
    for _file_node_attr in _file_nodes:
        _file_node = _file_node_attr.split(".")[0]
        _type = cmds.nodeType(_file_node)
        _ori_file_texture_path = _get_file_full_name(_file_node_attr)
        _file_texture_path = _ori_file_texture_path
        _extend_file = _file_texture_path.split(src)[-1]
        if _extend_file.startswith("/"):
            _extend_file = _extend_file[1::]
        _new_file_text_path = "%s/%s"%(dst, _extend_file)
        # 锁定节点色彩空间，防止替换贴图时色彩空间设置丢失
        if _type == "file" and not cmds.getAttr("{}.ignoreColorSpaceFileRules".format(_file_node)):
            cmds.setAttr("{}.ignoreColorSpaceFileRules".format(_file_node), 1)
        while True:
            # _file_name = cmds.getAttr("{}.{}".format(_file_node,TEXTURE_ATTR_DICT[_type]))
            cmds.setAttr(_file_node_attr, _new_file_text_path, type = 'string')
            # print()
            if _get_file_full_name(_file_node_attr) == _new_file_text_path:
                break
        # 取消色彩空间锁定
        if _type == "file":
            cmds.setAttr("{}.ignoreColorSpaceFileRules".format(_file_node), 0)

def error_nodes():
    """get error file node
       判断 file 节点是否错误,填入错误贴图地址
    
    :rtype: list
    """
    _all_files = cmds.file(query=1, list=1, withoutCopyNumber=1)

    _all_files_dict = {}
    for _file in _all_files:
        _file_dir_name = os.path.dirname(_file)
        _, _file_suffix = os.path.splitext(_file)
        _all_files_dict[_file] = [ _file_dir_name, _file_suffix ]
    _file_nodes = cmds.ls( type = TEXT_NODE )
    _error_nodes = []
    for _file_node in _file_nodes:
        _type = cmds.nodeType(_file_node)
        _is_reference = cmds.referenceQuery(_file_node, isNodeReferenced = True)

        # _is_lock = cmds.getAttr("{}.{}".format(_file_node,TEXTURE_ATTR_DICT[_type]), l = True)
        # if _is_reference and _is_lock:
        #     continue
        if _is_reference:
            continue

        _file_name = _get_file_full_name("{}.{}".format(_file_node,TEXTURE_ATTR_DICT[_type]))
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

# def nodes():
#     """ 获取file节点

#     :rtype: list
#     """
#     _file_nodes = cmds.ls(type = TEXT_NODE)
#     _result_nodes = []
#     for _file_node in _file_nodes:
#         _type = cmds.nodeType(_file_node)
#         _is_reference = cmds.referenceQuery(_file_node, isNodeReferenced = True)
#         _is_lock = cmds.getAttr("{}.{}".format(_file_node,TEXTURE_ATTR_DICT[_type]), l = True)
#         if _is_reference and _is_lock:
#             continue
#         _result_nodes.append(_file_node)
#     return _result_nodes

def nodes(withAttribute = True,ignoreReference = True):
    """ 获取file节点

    :rtype: list
    """
    _list = []
    cmds.filePathEditor(rf = 1)
    item = cmds.filePathEditor(query=True, listFiles="", unresolved=False, withAttribute=True)
    if item:
        files = item[0::2]
        nodes = item[1::2]
        for _file,_node_attr in zip(files,nodes):
            _node = _node_attr.split(".")[0]
            if os.path.splitext(_file)[-1].lower() in TEX_SUFFIX:
                _is_reference = cmds.referenceQuery(_node, isNodeReferenced = True)

                # _is_lock = cmds.getAttr(_node_attr, l = True)
                # if _is_reference and _is_lock:
                #     continue
                if _is_reference and ignoreReference:
                    continue

                if withAttribute:
                    _list.append(_node_attr)
                else:
                    _list.append(_node)
    return _list

def files():
    _texture_files = []
    _nodes = nodes()
    if _nodes:
        for _node_attr in _nodes:
            _node = _node_attr.split(".")[0]
            _path = _get_file_full_name(_node_attr)
            _is_reference = cmds.referenceQuery(_node, isNodeReferenced = True)
            # _is_lock = cmds.getAttr(_node_attr, l = True)
            # if _is_reference and _is_lock:
            #     continue
            if _is_reference:
                continue
            _mode,_ani = 0,0
            if cmds.objExists("%s.uvTilingMode"%_node):
                _mode = cmds.getAttr("%s.uvTilingMode"%_node)
            if cmds.objExists("%s.useFrameExtension"%_node):
                _ani = cmds.getAttr("%s.useFrameExtension"%_node)
            if "<UDIM>" in os.path.basename(_path):
                _mode = 1
            if not _mode and not _ani:
                _texture_files.append(_path)
            else:
                if _mode:
                    _texture_files.extend(get_udim_texfile(_path,False))
                if _ani:
                    _texture_files.extend(get_frame_texfile(_path,False))


    return list(set(_texture_files))



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


def get_udim_texfile(filepath,boolean = True):
    '''get udim file
    '''
    filelist = []
    _path,_name = os.path.split(filepath)
    if os.path.exists(_path):
        _str,_suffix = os.path.splitext(_name)
        if "<UDIM>" in _str:
            _ele = _str.split("<UDIM>")
            _check_str = "\d{4}".join(_ele)
            for _i in os.listdir(_path):
                if re.search(r"{}{}".format(_check_str,_suffix),_i):
                    filelist.append("{}/{}".format(_path,_i))
        else:
            _udim = re.findall("\d{4}",_str)
            if _udim:
                ele = _str.split(_udim[-1])
                _check_str = _udim[-1].join(ele[:-1])
                for _j in os.listdir(_path):
                    if re.search(r"%s\d{4}%s"%(_check_str,_suffix),_j):
                        filelist.append("{}/{}".format(_path,_j))
    if filelist:
        if boolean:
            return True
        else:
            return filelist
    else:
        if boolean:
            return False
        else:
            return [filepath]

def get_frame_texfile(filepath,boolean = True):
    '''get frame file
    '''
    filelist = []
    _path,_name = os.path.split(filepath)
    if os.path.exists(_path):
        _str,_suffix = os.path.splitext(_name)
        if "<f>" in _str:
            _ele = _str.split("<f>")
            _check_str = "\d+".join(_ele)
            for _i in os.listdir(_path):
                if re.search("{}{}".format(_check_str,_suffix),_i):
                    filelist.append(r"{}/{}".format(_path,_i))
        else:
            _f = re.findall("\d+",_str)
            if _f:
                ele = _str.split(_f[-1])
                _check_str = _f[-1].join(ele[:-1])
                for _j in os.listdir(_path):
                    if re.search(r"%s\d{4}%s"%(_check_str,_suffix),_j):
                        filelist.append("{}/{}".format(_path,_j))
    if filelist:
        if boolean:
            return True
        else:
            return filelist
    else:
        if boolean:
            return False
        else:
            return [filepath]


def _get_file_full_name(file_node):
    _path = cmds.getAttr(file_node)
    if "" not  in os.path.splitdrive(_path):
        return _path
    workpath = cmds.workspace(q = 1,fn = 1)
    return r"{}/{}".format(workpath,_path)