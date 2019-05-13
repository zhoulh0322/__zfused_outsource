# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

""" 修改mesh shape名,统一产线 """

from __future__ import print_function

import maya.cmds as cmds

import logging
logger = logging.getLogger(__name__)


def fix_mesh_name(post_fix_name, group_list = []):
    """修改shape名

    :param post_fix_name: 修改的后缀名称
    :param group_list: 组列表, 按组改名

    :rtype: None
    """

    # 获取组内transform

    def repair_shader(shape,transform):
        meshdict = {}
        _sgs = cmds.listConnections(_shape,d = 1,type = "shadingEngine")
        if _sgs:
            for _sg in _sgs:
                # mat = cmds.listConnections("%s.surfaceShader"%_sg)
                cmds.hyperShade(objects = _sg)
                sel = cmds.ls(sl = 1,l = 1)
                print ([i for i in sel if transform in i])
                meshdict[_sg] = [i for i in sel if transform in i]
        return meshdict

    _transforms = []
    if group_list:
        _transforms = cmds.ls(group_list, dag = True, type = "transform")
    else:
        _transforms = cmds.ls(type = "transform")

    if not _transforms:
        return

    shader_dict = {}
    for _transform in _transforms:
        _show_shapes = cmds.listRelatives(_transform, s = True, ni = True, f = True, type = "mesh")
        if not _show_shapes:
            continue
        _all_shapes = cmds.listRelatives(_transform, s = True, f = True, type = "mesh")
        _other_shapes = list(set(_all_shapes) - set(_show_shapes))
        if _other_shapes:
            for _shape in _other_shapes:
                if _shape.endswith(post_fix_name):
                    cmds.rename(_shape, "{}_orig".format(_shape.split("|")[-1][0:len(_shape)-len(post_fix_name)]))
        for _shape in _show_shapes:
            _dict = repair_shader(_shape,_transform)

            _new_shape = "{}{}".format(_transform, post_fix_name)
            if "|" in "{}{}".format(_transform, post_fix_name):
                _new_shape = _new_shape.split("|")[-1]
            _new = cmds.rename(_shape, _new_shape)

        if _dict:
            for k,v in _dict.items():
                _mesh = [i.replace(i.split(".")[0],_transform) for i in v]
                # print (">>>>>>>>>>>>>>>>>>>>",mesh)
                # cmds.select(_mesh)
                # cmds.hyperShade(assign = "lambert1")
                # cmds.select(cl = 1)
                # cmds.select(_mesh)haim
                # cmds.hyperShade(assign = k)
                if k not in shader_dict:
                    shader_dict[k] = []
                shader_dict[k].extend(_mesh)

    # if shader_dict:
    #     for k2,v2 in shader_dict.items():
    #         cmds.select(v2)
    #         cmds.hyperShade(assign = "lambert1")
    #         cmds.hyperShade(assign = k2)
    return shader_dict





def fix_deformed_mesh_name(post_fix_name, group_list = []):
    # """修改deformed名
    # :param post_fix_name: 修改的后缀名称
    # :param group_list: 组列表, 按组改名
    # :rtype: None
    # """

    #获取组内transform
    _transforms = []
    if group_list:
        _transforms = cmds.ls(group_list, dag = True, type = "transform")
    else:
        _transforms = cmds.ls(type = "transform")
    if not _transforms:
        return
    for _transform in _transforms:
        _show_shapes = cmds.listRelatives(_transform, s = True, ni = True, f = True, type = "mesh")
        if not _show_shapes:
            continue
        for _shape in _show_shapes:
            if not _shape.endswith(post_fix_name):
                # 导出abc缓存时会自动补齐shape的空间名
                _name = "{}{}".format(_transform.split(":")[-1], post_fix_name)
                cmds.rename(_shape,_name)


if __name__ == "__main__":
    fix_mesh_name("_rendering", ["c_fengzhiwei_model_GRP"])