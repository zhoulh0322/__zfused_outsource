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

import zfused_maya.core.resource as resource
import zfused_maya.widgets.window as win

from zfused_maya.node.core.download_asset import *

class WBLloadUIFile(object):

    def __init__(self, uifilename):
        super(WBLloadUIFile, self).__init__()

    def _loadUiWidget(self, uifilename):
        uiFullPath = uifilename
        # uiFullPath = '%s/%s.ui' % (os.path.split(os.path.abspath(__file__))[0], uifilename)
        if not os.path.exists(uiFullPath):
            print '%s is not exists' % uiFullPath
            return False
        loader = QtUiTools.QUiLoader()
        uifile = QtCore.QFile(uiFullPath)
        uifile.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(uifile)
        uifile.close()


# class Download(WBLloadUIFile):
class AssetIO(WBLloadUIFile):
    def __init__(self, uifilename):
        super(WBLloadUIFile, self).__init__()

    def set_description(self):
        _item = self.ui.asset_list.currentItem()
        _assets = self.get_asset()
        for _asset in _assets:
            if _item.text() in _asset.name_code():
                _desc = _asset.description()
                # print _desc
                self.ui.description.setText(_desc)
                return
        # _code = re.findall("(\w+)",_item.text())[-1]
        # print _code

    def get_asset_with_filter(self):
        _f = self.ui.asset_filters.text()
        # print _f
        self.set_asset(_f)

    def additem(self, items, listwidget):
        for item in items:
            listwidget.addItem(item)

    def cleanitem(self, listwidget):
        listwidget.clear()

    def comboBoxSelectitem(self,comboBox):
        item = comboBox.currentText()
        if item != "None":
            return item
        return None

class Download(AssetIO,WBLloadUIFile):
    def __init__(self, uifilename,stage):
        super(AssetIO, self).__init__(uifilename)
        self._loadUiWidget(uifilename)
        # self.set_asset()
        # self.set_step()
        self.shot_split()
        # self._set_stage(stage)
        # self.ui.asset_list.itemSelectionChanged.connect(self.set_description)
        # self.ui.file_step.currentIndexChanged.connect(self.test)
        # self.ui.asset_filters.textChanged.connect(self.get_asset_with_filter)

    def test(self):
        print "aaa"

    def shot_split(self):
        _show = [str(i) for i in xrange(100)]
        self.additem(_show,self.ui.ep_split)
        self.additem(_show,self.ui.seq_split)
        self.additem(_show,self.ui.shot_split)

    def _set_stage(self,stage):
        pass

uiPath = resource.get("uis", "download_shot.ui")
mainWindow = win.Window()
mainWindow.central_widget.setStyleSheet("background-color:#444444;")
qtWinInst = Download(uiPath,"ani")
mainWindow.set_central_widget(qtWinInst.ui)
mainWindow.set_title_name(u"领取镜头(download_shot)")
mainWindow.setFixedSize(680+15,550+55)

if __name__ == '__main__':
    mainWindow.show()