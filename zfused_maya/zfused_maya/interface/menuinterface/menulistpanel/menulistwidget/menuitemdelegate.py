# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import datetime
import logging

from qtpy import QtWidgets, QtGui, QtCore

import zfused_api
import zfused_maya.core.color as color

import constants

__all__ = ["MenuItemDelegate"]

logger = logging.getLogger(__name__)


class MenuItemDelegate(QtWidgets.QStyledItemDelegate):
    THUMBNAIL_PIXMAP = {}
    THUMBNAIL = {}

    def __init__(self, parent=None):
        super(MenuItemDelegate, self).__init__(parent)

        self._spacing = 15
        self._spacing_height = 6

    def _paint_category(self, painter, option, category_item):
        _rect = option.rect

        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0), 0))
        painter.setBrush(QtGui.QColor(constants.Constants.CATEGORY_BACKGROUND_COLOR))
        painter.drawRoundedRect(option.rect, 1, 1)

        #
        painter.setPen(QtGui.QPen(QtGui.QColor(constants.Constants.CATEGORY_NAME_COLOR), 1))
        _status_text = u"{} · {}".format(category_item.data(), str(category_item.child_count()))
        _status_rect = QtCore.QRect(_rect.x() + 10, 
                                    _rect.y(), 
                                    _rect.width(), 
                                    _rect.height())
        painter.drawText(_status_rect, QtCore.Qt.AlignLeft |
                         QtCore.Qt.AlignVCenter, _status_text)


    def _paint_cmd(self, painter, option, cmd_item):
        _rect = option.rect

        painter.setPen(QtGui.QPen(QtGui.QColor(constants.Constants.CMD_NAME_COLOR), 0.1))
        painter.setBrush(QtGui.QColor(constants.Constants.CMD_BACKGROUND_COLOR))
        painter.drawRoundedRect(_rect, 1, 1)

        # 绘制命令颜色条
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 0), 1))
        painter.setBrush(QtGui.QColor(cmd_item.data()["color"]))
        _project_color_x = _rect.x() + self._spacing
        _project_color_y = _rect.y() + self._spacing_height
        _project_color_width = _rect.width() - self._spacing * 2
        _project_color_height = constants.Constants.THUMBNAIL_HEIGHT
        painter.drawRoundedRect(_project_color_x, _project_color_y,
                                _project_color_width, _project_color_height, 2, 2)

        # 绘制命令名称
        _project_name_x = _project_color_x
        _project_name_y = _project_color_y + _project_color_height + self._spacing_height
        _project_name_width = _project_color_width
        _project_name_height = 15
        painter.setPen(QtGui.QPen(QtGui.QColor(constants.Constants.CMD_NAME_COLOR), 1))
        painter.drawText(_project_name_x, 
                         _project_name_y, 
                         _project_name_width, 
                         _project_name_height,
                         QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, 
                         cmd_item.data()["name"])

        # 绘制命令代号
        _project_time_x = _rect.x() + self._spacing
        _project_time_y = _project_name_y + _project_name_height + self._spacing_height
        _project_time_width = _rect.width() - self._spacing*2
        _project_time_height = 15
        painter.drawText(_project_time_x, 
                         _project_time_y, 
                         _project_time_width, 
                         _project_time_height,
                         QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, 
                         cmd_item.data()["code"])
        '''
        return
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
        '''

    def paint(self, painter, option, index):
        _item = index.data()
        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        # painter.setPen(QtGui.QPen(QtGui.QColor("#343D46"), 0.1))
        _font = QtGui.QFont("Microsoft YaHei UI", 9)
        _font.setPixelSize(12)
        _font.setBold(True)
        painter.setFont(_font)

        if _item.object() == "category":
            self._paint_category(painter, option, _item)
        elif _item.object() == "menu_cmd":
            self._paint_cmd(painter, option, _item)

        if _item.object() == "menu_cmd":
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
        if _item.object() == "category":
            return QtCore.QSize(self.parent().width(), 20)
        elif _item.object() == "menu_cmd":
            return QtCore.QSize(constants.Constants.ITEM_DELEGATE_SIZE[0], constants.Constants.ITEM_DELEGATE_SIZE[1])