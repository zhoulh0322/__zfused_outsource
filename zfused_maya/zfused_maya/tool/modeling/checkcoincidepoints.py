# coding:utf-8
# --author-- 王柄鹭

import maya.OpenMayaUI as mui
import maya.cmds as cmds
import maya.api.OpenMaya as om
import os,sys
import time,datetime

try:
    from PySide import QtCore,QtUiTools
    from PySide import QtGui as QtGui
    from shiboken import wrapInstance
except Exception as err:
    from PySide2 import QtCore,QtUiTools
    from PySide2 import QtWidgets as QtGui
    from shiboken2 import wrapInstance

import zfused_maya.core.resource as resource
import zfused_maya.widgets.window as win

'''try:
    qt_app = QtGui.QApplication(sys.argv)
except RuntimeError:
    qt_app = QtCore.QCoreApplication.instance()'''
    
class WBLwin(object):
    def __init__(self, uifilename, parent = None):
        super(WBLwin,self).__init__()
        self._loadUiWidget(uifilename, parent = None)
        self.ui.WBLpushBtn.clicked.connect(self.WBLrunCheck)
        self.ui.WBLSuperVerUI.itemSelectionChanged.connect(self.selectitem)
        self.ui.WBLselAllBtn.clicked.connect(self.selectallitem)
        self.ui.WBLunselAllBtn.clicked.connect(self.unselectitem)
        print "hahhaha"

    def _loadUiWidget(self,uifilename,parent = None):
        if not os.path.exists(uifilename):
            print "%s is not exists"%uifilename
            return False
        loader = QtUiTools.QUiLoader()
        uifile = QtCore.QFile(uifilename)
        uifile.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(uifile,parent = None)
        uifile.close()

    def additem(self,wrongVer):
        self.ui.WBLSuperVerUI.clear()
        for item in wrongVer:
            self.ui.WBLSuperVerUI.addItem(item)
            
    def cleanitem(self):
        self.ui.WBLSuperVerUI.clear()
    
    def selectitem(self):
        #lis = []
        #cur = self.ui.WBLSuperVerUI.currentItem()
        name = self.ui.WBLSuperVerUI.selectedItems()
        cmds.select(cl = 1)
        #cmds.select(cur.text(),add = 1)
        for i in name:
            #lis.append(i.text())
            cmds.select(i.text(),add = 1)
        #print lis
        #cmds.select(sel,r = 1)
    
    def selectallitem(self):
        #all = self.ui.WBLSuperVerUI.item(20)
        self.ui.WBLSuperVerUI.selectAll()
    
    def unselectitem(self):
        self.ui.WBLSuperVerUI.clearSelection()
            
    def WBLrunCheck(self):
        #getmesh
        checkobj = cmds.ls(sl = 1) or []
        meshList = []
        if checkobj:
            #print checkobj
            meshList = cmds.listRelatives(checkobj,type = "mesh",)
            trans_list = cmds.listRelatives(meshList,p = 1,pa = 1)
        else:
            meshList = cmds.ls(type = "mesh",fl = 1)
            trans_list = cmds.listRelatives(meshList,p = 1,pa = 1)
    
        starttime = datetime.datetime.now()
    
            #getMeshGrp
            # if cmds.objExists(checkobj) and len(cmds.ls(checkobj)) == 1:
            #     meshList = cmds.listRelatives(checkobj,ad = 1,pa =1)
            #     meshList = cmds.ls(meshList,type = "mesh",fl = 1)
            # trans_list = cmds.listRelatives(meshList,p = 1,pa = 1)
        mSel = om.MSelectionList()
        resDir = {}
        mDagPath = om.MDagPath()
        wrongVer = []
        
        #进度条
        numVerticesAll = 0
        
        if not trans_list:
            cmds.confirmDialog(t = "",m = u"请选择正确的模型")
            return None
        else:
            for trans in trans_list:
                mSel.clear()
                mSel.add(trans)
                mDagPath = mSel.getDagPath(0)
                mFnMesh = om.MFnMesh(mDagPath)
                numVerticesAll += mFnMesh.numVertices
            progress_window = cmds.window(title=u'进度条')
            cmds.columnLayout()
            progressControl = cmds.progressBar(maxValue = numVerticesAll, width = 300)
            cmds.showWindow(progress_window)
            
            for trans in trans_list:
                mSel.clear()
                mSel.add(trans)
                mDagPath = mSel.getDagPath(0)
                mName = mDagPath.partialPathName()
                resDir[mName] = {}
                mFnMesh = om.MFnMesh(mDagPath)
                for index in xrange(mFnMesh.numVertices):
                    listTemp = []
                    for v in mFnMesh.getPoint(index,space = 4):
                        listTemp.append(v)
                    tupleTemp = tuple(listTemp[0:3])
                    #print tupleTemp
                    if tupleTemp not in resDir[mName].keys():
                        resDir[mName][tupleTemp] = index
                    else:
                        wrongVer.append(r"%s.vtx[%s]"%(mName,index))
                
                #进度条
                cmds.progressBar(progressControl, edit=True, step=mFnMesh.numVertices)
            cmds.deleteUI(progress_window)
        
        # for i in wrongVer:
        #     #选中点
        #     cmds.select(i,add = 1)
        overtime = datetime.datetime.now()
        print "Use %s seconds"%(overtime - starttime).seconds
    
        if wrongVer:
            self.additem(wrongVer)
        else:
            self.cleanitem()
            cmds.confirmDialog(t = "",m = u"模型没有重合点")

def getQtMayaWindow():
    try:
        ptr = mui.MQtUtil.mainWindow()
        return wrapInstance(long(ptr),QtGui.QMainWindow)
    except:
        return None

def UI():
    mainWindow.show()

uiPath = resource.get("uis", "checkcoincidepoints.ui")
mainWindow = win.Window()
qtWinInst = WBLwin(uiPath,parent = getQtMayaWindow())
mainWindow.set_central_widget(qtWinInst.ui)
mainWindow.set_title_name(u"check_coincide_points")
mainWindow.setFixedSize(475,463)

if __name__ == '__main__':
    UI()
    