# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import logging

from qtpy import QtWidgets, QtGui, QtCore

__all__ = ["TaskListView"]

logger = logging.getLogger(__name__)

class TaskListView(QtWidgets.QListView):
    def __init__(self, parent=None):
        super(TaskListView, self).__init__(parent)

        self.setSpacing(5)

        self.setMouseTracking(True)
        #self.setSelectionRectVisible(True)
        #self.setViewMode(QtWidgets.QListView.IconMode)
        self.setResizeMode(QtWidgets.QListView.Adjust)
        self.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)

        self.viewport().setAutoFillBackground( False )