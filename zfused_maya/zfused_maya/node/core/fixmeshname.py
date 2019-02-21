# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

""" 修改mesh shape名,统一产线 """

from __future__ import print_function

import maya.cmds as cmds

import logging


def fix_mesh_name(post_fix_name, group_list = []):
    """修改shape名

    :param post_fix_name: 修改的后缀名称
    :param group_list: 组列表, 按组改名

    :rtype: None
    """

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
        _all_shapes = cmds.listRelatives(_transform, s = True, f = True, type = "mesh")
        _other_shapes = list(set(_all_shapes) - set(_show_shapes))
        if _other_shapes:
            for _shape in _other_shapes:
                if _shape.endswith(post_fix_name):
                    cmds.rename(_shape, "{}_orig".format(_shape.split("|")[-1][0:len(_shape)-len(post_fix_name)]))
        for _shape in _show_shapes:
            cmds.rename(_shape, "{}{}".format(_transform, post_fix_name))


if __name__ == "__main__":
    fix_mesh_name("_rendering", ["c_fengzhiwei_model_GRP"])