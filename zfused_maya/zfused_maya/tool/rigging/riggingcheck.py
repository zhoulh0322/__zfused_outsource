# coding:utf-8
# --author-- lanhua.zhou
import maya.cmds as cmds

import zfused_maya.node.core.check as check
import zfused_maya.node.core.clear as clear

import zfused_maya.widgets.checkwidget as checkwidget

class RiggingCheck(checkwidget.CheckWidget):
    def __init__(self):
        super(RiggingCheck, self).__init__()
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
        check.Check.value = _is_ok

    def show(self):
        import zfused_maya.core.restricted as restricted
        import maya.cmds as cmds
        _has_per, _info = restricted.restricted()
        if not _has_per:
            cmds.confirmDialog(message = _info)
            return 
        super(RiggingCheck, self).show()

    def _init(self):
        self.set_title_name(u"绑定文件检查")

        #check file name
        widget = checkwidget.ItemWidget(u"检查文件名", check.file_name, None)
        self.add_widget(widget)
        
        #check rendering hierarchy
        widget = checkwidget.ItemWidget(u"检查文件结构", _check_hierarchy, None, False)
        self.add_widget(widget)

        #check reference
        widget = checkwidget.ItemWidget(u"检查动画层", check.animation_layer, clear.animation_layer)
        self.add_widget(widget)

        widget = checkwidget.ItemWidget(u"检查未知节点", check.unknown_node, clear.unknown_node)
        self.add_widget(widget)
        #check un exists files
        widget = checkwidget.ItemWidget(u"检查贴图文件是否不存在", check.file_node, None, False)
        self.add_widget(widget)

        widget = checkwidget.ItemWidget(u"检查灯光文件", check.light, clear.light)
        self.add_widget(widget)

        widget = checkwidget.ItemWidget(u"检查显示层", check.display_layer, clear.display_layer)
        self.add_widget(widget)

        widget = checkwidget.ItemWidget(u"检查渲染层", check.render_layer, clear.render_layer)
        self.add_widget(widget)

        widget = checkwidget.ItemWidget(u"检查重命名", check.repeat, None)
        self.add_widget(widget)
        
        #check texture path
        widget = checkwidget.ItemWidget(u"检查贴图路径", check.texture_path, None, False)
        self.add_widget(widget)


def _check_hierarchy():
    rendering = []
    allDags = cmds.ls(dag = True)
    for dag in allDags:
        #print dag
        #get 
        if cmds.objExists("%s.rendering"%dag):
            value = cmds.getAttr("%s.rendering"%dag)
            if value:
                rendering.append(dag)
    #return rendering
    if not rendering:
        info = u"文件组织结构错误,请用分组共组分组整合文件\n"
        return False,info
    else:
        return True, None