# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os
import json
import logging

from qtpy import QtWidgets, QtGui, QtCore

import zfused_api
import zfused_maya.core.restricted as restricted
import zfused_maya.core.resource as resource
import zfused_maya.core.record as record
import zfused_maya.core.menu as menu 

from .menulistwidget import menulistmodel
from .menulistwidget import menulistview
from .menulistwidget import menuitemdelegate
from .menulistwidget import item

import zfused_maya.interface.tomaya as tomaya

class MenuListPanel(QtWidgets.QMainWindow):

    def __init__(self):
        super(MenuListPanel, self).__init__(parent = tomaya.GetMayaMainWindowPoint())
        self._build()

        self.close_button.clicked.connect(self.close)

        self.menu_list_widget.clicked.connect(self._run_cmd)
        self.menu_list_widget.doubleClicked.connect(self._run_cmd)
        #test
        #self.load_menu("modeling")

    def _run_cmd(self, index):
        """ run maya cmd

        :rtype: None
        """

        '''
        import zfused_maya.core.restricted as restricted
        import maya.cmds as cmds
        _has_per, _info = restricted.restricted()
        if not _has_per:
            cmds.confirmDialog(message = _info)
            return 
        '''

        try:
            _item = index.data()
            exec(_item.data()["cmd"]) 
        except:
            pass
        self.close()


    def load_menu(self, menu_type):
        """ 加载插件命令

        """
        _menu_data = menu.get_menu_data()
        _menu_type_data = _menu_data[menu_type]
        if not _menu_type_data:
            return 
        category = []
        category_cmds = {}
        category_cmds_list = []
        for data in _menu_type_data:
            cate = data["category"]
            if not cate in category:
                category.append(cate)
                cate_item = item.Item("category", cate)
                category_cmds[cate] = cate_item
                category_cmds_list.append(cate_item)
            data_item = item.Item("menu_cmd", data)
            category_cmds[cate].append_child(data_item)
        _all_data = []
        for _head_item in category_cmds_list:
            _all_data.append(_head_item)  
            for _child_item in _head_item.children():
                _all_data.append(_child_item)
        _model = menulistmodel.MenuListModel(_all_data, self.menu_list_widget)
        self.menu_list_widget.setModel(_model)

    def _build(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        #self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        #self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        main_widget = QtWidgets.QFrame()
        self.setCentralWidget(main_widget)
        _layout =QtWidgets.QVBoxLayout(main_widget)
        _layout.setContentsMargins(0,0,0,0)
        _layout.setSpacing(0)
        main_widget.setObjectName("widget")

        self.close_frame = QtWidgets.QFrame()
        self.close_frame.setMinimumHeight(30)
        self.close_frame.setObjectName("close_frame")
        self.close_layout = QtWidgets.QHBoxLayout(self.close_frame)
        self.close_layout.setContentsMargins(10,0,10,0)
        self.close_layout.setSpacing(0)
        # title button
        self.title_button = QtWidgets.QPushButton()
        self.title_button.setObjectName("title_button")
        self.title_button.setIcon(QtGui.QIcon(resource.get("icons", "menu.png")))
        self.title_button.setText(u"命令菜单")
        self.close_layout.addWidget(self.title_button)
        # close button
        self.close_button = _Button(self.close_frame, resource.get("icons", "close.png"), 
                                                     resource.get("icons", "close_hover.png"), 
                                                     resource.get("icons", "close_hover.png"))
        self.close_button.setObjectName("close_button")
        self.close_button.setFlat(True)
        self.close_button.setMinimumSize(15, 15)
        self.close_button.setMaximumSize(15, 15)
        self.close_layout.addStretch(True)
        self.close_layout.addWidget(self.close_button)

        self.menu_list_widget = menulistview.MenuListView()
        self.menu_list_widget.setItemDelegate(menuitemdelegate.MenuItemDelegate(self.menu_list_widget))

        _layout.addWidget(self.close_frame)
        _layout.addWidget(self.menu_list_widget)

        _qss = resource.get("qss", "ui/menulistpanel.qss")
        with open(_qss) as f:
            qss = f.read()
            self.setStyleSheet(qss)


class _Button(QtWidgets.QPushButton):
    def __init__(self, parent = None, normal_icon = None, hover_icon = None, pressed_icon = None):
        super(_Button, self).__init__(parent)
        self._normal_icon = QtGui.QIcon(normal_icon)
        self._hover_icon = QtGui.QIcon(hover_icon)
        self._pressed_icon = QtGui.QIcon(pressed_icon)

        self.setMouseTracking(True)
        self.setIcon(self._normal_icon)

    def enterEvent(self, event):
        super(_Button, self).enterEvent(event)
        self.setIcon(self._hover_icon)

    def leaveEvent(self, event):
        super(_Button, self).leaveEvent(event)
        self.setIcon(self._normal_icon)

    def mousePressEvent(self, event):
        super(_Button, self).mousePressEvent(event)
        self.setIcon(self._pressed_icon)

    def mouseReleaseEvent(self, event):
        super(_Button, self).mouseReleaseEvent(event)
        self.setIcon(self._normal_icon)