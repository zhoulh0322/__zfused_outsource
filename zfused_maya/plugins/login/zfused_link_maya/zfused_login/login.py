# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import maya.cmds as cmds

import sys
import os
import random
import logging

from qtpy import QtWidgets, QtGui, QtCore

import zfused_login.ui.logininterface as logininterface
import zfused_login.ui.tomaya as tomaya
import zfused_login.core.record as record
import zfused_login.core.config as config

logger = logging.getLogger(__name__)


def _get_maya_version():
    version = cmds.about(q=True, version=True)
    os = cmds.about(q=True, os=True)
    return "maya-%s-%s" % (version, os)


class Login(logininterface.LoginInterface):
    def __init__(self, autoload = True):
        super(Login, self).__init__(parent = tomaya.GetMayaMainWindowPoint())
        
        self.inside_login_widget.login_button.clicked.connect(self._login_inside)
        self.outside_login_widget.login_button.clicked.connect(self._login_outside)

        self.inside_login_widget._autoload = autoload
        self.outside_login_widget._autoload = autoload

    def _center(self):

        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def show(self):
        super(Login, self).show()   
        self._center()
        _record = record.Login()

        # get login type id
        _login_type = record.LoginType.login_type()
        print(_login_type)

        if _login_type == 0:        
            if self.inside_login_widget._autoload and _record.autoload():
                logger.info(u"自动登陆")
                self._login_inside()
        elif _login_type == 1:
            if self.outside_login_widget._autoload and _record.autoload():
                logger.info(u"自动登陆")
                self._login_outside()

        # login tab switch
        self.tab_widget.setCurrentIndex(_login_type)

    def _clear(self):
        pass

    def _login_outside(self):
        """ login outsource

        """
        self.outside_login_widget.error = None
        _name = self.outside_login_widget.name()
        _password = self.outside_login_widget.password()
        _outsource_path = self.outside_login_widget.outsource_path()
        
        if not _outsource_path:
            self.outside_login_widget.error = u"填写zfused outsource library路径"
            return 
        if not _name:
            self.outside_login_widget.error = u"填写登陆账号"
            return
        if not _password:
            self.outside_login_widget.error = u"填写密码"
            return
        
        # clear ui
        try:
            import zfused_maya.interface.launch as launch
            launch.repair()
        except:
            pass

        _python_path = _outsource_path

        # remove sys path
        #
        if _python_path in sys.path:
            sys.path.remove(_python_path)
            sys.path.remove("{}/packages/{}".format(_python_path, _get_maya_version()))
            sys.path.remove("{}/zfused_maya".format(_python_path))
            sys.path.remove("{}/zfused_api".format(_python_path))

        # remove class
        # 
        for k in sorted(k for k, m in sys.modules.items() if m and k.startswith('zfused_maya')):
            logger.info('reloading: {}'.format(sys.modules.get(k)))
            del sys.modules[k]
        for k in sorted(k for k, m in sys.modules.items() if m and k.startswith('zfused_api')):
            logger.info('reloading: {}'.format(sys.modules.get(k)))
            del sys.modules[k]

        # append python python library
        #
        sys.path.insert(0, _python_path)
        sys.path.insert(0, "{}/zfused_maya".format(_python_path))
        sys.path.insert(0, "{}/packages/{}".format(_python_path, _get_maya_version()))
        sys.path.insert(0, "{}/zfused_api".format(_python_path))

        # login maya
        print("login maya")
        # =======================================
        # login user
        import zfused_api
        """
        _path = "{0}:{1}".format(_address.host(), _address.port())
        _z = zfused_api.zFused(_path, _name, _password)
        _result, _info = _z.login()
        if not _result:
            self.outside_login_widget.error = _info
            return
        """
        # ======================================
        # load maya ui
        import zfused_maya.interface.launch as launch
        launch.load()
        
        self.close()


    def _login_inside(self):
        """
        login ui

        """
        self.inside_login_widget.error = None

        _name = self.inside_login_widget.name()
        _password = self.inside_login_widget.password()
        _address_name = self.inside_login_widget.address_name()
        _address = config.Config().address(_address_name)

        if not _name:
            self.inside_login_widget.error = u"填写登陆账号"
            return
        if not _password:
            self.inside_login_widget.error = u"填写密码"
            return

        # clear ui
        try:
            import zfused_maya.interface.launch as launch
            launch.repair()
        except:
            pass

        _python_path = _address.python_path()
        # remove sys path
        #
        if _python_path in sys.path:
            sys.path.remove(_python_path)
            sys.path.remove("{}/packages/{}".format(_python_path, _get_maya_version()))
            sys.path.remove("{}/zfused_api".format(_python_path))
            sys.path.remove("{}/zfused_maya".format(_python_path))

        # remove class
        # 
        for k in sorted(k for k, m in sys.modules.items() if m and k.startswith('zfused_maya')):
            logger.info('reloading: {}'.format(sys.modules.get(k)))
            del sys.modules[k]
        for k in sorted(k for k, m in sys.modules.items() if m and k.startswith('zfused_api')):
            logger.info('reloading: {}'.format(sys.modules.get(k)))
            del sys.modules[k]

        # append python python library
        #
        sys.path.insert(0, _python_path)
        sys.path.insert(0, "{}/zfused_maya".format(_python_path))
        sys.path.insert(0, "{}/packages/{}".format(_python_path, _get_maya_version()))
        sys.path.insert(0, "{}/zfused_api".format(_python_path))

        # =======================================
        # login user
        import zfused_api
        _path = "{0}:{1}".format(_address.host(), _address.port())
        _z = zfused_api.zFused(_path, _name, _password)
        _result, _info = _z.login()
        if not _result:
            self.inside_login_widget.error = _info
            return

        # ======================================
        # load maya ui
        import zfused_maya.interface.launch as launch
        launch.load()

        self.close()
