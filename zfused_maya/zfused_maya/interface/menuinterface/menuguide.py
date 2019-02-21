# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os
import json
import logging

from PySide2 import QtWidgets, QtCore

import menuframe
import menulistpanel

class MenuGuide(QtWidgets.QFrame):
    def __init__(self, parent = None):
        super(MenuGuide, self).__init__(parent)
        self._build()

    def _show_project_list_panel(self):
        """
        show and move project_list_widget

        :rtype: None
        """
        self.project_list_panel.show()
        self.project_list_panel.load_config()
        # set geometry
        _button_pos = self.project_frame.projectlist_button.pos()
        _button_height = self.project_frame.projectlist_button.height()
        _glo_pos = self.mapTo(tomaya.GetMayaMainWindowPoint(), _button_pos)

        self.project_list_panel.setGeometry(x, _glo_pos.y() + _button_height, self.width()*2/3.0, tomaya.GetMayaMainWindowPoint().height()*2/3.0)


    def _build(self):
        self.setObjectName("menu_interface")
        _layout = QtWidgets.QHBoxLayout(self)
        _layout.setSpacing(0)
        _layout.setContentsMargins(0,0,0,0)

        # menu frame
        self.menu_frame = menuframe.MenuFrame()

        # menu panel 
        self.menu_list_panel = menulistpanel.MenuListPanel()

        _layout.addWidget(self.menu_frame)