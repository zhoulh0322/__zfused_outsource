# coding:utf-8
# --author-- binglu.wang
import os

try:
    from PySide import QtGui
    from PySide import QtCore, QtUiTools
    from shiboken import wrapInstance
except ImportError:
    from PySide2 import QtWidgets as QtGui
    from PySide2 import QtCore, QtUiTools
    from shiboken2 import wrapInstance

# import zfused_maya.core.resource as resource
# import zfused_maya.widgets.window as win

from zfused_maya.node.core.download_asset import *

class Upload(AssetIO,WBLloadUIFile):
    def __init__(self, uifilename,stage):
        super(AssetIO, self).__init__(uifilename)
        # self.QUERY = True
        self._loadUiWidget(uifilename)
        self.set_asset()
        self.set_step(stage)
        self._set_stage(stage)
        # self.ui.asset_list.itemSelectionChanged.connect(self.set_description)
        self.ui.file_step.currentIndexChanged.connect(self.test)
        self.ui.asset_list.itemDoubleClicked.connect(self._set_name)
        self.ui.upload_name.editingFinished.connect(self.upload_name_check)
        # self.ui.asset_filters.textChanged.connect(self.get_asset_with_filter)
        self.ui.upload_btn.clicked.connect(self._upload_file)

    def test(self):
        print "aaa"

    def _set_stage(self,stage):
        pass

    def upload_name_check(self,code = None):
        if not code:
            code = self.ui.upload_name.text()
            print code
        _group_name = self._get_group_name()
        if _group_name == code:
            _v = "background:#00ff5d;"
            self.ui.upload_btn.setEnabled(True)
        else:
            _v = "background:#ff0000;"
            self.ui.upload_btn.setEnabled(False)
        self.ui.upload_name_check.setStyleSheet(_v)

    def _set_name(self):
        _n = self.ui.asset_list.selectedItems()
        if _n:
            _assets = self.get_asset()
            for _asset in _assets:
                if _n[0].text() ==_asset.name_code():
                    _code = _asset.code()
                    break
            self.cleanitem(self.ui.upload_name)
            self.ui.upload_name.setText(_code)
            self.upload_name_check(_code)

    def _get_group_name(self):
        import maya.cmds as cmds
        for _i in cmds.ls(tr = 1):
            try:
                _asset_name = cmds.getAttr("%s.treeName"%_i)
                # print _asset_name
                return _asset_name
            except:
                pass
        return None

    def _upload_file(self):
        _check_cmd = self.get_step_cmd()



# uiPath = resource.get("uis", "upload_asset.ui")
# mainWindow = win.Window()
# mainWindow.central_widget.setStyleSheet("background-color:#444444;")
# qtWinInst = Upload(uiPath,"model")
# mainWindow.set_central_widget(qtWinInst.ui)
# mainWindow.set_title_name(u"upload_asset")
# mainWindow.setFixedSize(680+15,550+55)

# if __name__ == '__main__':
#     mainWindow.show()