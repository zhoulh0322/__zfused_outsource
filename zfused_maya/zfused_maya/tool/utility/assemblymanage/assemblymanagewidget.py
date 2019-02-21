# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import logging

from qtpy import QtWidgets, QtGui, QtCore

import zfused_api
import zfused_maya.core.record as record
import zfused_maya.core.resource as resource
import zfused_maya.widgets.window as window

from . import filterwidget
from . import assetlistwidget
from . import operationwidget

__all__ = ["AssemblyManageWidget"]

logger = logging.getLogger(__name__)


class AssemblyManageWidget(window.Window):
    def __init__(self, parent = None):
        super(AssemblyManageWidget, self).__init__()
        self._build()

        self._asset_id = 0

        self.filter_widget.asset_type_changed.connect(self._filter_asset_types)
        self.asset_list_widget.asset_list_view.clicked.connect(self._load_asset)

    def _load_asset(self, index):
        _data = index.data()
        _asset_id = _data["Id"]
        self._asset_id = _asset_id
        self.operation_widget.load_asset_id(_asset_id)

    def _filter_asset_types(self, type_ids = []):
        self.asset_list_widget.asset_proxy_model.filter_type(type_ids)

    def _build(self):
        self.resize(1300, 700)
        self.setObjectName("asset_manage_widget")
        self.set_title_name(u"场景集合管理(assemblys management widget)")

        # 分割窗口
        self.splitter = QtWidgets.QSplitter()

        # 过滤面板
        self.filter_widget = filterwidget.FilterWidget(self.splitter)
        self.filter_widget.setMaximumWidth(200)
        # 资产列表面板
        self.asset_list_widget = assetlistwidget.AssetListWidget(self.splitter)
        self.set_central_widget(self.splitter)

        # operation widget
        self.operation_widget = operationwidget.OperationWidget()

        self.set_tail_widget(self.operation_widget)