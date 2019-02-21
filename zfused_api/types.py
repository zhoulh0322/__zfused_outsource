# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os
import json
import logging

import zfused_api

# read database
DATABASE_PATH = os.path.dirname(os.path.dirname(__file__))
TYPE_DATABASE_FILE = "{}/database/type.json".format(DATABASE_PATH)
PROJECT_TYPE_DATABASE_FILE = "{}/database/conn_project_type.json".format(DATABASE_PATH)

with open(TYPE_DATABASE_FILE, 'r') as f:
    TYPE_DATABASE = json.load(f)
with open(PROJECT_TYPE_DATABASE_FILE, 'r') as f:
    PROJECT_TYPE_DATABASE = json.load(f)

logger = logging.getLogger(__name__)

def project_types(project_ids = []):
    """ get project steps

    """
    if not project_ids:
        return PROJECT_TYPE_DATABASE
    _types = []
    for _project_type in PROJECT_TYPE_DATABASE:
        if _project_type["ProjectId"] in project_ids:
            _types.append(_project_type)
    return _types


class Types(object):
    global_dict = {}

    def __init__(self, id, data=None):
        self.id = id
        self.data = data

        if not self.global_dict.__contains__(self.id):
            if self.data:
                self.global_dict[self.id] = self.data
            else:
                _data = None
                for _type in TYPE_DATABASE:
                    if id == _type["Id"]:
                        _data = _type
                if not _data:
                    logger.error("type id {0} not exists".format(self.id))
                    return
                self.data = _data
                self.global_dict[self.id] = _data
        else:
            if self.data:
                self.global_dict[self.id] = self.data
            else:
                self.data = self.global_dict[self.id]

    def object(self):
        return "type"

    def code(self):
        """get code

        :rtype: str
        """
        return u"{}".format(self.data["Code"])   

    def name(self):
        """get name

        :rtype: str
        """
        return u"{}".format(self.data["Name"])

    def name_code(self):
        """get name code

        :rtype: str
        """
        return u"{}({})".format(self.name(), self.code())