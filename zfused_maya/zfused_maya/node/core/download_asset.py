# coding:utf-8
# --author-- binglu.wang
import os
import re

try:
    from PySide import QtGui
    from PySide import QtCore, QtUiTools
    from shiboken import wrapInstance
except ImportError:
    from PySide2 import QtWidgets as QtGui
    from PySide2 import QtCore, QtUiTools
    from shiboken2 import wrapInstance

import zfused_api
import zfused_maya.core.record as record
from functools import partial
# import zfused_maya.core.resource as resource
# import zfused_maya.widgets.window as win


# def getQtMayaWindow():
#     try:
#         ptr = mui.MQtUtil.mainWindow()
#         return wrapInstance(long(ptr), QtGui.QMainWindow)
#     except:
#         return None

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

    def set_step(self,*args):
        _show = []
        _steps = self.get_step()
        for _step in _steps:
            if args:
                _show.extend([_step.code() for _f in args if _f in _step.code()])
            else:
                _show.append(_step.code())
        if _show:
            self.additem(_show,self.ui.file_step)

    def get_step(self):
        _step_list = []
        _project_id = record.current_project_id()
        _project_steps = zfused_api.step.project_steps([_project_id])
        for _project_step in _project_steps:
            # print zfused_api.step.ProjectStep(_project_step["Id"])
            step_handle = zfused_api.step.ProjectStep(_project_step["Id"])
            # print(step_handle.name_code())
            # print(step_handle.check_script())
            _step_list.append(step_handle)
        return _step_list

    def get_step_cmd(self):
        _steps = self.get_step()
        _step_c = self.ui.file_step.currentText()
        for _step in _steps:
            if _step.code() ==_step_c:
                print _step.code(),_step.check_script()
                return _step.check_script()
        return None


    def get_asset(self):
        _asset_list = []
        _project_id = record.current_project_id()
        _project_assets = zfused_api.asset.project_assets([_project_id])
        # print _project_assets
        for _asset in _project_assets:
            _asset_list.append(zfused_api.asset.Asset(_asset["Id"]))
        return _asset_list

    def set_asset(self,**kwargs):
        _show = []
        _assets = self.get_asset()
        if kwargs:
            if kwargs.has_key("filter"):
                for _asset in _assets:
                    if kwargs["filter"] in _asset.name_code():
                        _show.append(_asset.name_code())
            if kwargs.has_key("complete"):
                print "complete"
        else:
            for _asset in _assets:
                _show.append(_asset.name_code())
        self.cleanitem(self.ui.asset_list)
        if _show:
            self.additem(_show,self.ui.asset_list)

    def set_description(self):
        _item = self.ui.asset_list.currentItem()
        _assets = self.get_asset()
        for _asset in _assets:
            if _item.text() in _asset.name_code():
                _desc = _asset.description()
                self.ui.description.setText(_desc)

    def get_asset_with_filter(self):
        _f = self.ui.asset_filters.text()
        _f_dict = {"filter" : _f}
        self.set_asset(**_f_dict)

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
        self.set_asset()
        self.set_step(stage) #"model","rig","shader","assembly"
        self.ui.asset_list.itemSelectionChanged.connect(partial(self._set_version, False))
        self.ui.asset_list.itemSelectionChanged.connect(self.set_description)
        self.ui.asset_list.itemDoubleClicked.connect(self._download_file)
        self.ui.file_step.currentIndexChanged.connect(self.test)
        self.ui.asset_filters.textChanged.connect(self.get_asset_with_filter)
        self.ui.download_btn.clicked.connect(self._download_file)

    def test(self):
        print "aaa"

    def _set_version(self,showtype):
        # 获取全版本
        _show = []
        _name = self._get_path()[-1]
        _path = self._get_full_path()
        if os.path.exists(_path):
            _num = len(os.listdir(_path))
            if _num > 0:
                _final = self._get_final_version(_name,_path)
                if _final:
                    for _i in xrange(_num-1):
                        _show.append(str(_i+1))
                    _show.append("final")
                else:
                    for _i in xrange(_num):
                        _show.append(str(_i+1))
                self.cleanitem(self.ui.file_version)
                if showtype and _show:
                    self.additem(_show,self.ui.file_version)
                    self.ui.file_version.setCurrentIndex(_num-1)
                    return
                elif not showtype and _final:
                    self.additem(["final"],self.ui.file_version)
                    self.ui.file_version.setCurrentIndex(0)
                    return
        self.cleanitem(self.ui.file_version)


    def _get_final_version(self,name,path):
        for _i in os.listdir(path):
            if os.path.splitext(_i)[0] == name:
                return True
        return False

    def _get_full_path(self,version = None):
        _step = self._get_step()
        _path,_name = self._get_path()
        if version:
            print re.findall("\d+",version)
            if re.findall("\d+",version):
                return "/".join([_path,_step,r"maya2017/file","%s.%s.mb"%(_name,str(version).zfill(4))])
            else:
                return "/".join([_path,_step,r"maya2017/file","%s.mb"%_name])
        else:
            return "/".join([_path,_step,r"maya2017/file"])

    def _get_step(self):
        # print self.ui.file_step.currentText()
        return self.ui.file_step.currentText()

    def _get_version(self):
        return self.ui.file_version.currentText()

    def _get_path(self):
        _n = self.ui.asset_list.selectedItems()
        if _n:
            _assets = self.get_asset()
            for _a in _assets:
                if _n[0].text() == _a.name_code():
                    # print _a.production_path()
                    return _a.production_path(),_a.code()

    def _download_file(self):
        import maya.cmds as cmds
        _v = self._get_version()
        if _v:
            _file_path = self._get_full_path(_v)
            # print _file_path
            if os.path.exists(_file_path):
                cmds.file(f = 1,new = 1)
                cmds.file(_file_path,o = 1,f = 1)


# uiPath = resource.get("uis", "download_asset.ui")
# mainWindow = win.Window()
# mainWindow.central_widget.setStyleSheet("background-color:#444444;")
# mainWindow.set_title_name(u"download_asset")
# mainWindow.setFixedSize(680+15,550+55)
# _ui = Download(uiPath,"model")
# mainWindow.set_central_widget(_ui.ui)

# if __name__ == '__main__':
#     mainWindow.show()




