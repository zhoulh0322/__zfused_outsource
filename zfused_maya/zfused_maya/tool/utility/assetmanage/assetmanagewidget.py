# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import logging

from qtpy import QtWidgets, QtGui, QtCore

import zfused_api
import zfused_maya.core.record as record
import zfused_maya.core.resource as resource
import zfused_maya.widgets.window as window

import searchline
import filterwidget
import assetlistwidget
import assetstepwidget

__all__ = ["AssetManageWidget"]

logger = logging.getLogger(__name__)


class AssetManageWidget(window.Window):
    def __init__(self, parent = None):
        super(AssetManageWidget, self).__init__()
        self._build()

        self._asset_id = 0
        self._project_step_id = 0

        self.filter_widget.asset_type_changed.connect(self._filter_asset_types)
        self.filter_widget.asset_step_changed.connect(self._filter_asset_step)
        self.asset_list_widget.asset_list_view.clicked.connect(self._load_asset)
        self.search_line.textChanged.connect(self._search)

    def _search(self):
        # get search text
        _text = self.search_line.text()
        self.asset_list_widget.asset_proxy_model.search(_text)

    def _refresh_asset_step_panel(self):
        self.asset_step_widget.load_asset_id(self._asset_id)
        # load project step id
        self.asset_step_widget.load_project_step_id(self._project_step_id)

    def _load_asset(self, index):
        _data = index.data()
        _asset_id = _data["Id"]
        self._asset_id = _asset_id
        self._refresh_asset_step_panel()

    def _filter_asset_types(self, type_ids = []):
        self.asset_list_widget.asset_proxy_model.filter_type(type_ids)

    def _filter_asset_step(self, project_step_id):
        self._project_step_id = project_step_id
        self._refresh_asset_step_panel()

    def _show_step_widget(self):
        pass

    def _build(self):
        self.resize(1300, 700)
        self.setObjectName("asset_manage_widget")
        self.set_title_name(u"资产管理(assets management widget)")

        #  搜索窗
        self.search_widget = QtWidgets.QFrame()
        self.search_widget.setMaximumHeight(25)
        self.search_widget.setMinimumHeight(25)
        self.search_widget.setObjectName("search_widget")
        self.search_layout = QtWidgets.QHBoxLayout(self.search_widget)
        self.search_layout.setContentsMargins(0, 0, 0, 0)
        self.search_line = searchline.SearchLine()
        self.search_layout.addWidget(self.search_line)
        self.search_line.setMinimumWidth(400)
        self.search_layout.addStretch(True)
        self.refresh_button = QtWidgets.QPushButton()
        self.refresh_button.setMinimumHeight(20)
        self.refresh_button.setText(u"刷新")
        self.refresh_button.setIcon(QtGui.QIcon(resource.get("icons","refresh.png")))
        self.search_layout.addWidget(self.refresh_button)

        # 分割窗口
        self.splitter = QtWidgets.QSplitter()

        # 过滤面板
        self.filter_widget = filterwidget.FilterWidget(self.splitter)
        self.filter_widget.setMaximumWidth(200)
        # 资产列表面板
        self.asset_list_widget = assetlistwidget.AssetListWidget(self.splitter)
        # 封装面板
        self.asset_step_widget = assetstepwidget.AssetStepWidget()
        #  封装面版默认隐藏
        #self.asset_step_widget.setHidden(True)
        self.asset_list_widget.load_panel_widget("asset panel", self.asset_step_widget)

        self.set_central_widget(self.search_widget)
        self.set_central_widget(self.splitter)