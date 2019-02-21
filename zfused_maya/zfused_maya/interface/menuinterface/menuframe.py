# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function
from functools import partial

import os

from qtpy import QtWidgets, QtGui, QtCore

import zfused_api
import zfused_maya.core.resource as resource
import zfused_maya.core.color as color
import zfused_maya.core.record as record
import zfused_maya.core.menu as menu

import menulistpanel

import zfused_maya.interface.tomaya as tomaya


class MenuFrame(QtWidgets.QFrame):
    def __init__(self, parent = None):
        super(MenuFrame, self).__init__(parent)
        self._build()

    def _show_menu_list_panel(self, menu_type):
        """
        show and move project_list_widget

        :rtype: None
        """
        self.menu_list_panel.load_menu(menu_type)
        self.menu_list_panel.show()

        # set geometry
        _button_pos = self.pos()
        _button_height = self.height()
        _glo_pos = self.mapTo(tomaya.GetMayaMainWindowPoint(), _button_pos)
        if self.width() > tomaya.GetMayaMainWindowPoint().width()*1/2.0:
            x = _button_pos.x()
        else:
            x = _button_pos.x() - (tomaya.GetMayaMainWindowPoint().width()*1/2.0 - self.width())
        self.menu_list_panel.setGeometry(x + 18, 
                                         _glo_pos.y() + _button_height, 
                                         tomaya.GetMayaMainWindowPoint().width()*1/2.0, 
                                         tomaya.GetMayaMainWindowPoint().height()*1/2.0)

    def _build(self):
        _layout = QtWidgets.QHBoxLayout(self)
        _layout.setContentsMargins(0,0,0,0)
        _layout.setSpacing(0)

        for _menu_text in menu.MENU_KEY:
            _menu_button = QtWidgets.QPushButton()
            _menu_button.setIcon(QtGui.QIcon(resource.get("icons","{}.png".format(_menu_text))))
            _menu_button.setText(_menu_text)
            _layout.addWidget(_menu_button)

            _menu_button.clicked.connect(partial(self._show_menu_list_panel, _menu_text))

        self.menu_list_panel = menulistpanel.MenuListPanel()

        #_layout.addStretch(True)
        _qss = resource.get("qss", "ui/menu.qss")
        with open(_qss) as f:
            qss = f.read()
            self.setStyleSheet(qss)