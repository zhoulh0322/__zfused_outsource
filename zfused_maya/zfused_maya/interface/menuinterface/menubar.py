# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os
import json
import logging

import maya.cmds as cmds

import zfused_maya.core.menu as menu

__all__ = ["build", "delete", "rebuild"]

logger = logging.getLogger(__name__)


def build():
    """
    build zfused maya menu 

    """

    # main menu
    cmds.menu("zfused_maya_menu", parent="MayaWindow",
              label=u"星龙传媒 zFused Maya", tearOff=True)
    _menu_data = menu.get_menu_data()

    for _menu_title in menu.MENU_KEY:
        cmds.menuItem(_menu_title, label=_menu_title.capitalize(),
                      parent="zfused_maya_menu", subMenu=True, tearOff=True)
        if _menu_title in _menu_data.keys():
            # load menu
            category = []
            category_cmds = {}
            menu_data = _menu_data[_menu_title]
            for data in menu_data:
                cate = data["category"]
                if not cate in category:
                    category.append(cate)
                if not cate in category_cmds:
                    category_cmds[cate] = []
                category_cmds[cate].append(data)
            for ca in category:
                cmds.menuItem(label = ca, divider=True, parent = _menu_title)
                for data in category_cmds[ca]:
                    cmds.menuItem(data["name"], label=data["title"],
                                  parent=_menu_title, command=data["cmd"])
        cmds.menuItem(divider=True, parent="zfused_maya_menu")


def delete():
    if cmds.menu("zfused_maya_menu", q=True, exists=True):
        cmds.deleteUI("zfused_maya_menu")


def rebuild():
    delete()
    build()
