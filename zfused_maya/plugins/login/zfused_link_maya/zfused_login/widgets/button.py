# coding:utf-8
#--author-- lanhua.zhou

""" custom button class """

from __future__ import print_function

import time
import tempfile
import logging

from PySide2 import QtWidgets, QtGui, QtCore

__all__ = ["ThumbnailButton"]

logger = logging.getLogger(__name__)


class ThumbnailButton(QtWidgets.QPushButton):
    def __init__(self, thumbnail = None, video = None, parent = None):
        super(ThumbnailButton, self).__init__(parent)

        self._tips = u"无缩略图"
        self._thumbnail = thumbnail

    def thumbnail(self):
        """ get thumbnail file

        :rtype: str
        """
        return self._thumbnail

    def set_thumbnail(self, thumbnail):
        """ set thumbnail file for show
        
        :rtype: None
        """
        self._thumbnail = thumbnail
        self.update()

    def paintEvent(self, event):
        super(ThumbnailButton, self).paintEvent(event)
        _rect = self.rect()
        _painter = QtGui.QPainter(self)
        _painter.save()
        _painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        if self._thumbnail:
            _pixmap = QtGui.QPixmap(self._thumbnail)
            _pixmap_size = _pixmap.size()

            _label_size = QtCore.QSize(_rect.width(), _rect.height())
            scale = max(float(_label_size.width() / float(_pixmap_size.width())),
                        float(_label_size.height()) / float(_pixmap_size.height()))
            _pixmap = _pixmap.scaled(_pixmap_size.width() * scale, 
                                     _pixmap_size.height() * scale)
            _thumbnail_pixmap = _pixmap.copy((_pixmap_size.width() * scale - _label_size.width()) / 2.0, 
                                             (_pixmap_size.height() * scale - _label_size.height()) / 2.0, 
                                             _label_size.width(), 
                                             _label_size.height())
            _painter.drawPixmap(_rect.x(), _rect.y(), _thumbnail_pixmap)
        else:
            _painter.drawText(_rect, QtCore.Qt.AlignCenter, u"无缩略图")
        _painter.restore()