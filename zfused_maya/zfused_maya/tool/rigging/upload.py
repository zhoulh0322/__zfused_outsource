# coding:utf-8
# --author-- binglu.wang


import zfused_maya.widgets.window as win
import zfused_maya.core.resource as resource

from zfused_maya.node.core.upload_asset import *

uiPath = resource.get("uis", "upload_asset.ui")
mainWindow = win.Window()
mainWindow.central_widget.setStyleSheet("background-color:#444444;")
mainWindow.set_title_name(u"上传资产(upload_asset)")
mainWindow.setFixedSize(680+15,550+55)
qtWinInst = Upload(uiPath,"rig")
mainWindow.set_central_widget(qtWinInst.ui)


if __name__ == '__main__':
    mainWindow.show()
