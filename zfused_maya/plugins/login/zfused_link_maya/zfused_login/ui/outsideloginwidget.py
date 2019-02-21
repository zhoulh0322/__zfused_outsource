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

__all__ = ["OutsideLoginWidget"]

logger = logging.getLogger(__name__)


class OutsideLoginWidget(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(OutsideLoginWidget, self).__init__(parent)
        self._build()
        self.loadConfig()

        #self.address_combobox.currentIndexChanged.connect(self._write_address_name)
        self.name_lineedit.textChanged.connect(self._write_name)
        self.password_lineedit.textChanged.connect(self._write_password)
        self.remember_checkbox.stateChanged.connect(self._write_remember)
        self.autoload_checkbox.stateChanged.connect(self._write_autoload)
        self.python_path_lineedit.textChanged.connect(self._write_outsource_lib)

    def _set_address(self):
        _config = config.Config()
        _addresss = _config.get()
        if _addresss:
            for _address in _addresss:
                _name = _address["name"]
                self.address_combobox.addItem(_name)
        # if has login
        _login = record.Login()
        _address_name = _login.address_name()
        if _address_name:
            _index = self.address_combobox.findText(_address_name)
            if _index:
                self.address_combobox.setCurrentIndex(_index)

    def _set_python_path(self):
        """ set python path

        """
        _login = record.Login()
        _python_path = _login.outsource_path()
        if _python_path:
            self.python_path_lineedit.setText(_python_path)

    def loadConfig(self):
        """
        read last setting

        """
        logger.info(u"加载初始化数据--开始")
        _login = record.Login()
        if _login.remember():
            self.remember_checkbox.setChecked(True)
            _user = record.User()
            # set name
            _user_name = _user.name()
            if _user_name:
                self.name_lineedit.setText(_user_name)
            # set password
            _user_password = _user.password()
            if _user_password:
                self.password_lineedit.setText(_user_password)
            
        #self._set_address()
        self._set_python_path()

        if _login.autoload():
            self.autoload_checkbox.setChecked(True)
        
        logger.info(u"加载初始化数据--完成")

    def _write_address_name(self):
        _address_name = self.address_combobox.currentText()
        _login = record.Login()
        _login.set_address_name(_address_name)

    def _write_name(self, _v):
        """
        change user record file

        """
        _user = record.User()
        _user.set_name(_v)

    def _write_outsource_lib(self, _v):
        """
        """
        _login = record.Login()
        _login.set_outsource_path(_v)

    def _write_password(self, _v):
        """
        change user record file

        """
        _user = record.User()
        _user.set_password(_v)

    def _write_remember(self, _v=True):
        """
        change login record file

        """
        _login = record.Login()
        _login.set_remember(_v)

    def _write_autoload(self, _v = True):
        """
        change login record file

        """
        _login = record.Login()
        _login.set_autoload(_v)

    @property
    def error(self):
        return self.error_label.text()

    @error.setter
    def error(self, tex):
        if tex:
            self.error_label.setHidden(False)
        else:
            self.error_label.setHidden(True)
        self.error_label.setText(tex)

    def name(self):
        return self.name_lineedit.text()

    def password(self):
        return self.password_lineedit.text()

    def address_name(self):
        return self.address_combobox.currentText()

    def remember(self):
        return self.remember_checkbox.isChecked()

    def autoload(self):
        return self.autoload_checkbox.isChecked()

    def outsource_path(self):
        return self.python_path_lineedit.text()

    def _build(self):
        """
        build ui

        retype: null
        """
        _body_layout = QtWidgets.QHBoxLayout(self)
        _body_layout.setSpacing(0)
        _body_layout.setContentsMargins(0, 0, 0, 0)
        _resource = zfused_login.resource()

        self.login_frame = QtWidgets.QFrame()
        self.login_layout = QtWidgets.QVBoxLayout(self.login_frame)
        self.login_layout.setSpacing(15)
        self.login_layout.setContentsMargins(30, 30, 30, 0)

        """
        # address
        self.address_frame = QtWidgets.QFrame()
        self.address_layout = QtWidgets.QHBoxLayout(self.address_frame)
        self.address_layout.setSpacing(0)
        self.address_layout.setContentsMargins(0, 0, 0, 0)
        self.address_combobox = QtWidgets.QComboBox()
        self.address_combobox.setStyleSheet(
            "QComboBox:editable{background-color:#FFFFFF}")
        self.address_combobox.setMaximumHeight(25)
        self.address_combobox.setMinimumHeight(25)
        self.address_button = QtWidgets.QPushButton()
        self.address_button.setFlat(True)
        _setting_png = _resource.get("icons", "setting.png")
        self.address_button.setIcon(QtGui.QPixmap(_setting_png))
        self.address_button.setMaximumSize(30, 30)
        self.address_button.setMinimumSize(25, 25)
        self.address_layout.addWidget(self.address_combobox)
        self.address_layout.addWidget(self.address_button)
        """

        # python path 
        self.python_path_frame = QtWidgets.QFrame()
        self.python_path_layout = QtWidgets.QVBoxLayout(self.python_path_frame)
        self.python_path_layout.setSpacing(25)
        self.python_path_layout.setContentsMargins(0, 0, 0, 0)
        self.python_path_lineedit = lineedit.LineEdit()
        self.python_path_lineedit.set_tip(u"zfused_outsource library 路径")
        self.python_path_lineedit.setMinimumHeight(30)
        self.python_path_layout.addWidget(self.python_path_lineedit)

        # name and password frame
        self.name_password_frame = QtWidgets.QFrame()
        self.name_password_layout = QtWidgets.QVBoxLayout(self.name_password_frame)
        self.name_password_layout.setSpacing(25)
        self.name_password_layout.setContentsMargins(0, 0, 0, 0)
        self.name_lineedit = lineedit.LineEdit()
        self.name_lineedit.set_tip(u"用户名")
        self.name_lineedit.setMinimumHeight(30)
        self.password_lineedit = lineedit.LineEdit()
        self.password_lineedit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_lineedit.set_tip(u"密码")
        self.password_lineedit.setMinimumHeight(30)
        self.name_password_layout.addWidget(self.name_lineedit)
        self.name_password_layout.addWidget(self.password_lineedit)

        # check group
        self.check_frame = QtWidgets.QFrame()
        self.check_layout = QtWidgets.QHBoxLayout(self.check_frame)
        self.check_layout.setContentsMargins(0,0,0,0)
        #  remember checkbox
        self.remember_checkbox = QtWidgets.QCheckBox()
        self.remember_checkbox.setText(u"记住密码")

        #  auto load
        self.autoload_checkbox = QtWidgets.QCheckBox()
        self.autoload_checkbox.setText(u"自动登陆")

        self.check_layout.addWidget(self.remember_checkbox)
        self.check_layout.addStretch(True)
        self.check_layout.addWidget(self.autoload_checkbox)

        # error info
        self.error_label = QtWidgets.QLabel()
        self.error_label.setStyleSheet(
            "QLabel{color:#FF0000;font-family:Microsoft YaHei UI;font: bold 12px;}")
        self.error_label.setText("error info")
        self.error = None

        # login button
        self.login_button = QtWidgets.QPushButton()
        self.login_button.setText(u"登陆")
        self.login_button.setMinimumHeight(30)
        self.login_button.setStyleSheet("QPushButton{font-family:Microsoft YaHei UI;font: bold 12px;color:#FFFFFF}"
                                        "QPushButton{background-color:#1C9FF0}"
                                        "QPushButton:hover{background-color:#094962}"
                                        "QPushButton:pressed{background-color:#462544}"
                                        "QPushButton{border:0px }")

        self.login_layout.addWidget(self.python_path_frame)
        self.login_layout.addWidget(self.name_password_frame)
        self.login_layout.addWidget(self.check_frame)
        self.login_layout.addWidget(self.error_label)
        self.login_layout.addWidget(self.login_button)
        self.login_layout.addStretch(True)

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
