# coding:utf-8
# author binglu.wang
import sys
import os

try:
    from PySide import QtGui as QtWidgets
    from PySide import QtCore, QtUiTools
    from shiboken import wrapInstance
except ImportError:
    from PySide2 import QtWidgets,QtGui,QtCore,QtUiTools
    from shiboken2 import wrapInstance

import zfused_maya.core.resource as resource
import zfused_maya.widgets.window as zfwin

import shading_widget
reload(shading_widget)
import matarial_widget
reload(matarial_widget)
import texture_widget
reload(texture_widget)

# from shader_widget import *
# import zfused_maya.widgets.window as win
# import zfused_maya

class Win(QtWidgets.QMainWindow):
    def __init__(self,parent = None):
        super(Win, self).__init__()
        print (self.layoutDirection())
        self._build()
        self._toolbar()

        self.toolBar.actionTriggered[QtWidgets.QAction].connect(self.test)

    def _build(self):
        self.resize(1000, 600)
        self.setObjectName("repair_shader_tool")
        self.setWindowTitle(u"材质重命名工具(repair_shader_tool)")
        self.shading_frame = shading_widget.ShadingWidget()
        self.setCentralWidget(self.shading_frame)

    # 添加工具栏
    def _toolbar(self):
        self.toolBar = self.addToolBar('type')
        # self.toolBar.setMinimumSize(QtCore.QSize(50, 0))

        self.bar1=QtWidgets.QAction('shading engine',self)
        self.toolBar.addAction(self.bar1)
        self.toolBar.addSeparator()

        self.bar2=QtWidgets.QAction('matarials',self)
        self.toolBar.addAction(self.bar2)
        self.toolBar.addSeparator()

        self.bar2=QtWidgets.QAction('textures',self)
        self.toolBar.addAction(self.bar2)

    def test(self,action):
        if action.text() == "shading engine":
            self.shading_frame = shading_widget.ShadingWidget()
            self.setCentralWidget(self.shading_frame)
        elif action.text() == "matarials":
            self.matarial_frame = matarial_widget.MatarialWidget()
            self.setCentralWidget(self.matarial_frame)
        else:
            self.texture_frame = texture_widget.TextureWidget()
            self.setCentralWidget(self.texture_frame)


# zfwin
win = zfwin.Window()
ui = Win()
win.set_central_widget(ui)
win.set_title_name(u"材质重命名工具(repair_shader_tool)")


if __name__ == '__main__':
    # 外部调用
    app = QtWidgets.QApplication(sys.argv)
    win = Win()
    win.show()
    sys.exit(app.exec_())
