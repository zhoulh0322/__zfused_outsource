# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

""" alembic缓存文件操作集合 """

import os
import maya.cmds as cmds
import zfused_maya.core.filefunc as filefunc
import zfused_maya.node.core.element as element
import zfused_maya.node.core.assets as assets

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

def create_frame_cache(_path,startTime,endTime,grpname,*args):
    '''生成创建缓存命令
    '''
    if isinstance(grpname,list):
        roots = ''.join(["-root %s "%i for i in grpname])
    else:
        roots = "-root %s "%grpname
    # 导出附加参数
    if args:
        exOptions = ''.join([" -%s"%j for j in args])
    else:
        exOptions = ''
    joborder = "-frameRange %s %s %s -dataFormat hdf %s -file %s"%(startTime,endTime,exOptions,roots,_path)
    return joborder

def import_cache(asset,namespace,node,path,texfile = None):
    '''导入缓存
    '''
    # def get_ns(nameSpace):
    #     # 自动生成空间名序号,暂不使用
    #     index = 0
    #     _namespaces = list(set(cmds.namespaceInfo(r = 1, lon = 1)) - set(["shared","UI"]))
    #     while True:
    #         if nameSpace in _namespaces:
    #             if nameSpace[-1].isdigit():
    #                 _num = re.findall("\d+",nameSpace)[-1]
    #                 nameSpace = "{}{}".format(nameSpace[:-len(_num)],int(_num)+index)
    #             else:
    #                 nameSpace = "{}{}".format(nameSpace,index)
    #             index += 1
    #         else:
    #             return nameSpace

    def connect_usedattr(src,dst):
        """connect transform attr
        """
        abc_trans = list(set(cmds.listRelatives(src,ad = 1,type = "transform")) | set([src]))
        tex_trans = list(set(cmds.listRelatives(dst,ad = 1,type = "transform")) | set([dst]))
        for _s,_d in zip(sorted(abc_trans),sorted(tex_trans)):
            # set visibility value
            if cmds.objExists("{}.v".format(_s)) and not cmds.getAttr("{}.v".format(_s)):
                cmds.setAttr("{}.v".format(_d),0)
            # set connected attr
            _usedattr = cmds.listConnections(_s,p = 1,c = 1,d = 0)
            if _usedattr:
                for _i in _usedattr[0::2]:
                    _attrname = _i.split(_s)[-1]
                    cmds.connectAttr(_i,"{}{}".format(_d,_attrname))
                    print ("connect attr:{} to {}".format(_i,"{}{}".format(_d,_attrname)))

    _grp_name = "abc_hidegrp"
    # create abc_grp
    if not cmds.objExists(_grp_name):
        _grp = cmds.createNode("transform",n = _grp_name)
        # cmds.setAttr("{}.hiddenInOutliner".format(_grp),1)
        cmds.setAttr("{}.v".format(_grp),0)
    else:
        _grp = _grp_name

    if asset:
        if not cmds.objExists(texfile):
            raise 
        # load alembic file
        _newns = "abc_{}".format(namespace)
        # _newns = get_ns(namespace)
        cmds.file(path,i = 1,iv = 1,ra = 1,mergeNamespacesOnClash = 0,ns = _newns,pr = 1,ifr = 1,itr = "override",type = "Alembic")
        _abcnode = "{}:{}".format(_newns,node)
        cmds.parent(_abcnode,_grp)
        cmds.setAttr("{}.t".format(_abcnode),lock = 1)
        cmds.setAttr("{}.r".format(_abcnode),lock = 1)
        cmds.setAttr("{}.s".format(_abcnode),lock = 1)
        _bsnode = cmds.blendShape(_abcnode,texfile,w = (0,1.0))
        # cmds.setAttr("{}.{}".format(_bsnode[-1],node),1)
        cmds.setAttr("{}.origin".format(_bsnode[-1]),0)
        connect_usedattr(_abcnode,texfile)
    else:
        cmds.file(path,i = 1,iv = 1,ra = 1,mergeNamespacesOnClash = 1,ns = ":",pr = 1,ifr = 1,itr = "override",type = "Alembic")
        cmds.setAttr("{}.t".format(namespace),lock = 1)
        cmds.setAttr("{}.r".format(namespace),lock = 1)
        cmds.setAttr("{}.s".format(namespace),lock = 1)
    return True

