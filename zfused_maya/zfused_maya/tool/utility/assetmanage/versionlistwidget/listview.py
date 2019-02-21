# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import logging

from qtpy import QtWidgets, QtGui, QtCore

logger = logging.getLogger(__name__)

class ListView(QtWidgets.QListView):
    def __init__(self, parent=None):
        super(ListView, self).__init__(parent)

        self.setSpacing(5)

        self.setMouseTracking(True)
        #self.setSelectionRectVisible(True)
        self.setViewMode(QtWidgets.QListView.IconMode)
        self.setResizeMode(QtWidgets.QListView.Adjust)
        self.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)

        self.viewport().setAutoFillBackground( False )


    def paintEvent(self, event):
        super(ListView, self).paintEvent(event)
        _rect = self.rect()
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setBrush(QtGui.QColor(255, 255, 0))
        painter.drawRoundedRect(_rect, 0, 0)
        painter.drawText(_rect, QtCore.Qt.AlignCenter, "Name")
        painter.end()