# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os
import json
import logging

import zfused_api

# read database
DATABASE_PATH = os.path.dirname(os.path.dirname(__file__))
STATUS_DATABASE_FILE = "{}/database/status.json".format(DATABASE_PATH)
PROJECT_STATUS_DATABASE_FILE = "{}/database/conn_project_status.json".format(DATABASE_PATH)
with open(STATUS_DATABASE_FILE, 'r') as f:
    print("read")
    STATUS_DATABASE = json.load(f)
with open(PROJECT_STATUS_DATABASE_FILE, 'r') as f:
    print("read")
    PROJECT_STATUS_DATABASE = json.load(f)

logger = logging.getLogger(__name__)


def active_status():
    """
    获取激活可制作的任务

    """
    _active_status = zfused_api.zFused.get("status", filter = {"IsActive":1}, sortby = ["Sort"], order = ["asc"])
    if _active_status:
        return [Status(_status["Id"]) for _status in _active_status]
    return []

def active_status_ids():
    """
    获取激活可制作的任务

    """
    _active_status = zfused_api.zFused.get("status", filter = {"IsActive":1}, sortby = ["Sort"], order = ["asc"])
    if _active_status:
        return [_status["Id"] for _status in _active_status]
    return []

def working_status():
    """
    获取制作中的状态标签

    """
    _woking_status = zfused_api.zFused.get("status", filter = {"IsWorking":1}, sortby = ["Sort"], order = ["asc"])
    if _woking_status:
        return [Status(_status["Id"]) for _status in _working_status]
    return []

def working_status_ids():
    """
    获取制作中的状态id
    """
    _woking_status = zfused_api.zFused.get("status", filter = {"IsWorking":1}, sortby = ["Sort"], order = ["asc"])
    if _woking_status:
        return [_status["Id"] for _status in _woking_status]
    return []

def final_status():
    """ 获取完结状态

    """
    _final_status = zfused_api.zFused.get("status", filter = {"IsFinal":1}, sortby = ["Sort"], order = ["asc"])
    if _final_status:
        return [Status(_status["Id"]) for _status in _final_status]
    return []

def final_status_ids():
    """ 获取完结状态

    """
    _final_status = zfused_api.zFused.get("status", filter = {"IsFinal":1}, sortby = ["Sort"], order = ["asc"])
    if _final_status:
        return [_status["Id"] for _status in _final_status]
    return []

def status_ids():
    """
    获取所有状态id
    """
    _status = zfused_api.zFused.get("status", sortby = ["Sort"], order = ["asc"])
    if _status:
        return [_statu["Id"] for _statu in _status]
    return []


class Status(object):
    global_dict = {}
    def __init__(self, id, data = None):
        self.id = id
        self.data = data

        if not self.global_dict.__contains__(self.id):
            if self.data:
                self.global_dict[self.id] = self.data
            else:
                _data = None
                for _status in STATUS_DATABASE:
                    if id == _status["Id"]:
                        _data = _status
                        break
                if not _data:
                    logger.error("status id {0} not exists".format(self.id))
                    return
                self.data = _data
                self.global_dict[self.id] = _data
        else:
            if self.data:
                self.global_dict[self.id] = self.data
            else:
                self.data = self.global_dict[self.id]

    def color(self):
        """ return project color

        """
        return self.data["Color"]

    def object(self):
        return "status"

    def code(self):
        """
        get code

        rtype: str
        """
        return u"{}".format(self.data["Code"])   

    def name(self):
        """
        get name

        rtype: str
        """
        return u"{}".format(self.data["Name"])

    def name_code(self):
        """
        get name code

        rtype: str
        """ 
        return u"{}({})".format(self.name(),self.code())

    def full_code(self):
        """
        get full path code

        rtype: str
        """
        return self.data["Code"]

    def full_name(self):
        """
        get full path name

        rtype: str
        """
        return self.data["Name"]


    def full_name_code(self):
        """
        get full path name and code

        rtype: str
        """
        return u"{}({})".format(self.full_name(), self.full_code())


    @classmethod
    def final_status_ids(cls):
        """ get final status ids

        """
        return 
