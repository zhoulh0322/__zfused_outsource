# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os

from qtpy import QtWidgets, QtGui, QtCore

import zfused_api
import zfused_maya
import zfused_maya.core.resource as resource
import zfused_maya.core.record as record

from . import tasklistview
from . import tasklistmodel
from . import taskitemdelegate

import zfused_maya.interface.tomaya as tomaya

__all__ = ["TaskListPanel"]

class TaskListPanel(QtWidgets.QFrame):
    def __init__(self):
        super(TaskListPanel, self).__init__(parent = tomaya.GetMayaMainWindowPoint())
        #self.setStyleSheet("QFrame{background-color:#F0F0F0}")
        self._build()
        #self._load_config()

        self.close_button.clicked.connect(self.close)
        self.task_list_widget.doubleClicked.connect(self._set_project)
    
    def _set_project(self, index):
        _project_id = index.data().id()

        _ui_record = record.Interface()
        #_project_id = _ui_record.get("current_project_id")
        _ui_record.write("current_project_id", _project_id)

        self.close()

    def load_config(self):
        """ 加载激活中任务

        """
        # 获取任务
        _active_status_ids = zfused_api.status.active_status_ids()
        def _sort(x,y):
            if _active_status_ids.index(x["StatusId"]) > _active_status_ids.index(y["StatusId"]):
                return 1
            if _active_status_ids.index(x["StatusId"]) < _active_status_ids.index(y["StatusId"]):
                return -1
            return 0

        # zfused api reset 
        zfused_api.zFused.RESET = True
        _user_id = zfused_api.zFused.USER_ID
        _current_project_id = record.current_project_id()
        _software_id = zfused_maya.software_id()

        _tasks = zfused_api.zFused.get("task", filter={"AssignedTo": zfused_api.zFused.USER_ID, 
                                                       #"SoftwareId": _software_id, 
                                                       "StatusId__in":"|".join([str(_status_id) for _status_id in _active_status_ids]),
                                                       #"ProjectId": _current_project_id}
                                                       })
        if _tasks:
            _tasks = sorted(_tasks, _sort)
        model = tasklistmodel.TaskListModel(_tasks, self.task_list_widget)
        self.task_proxy_model.setSourceModel(model)
        zfused_api.zFused.RESET = False

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
        self.title_button.setIcon(QtGui.QIcon(resource.get("icons", "task.png")))
        self.title_button.setText(u"激活中的任务列表")
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

        # task list widget
        self.task_list_widget = tasklistview.TaskListView()
        self.task_list_widget.setObjectName("task_list_widget")
        self.task_proxy_model = tasklistmodel.TaskListFilterProxyModel()
        self.task_list_widget.setModel(self.task_proxy_model)
        self.task_list_widget.setItemDelegate(taskitemdelegate.TaskItemDelegate(self.task_list_widget))

        _layout.addWidget(self.close_frame)
        _layout.addWidget(self.task_list_widget)

        _qss = resource.get("qss", "ui/tasklistpanel.qss")
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