# coding:utf-8
# --author-- 张伟
# cmds.polyTransfer('zero:p_zero_luoxuanjiang_1', v = 0, vc = 0, uv = 1, ao = 'zero_172:p_zero_luoxuanjiang_1')

from PySide2 import QtWidgets, QtCore
import maya.OpenMayaUI as oi 
import shiboken2 as shiboken
import zfused_maya.widgets.window as win
import maya.cmds as cmds

class PolyTransfer():
    def __init__(self):
        self.showUI()
        self.__uiwindow = oi.MQtUtil.findWindow(u"传递UV")
        self.__uiwindow = shiboken.wrapInstance(long(self.__uiwindow), QtWidgets.QWidget)        
        # pass
    def _returnwindow(self):
        return self.__uiwindow
    def showUI(self):
        windowName = u'传递UV'
        if cmds.window(windowName, q = True, exists = True):
            cmds.deleteUI(windowName)
        if cmds.windowPref(windowName, exists = True) == True:
            cmds.windowPref(windowName,remove = True)
        cmds.window(windowName,t = windowName,sizeable = True,w = 250)    
        PrimaryLayout = cmds.columnLayout(adj = True, bgc = [0.15,0.15,0.15])
        
        cmds.separator(h = 5)
        cmds.text(l = u'方 法 一', bgc = [0.2,0.2,0.2], height = 22)
        cmds.text(l = u'选择模型，单击\'<<<\'选定', h = 20)
        
        true_InfoGatherLayout = cmds.rowLayout(nc = 3, adjustableColumn = 2, p = PrimaryLayout)
        cmds.text(l = u"UV正确模型 : ")
        trueUV_Name = cmds.textField(w = 200)
        trueUV_Assign = cmds.button(l = '<<<', c = lambda *args: self.true_AssignBtnCmd())
        
        cmds.setParent(PrimaryLayout)
        false_InfoGatherLayout = cmds.rowLayout(nc = 3, adjustableColumn = 2, p = PrimaryLayout)
        cmds.text(l = u"UV错误模型 : ")
        falseUV_Name = cmds.textField(w = 200)
        falseUV_Assign = cmds.button(l = '<<<', c = lambda *agrs: self.false_AssignBtnCmd())
        
        cmds.setParent(PrimaryLayout)
        assignButton = cmds.button(l = u'传递', c = lambda *args: self.transferUV())
        
        cmds.setParent(PrimaryLayout)
        cmds.separator(h = 10, bgc = [0.2,0.2,0.2])
        cmds.separator(h = 10, bgc = [0.2,0.2,0.2])
        cmds.text(l = u'方 法 二', bgc = [0.2,0.2,0.2], height = 22)        
        cmds.text(l = u'先选正确UV模型，后选错误UV模型', h = 20)
        cmds.button(l = u'传递', c = lambda *args: self.secTransferUV())
        
        cmds.separator(h = 5)
        
        self.trueUV_Name = trueUV_Name
        self.falseUV_Name = falseUV_Name

    def setTextField(self, textFieldToSet, Value):
        cmds.textField(textFieldToSet, e = True, text = Value)
            
    def getTrueModel(self):
        selection = cmds.ls(sl = True)[0]
        return selection
        
    def true_AssignBtnCmd(self):
        trueUV_Name = self.trueUV_Name
        trueModelName = self.getTrueModel()
        self.setTextField(trueUV_Name, trueModelName)  
              
    def getFalseModel(self):
        selection = cmds.ls(sl = True)[0]
        return selection
        
    def false_AssignBtnCmd(self):
        falseUV_Name = self.falseUV_Name
        falseModelName = self.getFalseModel()
        self.setTextField(falseUV_Name, falseModelName)   
             
    def transferUV(self):
        trueUV_Name = self.trueUV_Name
        falseUV_Name = self.falseUV_Name
        trueName = cmds.textField(trueUV_Name, q = True, text = True)
        falseName = cmds.textField(falseUV_Name, q = True, text = True)
        cmds.polyTransfer(falseName, v = 0, vc = 0, uv = 1, ao = trueName)
        
    def secTransferUV(self):
        selects = cmds.ls(sl = True)
        cmds.polyTransfer(selects[1], v = 0, vc = 0, uv = 1, ao = selects[0])
    def UI(self):
        # self.showUI()
        # _uiwindow = oi.MQtUtil.findWindow(u"传递UV")
        # _uiwindow = shiboken.wrapInstance(long(_uiwindow), QtWidgets.QWidget)
        
        mainWindow = win.Window()
        mainWindow.set_central_widget(self._returnwindow())
        mainWindow.set_title_name(u"传递UV") 
        #mainWindow.setFixedSize(500,286)
        mainWindow.resize(500,286)
        mainWindow.show()
        
               
if __name__ == "__main__":
    polytransfer = PolyTransfer()
    polytransfer.UI()