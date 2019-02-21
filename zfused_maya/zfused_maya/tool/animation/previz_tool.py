# coding:utf-8
# author binglu.wang

from PySide2 import QtWidgets,QtGui,QtCore, QtUiTools
from shiboken2 import wrapInstance
import maya.OpenMayaUI as mui
import maya.cmds as cmds
import maya.mel as mm
import os

def getQtMayaWindow():
    try:
        ptr = mui.MQtUtil.mainWindow()
        return wrapInstance(long(ptr), QtWidgets.QMainWindow)
    except:
        return None

class Win(QtWidgets.QWidget):

    def __init__(self,parent = None):
        super(Win, self).__init__()
        self._build()
        self.pushButton.clicked.connect(self.unload_ref)
        self.pushButton2.clicked.connect(self.group_unselect_cam)
        self.pushButton3.clicked.connect(self.delete_unuse_cam)
        self.defcult_cam = [u'backShape', u'bottomShape', u'frontShape', u'perspShape', u'sideShape', u'topShape',"leftShape"]


    def _build(self):
        self.resize(350, 200)
        self.pushButton = QtWidgets.QPushButton()
        self.pushButton.setMinimumSize(QtCore.QSize(0, 60))
        self.pushButton.setMaximumSize(QtCore.QSize(350, 16777215))
        self.pushButton.setText(u"Unload reference\n取消无用参考")

        self.pushButton2 = QtWidgets.QPushButton()
        self.pushButton2.setMinimumSize(QtCore.QSize(0, 60))
        self.pushButton2.setMaximumSize(QtCore.QSize(350, 16777215))
        self.pushButton2.setText(u"Create simple camera\n创建简单相机")

        self.pushButton3 = QtWidgets.QPushButton()
        self.pushButton3.setMinimumSize(QtCore.QSize(0, 60))
        self.pushButton3.setMaximumSize(QtCore.QSize(350, 16777215))
        self.pushButton3.setText(u"Remove unuse camera\n移除无用相机")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(0, 5, 0, 5)

        self.layout.addWidget(self.pushButton)
        self.layout.addWidget(self.pushButton2)
        self.layout.addWidget(self.pushButton3)

        self.setLayout(self.layout)

    def unload_ref(self):
        sels = cmds.ls(sl = 1)
        if sels:
            for i in sels:
                refnode = cmds.referenceQuery(i,rfn = 1)
                cmds.file(ur = refnode)
        else:
            cmds.confirmDialog(title = '',message = u'请选择至少一个模型后操作',button = [u"确定"])

    def get_cam(self):
        cam = cmds.ls(sl = 1)
        if cam:
            if "|" in cam[0]:
                cmds.confirmDialog(title = '',message = u'文件中存在重名相机\n请重命名所选相机后操作',button = [u"确定"])
                return None
            if cmds.nodeType(cam) == "camera":
                if len(cmds.ls(cmds.listRelatives(cam,p = 1))) == 1:
                    return cam[0]
                else:
                    cmds.confirmDialog(title = '',message = u'文件中存在重名相机\n请重命名所选相机后操作',button = [u"确定"])
                    return None
            cam = cmds.listRelatives(cam[0],s = 1)
            if cmds.nodeType(cam[0]) == "camera":
                return cam[0]
        else:
            cam = [i for i in cmds.ls(ca = 1) if i not in self.defcult_cam]
            if len(cam) == 1 and len(cmds.ls(cmds.listRelatives(cam,p = 1))) == 1:
                return cam[0]
        cmds.confirmDialog(title = '',message = u'未能获取到正确的相机\n请手动选择后操作',button = [u"确定"])
        return None

    def create_cam(self,ori_cam):
        cam_trans = cmds.listRelatives(ori_cam,p = 1)[0]

        new_cam_name = "{}_PR".format(cam_trans)
        new_cam = cmds.rename(cmds.camera()[0], new_cam_name)
        new_cam_shape = cmds.listRelatives(new_cam,s = 1)[0]

        # trans povit
        cmds.parentConstraint(cam_trans, new_cam, maintainOffset = False)

        # trans attr
        presets_path = mm.eval("saveAttrPreset %s %s false;"%(ori_cam,ori_cam))
        presets_name = os.path.splitext(os.path.basename(presets_path))[0]
        mm.eval("applyAttrPreset %s %s 1;" %(new_cam_shape, presets_name))

        # trans connect attr
        connect_list = cmds.listConnections(ori_cam,p = 1,c = 1,d = 0)
        if connect_list:
            for _i in connect_list[::2]:
                _attr = _i.split(".")[-1]
                cmds.connectAttr("{}.{}".format(ori_cam,_attr),"{}.{}".format(new_cam_shape,_attr))

        # bakeframe
        min_time = cmds.playbackOptions(query = True, minTime = True)
        max_time = cmds.playbackOptions(query = True, maxTime = True)
        cmds.bakeResults(new_cam, s = True, sm = True, time = (min_time,max_time))


    def check_simple_cam(self,name):
        _attrs = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']
        while True:
            parent_grp = cmds.listRelatives(name, allParents = True,f= 1)
            if not parent_grp:
                break
            else:
                trans_value = [i for i in _attrs if cmds.getAttr("%s.%s"%(parent_grp[0],i)) != 0]
                if trans_value:
                    return False
                else:
                    name = parent_grp
        return True

    def group_unselect_cam(self):
        ori_cam = self.get_cam()
        if ori_cam:
            allcamera = [cmds.listRelatives(i,p = 1)[0] for i in cmds.ls(ca = 1) if i not in self.defcult_cam]
            ori_cam_trans = cmds.listRelatives(ori_cam,p = 1)[0]
            # print self.check_simple_cam(ori_cam_trans)
            if self.check_simple_cam(ori_cam_trans):
                cmds.inViewMessage(amg = u'选择相机无需创建操作', pos = 'midCenter', fade = True)
                allcamera.remove(ori_cam_trans)
            else:
                self.create_cam(ori_cam)
            cam_layer = "unuse_cam_layer"
            if cmds.objExists(cam_layer) and cmds.nodeType(cam_layer) == "displayLayer":
                cmds.delete(cam_layer)
            if allcamera:
                cam_layer = cmds.createDisplayLayer(n = cam_layer,e = 1)
                cmds.editDisplayLayerMembers(cam_layer,allcamera,nr = 1)

    def delete_unuse_cam(self):
        if cmds.objExists("unuse_cam_layer") and cmds.nodeType("unuse_cam_layer") == "displayLayer":
            sel = cmds.editDisplayLayerMembers("unuse_cam_layer",q = 1,fn =1)
            cmds.delete(sel)
            cmds.delete("unuse_cam_layer")

win = QtWidgets.QMainWindow(parent=getQtMayaWindow())
win.resize(350, 135)
ui = Win()
win.setCentralWidget(ui)
win.setWindowTitle("previz tool")

if __name__ == '__main__':
    win.show()