def remove_cache(*args):
    '''移除缓存的bs连接
        传入要移除的模型名(传入大组名或任意含有空间名的模型)
        没有传入值移除全部缓存
        附：blendShape常用查询命令
            t #获取所有变形模型
            g #获取所有被变形模型
            dt #获取所有变形器节点和groupid
            w #查询权重属性
            en #查询封套属性（envelope属性，一般不改）
    '''
    def get_removeinfo(nodes,*args):
        list1,list2,list3 = [],[],[]
        for _node in nodes:
            _deformednodes = cmds.blendShape(_node,q = 1,g = 1)
            _trans = cmds.listRelatives(_deformednodes,p = 1,type = "transform")
            _ns = set([cmds.referenceQuery(i,ns = 1) for i in _trans])
            if args and _ns not in args:
                continue
            orishape = set(cmds.listRelatives(_trans,s = 1))-set(cmds.listRelatives(_trans,s = 1,ni = 1))
            list1.extend(orishape)
            list2.extend(_deformednodes)
            list2.extend(cmds.blendShape(_node,q = 1,dt = 1))
            list2.append(_node)
            _target = cmds.blendShape(_node,q = 1,t = 1)
            if _target:
                _grp = get_cache_grp(_target)
                list2.append(_grp)
                _remove_ns = get_namespace(_grp)
                if _remove_ns:
                    list3.append(_remove_ns)
        return list1,list2,list3

    def get_cache_grp(node):
        while True:
            if "abc_hidegrp" in cmds.listRelatives(node,p = 1):
                return node
            else:
                node = cmds.listRelatives(node,p = 1)[0]

    def get_namespace(node):
        _ns = node[:-len(node.split(":")[-1])-1]
        if cmds.namespace(ex = _ns):
            return _ns
        return None

    bsnodes = cmds.ls(type = "blendShape")
    if not bsnodes:
        return
    bsnodes = [i for i in bsnodes if not cmds.referenceQuery(i,inr = 1)]
    _filters = []
    if args:
        _filters = [cmds.referenceQuery(i,ns = 1) for i in args]
    _orifiles,_removefiles,_namespacefiles = get_removeinfo(bsnodes,*_filters)
    if _removefiles:
        cmds.delete(_removefiles)
    if _orifiles:
        for _orifile in _orifiles:
            cmds.setAttr("{}.intermediateObject".format(_orifile),0)
    if _namespacefiles:
        for _namespacefile in _namespacefiles:
            cmds.namespace(rm = _namespacefile,mnr = 1)

def get_meshattr(group):
    _info = {}
    _trans = cmds.ls(group, dag = True, type = "transform")
    if not _trans:
        return _info
    for _tran in _trans:
        shapes = cmds.listRelatives(_tran,s = 1,ni = 1)
        if shapes:
            _attrs = cmds.listAttr(shapes[0],fp = 1,o = 1)
            if _attrs:
                _info[_tran] = {}
                for _attr in _attrs:
                    _info[_tran][_attr] = [cmds.getAttr("{}.{}".format(shapes[0],_attr)),cmds.getAttr("{}.{}".format(shapes[0],_attr),type = 1)]
                    # print (cmds.getAttr("{}.{}".format(shapes[0],_attr)))
    return _info

def set_meshattr(group,info):
    _trans = cmds.ls(group, dag = True, type = "transform")
    for _tran in _trans:
        shapes = cmds.listRelatives(_tran,s = 1,ni = 1)
        if shapes:
            if _tran in info:
                attr_info = info[_tran]
                for k,v in attr_info.items():
                    _v,_t = v
                    cmds.setAttr("{}.{}".format(shapes[0],k),_v,type = _t)
            else:
                print (">>>>>>>>>>>>>>>>>>>>>{} is not found".format(_tran))

def load_asset(cacheinfo,step,load = True):
    '''资产领取(外包端适用)
    '''
    _dict = {}
    _interpath = "maya2017/file"
    _assets = assets.get_assets()
    for item in cacheinfo:
        _assetname = item[0]
        if _assetname and _assetname in _assets:
            _ns = item[1].split(":")[-1]
            if _assetname in _dict:
                _dict[_assetname]["namespace"].append(_ns)
            else:
                _dict[_assetname] = {}
                _dict[_assetname]["namespace"] = [_ns]
                _production_path = "/".join([_assets[_assetname],step,_interpath])
                _dict[_assetname]["path"] = "{}/{}.mb".format(_production_path,_assetname)
            if load:
                cmds.file(_dict[_assetname]["path"],r = 1,iv = 1,mergeNamespacesOnClash = 1,ns = _ns)
    return _dict