# coding:utf-8
# --author-- lanhua.zhou

""" shading color widget """

from PySide2 import QtWidgets, QtGui

import maya.cmds as cmds

import shadingcolorwidget
import shadingcolorproc

import zfused_maya.widgets.progresswidget as progresswidget

class ShadingColor(shadingcolorwidget.ShadingColorWidget):
    def __init__(self, parent = True):
        super(ShadingColor, self).__init__(parent)

        self.refresh_button.clicked.connect(self._refresh)
        self.engine_listwidget.clicked.connect(self._isolate)
        self.engine_listwidget.clicked.connect(self._engine_content)
        self.color_button.clicked.connect(self._set_color)
        self.color_engine_button.clicked.connect(self._switch_color_shader)
        self.orignail_engine_button.clicked.connect(self._switch_orignail_shader)
        self._load_engines()

    def _refresh(self):
        """ 刷新界面

        """
        self._load_engines()

    def _switch_orignail_shader(self):
        """ 还原材质球

        """
        _engines = shadingcolorproc.get_shading_engines()
        if not _engines:
            return 
        shadingcolorproc.switch_orignail_shader(_engines)

    def _switch_color_shader(self):
        """ 切换至shading color材质球

        """
        _engines = shadingcolorproc.get_shading_engines()
        if not _engines:
            return 
        shadingcolorproc.switch_color_shader(_engines)

    def _load_engines(self):
        """ 加载引擎

        """
        self.engine_listwidget.clear()

        _engines = shadingcolorproc.get_shading_engines()
        print(_engines)
        if not _engines:
            return 
        # load progress
        _progress = progresswidget.ProgressWidget(["convert shader color"])
        try:
            _progress.show()
            for _index, _engine in enumerate(_engines):
                _color = shadingcolorproc.get_node_shading_color(_engine)
                # 可能会出问题
                if _color:
                    shadingcolorproc.set_node_shading_color(_engine, _color)
                print(_color)
                if not _color:
                    _color = shadingcolorproc.get_connect_color(_engine)
                    if _color:
                        shadingcolorproc.set_node_shading_color(_engine, _color)
                _progress.set_value("convert shader color", float(_index)/len(_engines)*100.0)
                _progress.repaint()
                self.engine_listwidget.addItem(_engine)
        except:
            pass
        finally:
            _progress.close()


    def _set_color(self):
        node = self.content_name_button.text()
        if not node:
            return
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.color_label.setStyleSheet("background-color: {}".format(color.name()))
            #palette = self.color_label.palette()
            #palette.setColor(QtGui.QPalette.Background, color.name())
            #self.color_label.setPalette(palette)
            shadingcolorproc.set_node_shading_color(node, color.name())

    def _engine_content(self, index):
        engine = index.data()
        # name
        self.content_name_button.setText(engine)
        # color widget
        _color = shadingcolorproc.get_node_shading_color(engine)
        if _color:
            self.color_label.setStyleSheet("background-color: {}".format(_color))
        else:
            self.color_label.setStyleSheet("background-color: #9D9D9D")
        cmds.hyperShade(objects = engine)
        _objects = cmds.ls(sl = True)
        self.object_listwidget.clear()
        self.object_listwidget.addItems(_objects)

    def _select_objects(self):
        pass

    def _isolate(self, index):
        """ 只显示

        """
        _engine_name = index.data()
        cmds.hyperShade(objects = _engine_name) 