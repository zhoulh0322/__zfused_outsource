# coding:utf-8
# author binglu.wang
import sys
import os
import re
import shutil
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
import zfused_maya.node.core.texture as texture

TEXT_NODE = texture.TEXT_NODE
TEXTURE_ATTR_DICT = texture.TEXTURE_ATTR_DICT

class TextureWidget(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(TextureWidget, self).__init__(parent)
        self.assetname = ""
        self.assettype = ""
        self.Texdict = {}
        self._build()
        self._show_preview()
        self.normalMode.setChecked(True)
        self.asCopy.setChecked(True)
        self.pushButton.clicked.connect(self._rename)
        self.pushButton2.clicked.connect(self.open_folder)
        self.pushButton3.clicked.connect(self.refresh)

        self.texListUI.itemSelectionChanged.connect(self._set_file)
        self.fileListUI.itemSelectionChanged.connect(self._set_mesh)
        self.fileListUI.itemSelectionChanged.connect(partial(self.selectitem, self.fileListUI))
        self.meshListUI.itemSelectionChanged.connect(partial(self.selectitem, self.meshListUI))
        self.meshListUI.itemSelectionChanged.connect(self._set_true_name)

        self.showPreview.stateChanged.connect(self._show_preview)
        self.showPath.stateChanged.connect(self._show_path)
        
        self.normalMode.clicked.connect(self._set_tex)
        self.tilingMode.clicked.connect(self._set_tex)
        self.sequenceMode.clicked.connect(self._set_tex)

        self.refresh()

    def _build(self):
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEdit.setPlaceholderText(u"标准命名")

        self.showPreview = QtWidgets.QCheckBox()
        self.showPreview.setMinimumSize(QtCore.QSize(0, 25))
        self.showPreview.setText(u"显示图片预览")

        self.pushButton = QtWidgets.QPushButton()
        self.pushButton.setMinimumSize(QtCore.QSize(120, 25))
        self.pushButton.setText(u"重命名")

        self.label1 = QtWidgets.QLabel()
        self.label1.setMinimumSize(QtCore.QSize(0, 20))
        self.label1.setText(u"贴图文件")

        self.showPath = QtWidgets.QCheckBox()
        self.showPath.setMinimumSize(QtCore.QSize(0, 20))
        self.showPath.setText(u"显示路径")

        self.pushButton2 = QtWidgets.QPushButton()
        self.pushButton2.setMinimumSize(QtCore.QSize(75, 0))
        self.pushButton2.setMaximumSize(QtCore.QSize(16777215, 20))
        self.pushButton2.setText(u"打开路径")

        self.pushButton3 = QtWidgets.QPushButton()
        self.pushButton3.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButton3.setMaximumSize(QtCore.QSize(25, 20))
        self.pushButton3.setIcon(QtGui.QIcon(resource.get("icons","refresh.png")))
        # self.pushButton3.setText(u"刷新")

        self.texListUI = QtWidgets.QListWidget()
        self.texListUI.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        self.label2 = QtWidgets.QLabel()
        self.label2.setMinimumSize(QtCore.QSize(0, 20))
        self.label2.setMaximumSize(QtCore.QSize(300, 16777215))
        self.label2.setText(u"关联模型")

        self.label3 = QtWidgets.QLabel()
        self.label3.setMinimumSize(QtCore.QSize(0, 20))
        self.label3.setMaximumSize(QtCore.QSize(300, 16777215))
        self.label3.setText(u"关联贴图节点")

        self.meshListUI = QtWidgets.QListWidget()
        self.meshListUI.setMaximumSize(QtCore.QSize(300, 16777215))
        self.meshListUI.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection)
        self.fileListUI = QtWidgets.QListWidget()
        self.fileListUI.setMaximumSize(QtCore.QSize(300, 16777215))
        self.fileListUI.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection)

        self.asCopy = QtWidgets.QCheckBox()
        self.asCopy.setMinimumSize(QtCore.QSize(0, 25))
        self.asCopy.setText(u"拷贝副本")

        self.normalMode = QtWidgets.QRadioButton()
        self.normalMode.setMinimumSize(QtCore.QSize(0, 25))
        self.normalMode.setText(u"普通")

        self.tilingMode = QtWidgets.QRadioButton()
        self.tilingMode.setMinimumSize(QtCore.QSize(0, 25))
        self.tilingMode.setText(u"多象限贴图")

        self.sequenceMode = QtWidgets.QRadioButton()
        self.sequenceMode.setMinimumSize(QtCore.QSize(0, 25))
        self.sequenceMode.setText(u"纹理动画")

        self.graphicsView = QtWidgets.QGraphicsView()
        # self.graphicsView.resize(512, 512)
        self.graphicsView.setMinimumSize(QtCore.QSize(512, 512))
        self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.label4 = QtWidgets.QLabel()
        self.label4.setMinimumSize(QtCore.QSize(0, 25))
        self.label4.setMaximumSize(QtCore.QSize(300, 16777215))
        self.label4.setText(u"操作多象限贴图或纹理动画类型的节点时\n请注意切换复选框")

        self.thrlayout1 = QtWidgets.QHBoxLayout()
        self.thrlayout1.setSpacing(5)
        self.thrlayout1.setContentsMargins(0, 0, 0, 0)
        self.thrlayout1.addWidget(self.label1)
        self.thrlayout1.addStretch()
        self.thrlayout1.addWidget(self.showPath)
        self.thrlayout1.addWidget(self.pushButton2)
        self.thrlayout1.addWidget(self.pushButton3)

        self.thrlayout2 = QtWidgets.QHBoxLayout()
        self.thrlayout2.setSpacing(5)
        self.thrlayout2.setContentsMargins(0, 0, 0, 0)
        self.thrlayout2.addWidget(self.normalMode)
        self.thrlayout2.addWidget(self.tilingMode)
        self.thrlayout2.addWidget(self.sequenceMode)

        self.btnGrp = QtWidgets.QButtonGroup()
        self.btnGrp.addButton(self.normalMode)
        self.btnGrp.addButton(self.tilingMode)
        self.btnGrp.addButton(self.sequenceMode)

        self.seclayout1 = QtWidgets.QVBoxLayout()
        self.seclayout1.setSpacing(0)
        self.seclayout1.setContentsMargins(0, 0, 0, 0)
        self.seclayout1.addLayout(self.thrlayout1)
        self.seclayout1.addWidget(self.texListUI)

        self.seclayout2 = QtWidgets.QVBoxLayout()
        self.seclayout2.setSpacing(0)
        self.seclayout2.setContentsMargins(0, 0, 0, 0)
        self.seclayout2.addWidget(self.label2)
        self.seclayout2.addWidget(self.meshListUI)
        self.seclayout2.addWidget(self.label3)
        self.seclayout2.addWidget(self.fileListUI)
        self.seclayout2.addLayout(self.thrlayout2)
        self.seclayout2.addWidget(self.label4)

        self.firlayout1 = QtWidgets.QHBoxLayout()
        self.firlayout1.setSpacing(5)
        self.firlayout1.setContentsMargins(0, 0, 0, 0)
        self.firlayout1.addWidget(self.lineEdit)
        self.firlayout1.addWidget(self.asCopy)
        self.firlayout1.addWidget(self.showPreview)
        self.firlayout1.addWidget(self.pushButton)

        self.firlayout2 = QtWidgets.QHBoxLayout()
        self.firlayout2.setSpacing(5)
        self.firlayout2.setContentsMargins(0, 0, 0, 0)
        self.firlayout2.addLayout(self.seclayout1)
        self.firlayout2.addLayout(self.seclayout2)
        self.firlayout2.addWidget(self.graphicsView)

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setContentsMargins(5, 0, 5, 10)
        self.gridLayout.addLayout(self.firlayout1,0,0,1,2)
        self.gridLayout.addLayout(self.firlayout2,1,0,1,-1)

    def _show_path(self):
        showmode = self._get_texmode()
        # item = self.texListUI.currentItem()
        if self.Texdict and showmode in self.Texdict:
            if self.showPath.isChecked():
                self.additem(self.Texdict[showmode].keys(),self.texListUI)
            else:
                showlist = []
                for _i in self.Texdict[showmode].values():
                    showlist.append(_i["name"])
                self.additem(showlist,self.texListUI)
        else:
            self.texListUI.clear()
        # if item:
        #     self.texListUI.setCurrentItem(item)

    def _show_preview(self):
        if self.showPreview.isChecked():
            self.graphicsView.setHidden(False)
            self.texListUI.itemSelectionChanged.connect(self._draw_image)
            self._draw_image()
        else:
            self.graphicsView.setHidden(True)
            try:
                self.texListUI.itemSelectionChanged.disconnect(self._draw_image)
            except:
                pass

    def _draw_image(self):
        item = self.texListUI.currentItem()
        # showmode = self._get_texmode()
        if item:
            filename = self._get_fullpath(item.text())
            img=QtGui.QImage()
            img.load(filename)
            img=img.scaled(self.graphicsView.width(),self.graphicsView.height())
            scene=QtWidgets.QGraphicsScene()
            scene.addPixmap(QtGui.QPixmap().fromImage(img))
            self.graphicsView.setScene(scene)

    def additem(self, items, listwidget,clear = True):
        if clear:
            listwidget.clear()
        for item in items:
            listwidget.addItem(item)

    def selectitem(self, listwidget):
        items = listwidget.selectedItems()
        cmds.select(cl=1)
        for item in items:
            cmds.select(item.text(),add=1,ne = 1)

    def refresh(self):
        self._get_asset_name()
        if not self.assetname:
            cmds.inViewMessage(amg = u'未获取到资产名\n请检查文件大纲', pos = 'midCenter', fade = True)
            return
        self._get_file_dict()
        self._set_tex()
        self.fileListUI.clear()
        self.meshListUI.clear()

    def _rename(self):
        item = self.texListUI.currentItem()
        tex_c = item.text()
        new_texname = self.lineEdit.text()
        if not item or not new_texname:
            return
        if "<UDIM>" in new_texname or "<f>" in new_texname:
            renamedict = self._get_rename_dict(tex_c,new_texname[:-len(re.findall("<\w+>",new_texname)[-1])])
        else:
            renamedict = self._get_rename_dict(tex_c,new_texname)
        # # ========================debug=========================
        # for _k,_v in renamedict.items():
        #     print (_k,_v)
        # # ========================debug=========================
        if renamedict:
            # rename tex
            info = ""
            sort_relist = sorted(renamedict.keys())
            if "<UDIM>" in new_texname or "<f>" in new_texname:
                _p,_n = os.path.split(renamedict[sort_relist[0]])
                attrstr = "{}/{}{}".format(_p,new_texname,os.path.splitext(_n)[-1])
            else:
                attrstr = renamedict[sort_relist[0]]
            for _k in sort_relist:
                try:
                    if self.asCopy.isChecked():
                        shutil.copyfile(_k,renamedict[_k])
                    else:
                        os.rename(_k,renamedict[_k])
                except IOError as e:
                    print (e.errno, e.strerror)
                    info += u"重命名失败：{}\n".format(_k)
            if info:
                info += u"贴图可能被其他程序占用\n请手动修改"
                cmds.confirmDialog(title = '',message = info,button = [u"确定"])
            else:
                # rename filenode
                items = self.fileListUI.selectedItems()
                for item in items:
                    _file = item.text()
                    _type = cmds.nodeType(_file)
                    if _type =="file" and not cmds.getAttr("{}.ignoreColorSpaceFileRules".format(_file)):
                        cmds.setAttr("{}.ignoreColorSpaceFileRules".format(_file), 1)
                    cmds.setAttr("{}.{}".format(_file,TEXTURE_ATTR_DICT[_type]),attrstr,type = "string")
                    if _type =="file":
                        cmds.setAttr("{}.ignoreColorSpaceFileRules".format(_file), 0)
                self.refresh()

    def _get_asset_name(self):
        for i in cmds.ls(type = "transform"):
            if cmds.objExists("%s.treeName"%i):
                self.assetname = cmds.getAttr("%s.treeName"%i)
                self.assettype = cmds.getAttr("%s.Type"%i)

    def _get_texmode(self):
        if self.normalMode.isChecked():
            return "normalMode"
        if self.tilingMode.isChecked():
            return "tilingMode"
        if self.sequenceMode.isChecked():
            return "sequenceMode"

    def _get_str(self,mesh):
        def _set_filter(meshstr):
            _ture = meshstr.split("{}_{}".format(self.assettype,self.assetname))[-1]
            if _ture.startswith("_"):
                _ture = _ture[1:]
            return "{}_{}".format(self.assetname,_ture)

        item = self.texListUI.currentItem()
        if item:
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

            _str = os.path.splitext(item.text())[0].split("_")[-1]
            print (_str)
            showmode = self._get_texmode()
            if showmode == "normalMode":
                true_tex_name = u"T_{}_{}".format(_name,_str)
            elif showmode == "tilingMode":
                # if re.findall("\d{4}",_str):
                if "<UDIM>" in item.text().upper():
                    true_tex_name = u"T_{}_{}<UDIM>".format(_name,_str.replace("<UDIM>",""))
                else:
                    if re.findall("\d{4}",_str):
                        true_tex_name = u"T_{}_{}".format(_name,_str.replace(re.findall("\d{4}",_str)[-1],""))
                    else:
                        true_tex_name = u"T_{}_{}".format(_name,_str)
            else:
                if "<f>" in _str:
                    true_tex_name = u"T_{}_{}<f>".format(_name,_str.replace("<f>",""))
                else:
                    if re.findall("\d+",_str):
                        true_tex_name = u"T_{}_{}".format(_name,_str.replace(re.findall("\d+",_str)[-1],""))
                    else:
                        true_tex_name = u"T_{}_{}".format(_name,_str)
            return true_tex_name

    # def _get_frametex_info(self,filename,mode):
    #     if mode == "tilingMode":
    #         num = re.findall("\.\d+",filename)
    #     else:
    #         num = re.findall("\d+",filename)

    #     if num:
    #         filterstr = filename.split(num[-1])[0]
    #         return filterstr,num[-1]
    #     else:
    #         return None,None

    # new
    def _get_frametex_info(self,filename,mode):
        if mode == "tilingMode":
            num = re.findall("\d{4}",filename)
        else:
            num = re.findall("\d+",filename)
        if num:
            filterstr = filename.split(num[-1])
            _zfill = "\d{%d}"%(len(num[-1]))
            if len(filterstr)-2 > 0:
                return _zfill.join(filterstr).replace(_zfill,num[-1],len(filterstr)-2),num[-1]
            else:
                return _zfill.join(filterstr),num[-1]
        else:
            if "<UDIM>" in filename:
                filterstr = filename.split("<UDIM>")
                return "\d{4}".join(filterstr),None
            elif "<udim>" in filename:
                filterstr = filename.split("<udim>")
                return "\d{4}".join(filterstr),None
            # elif "<f>" in filename:
            #     filterstr = filename.split("<f>")
            #     return "\d+".join(filterstr),None
        return None,None

    def _get_file_dict(self):
        # {"Mode":{"path":{"node"["file1","file2"],mesh:["mesh1","mesh2"],name :"name"}},}
        def set_mode(node,path,name,mode):
            if mode not in self.Texdict:
                self.Texdict[mode] = {}
            self.Texdict[mode][path] = set_info(node,path,name,mode)

        def set_info(node,path,name,mode):
            if path in self.Texdict[mode]:
                _value = self.Texdict[mode][path]
                _value["node"].append(node)
            else:
                _value = {"node":[node],"name":name}
            return _value

        if self.Texdict:
            self.Texdict = {}
        # _files = cmds.ls(type = TEXT_NODE)
        nodes = texture.nodes()
        if nodes:
            for _node_attr in nodes:
                _node = _node_attr.split(".")[0]
                _type = cmds.nodeType(_node)
                # _path = cmds.getAttr(_node_attr)
                _path = texture._get_file_full_name(_node_attr)
                _mode,_ani = 0,0
                if cmds.objExists("%s.uvTilingMode"%_node):
                    _mode = cmds.getAttr("%s.uvTilingMode"%_node)
                if cmds.objExists("%s.useFrameExtension"%_node):
                    _ani = cmds.getAttr("%s.useFrameExtension"%_node)
                if "<UDIM>" in os.path.basename(_path):
                    _mode = 1
                if _path and (os.path.exists(_path) or texture.get_udim_texfile(_path) or texture.get_frame_texfile(_path)):
                    _name = os.path.basename(_path)
                    if _mode or _ani:
                        if _mode:
                            set_mode(_node,_path,_name,"tilingMode")
                        if _ani:
                            set_mode(_node,_path,_name,"sequenceMode")
                    else:
                        set_mode(_node,_path,_name,"normalMode")

    def _get_rename_dict(self,src,dst):
        info = u"贴图名已存在\n请在末尾加入序号区分\n(纹理动画注意和序号分割开\n以免动画失效)"
        renamedict = {}
        full_tex_c = self._get_fullpath(src)
        showmode = self._get_texmode()
        _p,_n = os.path.split(full_tex_c)
        _s,_e = os.path.splitext(_n)
        if showmode != "normalMode":# "sequenceMode"
            _f = self._get_frametex_info(_s,showmode)[0]
            for _i in os.listdir(_p):
                _temp_s = os.path.splitext(_i)[0]
                # if _temp_s[-1].isdigit():
                if re.findall("\d+",_temp_s):# 判断字符串中存在数字
                    _f2,_num = self._get_frametex_info(_temp_s,showmode)
                    if _f2 and _num and _f == _f2:
                    # if _f2 and _num and re.search(_f,_f2):
                        newname = "{}/{}".format(_p,"".join([dst,_num,_e]))
                        if "{}/{}".format(_p.replace("\\","/"),_i) != newname.replace("\\","/"):
                            if os.path.exists(newname):
                                cmds.confirmDialog(title = '',message = info,button = [u"确定"])
                                return None
                            renamedict["{}/{}".format(_p,_i)] = newname
        else:
            newname = "{}/{}".format(_p.replace("\\","/"),"".join([dst,_e]))
            if full_tex_c != newname:
                if os.path.exists(newname):
                    cmds.confirmDialog(title = '',message = info,button = [u"确定"])
                    return None
                renamedict[full_tex_c] = newname
        return renamedict

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

    def _get_fullpath(self,texname):
        _mode = self._get_texmode()
        if _mode in self.Texdict and texname not in self.Texdict[_mode]:
            _list = [i for i in self.Texdict[_mode].keys() if texname == self.Texdict[_mode][i]["name"]]
            if _list and len(_list) == 1:
                return _list[0]
            else:
                return ""
        else:
            return texname

    def _set_tex(self):
        _mode = self._get_texmode()
        if self.Texdict and _mode in self.Texdict:
            self._show_path()
        else:
            self.texListUI.clear()
        self.fileListUI.clear()
        self.meshListUI.clear()

    def _set_file(self):
        item = self.texListUI.currentItem()
        showmode = self._get_texmode()
        tex_c = self._get_fullpath(item.text())
        showlist = []
        if tex_c and showmode in self.Texdict:
            files = self.Texdict[showmode][tex_c]["node"]
            for file in files:
                if cmds.objExists(file):
                    showlist.append(file)
        if showlist:
            self.additem(showlist,self.fileListUI)
        else:
            self.fileListUI.clear()
        self.fileListUI.selectAll()

    def _set_mesh(self):
        def get_list(meshlist):
            templist = []
            if meshlist:
                for mesh in meshlist:
                    if re.findall("\.f\[\d+\]",mesh) or re.findall("\.f\[\d+.\d+\]",mesh):
                        templist.append(mesh)
                    else:
                        if cmds.nodeType(mesh) == "mesh":
                            try:
                                mesh = cmds.listRelatives(mesh,p = 1)[0]
                            except:
                                mesh = cmds.listRelatives(mesh,p = 1,f = 1)[0]
                        templist.append(mesh)
            return templist
        items = self.fileListUI.selectedItems()
        showlist = []
        files = []
        if items:
            for item in items:
                file_c = item.text()
                files.append(file_c)
                if cmds.objExists(file_c):
                    _sg = self._get_node(file_c,"shadingEngine",True,"transform","mesh")
                    if _sg:
                        cmds.hyperShade(objects = _sg[0])
                        meshs = cmds.ls(sl =1)
                        showlist.extend(get_list(meshs))
        if showlist:
            self.additem(showlist,self.meshListUI)
        else:
            self.meshListUI.clear()
        cmds.select(files,r=1,ne = 1)
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

    def open_folder(self):
        item = self.texListUI.currentItem()
        # showmode = self._get_texmode()
        if item:
            fullpath = self._get_fullpath(item.text())
            _path = os.path.dirname(fullpath)
            os.startfile("{}".format(_path))


if __name__ == '__main__':
    win = TextureWidget()
    win.show()