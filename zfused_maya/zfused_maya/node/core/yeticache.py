# coding:utf-8
# --author-- binglu.wang

""" yeti缓存操作集合 """

import os
import re
import logging
import shutil
import maya.cmds as cmds

import zfused_api
import zfused_maya.core.filefunc as filefunc
import zfused_maya.core.record as record
import zfused_maya.node.core.element as element
import zfused_maya.node.core.assets as assets

logger = logging.getLogger(__file__)

def nodes():
    '''get pgYteiMaya nodes
    
    '''
    return cmds.ls(type = "pgYetiMaya")

def publish_file(src, dst):
    """ upload files 

    """
    _files = os.listdir(src)
    for _file in _files:
        _srcfile = "{}/{}".format(src,_file)
        _dstfile = "{}/{}".format(dst,_file)
        logger.info("upload file {} to {}".format(_srcfile, _dstfile))
        _result = filefunc.publish_file(_srcfile, _dstfile)

def create_cache(yetiNode,path,startFrame,endFrame,frameSample):
    """ create yeticache 

    """
    if not os.path.isdir(os.path.split(path)[0]):
        os.makedirs(os.path.split(path)[0])
    cmds.pgYetiCommand(yetiNode,writeCache = path,range = [startFrame, endFrame], samples = frameSample,updateViewport = 0, generatePreview = 0)

def get_upload_info(nodes,frameLevel,publish_path,local_path,childfolder = True):
    """ get yeti info

    """
    _json_info = []
    _local_info = {}
    assetlist = get_asset_list()
    for node in nodes:
        try:
            _nsname = cmds.referenceQuery(node,ns = 1)
            if _nsname.startwith(":"):
                _nsname = _nsname[1:]
        except:
            _nsname = node[:-len(node.split(":")[-1])-1]
        cachename = node[len(_nsname)+1:]
        if _nsname in assetlist:
            _assetname = assetlist[_nsname]
            # 短空间名
            short_ns = _nsname.split(":")[-1]
            if childfolder:
                _webpath ="{}/{}/{}/{}.%0{}d.fur".format(publish_path,short_ns,cachename,cachename,frameLevel)
                _localpath ="{}/{}/{}/{}.%0{}d.fur".format(local_path,short_ns,cachename,cachename,frameLevel)
            else:
                _webpath ="{}/{}/{}.%0{}d.fur".format(publish_path,short_ns,cachename,frameLevel)
                _localpath ="{}/{}/{}.%0{}d.fur".format(local_path,short_ns,cachename,frameLevel)
            tempinfo = []
            tempinfo.append(_assetname)#assetname
            tempinfo.append(short_ns)#namespacename
            tempinfo.append(node.split("{}:".format(_nsname))[-1])#nodename
            tempinfo.append(_webpath)#cachepath
            _json_info.append(tempinfo)
            _local_info[node] = [_localpath,_webpath]
        else:
            logger.info("worng asset :{}".format(_nsname))
            continue
    return _json_info,_local_info

def get_asset_list():
    _dict = {}
    import zfused_maya.node.core.element as element
    _elements = element.scene_elements()
    for _element in _elements:
        _link_handle = zfused_api.objects.Objects(_element["link_object"], _element["link_id"])
        _dict[_element["namespace"]] = _link_handle.code()
    return _dict

def import_cache(path,texfile):
    cmds.setAttr("{}.fileMode".format(texfile),1)
    cmds.setAttr("{}.cacheFileName".format(texfile),path,type = "string")

def load_asset(cacheinfo,step,_dict = {}):
    '''资产领取(外包端适用)
    '''
    def get_ns(nameSpace):
        # 生成空间名
        index = 0
        _namespaces = list(set(cmds.namespaceInfo(r = 1, lon = 1)) - set(["shared","UI"]))
        while True:
            if nameSpace in _namespaces:
                index += 1
                if nameSpace[-1].isdigit():
                    _num = re.findall("\d+",nameSpace)[-1]
                    nameSpace = "{}{}".format(nameSpace[:-len(_num)],index)
                else:
                    nameSpace = "{}{}".format(nameSpace,index)
            else:
                return nameSpace

    _interpath = "maya2017/file"
    temp_dict = {}
    _assets = assets.get_assets()
    for i,item in enumerate(cacheinfo):
        _assetname = item[0]
        if _assetname in _assets:
            # set real namespace
            if item[1] in temp_dict:
                _ns = temp_dict[item[1]]
                cacheinfo[i][1] = temp_dict[item[1]]
            else:
                _ns = get_ns(item[1].split(":")[-1])
                temp_dict[item[1]] = _ns
                cacheinfo[i][1] = _ns

            if _assetname in _dict:
                _dict[_assetname]["namespace"].append(_ns)
            else:
                _dict[_assetname] = {}
                _dict[_assetname]["namespace"] = [_ns]
                _production_path = "/".join([_assets[_assetname],step,_interpath])
                _dict[_assetname]["path"] = "{}/{}.mb".format(_production_path,_assetname)
                cmds.file(_dict[_assetname]["path"],r = 1,iv = 1,mergeNamespacesOnClash = 1,ns = _ns)
    return _dict,cacheinfo

if __name__ == '__main__':
    get_cache_info()
