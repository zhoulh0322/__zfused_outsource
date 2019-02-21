# coding:utf-8
#--author-- lanhua.zhou

""" custom button class """

from __future__ import print_function

import time
import tempfile
import logging

import zfused_maya.core.video as video

from PySide2 import QtWidgets, QtGui, QtCore

__all__ = ["IconButton", "ThumbnailButton"]

logger = logging.getLogger(__name__)


class IconButton(QtWidgets.QPushButton):
    def __init__(self, parent = None, normal_icon = None, hover_icon = None, pressed_icon = None):
        super(IconButton, self).__init__(parent)
        self._normal_icon = QtGui.QIcon(normal_icon)
        self._hover_icon = QtGui.QIcon(hover_icon)
        self._pressed_icon = QtGui.QIcon(pressed_icon)

        self.setMouseTracking(True)
        self.setIcon(self._normal_icon)

    def enterEvent(self, event):
        super(IconButton, self).enterEvent(event)
        self.setIcon(self._hover_icon)
        #self.setCursor(QtCore.Qt.OpenHandCursor)

    def leaveEvent(self, event):
        super(IconButton, self).leaveEvent(event)
        self.setIcon(self._normal_icon)
        #self.setCursor(QtCore.Qt.ArrowCursor)

    def mousePressEvent(self, event):
        super(IconButton, self).mousePressEvent(event)
        self.setIcon(self._pressed_icon)
        #self.setCursor(QtCore.Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        super(IconButton, self).mouseReleaseEvent(event)
        self.setIcon(self._hover_icon)
        #self.setCursor(QtCore.Qt.OpenHandCursor)


class ThumbnailButton(QtWidgets.QPushButton):
    def __init__(self, thumbnail = None, video = None, parent = None):
        super(ThumbnailButton, self).__init__(parent)

        self._tips = u"无缩略图"
        self._thumbnail = thumbnail
        self._video = video

    def thumbnail(self):
        """ get thumbnail file

        :rtype: str
        """
        return self._thumbnail

    def video(self):
        """ get video file

        :rtype: str
        """
        return self._video

    def set_thumbnail(self, thumbnail):
        """ set thumbnail file for show
        
        :rtype: None
        """
        self._thumbnail = thumbnail
        self.update()

    def set_video(self, video_file):
        """ set video file for show

        :rtype: None
        """
        self._video = video_file
        tempDir = tempfile.gettempdir()
        _thumbnail = "%s/%s.png"%(tempDir,time.time())
        value = video.cut_image(video_file, _thumbnail)
        self.set_thumbnail(_thumbnail)

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