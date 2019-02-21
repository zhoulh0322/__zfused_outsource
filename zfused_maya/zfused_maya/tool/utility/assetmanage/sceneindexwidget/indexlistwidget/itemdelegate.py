# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import logging

from qtpy import QtWidgets, QtGui, QtCore

import zfused_api
import zfused_maya.core.color as color

import constants

__all__ = ["ItemDelegate"]

logger = logging.getLogger(__name__)


class _ThumbnailThread(QtCore.QThread):
    exec_ = False
    def __init__(self, parent = None):
        super(_ThumbnailThread, self).__init__(parent)

        self._parent = parent
        self._handle = None

    def load_thumbnail(self, handle, index):
        #self.num = 0
        self._handle = handle
        self._index = index
        self.start()

    def run(self):
        self._parent.THUMBNAIL[self._handle.data["Id"]] = None
        if self._handle.data:
            _thumbnail = self._handle.get_thumbnail()
            if not _ThumbnailThread.exec_:
                self._parent.THUMBNAIL[self._handle.data["Id"]] = _thumbnail
                self._parent.parent().update(self._index)
        self.quit()

class ItemDelegate(QtWidgets.QStyledItemDelegate):
    THUMBNAIL_PIXMAP = {}
    THUMBNAIL = {}

    def __init__(self, parent=None):
        super(ItemDelegate, self).__init__(parent)

        _ThumbnailThread.exec_ = False

    def __del__(self):
        _ThumbnailThread.exec_ = True

    def paint(self, painter, option, index):
        """ painter elements
        """
        _element = index.data()

        _asset_id = _element["link_id"]
        _asset_handle = zfused_api.asset.Asset(_asset_id)

        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        _rect = option.rect
        _pen = QtGui.QPen(QtGui.QColor("#343D46"), 0.1)
        painter.setPen(_pen)
        painter.setBrush(QtGui.QColor(constants.Constants.BACKGROUND_COLOR))
        painter.drawRoundedRect(option.rect, 0, 0)

        # painter version

        # painter name
        _name_rect = QtCore.QRect(_rect.x() + 20, 
                                  _rect.y(),
                                  _rect.width(), 
                                  constants.Constants.INFOMATION_HEIGHT)
        #painter.setBrush(QtGui.QColor(constants.Constants.NAME_BACKGROUND_COLOR))
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0), 1))
        painter.drawRoundedRect(_name_rect, 0, 0)
        _font = QtGui.QFont("Microsoft YaHei UI", 9)
        _font.setPixelSize(constants.Constants.FONT_SIZE)
        #_font.setBold(True)
        painter.setFont(_font)
        painter.setPen(QtGui.QPen(QtGui.QColor(constants.Constants.NAME_COLOR), 1))
        _name_code = _asset_handle.name_code()
        painter.drawText(_name_rect, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop, _name_code)

        # painter project step 
        _project_step_id = _element["project_step_id"]
        _project_step_handle = zfused_api.step.ProjectStep(_project_step_id)
        _project_step_name_code = _project_step_handle.name_code()
        _color = _project_step_handle.color()
        painter.setPen(QtGui.QPen(QtGui.QColor(_color), 1))
        painter.drawText(_name_rect, QtCore.Qt.AlignLeft|QtCore.Qt.AlignBottom, _project_step_name_code)

        # painter
        if option.state & QtWidgets.QStyle.State_MouseOver:
            bgBrush = QtGui.QBrush(QtGui.QColor(200, 200, 200, 150))
            bgPen = QtGui.QPen(QtGui.QColor(60, 60, 60, 0), 0)
            painter.setPen(bgPen)
            painter.setBrush(bgBrush)
            painter.drawRect(option.rect)
        elif option.state & QtWidgets.QStyle.State_Selected:
            bgBrush = QtGui.QBrush(QtGui.QColor(149, 194, 197, 150))
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
        return QtCore.QSize(constants.Constants.ITEM_DELEGATE_SIZE[0], constants.Constants.ITEM_DELEGATE_SIZE[1])
