# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

from PySide2 import QtWidgets, QtGui, QtCore

import zfused_maya
import zfused_maya.interface as interface
import zfused_maya.core.resource as resource

from . import button

class ShowPanelWidget(QtWidgets.QFrame):
    def __init__(self, parent = None):
        super(ShowPanelWidget, self).__init__(parent)
        self.build_panel()
        self.setMouseTracking(True)

    def mouseReleaseEvent(self, event):
        _pos = event.pos()
        _rect = QtCore.QRect(0, 0, self.width()-self.panel_content.width(), self.height())
        print(_rect)
        print(_pos)
        if _rect.contains(_pos):
            self.close_panel()

    def resizeEvent(self, event):
        """ resize event
        """
        super(ShowPanelWidget, self).resizeEvent(event)
        self.panel.setGeometry(0, 0, self.width(), self.height())

    def load_panel_widget(self, title, widget):
        """ load panel widget 

        """
        self.panel_content_layout.addWidget(widget)
        #self.panel_splitter.setSizes([self.width() - widget.width(), widget.width()])

    def close_panel(self):
        """ close panel

        """
        self.panel.setHidden(True)

    def show_panel(self):
        """ show panel

        """
        self.panel.setHidden(False)

    def build_panel(self):
        # build panel widget
        #  panel widget
        self.panel = QtWidgets.QWidget(self)
        self.panel.setHidden(True)
        self.panel_layout = QtWidgets.QHBoxLayout(self.panel)
        self.panel_layout.setContentsMargins(0,0,0,0)
        self.panel_layout.setSpacing(0)
        #  splitter widget
        self.panel_splitter = QtWidgets.QSplitter()
        self.panel_layout.addWidget(self.panel_splitter)
        self.panel_splitter.setStyleSheet("background-color:rgba(0,0,0,100)")
        #   panel widget
        #    panel blank content
        self.panel_blank_content = QtWidgets.QFrame(self.panel_splitter)
        #    panel widget content
        self.panel_content = QtWidgets.QFrame(self.panel_splitter)
        self.panel_content.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        shadow_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow_effect.setOffset(-3, 0)
        shadow_effect.setColor(QtCore.Qt.gray)
        shadow_effect.setBlurRadius(8)
        self.panel_content.setGraphicsEffect(shadow_effect)
        self.panel_content.setStyleSheet("QFrame{background-color:#FFFFFF;border:1px;border-radius:0px}")
        self.panel_content_layout = QtWidgets.QVBoxLayout(self.panel_content)
        self.panel_content_layout.setContentsMargins(0,0,0,0)
        self.panel_content_layout.setSpacing(0)
        """
        #     panel head widget
        self.panel_content_title_widget = QtWidgets.QFrame()
        self.panel_content_layout.addWidget(self.panel_content_title_widget)
        self.panel_content_title_layout = QtWidgets.QHBoxLayout(self.panel_content_title_widget)
        self.panel_content_title_layout.setSpacing(0)
        self.panel_content_title_layout.setContentsMargins(0,0,0,0)
        self.panel_content_name_button = QtWidgets.QPushButton()
        #self.panel_content_name_button.setIcon(QtGui.QIcon(resource.get("icons", "title.png")))
        self.panel_content_title_layout.addWidget(self.panel_content_name_button)
        """
        self.panel_splitter.setStretchFactor(0, 7)
        self.panel_splitter.setStretchFactor(1, 3)

        #_qss = resource.get("qss", "ui/widgets.qss")
        #with open(_qss) as f:
        #    qss = f.read()
        #    self.setStyleSheet(qss)