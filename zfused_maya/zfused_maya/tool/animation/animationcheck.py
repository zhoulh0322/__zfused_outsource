# coding:utf-8
# --author-- lanhua.zhou
import maya.cmds as cmds

import zfused_maya.node.core.check as check
import zfused_maya.node.core.clear as clear

import zfused_maya.widgets.checkwidget as checkwidget

class AnimationCheck(checkwidget.CheckWidget):
    def __init__(self):
        super(AnimationCheck, self).__init__()
        self._init()
        self._check_all()
        self.recheck_button.clicked.connect(self._check_all)

    @classmethod
    def Reset(cls):
        cls.value = False
    
    def _check_all(self):
        _is_ok = True
        for widget in self.allCheckWidget:
            if self.auto_clear():
                widget.clear()
            value = widget.check()
            if not value:
                _is_ok = False
                widget.setHidden(False)
            else:
                if not self.show_all():
                    widget.setHidden(True)
                else:
                    widget.setHidden(False)
        if _is_ok:
            self.close()
        checkwidget.CheckWidget.value = _is_ok

    def _init(self):
        self.set_title_name(u"动画文件检查")

        #check file name
        widget = checkwidget.ItemWidget(u"检查文件名", check.file_name, None)
        self.add_widget(widget)

        # check camera name
        # widget = checkwidget.ItemWidget(u"检查摄像机名", check.camera_name, None, False)
        # self.add_widget(widget)

        widget = checkwidget.ItemWidget(u"检查未知节点", check.unknown_node, clear.unknown_node)
        self.add_widget(widget)

        widget = checkwidget.ItemWidget(u"检查灯光文件", check.light, clear.light)
        self.add_widget(widget)

        widget = checkwidget.ItemWidget(u"检查渲染层", check.render_layer, clear.render_layer)
        self.add_widget(widget)