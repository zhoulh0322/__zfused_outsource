# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import logging

from qtpy import QtWidgets, QtGui, QtCore

import zfused_api
import zfused_maya.core.record as record
import zfused_maya.core.resource as resource
import zfused_maya.widgets.widgets as widgets

from . import assetlistmodel
from . import assetlistview
from . import assetitemdelegate

from . import searchline

__all__ = ["AssetListWidget"]

logger = logging.getLogger(__name__)


class AssetListWidget(widgets.ShowPanelWidget):
    def __init__(self, parent = None):
        super(AssetListWidget, self).__init__(parent)
        self._build()
        self._load()
        # self.build_panel()

        self.search_line.textChanged.connect(self._search)
        # self.asset_list_view.clicked.connect(self._show_panel)

    def _show_panel(self, model_index):
        """ show asset assembly panel
        
        """
        self.show_panel()

    def _search(self):
        """ search text
        
        """
        _text = self.search_line.text()
        self.asset_proxy_model.search(_text)

    def _load(self):
        """
        加载当前项目资产

        """
        _interface = record.Interface()
        _project_id = _interface.get("current_project_id")
        _project_assets = zfused_api.asset.project_assets([_project_id])
        if _project_id:
            self.asset_model = assetlistmodel.AssetListModel(_project_assets, self.asset_list_view)
            self.asset_proxy_model.setSourceModel(self.asset_model)
            self.asset_list_view.setModel(self.asset_proxy_model)

    def _build(self):
        _layout = QtWidgets.QVBoxLayout(self)
        _layout.setContentsMargins(0,0,0,0)
        _layout.setSpacing(0)

        #  搜索窗
        self.search_widget = QtWidgets.QFrame()
        self.search_widget.setMaximumHeight(25)
        self.search_widget.setMinimumHeight(25)
        self.search_widget.setObjectName("search_widget")
        _layout.addWidget(self.search_widget)
        self.search_layout = QtWidgets.QHBoxLayout(self.search_widget)
        self.search_layout.setContentsMargins(0, 0, 0, 0)
        self.search_line = searchline.SearchLine()
        self.search_layout.addWidget(self.search_line)
        self.search_line.setMinimumWidth(400)
        self.search_layout.addStretch(True)

        #  资产列表
        self.asset_list_view = assetlistview.AssetListView()
        _layout.addWidget(self.asset_list_view)
        self.asset_proxy_model = assetlistmodel.AssetListFilterProxyModel()
        self.asset_list_view.setItemDelegate(
            assetitemdelegate.AssetItemDelegate(self.asset_list_view))

        _qss = resource.get("qss", "tool/assemblymanage/assetlistwidget.qss")
        with open(_qss) as f:
            qss = f.read()
            self.setStyleSheet(qss)