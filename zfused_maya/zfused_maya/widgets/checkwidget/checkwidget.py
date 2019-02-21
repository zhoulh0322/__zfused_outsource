#coding:utf-8
#--author-- lanhua.zhou

#pyside and pyside2
from PySide2 import QtGui,QtWidgets,QtCore

import zfused_maya.node.core.check as check
import zfused_maya.interface.tomaya as tomaya
import zfused_maya.widgets.window as window

class CheckWidget(window.Window, check.Check):
    #value = False
    def __init__(self):
        super(CheckWidget, self).__init__(parent = tomaya.GetMayaMainWindowPoint())
        self._build()
        self.allCheckWidget = []

    def add_widget(self, widget):
        """ add check widget 

        """
        self.bodyLayout.addWidget(widget)
        self.allCheckWidget.append(widget)

    def addWidget(self, widget):
        self.bodyLayout.addWidget(widget)
        self.allCheckWidget.append(widget)

    def getAllCheckWidget(self):
        return self.allCheckWidget
        
    def auto_clear(self):
        return self.autoClearCheckBox.isChecked()

    def show_all(self):
        return self.show_all_checkbox.isChecked()

    def _build(self):
        self.resize(600,600)
        #self.set_title_name("检查场景(check scene)")

        # scroll widget
        #
        self.scroll_widget = QtWidgets.QScrollArea()
        self.scroll_widget.setWidgetResizable(True)
        self.scroll_widget.setBackgroundRole(QtGui.QPalette.NoRole)
        self.scroll_widget.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.bodyWidget = QtWidgets.QFrame()
        self.scroll_widget.setWidget(self.bodyWidget)
        layout = QtWidgets.QVBoxLayout(self.bodyWidget)
        layout.setContentsMargins(0,0,0,0)
        self.bodyLayout = QtWidgets.QVBoxLayout(self.bodyWidget)
        self.bodyLayout.setContentsMargins(0,0,0,0)
        #self.listWidget = listWidget.ListWidget()

        layout.addLayout(self.bodyLayout)
        layout.addStretch()

        # auto recheck button
        self.recheck_widget = QtWidgets.QWidget()
        self.recheck_layout = QtWidgets.QHBoxLayout(self.recheck_widget)
        self.recheck_layout.setSpacing(4)
        self.recheck_layout.setContentsMargins(0,0,0,0)
        # show all item widget
        self.show_all_checkbox = QtWidgets.QCheckBox()
        self.show_all_checkbox.setText(u"显示所有检查面板")
        self.recheck_layout.addWidget(self.show_all_checkbox)
        self.recheck_layout.addStretch(True)
        # auto checkbox
        self.autoClearCheckBox = QtWidgets.QCheckBox()
        self.recheck_layout.addWidget(self.autoClearCheckBox)
        self.autoClearCheckBox.setText(u"自动清理")
        # recheck button
        self.recheck_button = QtWidgets.QPushButton()
        self.recheck_button.setMinimumSize(100,30)
        self.recheck_layout.addWidget(self.recheck_button)
        self.recheck_button.setText(u"重新检查")

        self.set_central_widget(self.scroll_widget)
        self.set_tail_widget(self.recheck_widget)