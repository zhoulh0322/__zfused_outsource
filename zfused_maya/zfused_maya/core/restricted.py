# coding:utf-8
# --author-- lanhua.zhou

"""
    限制登陆使用zfused_outsource
        无项目不允许使用
        项目接制时候后不允许使用

"""

from __future__ import print_function

import sys
import datetime
import time

import zfused_api

from . import record



def restricted():
    """
    """
    # get project id
    # 
    _project_id = record.current_project_id()
    if not _project_id:
        return False, u"请选择pipeline项目"

    _project_handle = zfused_api.project.Project(_project_id)

    # 
    _end_time = _project_handle.end_time()

    _current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _current_time = datetime.datetime.strptime(_current_time, "%Y-%m-%d %H:%M:%S")

    if _end_time < _current_time:
        return False, u"无权限使用"

    return True, ""