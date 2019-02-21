# coding:utf-8
# --author-- lanhua.zhou
import maya.cmds as cmds

import zfused_maya.node.core.check as check
import zfused_maya.node.core.clear as clear

import zfused_maya.widgets.checkwidget as checkwidget
import zfused_maya.tool.modeling.materialcheck as materialcheck


class ShadingCheck(checkwidget.CheckWidget):
    def __init__(self):
        super(ShadingCheck, self).__init__()
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
        
        checkwidget.CheckWidget.value = _is_ok
        print(checkwidget.CheckWidget.value)
        check.Check.value = _is_ok

        if _is_ok:
            self.close()

    def show(self):
        import zfused_maya.core.restricted as restricted
        import maya.cmds as cmds
        _has_per, _info = restricted.restricted()
        if not _has_per:
            cmds.confirmDialog(message = _info)
            return 
        super(ShadingCheck, self).show()


    def _init(self):
        self.set_title_name(u"材质文件检查")

        #check file name
        widget = checkwidget.ItemWidget(u"检查文件名", check.file_name, None)
        self.add_widget(widget)
        
        #check transform attr
        widget = checkwidget.ItemWidget(u"检查通道属性值", _check_attr, None)
        self.add_widget(widget)
        #check rendering hierarchy
        widget = checkwidget.ItemWidget(u"检查文件结构", _check_hierarchy, None, False)
        self.add_widget(widget)
        #check history
        widget = checkwidget.ItemWidget(u"检查模型历史", _check_history, None, False)
        self.add_widget(widget)
        #check equal widget
        widget = checkwidget.ItemWidget(u"检查相同模型", _check_equalmesh, None)
        self.add_widget(widget)
        #check reference
        widget = checkwidget.ItemWidget(u"检查动画层", check.animation_layer, clear.animation_layer)
        self.add_widget(widget)
        widget = checkwidget.ItemWidget(u"检查未知节点", check.unknown_node, clear.unknown_node)
        self.add_widget(widget)
        #check un exists files
        widget = checkwidget.ItemWidget(u"检查贴图文件是否不存在", check.file_node, None, False)
        self.add_widget(widget)

        widget = checkwidget.ItemWidget(u"检查摄像机", check.camera, clear.camera)
        self.add_widget(widget)

        widget = checkwidget.ItemWidget(u"检查灯光文件", check.light, clear.light)
        self.add_widget(widget)

        widget = checkwidget.ItemWidget(u"检查动画曲线", check.anim_curve, clear.anim_curve)
        self.add_widget(widget)

        widget = checkwidget.ItemWidget(u"检查显示层", check.display_layer, clear.display_layer)
        self.add_widget(widget)

        widget = checkwidget.ItemWidget(u"检查渲染层", check.render_layer, clear.render_layer)
        self.add_widget(widget)

        widget = checkwidget.ItemWidget(u"检查命名空间", check.namespace, clear.namespace)
        self.add_widget(widget)
        
        widget = checkwidget.ItemWidget(u"检查重命名", check.repeat, None, False)
        self.add_widget(widget)
        
        #check texture path
        widget = checkwidget.ItemWidget(u"检查贴图路径", check.texture_path, None, False)
        self.add_widget(widget)

        widget = checkwidget.ItemWidget(u"检查材质命名", _check_material, materialcheck.CheckShader().repair, False)
        self.add_widget(widget)

        widget = checkwidget.ItemWidget(u"检查贴图命名", _check_tex_name, None, False)
        self.add_widget(widget)

def _check_attr():
    #get all transform
    _un = ["front","persp","side","top"]
    _all_trans = cmds.ls(type = "transform")
    _use_tans = list(set(_all_trans) - set(_un))
    _de = []
    for _tans in _use_tans:
        _t = cmds.getAttr("%s.translate"%_tans)
        _r = cmds.getAttr("%s.rotate"%_tans)
        _s = cmds.getAttr("%s.scale"%_tans)
        _child = cmds.listRelatives(_tans, c = True, type = "mesh")
        if _child:
            if _t != [(0.0, 0.0, 0.0)] or _r != [(0.0, 0.0, 0.0)] or _s != [(1.0, 1.0, 1.0)]:
                _de.append(_tans)
    if _de:
        info = u"通道属性值不为空\n"
        for child in _de:
            info += "{}\n".format(child)
        return False,info
    return True, None

def _check_history():
    import pymel.core as pm
    _history = []
    allDags = pm.ls(dag = 1)
    for dag in allDags: 
        _his = dag.history()
        #_his = [n for n in dag.history(il=1, pdo = True)]
        _his = [n for n in dag.history(il=1, pdo = True) if n.type() != "shadingEngine"]
        if _his and dag.type() == "mesh":
            _history.append(dag)
    if _history:
        _history = list(set(_history))
        info = u"错误:部分模型存在历史记录\n"
        for child in _history:
            info += u"%s\n"%child
        return False,info
    else:
        return True, None

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
        info = u"文件组织结构错误,请用分组工具分组整合文件\n"
        return False,info
    else:
        return True, None

def _check_equalmesh():
    import maya.api.OpenMaya as om
    _info = []
    _error_meshs = []
    _top_dags = cmds.ls(type = "mesh")
    for _top_dag in _top_dags:
        #get dag hierarchy
        allDags = cmds.ls(_top_dag, dag = True, ni = True, type = "mesh")
        # print allDags
        for dag in allDags:
            selectionList = om.MSelectionList()
            selectionList.add( dag)
            node = selectionList.getDependNode(0)
            fnMesh = om.MFnMesh(node)
            dag_info = ""
            dag_info += " %s"%(fnMesh.numVertices)
            dag_info += " %s"%(fnMesh.numEdges)
            dag_info += " %s"%(fnMesh.numPolygons)
            #_info.append(dag_info)
            if dag_info in _info:
                _error_meshs.append(fnMesh.name())
            else:
                _info.append(dag_info)
    if _error_meshs:
        _info = u"场景存在相同模型\n"
        for _mesh in _error_meshs:
            _info += "{}\n".format(_mesh)
            return False, _info
    return True, None

def _check_material():
    _check = materialcheck.CheckShader()
    _info = _check.check_shader()
    if _info:
        info = u"材质命名错误(无法修复的请检查是否是默认材质)\n"
        info += "".join(sorted(_info))
        return False, info
    return True, None

def _check_tex_name():
    _check = materialcheck.CheckShader()
    _info = _check.check_texture()
    if _info:
        info = u"贴图命名错误,请手动检查\n"
        info += "".join(sorted(_info))
        return False, info
    return True, None