# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import logging

import maya.cmds as cmds

from qtpy import QtWidgets, QtGui, QtCore

import zfused_api
import zfused_maya.core.record as record
import zfused_maya.core.resource as resource

import zfused_maya.widgets.window as window
import zfused_maya.widgets.lineedit as lineedit

import zfused_maya.node.inputattr.util as util

from . import listmodel

__all__ = ["ReceiveWidget"]

logger = logging.getLogger(__name__)


class ReceiveWidget(window.Window):
    def __init__(self, parent = None):
        super(ReceiveWidget, self).__init__()
        self._build()

        self._link_object = ""
        self._link_id = 0
        self._project_step_id = 0

        self._project_step_dict = {}
        self._element_dict = {}
        # 
        self.object_group.buttonClicked.connect(self._select_object)
        self.search_lineedit.textChanged.connect(self._search)
        self.element_listview.doubleClicked.connect(self._select_element)
        self.project_step_combobox.currentIndexChanged.connect(self._select_project_step)

        self.receive_button.clicked.connect(self._publish)

    def _publish(self):
        if not self._link_id:
            cmds.confirmDialog( message = u"未选择领取元素" )
            return 
        util.assembly_file( self._link_object, self._link_id, self._project_step_id )

    def _search(self):
        # get search text
        _text = self.search_lineedit.text()
        self.element_filtermodel.search(_text)

    def _select_element(self, index):
        _data = index.data()        
        self.element_label.setText(_data)
        self._link_id = self._element_dict[_data]["Id"]
        _interface = record.Interface()
        _interface.write("current_link",(self._link_object, self._link_id))

    def _select_project_step(self):
        _text = self.project_step_combobox.currentText()
        self.project_step_label.setText(_text)
        _project_step_id = self._project_step_dict[_text]["Id"]
        self._project_step_id = _project_step_id
        _interface = record.Interface()
        _interface.write("current_project_step_id", _project_step_id)

    def _select_object(self, button):
        _obj = button.text()
        self._link_object = _obj.lower()
        self._load_object(_obj.lower())

    def _load_object(self, obj):
        _project_id = record.current_project_id()
        _project_steps = zfused_api.step.project_steps([_project_id])
        _in_project_steps = []
        for _project_step in _project_steps:
            if _project_step["Object"] == obj:
                _in_project_steps.append(_project_step)
                self._project_step_dict[_project_step["Code"]] = _project_step
        self.project_step_combobox.clear()
        for _in_project_step in _in_project_steps:
            self.project_step_combobox.addItem(_in_project_step["Code"])
            # self._project_step_dict
        
        self._element_dict = {}
        if obj == "asset":
            _elements = zfused_api.asset.project_assets([_project_id])
            for _element in _elements:
                _element_handle = zfused_api.asset.Asset(_element["Id"])
                self._element_dict[_element_handle.file_code()] = _element
        elif obj == "shot":
            _elements = zfused_api.shot.project_shots([_project_id])
            for _element in _elements:
                _element_handle = zfused_api.shot.Shot(_element["Id"])
                self._element_dict[_element_handle.file_code()] = _element
        _names = self._element_dict.keys()
        _names.sort()
        self.element_listmodel = listmodel.ListModel(_names)
        self.element_filtermodel = listmodel.ListFilterProxyModel()
        self.element_filtermodel.setSourceModel(self.element_listmodel)
        self.element_listview.setModel(self.element_filtermodel)

        self._select_project_step()

    def _build(self):
        self.resize(800, 600)
        self.setObjectName( "receive_widget" )
        self.set_title_name( u"领取(receive widget)" )

        self.content_widget = QtWidgets.QFrame()
        self.set_central_widget(self.content_widget)
        self.content_layout = QtWidgets.QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0,0,0,0)
        # object frame
        self.object_frame = QtWidgets.QFrame()
        self.content_layout.addWidget(self.object_frame)
        self.object_layout = QtWidgets.QHBoxLayout(self.object_frame)
        self.asset_checkbox = QtWidgets.QCheckBox()
        self.asset_checkbox.setText("Asset")
        self.shot_checkbox = QtWidgets.QCheckBox()
        self.shot_checkbox.setText("Shot")
        self.object_group = QtWidgets.QButtonGroup()
        _checkboxs = [self.asset_checkbox, self.shot_checkbox]
        for _checkbox in _checkboxs:
            self.object_group.addButton(_checkbox)
            self.object_layout.addWidget(_checkbox)
        self.project_step_combobox = QtWidgets.QComboBox()
        self.project_step_combobox.setMinimumSize(200, 25)
        self.object_layout.addWidget(self.project_step_combobox)
        self.object_layout.addStretch(True)

        # asset widget
        self.element_widget = QtWidgets.QFrame()
        self.content_layout.addWidget(self.element_widget)
        self.element_layout = QtWidgets.QVBoxLayout(self.element_widget)
        self.search_lineedit = lineedit.SearchLine()
        self.element_layout.addWidget(self.search_lineedit)
        self.element_listview = QtWidgets.QListView()
        self.element_layout.addWidget(self.element_listview)

        # operation widget
        self.operation_widget = QtWidgets.QFrame()
        self.content_layout.addWidget(self.operation_widget)
        self.operation_layout = QtWidgets.QHBoxLayout(self.operation_widget)
        self.project_step_label = QtWidgets.QLabel()
        self.operation_layout.addWidget(self.project_step_label)
        self.element_label = QtWidgets.QLabel()
        self.operation_layout.addWidget(self.element_label)
        self.operation_layout.addStretch(True)
        self.receive_button = QtWidgets.QPushButton()
        self.operation_layout.addWidget(self.receive_button)
        self.receive_button.setText(u"领取文件")
        self.receive_button.setMinimumSize(100, 30)