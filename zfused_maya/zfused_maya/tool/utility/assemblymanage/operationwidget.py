# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import sys
import os
import logging

from PySide2 import QtWidgets, QtGui, QtCore

import zfused_api
import zfused_maya.core.record as record
import zfused_maya.core.resource as resource

import zfused_maya.node.core.assembly as assembly

__all__ = ["OperationWidget"]

logger = logging.getLogger(__name__)


class OperationWidget(QtWidgets.QFrame):
    asset_type_changed = QtCore.Signal(list)
    def __init__(self, parent=None):
        super(OperationWidget, self).__init__(parent)
        self._build()

        self._asset_id = 0
        self._asset_handle = None

        self.assembly_button.clicked.connect(self._import_assembly)

    def load_asset_id(self, asset_id):
        """ load asset 
        """
        self._asset_id = asset_id
        self._asset_handle = zfused_api.asset.Asset(self._asset_id)
        self.infomation_label.setText(self._asset_handle.name_code())

        #
        _production_path = self._asset_handle.production_path()
        # 固定路径 未匹配数据库
        _gpu_file = "{}/model/maya2017/assemblyDefinition/{}.mb".format(_production_path, self._asset_handle.code())
        if not os.path.isfile(_gpu_file):
            self.setEnabled(False)
            self.infomation_label.setStyleSheet("QLabel{color:#FF0000}")
        else:
            self.setEnabled(True)
            self.infomation_label.setStyleSheet("QLabel{color:#3FA847}")

    def _import_assembly(self):
        """ if 
        """
        _code = self._asset_handle.data["Code"]
        _production_path = self._asset_handle.production_path()
        # _assembly = assembly.create_assembly(_code)
        # 固定路径 未匹配数据库
        _file = "{}/model/maya2017/assemblyDefinition/{}.mb".format(_production_path, self._asset_handle.code())
        # _assembly.create_representation("gpu", "Cache", _gpu_file)
        # _assembly.set_active("gpu")
        assembly.create_assembly_reference(self._asset_handle.code(), _file)        

    def _build(self):
        _layout = QtWidgets.QHBoxLayout(self)
        _layout.setSpacing(2)
        _layout.setContentsMargins(2,2,2,0)

        # infomation
        self.infomation_label = QtWidgets.QLabel()
        _layout.addWidget(self.infomation_label)
        _layout.addStretch(True)

        # load assembly button
        self.assembly_button = QtWidgets.QPushButton()
        self.assembly_button.setMinimumSize(100, 40)
        self.assembly_button.setText(u"加载 Assembly Reference 文件")
        
        _layout.addWidget(self.assembly_button)