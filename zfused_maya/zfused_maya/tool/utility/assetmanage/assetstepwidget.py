# coding:utf-8
# --author-- lanhua.zhou

from __future__ import print_function

import os

from PySide2 import QtWidgets, QtGui, QtCore

import zfused_api
import zfused_maya.core.resource as resource
import zfused_maya.core.record as record
import zfused_maya.widgets.button as button

import zfused_maya.node.core.attr as attr
import zfused_maya.node.core.relatives as relatives

import versionlistwidget

class AssetStepWidget(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(AssetStepWidget, self).__init__(parent)
        self._build()

        self._asset_id = 0
        self._asset_handle = None
        self._project_step_id = 0

        self._index_version = {}

        self.version_listwidget.list_view.clicked.connect(self._load_version)
        self.reference_button.clicked.connect(self._reference_file)

    def load_project_step_id(self, project_step_id):
        """ load project step id

        """
        self.version_combobox.clear()
        self._index_version = {}
        self.description_textedit.setHidden(True)
        self.file_name_label.clear()

        if not project_step_id or not self._asset_id:
            return 

        self._project_step_id = project_step_id
        # 
        _project_step_handle = zfused_api.step.ProjectStep(project_step_id)
        _project_step_name_code = _project_step_handle.name_code()
        self.step_button.setText(_project_step_name_code)

        _software_handle = zfused_api.software.Software(_project_step_handle.data["SoftwareId"])
        _software_code = "{}".format(_software_handle.code())
        _production_path = self._asset_handle.production_path()
        # peoject step code
        _project_step_code = _project_step_handle.code()
        versions = []
        _file_path = "{}/{}/{}/file".format(_production_path, _project_step_code, _software_code)
        # get key output attr
        _key_output_attr = _project_step_handle.key_output_attr()
        if _key_output_attr:
            _file = "{}/{}{}".format(_file_path, self._asset_handle.code(), _key_output_attr["Suffix"])
        else:
            _file = "{}/{}.mb".format(_file_path, self._asset_handle.code())
        self.file_name_label.setText(_file.split(_production_path)[-1])
        if os.path.isfile(_file):
            self.reference_button.setEnabled(True)
            self.file_name_label.setStyleSheet("QLabel{color:#3FA847}")
        else:
            self.reference_button.setEnabled(False)
            self.file_name_label.setStyleSheet("QLabel{color:#FF0000}")

    def load_asset_id(self, asset_id):
        self._asset_id = asset_id
        if not asset_id:
            return
        self._asset_handle = zfused_api.asset.Asset(asset_id)
        self.name_button.setText(self._asset_handle.full_name_code())
        self.thumbnail_button.set_thumbnail(self._asset_handle.get_thumbnail())


    def _load_version(self, version_index):
        """ load version index
        """
        self.description_textedit.clear()
        _data = version_index.data()
        self.description_textedit.setText(_data["Description"])
        self.file_name_label.setText(_data["FilePath"])

    def _reference_file(self):
        """
        """
        import maya.cmds as cmds
        _project_step_handle = zfused_api.step.ProjectStep(self._project_step_id)
        _project_step_name_code = _project_step_handle.name_code()
        self.step_button.setText(_project_step_name_code)
        _software_handle = zfused_api.software.Software(_project_step_handle.data["SoftwareId"])
        _software_code = "{}".format(_software_handle.code())
        _production_path = self._asset_handle.production_path()
        # peoject step code
        _project_step_code = _project_step_handle.code()
        versions = []
        _file_path = "{}/{}/{}/file".format(_production_path, _project_step_code, _software_code)
        # if not os.path.isdir(_file_path):
        #     return 
        # _files = os.listdir(_file_path)
        # _last_file = _files[-1]
        # if len(_last_file.split(".")) == 2:
        #     rf = cmds.file("{}/{}".format(_file_path, _last_file), r = True, ns = self._asset_handle.code())
        #     rfn = cmds.referenceQuery(rf, rfn = True)
        # get key output attr
        _key_output_attr = _project_step_handle.key_output_attr()
        if _key_output_attr:
            _file = "{}/{}{}".format(_file_path, self._asset_handle.code(), _key_output_attr["Suffix"])
        else:
            _file = "{}/{}.mb".format(_file_path, self._asset_handle.code())
        if os.path.isfile(_file):
            rf = cmds.file(_file, r = True, ns = self._asset_handle.code())
            rfn = cmds.referenceQuery(rf, rfn = True)


    def _reference_file_old(self):
        """ reference version file

        """
        import maya.cmds as cmds
        # get version index
        _index = self.version_listwidget.list_view.currentIndex()
        if not _index:
            return
        _data = _index.data()
        _version_handle = zfused_api.version.Version(_data["Id"], _data)
        _production_file = _version_handle.production_file()
        _task_handle = zfused_api.task.Task(_data["TaskId"])
        _project_step_handle = zfused_api.step.ProjectStep(_task_handle.data["ProjectStepId"])
        _key_output_attr = _project_step_handle.key_output_attr()
        # get output attr file

        rf = cmds.file(_production_file, r = True, ns = _task_handle.file_code())
        rfn = cmds.referenceQuery(rf, rfn = True)

        attr.set_node_attr(rfn, _key_output_attr["Id"], _version_handle.id, "true")
        relatives.create_relatives()

    def _build(self):
        self.resize(160, 200)
        #self.setMaximumWidth(300) 
        _layout = QtWidgets.QVBoxLayout(self)
        _layout.setSpacing(2)
        _layout.setContentsMargins(0,0,0,0)

        # name widget
        self.name_widget = QtWidgets.QFrame()
        self.name_widget.setMinimumHeight(25)
        self.name_layout = QtWidgets.QHBoxLayout(self.name_widget)
        self.name_layout.setSpacing(0)
        self.name_layout.setContentsMargins(0,0,0,0)
        #  name button
        self.name_button = QtWidgets.QPushButton()
        self.name_button.setIcon(QtGui.QIcon(resource.get("icons", "asset.png")))
        self.name_layout.addWidget(self.name_button)
        """
        #  close button
        self.close_button = button.IconButton(self.name_widget, resource.get("icons", "close.png"), 
                                                     resource.get("icons", "close_hover.png"), 
                                                     resource.get("icons", "close_hover.png"))
        self.close_button.setObjectName("close_button")
        self.close_button.setFlat(True)
        self.close_button.setMinimumSize(20, 20)
        self.close_button.setMaximumSize(20, 20)
        self.name_layout.addWidget(self.close_button)
        """
        # thumbnail widget
        self.thumbnail_widget = QtWidgets.QFrame()
        self.thumbnail_layout = QtWidgets.QVBoxLayout(self.thumbnail_widget)
        self.thumbnail_layout.setSpacing(0)
        self.thumbnail_layout.setContentsMargins(0,0,0,0)
        self.thumbnail_button = button.ThumbnailButton()
        self.thumbnail_button.setMinimumSize(200, 162)
        self.thumbnail_layout.addWidget(self.thumbnail_button)

        # project step widget
        #
        self.step_widget = QtWidgets.QFrame()
        self.step_widget.setMinimumHeight(25)
        self.step_layout = QtWidgets.QVBoxLayout(self.step_widget)
        self.step_layout.setSpacing(0)
        self.step_layout.setContentsMargins(0,0,0,0)
        # name button
        self.step_button = QtWidgets.QPushButton()
        self.step_button.setText(u"项目步骤")
        self.step_button.setIcon(QtGui.QIcon(resource.get("icons", "step.png")))
        self.step_layout.addWidget(self.step_button)

        # version widget
        #
        self.version_widget = QtWidgets.QFrame()
        self.version_widget.setMinimumHeight(25)
        self.version_layout = QtWidgets.QHBoxLayout(self.version_widget)
        self.version_layout.setSpacing(20)
        self.version_layout.setContentsMargins(20,0,20,0)
        #  version name button
        self.version_name_button = QtWidgets.QPushButton()
        self.version_name_button.setText(u"版本")
        #self.version_name_button.setIcon(QtGui.QIcon(resource.get("icons", "attributes.png")))
        # self.version_layout.addWidget(self.version_name_button)
        #  version combobox
        self.version_combobox = QtWidgets.QComboBox()
        self.version_layout.addWidget(self.version_combobox)
        self.version_layout.addStretch(True)

        # listwidget
        self.version_listwidget = versionlistwidget.listwidget.ListWidget()

        # description widget
        self.description_textedit = QtWidgets.QTextEdit()
        self.description_textedit.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.description_textedit.setEnabled(False)
        self.description_textedit.setMaximumHeight(40)
        self.description_textedit.setPlaceholderText("version description")

        # operation widget
        # 
        self.operation_widget = QtWidgets.QFrame()
        self.operation_widget.setObjectName("operation_widget")
        #self.operation_widget.setMinimumHeight(30)
        self.operation_layout = QtWidgets.QHBoxLayout(self.operation_widget)
        self.operation_layout.setContentsMargins(2,2,2,2)
        # file name
        self.file_name_label = QtWidgets.QLabel()
        self.operation_layout.addWidget(self.file_name_label)
        self.operation_layout.addStretch(True)
        # reference file
        self.reference_button = QtWidgets.QPushButton()
        self.reference_button.setObjectName("reference_button")
        self.reference_button.setMinimumSize(100,30)
        self.reference_button.setText(u"参考文件")
        self.operation_layout.addWidget(self.reference_button)
        # import gpu
    
        _layout.addWidget(self.name_widget)
        _layout.addWidget(self.thumbnail_widget)
        _layout.addWidget(self.step_widget)
        # _layout.addWidget(self.version_widget)
        # _layout.addStretch(True)
        _layout.addWidget(self.version_listwidget )
        _layout.addWidget(self.description_textedit)
        _layout.addWidget(self.operation_widget)

        _qss = resource.get("qss", "tool/assetmanagewidget/assetstepwidget.qss")
        with open(_qss) as f:
            qss = f.read()
            self.setStyleSheet(qss)