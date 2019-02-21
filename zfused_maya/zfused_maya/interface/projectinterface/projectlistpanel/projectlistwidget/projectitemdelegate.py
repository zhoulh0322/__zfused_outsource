# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import datetime
import logging

from qtpy import QtWidgets, QtGui, QtCore

import zfused_api
import zfused_maya.core.color as color

import constants

__all__ = ["ProjectItemDelegate"]

logger = logging.getLogger(__name__)


class ProjectItemDelegate(QtWidgets.QStyledItemDelegate):
    THUMBNAIL_PIXMAP = {}
    THUMBNAIL = {}

    def __init__(self, parent=None):
        super(ProjectItemDelegate, self).__init__(parent)

        self._spacing = 15
        self._spacing_height = 6

    def _paint_active(self, painter, option, status_item):
        _rect = option.rect
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0), 0))
        painter.setBrush(QtGui.QColor(constants.Constants.STATUS_BACKGROUND_COLOR))
        painter.drawRoundedRect(option.rect, 1, 1)

        fm = QtGui.QFontMetrics(painter.font())

        painter.setPen(QtGui.QPen(QtGui.QColor("#A5A6A8"), 1))
        _status_text = u"激活 · active"
        _status_rect = QtCore.QRect(
            _rect.x() + 10, _rect.y(), fm.width(_status_text), _rect.height())
        painter.drawText(_status_rect, QtCore.Qt.AlignLeft |
                         QtCore.Qt.AlignVCenter, _status_text)
        painter.setPen(QtGui.QPen(QtGui.QColor("#A5A6A8"), 1))
        painter.drawLine(_status_rect.x() + _status_rect.width() + 10,
                         _rect.y() + _rect.height()/2.0,
                         _rect.x() + _rect.width(),
                         _rect.y() + _rect.height()/2.0)

    def _paint_status(self, painter, option, status_item):
        _rect = option.rect
        _status_handle = zfused_api.status.Status(status_item.id())

        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0), 0))
        #painter.setBrush(QtGui.QColor(_status_handle.data["Color"]))
        painter.setBrush(QtGui.QColor(constants.Constants.STATUS_BACKGROUND_COLOR))
        painter.drawRoundedRect(option.rect, 1, 1)

        fm = QtGui.QFontMetrics(painter.font())

        painter.setPen(QtGui.QPen(QtGui.QColor(_status_handle.data["Color"]), 1))
        _status_text = u"{} · {}".format(_status_handle.full_name_code(), 
                                         status_item.child_count())
        _status_rect = QtCore.QRect(_rect.x() + 10, 
                                    _rect.y(), 
                                    fm.width(_status_text), 
                                    _rect.height())
        painter.drawText(_status_rect, QtCore.Qt.AlignLeft |
                         QtCore.Qt.AlignVCenter, _status_text)

        painter.setPen(QtGui.QPen(QtGui.QColor(_status_handle.data["Color"]), 1))
        painter.drawLine(_status_rect.x() + _status_rect.width() + 10,
                         _rect.y() + _rect.height()/2.0,
                         _rect.x() + _rect.width(),
                         _rect.y() + _rect.height()/2.0)

    def _paint_project(self, painter, option, project_item):
        _rect = option.rect
        _project_handle = zfused_api.project.Project(project_item.id())

        painter.setPen(QtGui.QPen(QtGui.QColor(constants.Constants.PROJECT_NAME_COLOR), 0.01))
        painter.setBrush(QtGui.QColor(
            constants.Constants.PROJECT_BACKGROUND_COLOR))
        painter.drawRoundedRect(_rect, 1, 1)

        # 绘制项目颜色条
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 0), 1))
        painter.setBrush(QtGui.QBrush(
            QtGui.QColor(_project_handle.profile["Color"])))
        _project_color_x = _rect.x() + self._spacing
        _project_color_y = _rect.y() + self._spacing_height
        _project_color_width = _rect.width() - self._spacing * 2
        _project_color_height = constants.Constants.THUMBNAIL_HEIGHT
        painter.drawRoundedRect(_project_color_x, _project_color_y,
                                _project_color_width, _project_color_height, 2, 2)

        # 绘制项目名称
        '''
        _project_name_x = _rect.x() + self._spacing
        _project_name_y = _project_color_y + self._spacing_height + _project_color_height
        _project_name_width = _rect.width() - self._spacing * 2
        _project_name_height = 20
        '''
        _project_name_x = _project_color_x
        _project_name_y = _project_color_y + _project_color_height + self._spacing_height
        _project_name_width = _project_color_width
        _project_name_height = 15
        painter.setPen(QtGui.QPen(QtGui.QColor(constants.Constants.PROJECT_NAME_COLOR), 1))
        painter.drawText(_project_name_x, _project_name_y, _project_name_width, _project_name_height,
                         QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, _project_handle.full_name_code())

        # 绘制项目时间
        _font = QtGui.QFont("Microsoft YaHei UI",8)  
        _font.setPixelSize(12)      
        painter.setFont(_font)
        _project_time_x = _rect.x() + self._spacing
        _project_time_y = _project_name_y + _project_name_height + self._spacing_height
        _project_time_width = _rect.width() - self._spacing*2
        _project_time_height = 15
        #painter.drawText(_project_time_x , _project_time_y, _project_time_width, _project_time_height, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter, u"2017.12.28 - 2018.12.28")

        # 绘制起始时间
        _font = QtGui.QFont("Microsoft YaHei UI", 8)
        _font.setPixelSize(12)
        painter.setFont(_font)
        painter.setPen(QtGui.QPen(QtGui.QColor(constants.Constants.PROJECT_NAME_COLOR), 1))
        fm = QtGui.QFontMetrics(_font)
        _start_time_text = _project_handle.start_time().strftime("%Y-%m-%d")
        _end_time_text = _project_handle.end_time().strftime("%Y-%m-%d")
        _time_text = "{0} - {1}".format(_start_time_text, _end_time_text)
        _time_start_x = _rect.x() + self._spacing
        _time_start_y = _project_name_y + _project_name_height + self._spacing_height
        _time_start_width = fm.width(_start_time_text) + self._spacing
        _time_start_height = 10
        painter.drawText(_time_start_x, _time_start_y, _time_start_width, _time_start_height,
                         QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignTop, _start_time_text) 
        _time_end_width = fm.width(_end_time_text)
        _time_end_height = 10
        _time_end_x = _rect.x() + _rect.width() - _time_end_width - self._spacing
        _time_end_y = _project_name_y + _project_name_height + self._spacing_height
        painter.drawText(_time_end_x, _time_end_y, _time_end_width, _time_end_height,
                         QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignTop, _end_time_text) 
        
        _time_progress_x = _time_start_x
        _time_progress_y = _time_start_y + _project_time_height
        _time_progress_width = _rect.x() + _rect.width() - _time_progress_x - self._spacing
        _time_progress_height = 4
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 0), 1))
        #painter.setBrush(QtGui.QColor(_project_handle.profile["Color"]))
        painter.setBrush(QtGui.QColor("#555555"))
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


    def paint(self, painter, option, index):
        _item = index.data()
        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        # painter.setPen(QtGui.QPen(QtGui.QColor("#343D46"), 0.1))
        _font = QtGui.QFont("Microsoft YaHei UI", 9)
        _font.setPixelSize(14)
        _font.setBold(True)
        painter.setFont(_font)

        if _item.object() == "status":
            self._paint_status(painter, option, _item)
        elif _item.object() == "active":
            self._paint_active(painter, option, _item)
        elif _item.object() == "project":
            self._paint_project(painter, option, _item)

        if _item.object() == "project":
            if option.state & QtWidgets.QStyle.State_MouseOver:
                bgBrush = QtGui.QBrush(QtGui.QColor(200, 200, 200, 150))
                bgPen = QtGui.QPen(QtGui.QColor(60, 60, 60, 0), 0)
                painter.setPen(bgPen)
                painter.setBrush(bgBrush)
                painter.drawRect(option.rect)
            elif option.state & QtWidgets.QStyle.State_Selected:
                bgBrush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 150))
                bgPen = QtGui.QPen(QtGui.QColor(160, 60, 60, 0), 0)
                painter.setPen(bgPen)
                painter.setBrush(bgBrush)
                painter.drawRect(option.rect)
            else:
                bgBrush = QtGui.QBrush(QtGui.QColor(200, 200, 200, 0))
                bgPen = QtGui.QPen(QtGui.QColor(160, 60, 60, 0), 0)
                painter.setPen(bgPen)
                painter.setBrush(bgBrush)
                painter.drawRect(option.rect)

        painter.restore()

    def sizeHint(self, option, index):
        _item = index.data()
        if _item.object() == "status":
            return QtCore.QSize(self.parent().width(), 20)
        if _item.object() == "active":
            return QtCore.QSize(self.parent().width(), 20)
        elif _item.object() == "project":
            return QtCore.QSize(constants.Constants.ITEM_DELEGATE_SIZE[0], constants.Constants.ITEM_DELEGATE_SIZE[1])