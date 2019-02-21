# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os
import datetime

from qtpy import QtWidgets, QtGui, QtCore

import zfused_api
import zfused_maya.core.resource as resource
import zfused_maya.core.color as color
import zfused_maya.core.record as record


class ProjectFrame(QtWidgets.QFrame):
    """
    当前正在制作的任务面板
    """
    project_id = 0

    def __init__(self, parent=None):
        super(ProjectFrame, self).__init__(parent)
        self._build()

        self._spacing = 10
        self._indent = 2

    def _get_active_project(self):
        """
        获取制作中任务

        rtype: int
        """
        _ui_record = record.Interface()
        _project_id = _ui_record.get("current_project_id")
        '''
        if not _project_id:
            # get first project
            _projects = zfused_api.zFused.get("project")
            if not _projects:
                return 0
            _project_id = _projects[0]["Id"]
        '''
        return _project_id

    def paintEvent(self, event):
        _rect = self.rect()
        _rect = QtCore.QRect(_rect.x() + 20,
                             _rect.y(),
                             _rect.width() - 30,
                             _rect.height())

        _project_id = self._get_active_project()
        self.project_id = _project_id

        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        # 设置字体
        _font = QtGui.QFont("Microsoft YaHei UI", 10)
        _font.setBold(True)
        _font.setPixelSize(12)
        painter.setFont(_font)
        fm = QtGui.QFontMetrics(_font)

        if not self.project_id:
            painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 0), 1))
            painter.setBrush(QtGui.QColor(255, 255, 255, 0))
            painter.drawRoundedRect(_rect, 0, 0)
            _pen = QtGui.QPen(QtGui.QColor("#CACACA"), 1, QtCore.Qt.SolidLine)
            painter.setPen(_pen)
            painter.drawText(_rect.x(), _rect.y(), _rect.width(), _rect.height(),
                             QtCore.Qt.AlignCenter, u"没有选择项目")
            painter.end()
            return
        
        """
        _projects = zfused_api.zFused.get("project")
        if not self.project_id in [_project["Id"] for _project in _projects]:
            painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 0), 1))
            painter.setBrush(QtGui.QColor(255, 255, 255, 0))
            painter.drawRoundedRect(_rect, 0, 0)
            _pen = QtGui.QPen(QtGui.QColor("#CACACA"), 1, QtCore.Qt.SolidLine)
            painter.setPen(_pen)
            painter.drawText(_rect.x() + 20, _rect.y(), _rect.width(), _rect.height(),
                             QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter, u"没有选择项目")
            painter.end()
            return
        """

        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 0), 1))
        _project_handle = zfused_api.project.Project(self.project_id)
        painter.setBrush(QtGui.QColor(_project_handle.profile["Color"]))
        painter.drawRoundedRect(_rect.x(), 
                                _rect.y(), 
                                _rect.width(), 
                                #_rect.height(), 
                                2,
                                0, 0)

        # 绘制项目
        _pen = QtGui.QPen(QtGui.QColor("#FFFFFF"), 1, QtCore.Qt.SolidLine)
        painter.setPen(_pen)
        _project_full_name_code = _project_handle.full_name_code()
        _project_x = _rect.x() + 20
        _project_y = _rect.y() + _rect.height()*1/5.0/2.0
        _project_width = fm.width(_project_full_name_code) + self._spacing
        _project_height = _rect.height()*4/5.0
        painter.drawText(_project_x, _project_y, _project_width, _project_height,
                         QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, _project_full_name_code)

        # 绘制状态
        _status_handle = zfused_api.status.Status(
            _project_handle.data["StatusId"])
        _status_full_name_code = _status_handle.full_name_code()
        _status_x = _project_x + _project_width
        _status_y = _rect.y() + _rect.height()*1/5.0/2.0
        _status_width = fm.width(_status_full_name_code) + self._spacing
        _status_height = _rect.height()*4/5.0
        _pen = QtGui.QPen(QtGui.QColor(255, 255, 255, 0), 1)
        painter.setPen(_pen)
        painter.setBrush(QtGui.QColor(_status_handle.data["Color"]))
        """
        painter.drawRoundedRect(_status_x, 
                                _status_y, 
                                _status_width, 
                                _status_height, 
                                2, 2)
        """
        _pen = QtGui.QPen(QtGui.QColor("#FFFFFF"), 2)
        painter.setPen(_pen)
        painter.drawText(_status_x, _status_y, _status_width, _status_height,
                         QtCore.Qt.AlignCenter, _status_full_name_code)

        # 绘制起始时间
        _font = QtGui.QFont("Microsoft YaHei UI", 8)
        _font.setPixelSize(10)
        painter.setFont(_font)
        _start_time_text = _project_handle.start_time().strftime("%Y-%m-%d")
        _end_time_text = _project_handle.end_time().strftime("%Y-%m-%d")
        _time_text = "{0} - {1}".format(_start_time_text, _end_time_text)
        _time_start_x = _status_x + _status_width + self._spacing
        _time_start_y = _rect.y() + 3
        _time_start_width = fm.width(_start_time_text) + self._spacing
        _time_start_height = _rect.height()/2.0
        painter.drawText(_time_start_x, _time_start_y, _time_start_width, _time_start_height,
                         QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignTop, _start_time_text) 
        _time_end_width = fm.width(_end_time_text)
        _time_end_height = _rect.height()/2.0
        _time_end_x = _rect.x() + _rect.width() - _time_end_width - self._spacing
        _time_end_y = _rect.y() + 3
        painter.drawText(_time_end_x, _time_end_y, _time_end_width, _time_end_height,
                         QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignTop, _end_time_text) 
        
        _time_progress_x = _time_start_x
        _time_progress_y = _rect.y() + _rect.height()/2.0 + 6
        _time_progress_width = _rect.x() + _rect.width() - _time_progress_x - self._spacing
        _time_progress_height = 2
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 0), 1))
        painter.setBrush(QtGui.QColor(255, 255, 255))
        painter.drawRoundedRect(_time_progress_x, _time_progress_y, _time_progress_width, _time_progress_height, 2, 2)

        if not _project_handle.start_time() > datetime.datetime.now():
            _use_date = _project_handle.end_time() - datetime.datetime.now()
            if _use_date.days <= 0:
                _use_time_width = _time_progress_width
            else:
                _all_date = _project_handle.end_time() - _project_handle.start_time()
                _use_per = _use_date.days/float(_all_date.days)
                _use_time_width = _time_progress_width * _use_per
            painter.setBrush(QtGui.QColor("#FF0000"))
            painter.drawRoundedRect(_time_progress_x, _time_progress_y, _use_time_width, _time_progress_height, 2, 2)

        painter.end()

    def _build(self):
        _layout = QtWidgets.QHBoxLayout(self)
        _layout.setContentsMargins(0, 0, 0, 0)
        _layout.setSpacing(0)
        self.projectlist_button = QtWidgets.QPushButton()
        #self.projectlist_button.setText(u"项目列表")
        self.projectlist_button.setFlat(True)
        #self.projectlist_button.setMinimumHeight(20)
        self.projectlist_button.setMinimumSize(20,20)
        self.projectlist_button.setStyleSheet(
            "QPushButton{background-color:#5D5D5D;color:#FFFFFF;font-family: Microsoft YaHei UI;font: bold 12px;border: 0px solid #FFFFFF;}"
            "QPushButton:hover{background-color:#363636;color:#FFFFFF}"
            "QPushButton:checked{background-color:#6E3F6F;color:#FFFFFF}"
            "QPushButton:pressed{background-color:#6E3F6F;color:#FFFFFF}"
            "QPushButton:{margin: 10;}"
        )
        
        #self.projectlist_button.setCheckable(True)
        self.projectlist_button.setIcon(QtGui.QIcon(resource.get("icons", "select_list.png")))
        #self.projectlist_button.setText(u"项目列表")
        _layout.addWidget(self.projectlist_button)
        _layout.addStretch(True)
