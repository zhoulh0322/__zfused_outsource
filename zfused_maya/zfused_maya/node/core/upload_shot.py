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
        # self._loadUiWidget(uifilename)
        # self.set_step()
        # self.ui.asset_filters.editingFinished.connect(self.test)
        # self.ui.file_step.currentIndexChanged.connect(self.test)

    # def set_step(self,*args):
    #     _show = []
    #     _project_id = record.current_project_id()
    #     _project_steps = zfused_api.step.project_steps([_project_id])
    #     for _project_step in _project_steps:
    #         _step_handle = zfused_api.step.ProjectStep(_project_step["Id"])
    #         # print _project_step
    #         # print _step_handle.code()
    #         if args:
    #             _show.extend([_step_handle.name_code() for _f in args if _f in _step_handle.code()])
    #         else:
    #             _show.append(_step_handle.name_code())
    #     if _show:
    #         self.additem(_show,self.ui.file_step)

    # def get_asset(self):
    #     _asset_list = []
    #     _project_id = record.current_project_id()
    #     _project_assets = zfused_api.asset.project_assets([_project_id])
    #     for _asset in _project_assets:
    #         _asset_list.append(zfused_api.asset.Asset(_asset["Id"]))
    #     return _asset_list

    # def set_asset(self,filters = None):
    #     _show = []
    #     _assets = self.get_asset()
    #     if filters:
    #         for _asset in _assets:
    #             if filters in _asset.name_code():
    #                 _show.append(_asset.name_code())
    #     else:
    #         for _asset in _assets:
    #             _show.append(_asset.name_code())
    #     self.cleanitem(self.ui.asset_list)
    #     if _show:
    #         self.additem(_show,self.ui.asset_list)

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

class Upload(AssetIO,WBLloadUIFile):
    def __init__(self, uifilename,stage):
        super(AssetIO, self).__init__(uifilename)
        self._loadUiWidget(uifilename)
        # self.ui.asset_list.itemSelectionChanged.connect(self.set_description)
        # self.ui.file_step.currentIndexChanged.connect(self.test)
        # self.ui.asset_filters.textChanged.connect(self.get_asset_with_filter)

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


uiPath = resource.get("uis", "upload_shot.ui")
mainWindow = win.Window()
mainWindow.central_widget.setStyleSheet("background-color:#444444;")
mainWindow.set_title_name(u"上传镜头(upload_shot)")
mainWindow.setFixedSize(680+15,550+55)

_ui = Upload(uiPath,"ani")
mainWindow.set_central_widget(_ui.ui)

if __name__ == '__main__':
    mainWindow.show()