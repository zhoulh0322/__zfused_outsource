# coding:utf-8
# author binglu.wang
import sys
import os
import re
from functools import partial

try:
    from PySide import QtGui as QtWidgets
    from PySide import QtCore, QtUiTools
    from shiboken import wrapInstance
except ImportError:
    from PySide2 import QtWidgets,QtGui,QtCore,QtUiTools
    from shiboken2 import wrapInstance

import maya.cmds as cmds
import zfused_maya.core.resource as resource

class MatarialWidget(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(MatarialWidget, self).__init__(parent)
        self.assetname = ""
        self._build()
        self.pushButton.clicked.connect(self._rename)
        self.pushButton2.clicked.connect(self.refresh)
        self.matListUI.itemSelectionChanged.connect(partial(self.selectitem, self.matListUI))
        self.matListUI.itemSelectionChanged.connect(self._set_mesh)
        # self.matListUI.itemSelectionChanged.connect(self._set_true_name)
        self.meshListUI.itemSelectionChanged.connect(partial(self.selectitem, self.meshListUI))
        self.meshListUI.itemSelectionChanged.connect(self._set_true_name)
        self.refresh()

    def _build(self):
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEdit.setPlaceholderText(u"标准命名")

        self.pushButton = QtWidgets.QPushButton()
        self.pushButton.setMinimumSize(QtCore.QSize(120, 25))
        self.pushButton.setText(u"重命名")

        self.label1 = QtWidgets.QLabel()
        self.label1.setMinimumSize(QtCore.QSize(0, 20))
        self.label1.setText(u"材质球节点")

        self.pushButton2 = QtWidgets.QPushButton()
        self.pushButton2.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButton2.setMaximumSize(QtCore.QSize(25, 20))
        self.pushButton2.setIcon(QtGui.QIcon(resource.get("icons","refresh.png")))
        # self.pushButton2.setText(u"刷新")

        self.label2 = QtWidgets.QLabel()
        self.label2.setMinimumSize(QtCore.QSize(0, 20))
        self.label2.setText(u"关联模型")

        self.matListUI = QtWidgets.QListWidget()
        self.matListUI.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.meshListUI = QtWidgets.QListWidget()
        self.meshListUI.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection)

        self.seclayout1 = QtWidgets.QHBoxLayout()
        self.seclayout1.setSpacing(5)
        self.seclayout1.setContentsMargins(0, 0, 0, 0)
        self.seclayout1.addWidget(self.label1)
        self.seclayout1.addStretch()
        self.seclayout1.addWidget(self.pushButton2)

        self.firlayout1 = QtWidgets.QHBoxLayout()
        self.firlayout1.setSpacing(5)
        self.firlayout1.setContentsMargins(0, 0, 0, 0)
        self.firlayout1.addWidget(self.lineEdit)
        self.firlayout1.addWidget(self.pushButton)

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setContentsMargins(5, 0, 5, 10)
        self.gridLayout.addLayout(self.firlayout1, 0, 0, 1, 2)
        self.gridLayout.addLayout(self.seclayout1, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.label2, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.matListUI, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.meshListUI, 3, 1, 1, 1)
        self.setLayout(self.gridLayout)

    def additem(self, items, listwidget,clear = True):
        if clear:
            listwidget.clear()
        for item in items:
            listwidget.addItem(item)

    def selectitem(self, listwidget):
        items = listwidget.selectedItems()
        cmds.select(cl=1)
        for item in items:
            cmds.select(item.text(), add=1,ne = 1)

    def refresh(self):
        self._get_asset_name()
        if not self.assetname:
            cmds.inViewMessage(amg = u'未获取到资产名\n请检查文件大纲', pos = 'midCenter', fade = True)
            return
        self._set_mat()
        self.meshListUI.clear()

    def _rename(self):
        item = self.matListUI.currentItem()
        mat_c = item.text()
        new_matname = self.lineEdit.text()
        if not new_matname or not item:
            return
        cmds.rename(mat_c,new_matname)
        self.refresh()

    def _get_asset_name(self):
        for i in cmds.ls(type = "transform"):
            if cmds.objExists("%s.treeName"%i):
                self.assetname = cmds.getAttr("%s.treeName"%i)

    def _get_node(self,node,nodetype,io = False,*args):
        _c_node = node
        filenode_list = []
        i = 0
        while i < 10:
            _c_list = cmds.listConnections(_c_node,d = io, s = not io,scn = 1)
            if _c_list:
                _c_list = list(set(_c_list))
                for j in _c_list:
                    if cmds.nodeType(j) == nodetype:
                        filenode_list.append(j)
                    if args and cmds.nodeType(j) in args:
                        _c_list.remove(j)
                _c_node = _c_list
            else:
                break
            i += 1
        if filenode_list:
            filenode_list = list(set(filenode_list))
        return filenode_list

    def _get_str(self,mesh):
        def _set_filter(meshstr):
            _ture = meshstr.split(self.assetname)[-1]
            if _ture.startswith("_"):
                _ture = _ture[1:]
            return "{}_{}".format(self.assetname,_ture)

        if re.findall("\.f\[\d+\]",mesh):
            mesh = mesh.replace(re.findall("\.f\[\d+\]",mesh)[-1],"")
        if re.findall("\.f\[\d+.\d+\]",mesh):
            mesh = mesh.replace(re.findall("\.f\[\d+.\d+\]",mesh)[-1],"")
        _name = _set_filter(mesh)
        if _name[-1].isdigit():
            _num = len(re.findall("\d+",_name)[-1])
            _name = _name[:-_num]
            if _name.endswith("_"):
                _name = _name[:-1]
        # true_sg_name = "M_{}_sg".format(_name)
        true_mat_name = "M_{}_mat".format(_name)
        return true_mat_name

    def _set_mat(self):
        defalut_mats = ["lambert1","particleCloud1"]
        allmats = [i for i in cmds.ls(mat = 1) if i not in defalut_mats]
        if allmats:
            self.additem(allmats,self.matListUI)

    def _set_mesh(self):
        item = self.matListUI.currentItem()
        mat_c = item.text()
        if cmds.objExists(mat_c):
            _sg = self._get_node(mat_c,"shadingEngine",True,"transform","mesh")[0]
            cmds.hyperShade(objects = _sg)
            meshs = cmds.ls(sl =1)
            if meshs:
                showlist = []
                for mesh in meshs:
                    if re.findall("\.f\[\d+\]",mesh) or re.findall("\.f\[\d+.\d+\]",mesh):
                        showlist.append(mesh)
                    else:
                        if cmds.nodeType(mesh) == "mesh":
                            try:
                                mesh = cmds.listRelatives(mesh,p = 1)[0]
                            except:
                                mesh = cmds.listRelatives(mesh,p = 1,f = 1)[0]
                        showlist.append(mesh)
                self.additem(showlist,self.meshListUI)
            else:
                self.meshListUI.clear()
            cmds.select(mat_c,r=1,ne = 1)
            self._set_true_name()

    def _set_true_name(self):
        if self.meshListUI.count() != 0:
            items = self.meshListUI.selectedItems()
            if not items:
                item = self.meshListUI.item(0)
            else:
                item = items[-1]
            _mesh = item.text()
            if cmds.objExists(_mesh):
                _name = self._get_str(_mesh)
                if _name:
                    self.lineEdit.setText(_name)
                else:
                    self.lineEdit.clear()
        else:
            self.lineEdit.clear()
