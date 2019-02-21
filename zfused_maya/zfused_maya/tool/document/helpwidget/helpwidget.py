# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import logging

from PySide2 import QtWidgets, QtGui, QtCore

import zfused_maya.widgets.window as window

class HelpWidget(window.Window):
    def __init__(self, parent = None):
        super(HelpWidget, self).__init__()
        self._build()

    def _build(self):
        """ build help widget

        """
        self.resize(800, 800)
        self.set_title_name("zFused_maya outsource update")
        # content widget
        self.content_widget = QtWidgets.QFrame()
        self.content_layout = QtWidgets.QHBoxLayout(self.content_widget)

        self.set_central_widget(self.content_widget)