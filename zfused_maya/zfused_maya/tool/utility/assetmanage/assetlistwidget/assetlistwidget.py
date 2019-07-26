# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import logging

from qtpy import QtWidgets, QtGui, QtCore

import zfused_api
import zfused_maya.core.record as record
import zfused_maya.core.resource as resource
import zfused_maya.widgets.widgets as widgets

from . import assetlistmodel, assetlistview, assetitemdelegate

__all__ = ["AssetListWidget"]

logger = logging.getLogger(__name__)


class AssetListWidget(widgets.ShowPanelWidget):
    def __init__(self, parent = None):
        super(AssetListWidget, self).__init__(parent)
        
        self._build()
        self._load()
        self.build_panel()

        self.asset_list_view.clicked.connect(self._show_panel)

    def _show_panel(self, model_index):
        """ show panel 
        """
        self.show_panel()

    def _load(self):
        """
        加载当前项目资产

        """
        _interface = record.Interface()
        _project_id = _interface.get("current_project_id")
        if _project_id:
            # get all project assets
            _project_assets = zfused_api.asset.project_assets([_project_id])
            self.asset_model = assetlistmodel.AssetListModel(_project_assets, self.asset_list_view)
            self.asset_proxy_model.setSourceModel(self.asset_model)
            self.asset_list_view.setModel(self.asset_proxy_model)

    def load_project_id(self, project_id):
        """ 加载项目资产
        
        :rtype: None
        """
        _asset_list = zfused_api.zFused.get("asset", filter={"ProjectId": project_id})
        self.asset_model = assetlistmodel.AssetListModel(_asset_list, self.asset_list_view)
        self.asset_proxy_model.setSourceModel(self.asset_model)
        self.asset_list_view.setModel(self.asset_proxy_model)


    def _build(self):
        _layout = QtWidgets.QVBoxLayout(self)
        _layout.setContentsMargins(0,0,0,0)
        _layout.setSpacing(0)

        #  资产列表
        self.asset_list_view = assetlistview.AssetListView()
        _layout.addWidget(self.asset_list_view)
        self.asset_proxy_model = assetlistmodel.AssetListFilterProxyModel()
        self.asset_list_view.setItemDelegate(assetitemdelegate.AssetItemDelegate(self.asset_list_view))

        #  load asset step panel
        # self.
        # self.load_panel_widget()

        _qss = resource.get("qss", "tool/assetmanagewidget/assetlistwidget.qss")
        with open(_qss) as f:
            qss = f.read()
            self.setStyleSheet(qss)