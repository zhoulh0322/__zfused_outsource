# coding:utf-8
# --author-- lanhua.zhou

from __future__ import print_function

from qtpy import QtWidgets, QtGui, QtCore

import zfused_api
import zfused_maya.core.resource as resource
import zfused_maya.core.record as record
import zfused_maya.widgets.button as button

import zfused_maya.node.core.attr as attr
import zfused_maya.node.core.relatives as relatives

import indexlistwidget

__all__ = ["SceneIndexWidget"]


class SceneIndexWidget(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(SceneIndexWidget, self).__init__(parent)

        return
        self._build()

        self.index_listwidget.refresh.connect(self._show_count)

        self.index_listwidget.refresh_scene()

    def _show_count(self, count):
        """ show scene element count
        """
        self.view_name_button.setText(u"场景元素管理 · {}".format(count))

    def _build(self):
        #self.setMaximumWidth(300) 
        _layout = QtWidgets.QVBoxLayout(self)
        _layout.setSpacing(2)
        _layout.setContentsMargins(0,0,0,0)

        # filter type widget
        self.view_widget = QtWidgets.QFrame()
        self.view_layout = QtWidgets.QHBoxLayout(self.view_widget)
        self.view_layout.setSpacing(0)
        self.view_layout.setContentsMargins(0,0,0,0)
        #  title button
        self.view_name_button = QtWidgets.QPushButton()
        self.view_name_button.setMaximumHeight(25)
        self.view_name_button.setText(u"场景元素管理")
        self.view_name_button.setIcon(QtGui.QIcon(resource.get("icons","assembly.png")))
        self.view_layout.addWidget(self.view_name_button)
        self.view_layout.addStretch(True)
        # view button
        self.view_button = QtWidgets.QPushButton()
        self.view_button.setIcon(QtGui.QIcon(resource.get("icons", "view.png")))
        self.view_layout.addWidget(self.view_button)

        # indexlistwidget
        self.index_listwidget = indexlistwidget.IndexListWidget()

        _layout.addWidget(self.view_widget)
        _layout.addWidget(self.index_listwidget)