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
        # self._check_all()
        # self.recheck_button.clicked.connect(self._check_all)
        cmds.delete(cmds.ls(typ="nodeGraphEditorInfo"))

    @classmethod
    def Reset(cls):
        cls.value = False
    
    def _check_all_del(self):
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

    def _init(self):
        self.set_title_name(u"绑定文件检查")

        #check file name
        widget = checkwidget.ItemWidget(u"检查文件名", check.file_name, None)
        self.add_widget(widget)
        
        #check rendering hierarchy
        widget = checkwidget.ItemWidget(u"检查文件结构", _check_hierarchy, None, False)
        self.add_widget(widget)

        # 检查动画key帧 _check_ani_key_curve
        widget = checkwidget.ItemWidget(u"检查动画key帧曲线", anim_curve, None, False)
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

        widget = checkwidget.ItemWidget(u"检查摄像机", check.camera, clear.camera)
        self.add_widget(widget)

        #check texture path
        widget = checkwidget.ItemWidget(u"检查贴图路径", check.texture_path, None, False)
        self.add_widget(widget)

        # check rendering group
        widget = checkwidget.ItemWidget(u"检查渲染组", _check_renderinggroup, repair_renderinggroup, False)
        self.add_widget(widget)
        # check null_reference
        widget = checkwidget.ItemWidget(u"检查无用Reference节点", _check_null_reference, _repair_null_reference, False)
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


def _check_renderinggroup():
    rendering = []
    _renderingdag = [i for i in cmds.ls(dag = 1) if cmds.objExists("{}.rendering".format(i))]
    if _renderingdag:
        for dag in _renderingdag:
            value = cmds.getAttr("%s.rendering"%dag)
            if value:
                rendering.append(dag)
        if rendering:
            if len(rendering) == 1:
                return True, None
            else:
                info = u"存在超过一个的可渲染组，请隐藏不参加渲染的组并关闭rendering属性\n"
                info += "\n".join(rendering)
                return False,info
        else:
            info = u"没有可用渲染组，请修改rendering属性值\n"
            info += "\n".join(_renderingdag)
            return False,info

def repair_renderinggroup():
    _renderingdag = [i for i in cmds.ls(dag = 1) if cmds.objExists("{}.rendering".format(i))]
    if _renderingdag:
        for dag in _renderingdag:
            _r = cmds.getAttr("%s.rendering"%dag)
            _v = check.isshow(dag)
            # _v = cmds.getAttr("%s.v"%dag)
            if not _v:
                # cmds.setAttr( "%s.rendering"%dag, 0 )
                cmds.deleteAttr(dag,at = "rendering")


def _check_null_reference():
    _references = cmds.ls(rf=True)
    _null_reference = []
    if not _references:
        return True, None
    info = u"存在无用的reference节点:\n\n"
    for _reference in _references:
        try:
            cmds.referenceQuery(_reference, f=1)
        except:
            info += _reference + "\n"
            _null_reference.append(_reference)
    if len(_null_reference) == 0:
        return True, None
    return False, info

def _repair_null_reference():
    _references = cmds.ls(rf=True)
    for _reference in _references:
        try:
            cmds.referenceQuery(_reference, f=1)
        except:
            cmds.lockNode(_reference, l=0)
            cmds.delete(_reference)
            print((u"成功删除节点：" + _reference))


def anim_curve():
    """ check anim key curves

    """
    _curves = cmds.ls(type = ["animCurveTL", "animCurveTA", "animCurveTT", "animCurveTU"])
    if _curves:
        if cmds.listConnections(_curves,d = 1,type = "transform"):
            _linktrans = set(cmds.listConnections(_curves,d = 1,type = "transform"))
            _linkshapes = cmds.listRelatives(list(_linktrans),s = 1,type = ["mesh","nurbsCurve"])
            if _linkshapes:
                _trans = cmds.listRelatives(list(set(_linkshapes)),p = 1)
                info = u"场景存在错误key帧曲线\n"
                info += "\n".join(_trans)
                return False, info
    return True, None