# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os
import json
import datetime
import logging

import zfused_api

# read database
DATABASE_PATH = os.path.dirname(os.path.dirname(__file__))
SOFTWARE_DATABASE_FILE = "{}/database/software.json".format(DATABASE_PATH)

with open(SOFTWARE_DATABASE_FILE, 'r') as f:
    SOFTWARE_DATABASE_ = json.load(f)


logger = logging.getLogger(__name__)


class Software(object):
    global_dict = {}

    def __init__(self, id, data = None):
        self.id = id
        self.data = data

        if not self.global_dict.__contains__(self.id):
            _datas = None
            for _software in SOFTWARE_DATABASE_:
                if id == _software["Id"]:
                    _datas = _software
                    break
            if not _datas:
                logger.error("project id {0} is not exists".format(self.id))
                return
            self.data = _datas
            self.global_dict[self.id] = self.data

        else:
            self.data = self.global_dict[self.id]

    def object(self):
        return "software"

    def code(self):
        """ get software code

        rtype: str
        """
        return u"{}{}".format(self.data["Code"], self.data["Version"])   

    def name(self):
        """ get software name

        rtype: str
        """
        return u"{}{}".format(self.data["Name"], self.data["Version"])   

    def version(self):
        """ get software version number

        """
        return self.data["Version"]