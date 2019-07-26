# # coding:utf-8
# # --author-- binglu.wang
import sys
import os
import json
from PySide2 import QtCore, QtGui, QtWidgets
import maya.cmds as cmds
from functools import partial

import maya.cmds as cmds
import zfused_maya.core.resource as resource
import zfused_maya.widgets.window as zfwin

class Win(QtWidgets.QFrame):
    def __init__(self, parent = None):
        super(Win,self).__init__(parent)
        self.COLOR = ["#ffe889","#00ffff","#bd86ff","#ff8799","#358631","#6b6672"]
        self.TYPE = {}
        self._build()
        self._build_btn()
        self._refresh()

        self.listWidget.itemSelectionChanged.connect(partial(self.selectitem, self.listWidget))
        self.pushButton4.clicked.connect(self._refresh)
        self.pushButton5.clicked.connect(partial(self.selectallitem, self.listWidget))
        self.pushButton6.clicked.connect(partial(self.clearselectitem, self.listWidget))
        self.lineEdit.textChanged.connect(self._set_item_with_filter)
        self.radioButton1.clicked.connect(self._sort_item)
        self.radioButton2.clicked.connect(self._sort_item)

    def _build(self):
        # self.resize(690, 1071)
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setMinimumSize(QtCore.QSize(0, 25))
        self.label_2.setMaximumSize(QtCore.QSize(150, 25))
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setText("sort by")

        self.pushButton4 = QtWidgets.QPushButton(self)
        self.pushButton4.setMinimumSize(QtCore.QSize(25, 25))
        self.pushButton4.setMaximumSize(QtCore.QSize(25, 25))
        self.pushButton4.setIcon(QtGui.QIcon(resource.get("icons","refresh.png")))
        # self.pushButton4.setText("re")

        self.pushButton5 = QtWidgets.QPushButton(self)
        self.pushButton5.setMinimumSize(QtCore.QSize(50, 25))
        self.pushButton5.setMaximumSize(QtCore.QSize(50, 25))
        self.pushButton5.setText("all")
        self.pushButton6 = QtWidgets.QPushButton(self)
        self.pushButton6.setMinimumSize(QtCore.QSize(50, 25))
        self.pushButton6.setMaximumSize(QtCore.QSize(50, 25))
        self.pushButton6.setText("clear")

        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEdit.setPlaceholderText(u"关键字筛选")
        self.lineEdit.setStyleSheet("border: 0px;")

        self.radioButton1 = QtWidgets.QRadioButton(self)
        self.radioButton1.setMinimumSize(QtCore.QSize(50, 15))
        self.radioButton1.setText("name")
        self.radioButton2 = QtWidgets.QRadioButton(self)
        self.radioButton2.setMinimumSize(QtCore.QSize(50, 15))
        self.radioButton2.setText("type")

        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection)
        self.listWidget.setStyleSheet("border: 0px;")

        self.horizontalLayout2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2.addWidget(self.radioButton1)
        self.horizontalLayout2.addWidget(self.radioButton2)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.addWidget(self.label_2)
        self.verticalLayout.addLayout(self.horizontalLayout2)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.addWidget(self.lineEdit)
        self.horizontalLayout.addWidget(self.pushButton5)
        self.horizontalLayout.addWidget(self.pushButton6)
        self.horizontalLayout.addWidget(self.pushButton4)

        self.gridLayout_2 = QtWidgets.QGridLayout(self)
        self.gridLayout_2.setVerticalSpacing(2)
        self.gridLayout_2.setContentsMargins(5, 0, 5, 10)
        # self.gridLayout_2.addWidget(self.label, 0, 0, 1, 2)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 2, 1)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.listWidget, 1, 1, 1, 1)

    def _build_btn(self):
        # print ("yes")
        self.get_shownode()
        for k,v in self.TYPE.items():
            self.k = QtWidgets.QPushButton(self)
            self.k.setMinimumSize(QtCore.QSize(150, 25))
            self.k.setText(k.upper())
            self.k.setStyleSheet("color:{};".format(v))
            self.verticalLayout.addWidget(self.k)
            self.k.clicked.connect(partial(self._convert,k))
        self.verticalLayout.addStretch()

    def get_shownode(self):
        import zfused_api
        import zfused_maya.core.color as color
        import zfused_maya.core.record as record
        _project_id = record.current_project_id()
        _priject_handle = zfused_api.project.Project(_project_id)
        _project_steps = zfused_api.step.project_steps([_project_id])
        _attrs = []
        for _project_step in _project_steps:
            _step_handle = zfused_api.step.ProjectStep(_project_step["Id"])
            _out_attrs = _step_handle.output_attrs()
            _attrs += _out_attrs
            
        _ass_codes = []
        for _attr in _attrs:
            if _attr["IsAssembly"] > 0:
                _ass_codes.append(_attr["Code"])
        if _ass_codes:
            _ass_codes = set(_ass_codes)
            for _i,_ass_code in enumerate(_ass_codes):
                self.TYPE[_ass_code] = self.COLOR[_i]
                # self.TYPE[_ass_code] = color.LetterColor.color(_ass_code[0])
        # self.TYPE["proxy"] = color.LetterColor.color("p")
        # self.TYPE["abc"] = color.LetterColor.color("a")

    def _get_sort_mode(self):
        if self.radioButton1.isChecked():
            return True
        else:
            return False

    def selectitem(self, listwidget):
        items = listwidget.selectedItems()
        cmds.select(cl=1)
        for item in items:
            cmds.select(item.text(), add=1,ne = 1)

    def selectallitem(self, listwidget):
        listwidget.selectAll()

    def clearselectitem(self, listwidget):
        listwidget.clearSelection()

    def _set_item_with_filter(self):
        _f = self.lineEdit.text()
        self._set_items(_f)
        self._sort_item()

    def _set_item(self,string,listwidget):
        self.listWidgetitem = QtWidgets.QListWidgetItem(listwidget)
        self.listWidgetitem.setText(string)

    def _set_items(self,_filter = None):
        arnodes = cmds.ls(type = "assemblyReference")
        if not arnodes:
            return
        self.listWidget.clear()
        for arnode in arnodes:
            if _filter:
                if _filter in arnode:
                    self._set_item(arnode,self.listWidget)
            else:
                self._set_item(arnode,self.listWidget)

    def _set_item_color(self): 
        _dict = self.get_all_item()
        if _dict:
            for key,value in _dict.items():
                for k,v in value.items():
                    _mode = cmds.assembly(k,q = 1,a = 1)
                    if _mode in self.TYPE:
                        _color = self.TYPE[_mode]
                        v.setTextColor(QtGui.QColor(_color))

    def _sort_item(self):
        _mode = self._get_sort_mode()
        _dict = self.get_all_item()
        if _dict:
            _list = []
            self.listWidget.clear()
            for key in sorted(_dict.keys()):
                _list.extend(sorted(_dict[key].keys()))
            if _mode:
                _list = sorted(_list)
            for i in _list:
                self._set_item(i,self.listWidget)
        self._set_item_color()


    def get_all_item(self):
        _dict = {}
        _rows = self.listWidget.count()
        if _rows > 0:
            for i in range(_rows):
                item = self.listWidget.item(i)
                _mode = cmds.assembly(item.text(),q = 1,a = 1)
                if _mode in _dict:
                    _ori = _dict[_mode]
                else:
                    _ori = {}
                _ori[item.text()] = item
                _dict[_mode] = _ori
        return _dict

    def _refresh(self):
        self.lineEdit.setText("")
        self.radioButton2.setChecked(True)
        self._set_items()
        self._sort_item()
        

    def _convert(self,mode):
        arnodes = cmds.ls(sl = 1,fl = 1)
        if arnodes:
            for arnode in arnodes:
                if cmds.nodeType(arnode) == "assemblyReference":
                    _mode = cmds.assembly(arnode,q = 1,a = 1)
                    if mode != _mode and mode in cmds.assembly(arnode,q = 1,lr = 1):
                        cmds.assembly(arnode,e = 1,a = "")
                        cmds.assembly(arnode,e = 1,a = mode)
        self._sort_item()



win = zfwin.Window()
ui = Win()
win.set_central_widget(ui)
win.set_title_name(u"场景集合显示切换(convert assembly)")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Win()
    win.show()
    sys.exit(app.exec_())