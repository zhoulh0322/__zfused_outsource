# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os
import json
import datetime
import logging

import zfused_api

logger = logging.getLogger(__name__)

DATABASE_PATH = os.path.dirname(os.path.dirname(__file__))
OUTPUT_DATABASE_FILE = "{}/database/step_attr_output.json".format(DATABASE_PATH)
with open(OUTPUT_DATABASE_FILE, 'r') as f:
    print("read")
    OUTPUT_DATABASE = json.load(f)


class OutputAttr(object):
    global_dict = {}

    def __init__(self, id, data=None):
        self.id = id
        self.data = data

        if not self.global_dict.__contains__(self.id):
            if self.data:
                self.global_dict[self.id] = self.data
            else:
                _data = None
                for _output in OUTPUT_DATABASE:
                    if id == _output["Id"]:
                        _data = _output
                if not _data:
                    logger.error("asset id {0} not exists".format(self.id))
                    return
                self.data = _data
                self.global_dict[self.id] = _data
        else:
            if self.data:
                self.global_dict[self.id] = self.data
            else:
                self.data = self.global_dict[self.id]

    def object(self):
        return "output_attr"

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

    def script(self):
        """
        get script

        rtype: str
        """
        return u"{}".format(self.data["Script"])

    def suffix(self):
        return self.data["Suffix"]