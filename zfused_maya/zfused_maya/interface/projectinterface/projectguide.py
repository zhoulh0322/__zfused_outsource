# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

from qtpy import QtWidgets, QtCore

import zfused_maya.interface.tomaya as tomaya
import projectframe
import taskframe
import zfused_maya.interface.menuinterface.menuframe as menuframe
import projectlistpanel
import tasklistpanel

class ProjectGuide(QtWidgets.QMainWindow):
    def __init__(self):
        super(ProjectGuide, self).__init__(parent = tomaya.GetMayaMainWindowPoint())
        self._build()

        self.project_frame.projectlist_button.clicked.connect(self._show_project_list_panel)
        # self.task_frame.tasklist_button.clicked.connect(self._show_task_list_panel)
        self.project_list_panel.project_list_widget.doubleClicked.connect(self.update)

    def _show_project_list_panel(self):
        """ show and move project_list_widget

        :rtype: None
        """
        self.project_list_panel.show()
        self.project_list_panel.load_config()
        # set geometry
        _button_pos = self.project_frame.projectlist_button.pos()
        _button_pos = self.project_frame.mapTo(self, _button_pos)
        _button_height = self.project_frame.projectlist_button.height()
        _glo_pos = self.mapTo(tomaya.GetMayaMainWindowPoint(), _button_pos)
        self.project_list_panel.setGeometry(_glo_pos.x(), _glo_pos.y() + _button_height, self.width()*1/2.0, tomaya.GetMayaMainWindowPoint().height()*1/2.0)

    def _show_task_list_panel(self):
        """ show and move task list widget

        :rtype: None
        """
        self.task_list_panel.show()
        self.task_list_panel.load_config()
        # set geometry
        _button_pos = self.task_frame.tasklist_button.pos()
        _button_pos = self.task_frame.mapTo(self, _button_pos)
        _button_height = self.task_frame.tasklist_button.height()
        _glo_pos = self.mapTo(tomaya.GetMayaMainWindowPoint(), _button_pos)
        self.task_list_panel.setGeometry(_glo_pos.x(), _glo_pos.y() + _button_height, self.task_frame.width(), tomaya.GetMayaMainWindowPoint().height()*1/2.0)

    def _build(self):
        self.setObjectName("project_interface")
        self.setMaximumHeight(20)
        self.main_frame = QtWidgets.QFrame()
        self.setCentralWidget(self.main_frame)
        self.main_layout = QtWidgets.QHBoxLayout(self.main_frame)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)

        #self.main_layout.addStretch(True)

        # project frame
        self.project_frame = projectframe.ProjectFrame(self)

        # project list panel
        self.project_list_panel = projectlistpanel.projectlistpanel.ProjectListPanel()

        # task frame
        self.task_frame = taskframe.TaskFrame(self)
        
        # menu list frame
        # self.task_list_panel = tasklistpanel.TaskListPanel()

        # menu frame
        self.menu_frame = menuframe.MenuFrame()

        self.main_layout.addWidget(self.project_frame)
        self.main_layout.addWidget(self.task_frame)
        self.main_layout.addWidget(self.menu_frame)

        