# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os

from qtpy import QtWidgets, QtGui, QtCore

import zfused_api
import zfused_maya.core.resource as resource
import zfused_maya.core.record as record

from .projectlistwidget import projectlistmodel
from .projectlistwidget import projectlistview
from .projectlistwidget import projectitemdelegate
from .projectlistwidget import item

import zfused_maya.interface.tomaya as tomaya

class ProjectListPanel(QtWidgets.QFrame):
    def __init__(self):
        super(ProjectListPanel, self).__init__(parent = tomaya.GetMayaMainWindowPoint())
        #self.setStyleSheet("QFrame{background-color:#F0F0F0}")
        self._build()
        #self._load_config()

        self.close_button.clicked.connect(self.close)
        self.project_list_widget.doubleClicked.connect(self._set_project)
    
    def _set_project(self, index):
        """ set current project 
        """
        _project_id = index.data().id()
        _ui_record = record.Interface()
        #_project_id = _ui_record.get("current_project_id")
        _ui_record.write("current_project_id", _project_id)

        self.close()

    def load_config(self):
        """ 加载项目列表

        """
        _projects = zfused_api.project.all_projects()
        _all_data = []

        # 获取当前项目
        _current_project_id = record.current_project_id()
        if _current_project_id:
            _active_item = item.Item("active", 0)
            _all_data.append(_active_item)
            _active_project_item = item.Item("project", _current_project_id)
            _all_data.append(_active_project_item)

        for _project in _projects:
            #if _status_id == _project["StatusId"]:
            _item = item.Item("project", _project["Id"])
            #_status_item.append_child(_item)
            _all_data.append(_item)

        _model = projectlistmodel.ProjectListModel(_all_data, self.project_list_widget)
        self.project_list_widget.setModel(_model)

    def _build(self):
        _layout =QtWidgets.QVBoxLayout(self)
        _layout.setContentsMargins(0,0,0,0)
        _layout.setSpacing(0)
        self.setObjectName("widget")

        self.close_frame = QtWidgets.QFrame()
        self.close_frame.setMinimumHeight(30)
        self.close_frame.setObjectName("close_frame")
        self.close_layout = QtWidgets.QHBoxLayout(self.close_frame)
        self.close_layout.setContentsMargins(10,0,10,0)
        self.close_layout.setSpacing(0)
        
        # title button
        self.title_button = QtWidgets.QPushButton()
        self.title_button.setObjectName("title_button")
        self.title_button.setIcon(QtGui.QIcon(resource.get("icons", "project.png")))
        self.title_button.setText(u"项目列表")
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

        self.project_list_widget = projectlistview.ProjectListView()
        self.project_list_widget.setItemDelegate(projectitemdelegate.ProjectItemDelegate(self.project_list_widget))

        _layout.addWidget(self.close_frame)
        _layout.addWidget(self.project_list_widget)

        _qss = resource.get("qss", "ui/projectlistpanel.qss")
        with open(_qss) as f:
            qss = f.read()
            self.setStyleSheet(qss)

class _Button(QtWidgets.QPushButton):
    def __init__(self, parent=None, normal_icon=None, hover_icon=None, pressed_icon=None):
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