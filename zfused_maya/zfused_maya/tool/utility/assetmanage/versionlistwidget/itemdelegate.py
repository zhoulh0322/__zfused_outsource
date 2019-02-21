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
        _shot_data = index.data()
        _shot_id = _shot_data["Id"]
        _shot_handle = zfused_api.version.Version(_shot_id, _shot_data)
        #_shot_handle = zfused_api.shot.Shot(_shot_id, _shot_data)
        #_name = _shot_handle.full_name_code().replace("/","_")

        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        _rect = option.rect

        _pen = QtGui.QPen(QtGui.QColor("#343D46"), 0.1)
        painter.setPen(_pen)
        painter.setBrush(QtGui.QColor(0, 0, 0, 0))
        painter.drawRoundedRect(option.rect, 0, 0)

        # painter thumbnail
        _thumbnail_pixmap = None
        if self.THUMBNAIL_PIXMAP.has_key(_shot_id):
            _thumbnail_pixmap = self.THUMBNAIL_PIXMAP[_shot_id]
        else:
            if self.THUMBNAIL.has_key(_shot_id):
                _thumbnail = self.THUMBNAIL[_shot_id]
                if _thumbnail:
                    _pixmap = QtGui.QPixmap(_thumbnail)
                    #_pixmap = QtGui.QImageReader(_thumbnail)
                    _pixmap_size = _pixmap.size()
                    if _pixmap_size.width() and _pixmap_size.height():
                        _label_size = QtCore.QSize(
                            _rect.width(), constants.Constants.THUMBNAIL_HEIGHT)
                        scale = max(float(_label_size.width() / float(_pixmap_size.width())),
                                    float(_label_size.height()) / float(_pixmap_size.height()))
                        _pixmap = _pixmap.scaled(
                            _pixmap_size.width() * scale, _pixmap_size.height() * scale)
                        #_pixmap = _pixmap.setScaledSize(QtCore.QSize(_pixmap_size.width()*scale, _pixmap_size.height()*scale))
                        _thumbnail_pixmap = _pixmap.copy((_pixmap_size.width() * scale - _label_size.width()) / 2.0, (_pixmap_size.height(
                        ) * scale - _label_size.height()) / 2.0, _label_size.width(), _label_size.height())
                        #_thumbnail_pixmap = _pixmap
                        self.THUMBNAIL_PIXMAP[_shot_id] = _thumbnail_pixmap
            else:
                _thumbnail_load = _ThumbnailThread(self)
                _thumbnail_load.load_thumbnail(_shot_handle, index)

        if _thumbnail_pixmap:
            painter.drawPixmap(_rect.x(), _rect.y(), _thumbnail_pixmap)
        else:
            _thumbnail_rect = QtCore.QRect(
                _rect.x(), _rect.y(), _rect.width(), constants.Constants.THUMBNAIL_HEIGHT - 1)
            painter.setBrush(QtGui.QColor(color.LetterColor.color(_shot_data["Name"].lower()[0])))
            painter.drawRoundedRect(_thumbnail_rect, 1, 1)
            painter.setPen(QtGui.QPen(QtGui.QColor(
                0, 0, 0, 255), 0.2, QtCore.Qt.DashLine))
            painter.drawRoundedRect(_thumbnail_rect, 1, 1)

        # painter name
        _name_rect = QtCore.QRect(_rect.x(), 
                                  _rect.y() + constants.Constants.THUMBNAIL_HEIGHT ,
                                  _rect.width(), constants.Constants.INFOMATION_HEIGHT)
        painter.setBrush(QtGui.QColor(constants.Constants.NAME_BACKGROUND_COLOR))
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0), 1))
        painter.drawRoundedRect(_name_rect, 0, 0)
        _font = QtGui.QFont("Microsoft YaHei UI", 9)
        _font.setPixelSize(constants.Constants.FONT_SIZE)
        #_font.setBold(True)
        painter.setFont(_font)
        painter.setPen(QtGui.QPen(QtGui.QColor(constants.Constants.NAME_COLOR), 1))
        _name = _shot_handle.data["FilePath"]
        _user_id = _shot_handle.data["UserId"]
        _user_handle = zfused_api.user.User(_user_id)
        _code = _user_handle.name_code()
        _time = _shot_handle.data["CreateTime"].split("+")[0].replace("T", " ")
        _name_code = u"{}\n{}\n{}".format(_name, _time, _code)
        painter.drawText(_name_rect, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop, _name_code)


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
