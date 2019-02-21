# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import logging

from qtpy import QtWidgets, QtGui, QtCore

import zfused_api
import zfused_maya.core.record as record
import zfused_maya.core.resource as resource
import zfused_maya.widgets.widgets as widgets

import listmodel
import listview
import itemdelegate


__all__ = ["ListWidget"]

logger = logging.getLogger(__name__)


class ListWidget(QtWidgets.QFrame):
    def __init__(self, parent = None):
        super(ListWidget, self).__init__(parent)
        self._build()

    def load_versions(self, versions):
        """
        加载版本

        """
        self.model = listmodel.ListModel(versions)
        self.proxy_model.setSourceModel(self.model)
        self.list_view.setModel(self.proxy_model)

    def _build(self):
        _layout = QtWidgets.QVBoxLayout(self)
        _layout.setContentsMargins(0,0,0,0)
        _layout.setSpacing(0)

        #  资产列表
        self.list_view = listview.ListView()
        _layout.addWidget(self.list_view)
        self.proxy_model = listmodel.ListFilterProxyModel()
        self.list_view.setItemDelegate(itemdelegate.ItemDelegate(self.list_view))

        return
        _qss = resource.get("qss", "tool/assetmanagewidget/assetlistwidget.qss")
        with open(_qss) as f:
            qss = f.read()
            self.setStyleSheet(qss)