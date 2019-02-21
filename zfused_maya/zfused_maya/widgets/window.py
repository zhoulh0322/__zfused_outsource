# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

from qtpy import QtWidgets, QtGui, QtCore

import zfused_maya
import zfused_maya.interface as interface
import zfused_maya.core.resource as resource


class Window(QtWidgets.QMainWindow):
    PADDING = 0.8
    DIR = None

    def __init__(self, parent = None):
        super(Window, self).__init__(parent = interface.tomaya.GetMayaMainWindowPoint())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        self._base_build()

        self._is_press = False
        self._dir = None
        self._drag_position = QtCore.QPoint(0, 0)

        self.close_button.clicked.connect(self.close)

    def show(self):
        import zfused_maya.core.restricted as restricted
        import maya.cmds as cmds
        _has_per, _info = restricted.restricted()
        if not _has_per:
            cmds.confirmDialog(message = _info)
            return 
        super(Window, self).show()
        
    def set_title_name(self, name_text):
        self.title_label.setText(u"  ·  {}".format(name_text))

    def set_central_widget(self, widget):
        self.central_layout.addWidget(widget)

    def set_tail_widget(self, widget):
        self.tail_widget.setHidden(False)
        self.tail_layout.addWidget(widget)

    def _get_region(self, cursor):
        pt_lu = self.mapToParent(self.rect().topLeft())
        pt_rl = self.mapToParent(self.rect().bottomRight())
        x = cursor.x()
        y = cursor.y()
        ret_dir = None
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

        # 获得鼠标当前所处窗口的边界方向
        if pt_lu.x() + self.PADDING >= x and pt_lu.x() <= x and pt_lu.y() + self.PADDING >= y and pt_lu.y() <= y:
            # 左上角
            ret_dir = "LEFTUPPER"
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeFDiagCursor))
        elif x >= pt_rl.x() - self.PADDING and x <= pt_rl.x() and y >= pt_rl.y() - self.PADDING and y <= pt_rl.y():
            # 右下角
            ret_dir = "RIGHTLOWER"
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeFDiagCursor))

        elif x <= pt_lu.x() + self.PADDING and x >= pt_lu.x() and y >= pt_rl.y() - self.PADDING and y <= pt_rl.y():
            # 左下角
            ret_dir = "LEFTLOWER"
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeBDiagCursor))
        elif x <= pt_rl.x() and x >= pt_rl.x() - self.PADDING and y >= pt_lu.y() and y <= pt_lu.y() + self.PADDING:
            # 右上角
            ret_dir = "RIGHTUPPER"
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeBDiagCursor))
        elif x <= pt_lu.x() + self.PADDING and x >= pt_lu.x():
            # 左边
            ret_dir = "LEFT"
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        elif x <= pt_rl.x() + self.PADDING and x >= pt_rl.x() - self.PADDING:
            # 右边
            ret_dir = "RIGHT"
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        elif y >= pt_lu.y() and y <= pt_lu.y() + self.PADDING:
            # 上边
            ret_dir = "UPPER"
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        elif y <= pt_rl.y() and y >= pt_rl.y() - self.PADDING:
            # 下边
            ret_dir = "LOWER"
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        else:
            ret_dir = None
            self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        
        return ret_dir

    def handleMousePressEvent(self, event):
        super(Window, self).mousePressEvent(event)
        self._is_press = True
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.pos()
            event.accept()

    def handleMouseReleaseEvent(self, event):
        super(Window, self).mouseReleaseEvent(event)
        self._is_press = False
        self.rect_ = None
        self._dir = None
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        event.accept()

    def leaveEvent(self, event):
        super(Window, self).leaveEvent(event)
        self._is_press = False
        self.rect_ = None
        self._dir = None
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def _recalculate(self, event):
        self._dir = None
        self.rect_ = None
        self._is_press = False

    def eventFilter(self, obj, event):
        if obj == self.widget:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self.handleMousePressEvent(event)
                return False
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                self.handleMouseReleaseEvent(event)
                return False
            elif event.type() == QtCore.QEvent.MouseMove:
                self.handleMouseMoveEvent(event)
                return False
            else:
                return False
        else:
            self._recalculate(event)
            return super(Window, self).eventFilter(obj, event)

    def handleMouseMoveEvent(self, event):
        gloPoint = self.mapToParent(event.pos())
        self.rect_ = self.rect()
        if not self._is_press:
            self.originPoint_ = self.mapToParent(self.rect().topLeft())
            self.originPoint_lu = self.mapToParent(self.rect().topLeft())
            self.originPoint_ll = self.mapToParent(self.rect().bottomLeft())
            self.originPoint_ru = self.mapToParent(self.rect().topRight())
            self.originPoint_rl = self.mapToParent(self.rect().bottomRight())
            self._dir = self._get_region(gloPoint)
        else:
            if event.buttons() == QtCore.Qt.LeftButton:
                global_x = gloPoint.x()
                global_y = gloPoint.y()
                if self._dir == None:
                    self.move(event.globalPos() - self.dragPosition)
                    event.accept()
                elif self._dir == "LEFT":
                    self.setGeometry(global_x,self.originPoint_lu.y(),abs(global_x - self.originPoint_rl.x()),self.rect_.height())
                elif self._dir == "RIGHT":
                    self.setGeometry(self.originPoint_lu.x(),self.originPoint_lu.y(),abs(global_x - self.originPoint_lu.x()),self.rect_.height())
                elif self._dir == "UPPER":
                    self.setGeometry(self.originPoint_lu.x(),global_y,self.rect_.width(),abs(global_y - self.originPoint_rl.y()))
                elif self._dir == "LOWER":
                    self.setGeometry(self.originPoint_lu.x(),self.originPoint_lu.y(),self.rect_.width(),abs(global_y - self.originPoint_lu.y()))
                elif self._dir == "LEFTUPPER":
                    self.setGeometry(global_x, global_y, self.originPoint_rl.x() - global_x, self.originPoint_rl.y() - global_y)
                elif self._dir == "LEFTLOWER":
                    self.setGeometry(global_x, self.originPoint_lu.y(), self.originPoint_rl.x() - global_x, - self.originPoint_ru.y() + global_y)
                elif self._dir == "RIGHTUPPER":
                    self.setGeometry(self.originPoint_lu.x(), global_y, global_x - self.originPoint_lu.x(), self.originPoint_rl.y() - global_y)
                elif self._dir == "RIGHTLOWER":
                    self.setGeometry(self.originPoint_lu.x(), self.originPoint_lu.y(), global_x - self.originPoint_lu.x(), global_y - self.originPoint_lu.y())
        return super(Window, self).mouseMoveEvent(event)

    def set_message(self, level, message):
        """
        write message

        """
        pass

    def _base_build(self):
        self.resize(1200,600)
        self.widget = QtWidgets.QFrame()
        self.widget.setObjectName("widget")
        self.widget.setMouseTracking(True)
        self.widget.installEventFilter(self)
        self.layout = QtWidgets.QVBoxLayout(self.widget)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(6, 6, 6, 6)
        self.setCentralWidget(self.widget)

        # title widget
        self.title_widget = QtWidgets.QFrame()
        self.title_widget.setObjectName("title_widget")
        self.title_widget.setMinimumHeight(40)
        self.title_widget.setMaximumHeight(40)
        self.title_layout = QtWidgets.QHBoxLayout(self.title_widget)
        self.title_layout.setSpacing(0)
        self.title_layout.setContentsMargins(0, 0, 5, 0)

        # logo
        self.logo_button = QtWidgets.QPushButton()
        self.logo_button = QtWidgets.QPushButton()
        self.logo_button.setFlat(True)
        self.logo_button.setIcon(QtGui.QIcon(resource.get("icons", "logo.png")))
        self.logo_button.setObjectName("logo_button")
        #self.logo_button.setEnabled(False)
        # self.logo_button.setText(u"星龙传媒")
        self.title_layout.addWidget(self.logo_button)
        #self.title_layout.addStretch(True)
        
        #  name frame
        self.name_widget = QtWidgets.QWidget()
        # self.name_widget.setMinimumHeight(30)
        self.title_layout.addWidget(self.name_widget)
        self.name_layout = QtWidgets.QHBoxLayout(self.name_widget)
        self.name_layout.setContentsMargins(0, 0, 0, 0)
        self.name_button = QtWidgets.QPushButton()
        self.name_button.setObjectName("name_button")
        self.name_button.setFlat(True)
        #self.name_button.setEnabled(False)
        self.name_button.setIcon(QtGui.QIcon(resource.get("icons", "z_title.png")))
        self.name_button.setText("zFused for maya {}".format(zfused_maya.version()))
        self.name_layout.addWidget(self.name_button)
        
        # title label
        self.title_label = QtWidgets.QPushButton()
        self.title_label.setFlat(True)
        #self.title_label.setIcon(QtGui.QIcon(resource.get("icons", "z_title.png")))
        self.title_label.setObjectName("title_button")
        self.title_label.setText("Title Name")
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addStretch(True)

        # close frame
        self.close_widegt = QtWidgets.QWidget()
        self.title_layout.addWidget(self.close_widegt)
        self.close_layout = QtWidgets.QHBoxLayout(self.close_widegt)
        self.close_layout.setContentsMargins(0, 0, 0, 0)
        self.min_button = _Button(self.close_widegt, resource.get("icons", "minimize.png"), 
                                                     resource.get("icons", "minimize_hover.png"), 
                                                     resource.get("icons", "minimize_hover.png"))
        self.min_button.setObjectName("min_button")
        self.min_button.setFlat(True)
        self.min_button.setMaximumSize(15, 15)
        self.min_button.setMinimumSize(15, 15)
        self.max_button = _Button(self.close_widegt, resource.get("icons", "maximize.png"), 
                                                     resource.get("icons", "maximize_hover.png"), 
                                                     resource.get("icons", "maximize_hover.png"))
        self.max_button.setObjectName("max_button")
        self.max_button.setFlat(True)
        self.max_button.setMinimumSize(15, 15)
        self.max_button.setMaximumSize(15, 15)
        self.close_button = _Button(self.close_widegt, resource.get("icons", "close.png"), 
                                                     resource.get("icons", "close_hover.png"), 
                                                     resource.get("icons", "close_hover.png"))
        self.close_button.setObjectName("close_button")
        self.close_button.setFlat(True)
        self.close_button.setMinimumSize(15, 15)
        self.close_button.setMaximumSize(15, 15)
        self.close_layout.addWidget(self.min_button)
        self.close_layout.addWidget(self.max_button)
        self.close_layout.addWidget(self.close_button)

        # central widget
        self.central_widget = QtWidgets.QFrame()
        self.central_widget.setObjectName("central_widget")
        self.central_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.central_layout.setSpacing(0)
        self.central_layout.setContentsMargins(0, 0, 0, 0)

        # tail widget
        self.tail_widget = QtWidgets.QFrame()
        self.tail_widget.setHidden(True)
        self.tail_widget.setMinimumHeight(40)
        self.tail_widget.setMaximumHeight(60)
        self.tail_widget.setObjectName("tail_widget")
        self.tail_layout = QtWidgets.QHBoxLayout(self.tail_widget)
        self.tail_layout.setSpacing(0)
        self.tail_layout.setContentsMargins(0,0,0,0)

        self.layout.addWidget(self.title_widget)
        self.layout.addWidget(self.central_widget)
        self.layout.addWidget(self.tail_widget)

        _qss = resource.get("qss", "ui/window.qss")
        with open(_qss) as f:
            qss = f.read()
            self.setStyleSheet(qss)


class _Button(QtWidgets.QPushButton):
    def __init__(self, parent=None, normal_icon=None, hover_icon=None, pressed_icon=None):
        super(_Button, self).__init__(parent)
        self._normal_icon = QtGui.QIcon(normal_icon)
        self._hover_icon = QtGui.QIcon(hover_icon)
        self._pressed_icon = QtGui.QIcon(pressed_icon)

        self.setMouseTracking(True)
        self.setIcon(self._normal_icon)

    def enterEvent(self, event):
        super(_Button, self).enterEvent(event)
        self.setIcon(self._hover_icon)

    def leaveEvent(self, event):
        super(_Button, self).leaveEvent(event)
        self.setIcon(self._normal_icon)

    def mousePressEvent(self, event):
        super(_Button, self).mousePressEvent(event)
        self.setIcon(self._pressed_icon)

    def mouseReleaseEvent(self, event):
        super(_Button, self).mouseReleaseEvent(event)
        self.setIcon(self._normal_icon)