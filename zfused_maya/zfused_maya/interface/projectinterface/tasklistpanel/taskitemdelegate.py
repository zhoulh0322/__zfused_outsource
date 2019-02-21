# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import datetime
import logging

from qtpy import QtWidgets, QtGui, QtCore

import zfused_api
import zfused_maya.core.color as color

import constants

__all__ = ["TaskItemDelegate"]

logger = logging.getLogger(__name__)


class _ThumbnailThread(QtCore.QThread):
    exec_ = False
    def __init__(self, parent=None):
        super(_ThumbnailThread, self).__init__(parent)

        self._parent = parent
        self._handle = None

    def load_thumbnail(self, handle, index):
        self._handle = handle
        self._object_handle = zfused_api.objects.Objects(handle.data["Object"], handle.data["LinkId"])
        self._index = index
        self.start()

    def run(self):
        self._parent.THUMBNAIL[self._handle.data["Id"]] = None
        if self._handle.data:
            _thumbnail = self._object_handle.get_thumbnail()
            if not _ThumbnailThread.exec_:
                self._parent.THUMBNAIL[self._handle.data["Id"]] = _thumbnail
                self._parent.parent().update(self._index)
        self.quit()


class TaskItemDelegate(QtWidgets.QStyledItemDelegate):
    THUMBNAIL_PIXMAP = {}
    THUMBNAIL = {}

    def __init__(self, parent=None):
        super(TaskItemDelegate, self).__init__(parent)

        self._spacing = 2
        self._extend_width = 10

        _ThumbnailThread.exec_ = False

    def __del__(self):
        _ThumbnailThread.exec_ = True

    def paint(self, painter, option, index):
        _data = index.data()
        _id = _data["Id"]
        _task_handle = zfused_api.task.Task(_id, _data)
        _name = _task_handle.full_name_code().replace("/","_")

        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        _rect = option.rect
        _pen = QtGui.QPen(QtGui.QColor(constants.Constants.INFO_TEXT_COLOR), 0.1)
        painter.setPen(_pen)
        painter.setBrush(QtGui.QColor(constants.Constants.INFO_BACKGROUND_COLOR))
        painter.drawRoundedRect(option.rect, 0, 0)

        # painter thumbnail
        _thumbnail_pixmap = None
        if self.THUMBNAIL_PIXMAP.has_key(_id):
            _thumbnail_pixmap = self.THUMBNAIL_PIXMAP[_id]
        else:
            if self.THUMBNAIL.has_key(_id):
                _thumbnail = self.THUMBNAIL[_id]
                if _thumbnail:
                    _pixmap = QtGui.QPixmap(_thumbnail)
                    #_pixmap = QtGui.QImageReader(_thumbnail)
                    _pixmap_size = _pixmap.size()
                    if _pixmap_size.width() and _pixmap_size.height():
                        _label_size = QtCore.QSize(constants.Constants.THUMBNAIL_SIZE[0], 
                                                   constants.Constants.THUMBNAIL_SIZE[1])
                        scale = max(float(_label_size.width() / float(_pixmap_size.width())),
                                    float(_label_size.height()) / float(_pixmap_size.height()))
                        _pixmap = _pixmap.scaled(
                            _pixmap_size.width() * scale, _pixmap_size.height() * scale)
                        #_pixmap = _pixmap.setScaledSize(QtCore.QSize(_pixmap_size.width()*scale, _pixmap_size.height()*scale))
                        _thumbnail_pixmap = _pixmap.copy((_pixmap_size.width() * scale - _label_size.width()) / 2.0, (_pixmap_size.height(
                        ) * scale - _label_size.height()) / 2.0, _label_size.width(), _label_size.height())
                        #_thumbnail_pixmap = _pixmap
                        self.THUMBNAIL_PIXMAP[_id] = _thumbnail_pixmap
            else:
                _thumbnail_load = _ThumbnailThread(self)
                _thumbnail_load.load_thumbnail(_task_handle, index)

        if _thumbnail_pixmap:
            painter.drawPixmap(_rect.x(), _rect.y(), _thumbnail_pixmap)
        else:
            _thumbnail_rect = QtCore.QRect(_rect.x(), _rect.y(), 
                                           constants.Constants.THUMBNAIL_SIZE[0], 
                                           constants.Constants.THUMBNAIL_SIZE[1])
            painter.setBrush(QtGui.QColor(color.LetterColor.color(_data["Name"].lower()[0])))
            painter.drawRoundedRect(_thumbnail_rect, 1, 1)
            painter.setPen(QtGui.QPen(QtGui.QColor(
                0, 0, 0, 255), 0.2, QtCore.Qt.DashLine))
            painter.drawRoundedRect(_thumbnail_rect, 1, 1)

        # info widget
        _info_rect = QtCore.QRect(
                _rect.x() + constants.Constants.THUMBNAIL_SIZE[0],
                _rect.y(),
                _rect.width() - constants.Constants.THUMBNAIL_SIZE[0],
                _rect.height()
            )
        #  painter status rect
        _status_rect = QtCore.QRect(
                _info_rect.x(),
                _info_rect.y(),
                _info_rect.width(),
                5
            )
        _status_id = _task_handle.data["StatusId"]
        _status_handle = zfused_api.status.Status(_status_id)
        painter.setBrush(QtGui.QColor(_status_handle.data["Color"]))
        painter.drawRoundedRect(_status_rect, 0, 0)
        
        #  绘制任务名
        _font = QtGui.QFont("Microsoft YaHei UI", 9)
        _font.setPixelSize(12)
        _font.setBold(True)
        _fm = QtGui.QFontMetrics(_font)
        painter.setFont(_font)
        painter.setPen(QtGui.QPen(QtGui.QColor(constants.Constants.INFO_TEXT_COLOR), 1))
        _name_code = _task_handle.data["Name"]
        _name_rect = QtCore.QRect(
                _status_rect.x() + self._extend_width,
                _status_rect.y() + _status_rect.height() + self._spacing,
                _fm.width(_name_code) + self._extend_width,
                20
            )
        painter.drawText(_name_rect, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter, _name_code)
        #  绘制任务状态
        _status_handle = zfused_api.status.Status(_task_handle.data["StatusId"])
        _status_code = _status_handle.name_code()
        _status_rect = QtCore.QRect(
                #_name_rect.x() + _name_rect.width() + self._extend_width,
                _rect.x() + _rect.width() - _fm.width(_status_code) - self._extend_width -self._spacing,
                _name_rect.y() + self._spacing,
                _fm.width(_status_code) + self._extend_width,
                20 - self._spacing*2
            )
        painter.setPen(QtGui.QPen(QtGui.QColor(0,0,0,0), 1))
        painter.setBrush(QtGui.QColor(_status_handle.data["Color"]))
        painter.drawRoundedRect(_status_rect, 2, 2)
        painter.setPen(QtGui.QPen(QtGui.QColor("#FFFFFF"), 1))
        painter.drawText(_status_rect, QtCore.Qt.AlignCenter, _status_code)
        #  绘制任务时间

        # 绘制link
        _link_handle = zfused_api.objects.Objects(_task_handle.data["Object"], _task_handle.data["LinkId"])
        _project_handle = zfused_api.project.Project(_task_handle.data["ProjectId"])
        if _task_handle.data["Object"] == "asset":
            _link_full_name = _link_handle.full_name()
            _link_full_name = u"{}/{}".format(_project_handle.name(),_link_full_name)
        else:
            _link_full_name = _link_handle.full_code()
            _link_full_name = u"{}/{}".format(_project_handle.code(),_link_full_name)
        _link_rect = QtCore.QRect(
                _name_rect.x(),
                _name_rect.y() + _name_rect.height() + self._spacing,
                _fm.width(_link_full_name),
                20
            )
        painter.setPen(QtGui.QPen(QtGui.QColor(constants.Constants.INFO_TEXT_COLOR), 1))
        painter.drawText(_link_rect, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter, _link_full_name)
        
        #  绘制任务步骤
        _project_step_handle = zfused_api.step.ProjectStep(_task_handle.data["ProjectStepId"])
        _step_handle = zfused_api.step.Step(_task_handle.data["StepId"])
        _step_code = _project_step_handle.name_code()
        _step_rect = QtCore.QRect(
                _link_rect.x() + _link_rect.width() + self._extend_width,
                _link_rect.y() + self._spacing,
                _fm.width(_step_code) + self._extend_width,
                20 - self._spacing*2
            )
        painter.setPen(QtGui.QPen(QtGui.QColor(0,0,0,0), 1))
        painter.setBrush(QtGui.QColor(_step_handle.data["Color"]))
        painter.drawRoundedRect(_step_rect, 2, 2)
        painter.setPen(QtGui.QPen(QtGui.QColor("#FFFFFF"), 1))
        painter.drawText(_step_rect, QtCore.Qt.AlignCenter, _step_code)

        #  绘制时间
        _font = QtGui.QFont("Microsoft YaHei UI", 9)
        _font.setPixelSize(12)
        #_font.setBold(True)
        _fm = QtGui.QFontMetrics(_font)
        painter.setFont(_font)
        try:
            _start_time_text = _task_handle.start_time().strftime("%Y-%m-%d")
        except:
            _start_time_text = u"未设置起始时间"
        try:
            _end_time_text = _task_handle.end_time().strftime("%Y-%m-%d")
        except:
            _end_time_text = u"未设置结束时间"
        _time_rect = QtCore.QRect(
                _link_rect.x(),
                _link_rect.y() + _link_rect.height() + self._spacing,
                _info_rect.width() - self._extend_width*2,
                20
            )
        painter.setPen(QtGui.QPen(QtGui.QColor(constants.Constants.INFO_TEXT_COLOR), 1))
        painter.drawText(_time_rect, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter, u"{}".format(_start_time_text))
        painter.drawText(_time_rect, QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter, u"{}".format(_end_time_text))

        if _task_handle.start_time() and _task_handle.end_time():
            _time_progress_x = _time_rect.x()
            _time_progress_y = _time_rect.y() + _time_rect.height()
            _time_progress_width = _time_rect.width()
            _time_progress_height = 3
            painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 0), 1))
            painter.setBrush(QtGui.QColor("#5C5C5C"))
            painter.drawRoundedRect(_time_progress_x, _time_progress_y, _time_progress_width, _time_progress_height, 2, 2)
            if not _task_handle.start_time() > datetime.datetime.now():
                _use_date = _task_handle.end_time() - datetime.datetime.now()
                if _use_date.days <= 0:
                    _use_time_width = _time_progress_width
                else:
                    _all_date = _task_handle.end_time() - _task_handle.start_time()
                    _use_per = _use_date.days/float(_all_date.days)
                    _use_time_width = _time_progress_width * _use_per
                painter.setBrush(QtGui.QColor("#FF0000"))
                painter.drawRoundedRect(_time_progress_x, _time_progress_y, _use_time_width, _time_progress_height, 2, 2)

        if option.state & QtWidgets.QStyle.State_MouseOver:
            bgBrush = QtGui.QBrush(QtGui.QColor(200, 200, 200, 150))
            bgPen = QtGui.QPen(QtGui.QColor(60, 60, 60, 0), 0)
            painter.setPen(bgPen)
            painter.setBrush(bgBrush)
            painter.drawRect(option.rect)
        elif option.state & QtWidgets.QStyle.State_Selected:
            bgBrush = QtGui.QBrush(QtGui.QColor(149, 194, 197, 150))
            bgPen = QtGui.QPen(QtGui.QColor(160, 60, 60, 0), 0)
            painter.setPen(bgPen)
            painter.setBrush(bgBrush)
            painter.drawRect(option.rect)
        else:
            bgBrush = QtGui.QBrush(QtGui.QColor(200, 200, 200, 0))
            bgPen = QtGui.QPen(QtGui.QColor(160, 60, 60, 0), 0)
            painter.setPen(bgPen)
            painter.setBrush(bgBrush)
            painter.drawRect(option.rect)
        
        painter.restore()

    def sizeHint(self, option, index):
        return QtCore.QSize(constants.Constants.ITEM_DELEGATE_SIZE[0], constants.Constants.ITEM_DELEGATE_SIZE[1])
