# coding:utf-8
#--author-- lanhua.zhou
from __future__ import print_function

import sys
import os
import random
import logging

from qtpy import QtWidgets, QtGui, QtCore

from zfused_login.widgets import lineedit
from zfused_login.widgets import button
from zfused_login.core import record, config
import zfused_login

from . import insideloginwidget
from . import outsideloginwidget

__all__ = ["LoginInterface"]

logger = logging.getLogger(__name__)


class LoginInterface(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(LoginInterface, self).__init__(parent)
        # self.setMouseTracking(True)
        self.setWindowTitle("zFused maya")
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
        
        self._build()
        self._drag_position = QtCore.QPoint(0, 0)

        self.tab_widget.currentChanged.connect(self._login_type)

    def _login_type(self, login_type):
        """
        """
        print(login_type)
        _login = record.Login()
        _login.set_login_type(login_type)

        # class
        record.LoginType.set_login_type(login_type)

        _widget = self.tab_widget.currentWidget()
        _widget.loadConfig()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._drag_position = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        super(LoginInterface, self).mouseMoveEvent(event)
        gloPoint = self.mapToParent(event.pos())
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self._drag_position)
            event.accept()

    def _build(self):
        """
        build ui

        retype: null
        """
        self.setMinimumWidth(660)
        self.setStyleSheet("QFrame{background-color:#FFFFFF}")
        _body_layout = QtWidgets.QHBoxLayout(self)
        _body_layout.setSpacing(0)
        _body_layout.setContentsMargins(0, 0, 0, 0)

        self.show_label = button.ThumbnailButton()
        #self.show_label.setScaledContents(True)
        _resource = zfused_login.resource()
        _background_png = _resource.get(
            "background", "%s.jpg" % random.randint(0, 12))
        self.show_label.set_thumbnail(QtGui.QPixmap(_background_png))
        self.show_label.setMaximumHeight(568)
        self.show_label.setMinimumHeight(568)
        self.show_label.setMaximumWidth(330)
        self.show_label.setMinimumWidth(330)

        self.login_frame = QtWidgets.QFrame()
        self.login_layout = QtWidgets.QVBoxLayout(self.login_frame)
        self.login_layout.setSpacing(15)
        self.login_layout.setContentsMargins(0, 0, 0, 0)

        # close button
        #self.close_button = QtGui.QPushButton()

        # title
        self.title_label = QtWidgets.QLabel()
        self.title_label.setMinimumHeight(200)
        self.title_label.setStyleSheet(  # "QLabel{background-color:#FEBED2}"
            "QLabel{font-family:Microsoft YaHei UI;font: bold 28px;color:#442342}"
            "QLabel{qproperty-alignment: AlignCenter}")
        self.title_label.setText("zFused maya")
        self.login_layout.addWidget(self.title_label)

        # login 
        self.tab_widget = QtWidgets.QTabWidget()
        self.login_layout.addWidget(self.tab_widget)
        # inside login
        self.inside_login_widget = insideloginwidget.InsideLoginWidget()
        self.tab_widget.addTab(self.inside_login_widget, "内部登陆")
        # outside login
        self.outside_login_widget = outsideloginwidget.OutsideLoginWidget()
        self.tab_widget.addTab(self.outside_login_widget, "外包登陆")
        self.login_layout.addWidget(self.tab_widget)

        _body_layout.addWidget(self.show_label)
        _body_layout.addWidget(self.login_frame)

        _resource = zfused_login.resource()
        _qss = _resource.get("qss", "core.qss")
        with open(_qss) as f:
            qss = f.read()
            self.setStyleSheet(qss)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = LoginInterface()
    ui.show()
    sys.exit(app.exec_())
