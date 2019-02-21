# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os

from qtpy import QtWidgets, QtGui, QtCore

import zfused_api
import zfused_maya
import zfused_maya.core.resource as resource
import zfused_maya.core.color as color

_component_color_data = color.get_component_color_data()
COMPONENT_COLOR = {
    "asset":_component_color_data["ASSET_COMPONENT_COLOR"],
    "episode":_component_color_data["EPISODE_COMPONENT_COLOR"],
    "sequence":_component_color_data["SEQUENCE_COMPONENT_COLOR"],
    "shot":_component_color_data["SHOT_COMPONENT_COLOR"],
    "task":_component_color_data["TASK_COMPONENT_COLOR"],
}

class TaskFrame(QtWidgets.QFrame):
    """
    当前正在制作的任务面板
    """

    def __init__(self, parent = None):
        super(TaskFrame, self).__init__(parent)
        self._build()

        self._spacing = 6
        self._indent = 2

    def _get_active_task(self):
        """
        获取制作中任务

        rtype: int
        """
        _user_id = zfused_api.zFused.USER_ID
        _tasks = zfused_api.user.User(_user_id).working_tasks()
        if _tasks:
            return _tasks[0]["Id"]
        return 0

    def paintEvent(self, event):
        _rect = self.rect()
        _rect = QtCore.QRect(_rect.x() + 20,
                             _rect.y(),
                             _rect.width() - 30,
                             _rect.height())

        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        # 设置字体
        _font = QtGui.QFont("Microsoft YaHei UI", 10)
        _font.setPixelSize(12)
        _font.setBold(True)
        painter.setFont(_font)
        fm = QtGui.QFontMetrics(_font)
        _pen = QtGui.QPen(QtGui.QColor("#CACACA"), 1, QtCore.Qt.SolidLine)
        _pen.setWidth(0.1)
        painter.setPen(_pen)
        #fm = QtGui.QFontMetrics(self.font())
        painter.setBrush(QtGui.QColor(COMPONENT_COLOR["task"]))

        painter.drawText(_rect, QtCore.Qt.AlignCenter, u"星龙传媒 zFused outsource maya {}".format(zfused_maya.version()))

        _time_rect = QtCore.QRect( _rect.x(), 
                                   _rect.y(),
                                   _rect.width(),
                                   2)
        _qlineargradient = QtGui.QLinearGradient(0, 0, self.width(), 0)
        _qlineargradient.setSpread(QtGui.QGradient.PadSpread)
        _qlineargradient.setColorAt(0, QtGui.QColor(112, 223, 2, 255))
        _qlineargradient.setColorAt(1, QtGui.QColor(68, 191, 249, 255))
        painter.setBrush(QtGui.QBrush(_qlineargradient))
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0), 0))
        painter.drawRoundedRect(_time_rect, 0, 0)

        painter.end()

    def _build(self):
        _layout = QtWidgets.QHBoxLayout(self)
        _layout.setContentsMargins(0,0,0,0)
        _layout.setSpacing(0)
        self.tasklist_button = QtWidgets.QPushButton()
        self.tasklist_button.setFlat(True)
        self.tasklist_button.setMinimumSize(20,20)
        self.tasklist_button.setStyleSheet(
            "QPushButton{background-color:#5D5D5D;color:#FFFFFF;font-family: Microsoft YaHei UI;font: bold 12px;border: 0px solid #FFFFFF;}"
            "QPushButton:hover{background-color:#363636;color:#FFFFFF}"
            "QPushButton:checked{background-color:#6E3F6F;color:#FFFFFF}"
            "QPushButton:pressed{background-color:#6E3F6F;color:#FFFFFF}"
            "QPushButton:{margin: 10;}"
        )
        #self.tasklist_button.setCheckable(True)
        #self.tasklist_button.setIcon(QtGui.QIcon(resource.get("icons", "select_list.png")))
        #self.tasklist_button.setText(u"任务列表")
        
        #_layout.addWidget(self.tasklist_button) 
        _layout.addStretch(True)
