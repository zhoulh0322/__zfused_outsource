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
STEP_DATABASE_FILE = "{}/database/step.json".format(DATABASE_PATH)
PROJECT_STEP_DATABASE_FILE = "{}/database/conn_project_step.json".format(DATABASE_PATH)
STEP_INPUTATTR_DATABASE_FILE = "{}/database/step_attr_input.json".format(DATABASE_PATH)
STEP_OUTPUTATTR_DATABASE_FILE = "{}/database/step_attr_output.json".format(DATABASE_PATH)
with open(STEP_DATABASE_FILE, 'r') as f:
    print("read")
    STEP_DATABASE = json.load(f)
with open(PROJECT_STEP_DATABASE_FILE, 'r') as f:
    print("read")
    PROJECT_STEP_DATABASE = json.load(f)
with open(STEP_INPUTATTR_DATABASE_FILE, 'r') as f:
    print("read")
    STEP_INPUTATTR_DATABASE = json.load(f)
with open(STEP_OUTPUTATTR_DATABASE_FILE, 'r') as f:
    print("read")
    STEP_OUTPUTATTR_DATABASE = json.load(f)

logger = logging.getLogger(__name__)


def project_steps(project_ids = []):
    """ get project steps

    """
    if not project_ids:
        return PROJECT_STEP_DATABASE
    _steps = []
    for _project_step in PROJECT_STEP_DATABASE:
        if _project_step["ProjectId"] in project_ids:
            _steps.append(_project_step)
    return _steps

class ProjectStep(object):
    global_dict = {}
    def __init__(self, id, data = None):
        self.id = id
        self.data = data

        if not self.global_dict.__contains__(self.id):
            if self.data:
                self.global_dict[self.id] = self.data
            else:
                _data = None
                for _project_step in PROJECT_STEP_DATABASE:
                    if id == _project_step["Id"]:
                        _data = _project_step
                #_data = self.get("conn_project_step", filter = {"Id":self.id})
                if not _data:
                    logger.error("project step id {0} not exists".format(self.id))
                    return
                self.data = _data
                self.global_dict[self.id] = _data
        else:
            if self.data:
                self.global_dict[self.id] = self.data
            else:
                self.data = self.global_dict[self.id]

    def color(self):
        """ return step color
            step数据库需要增加color属性,调用project step color效率低
        """
        # get project step color
        _step_handle = Step(self.data["StepId"])
        return _step_handle.color()

    def object(self):
        return "project_step"

    def name(self):
        return self.data["Name"]

    def code(self):
        return self.data["Code"]

    def name_code(self):
        return u"{}({})".format(self.name(),self.code())

    def approvalto_user_ids(self):
        _apps = self.get("approval_user", filter = {"Object":"project_step", "LinkId":self.id})
        if not _apps:
            return []
        return [_app["UserId"] for _app in _apps]

    def cc_user_ids(self):
        _ccs = self.get("cc_user", filter = {"Object":"project_step", "LinkId":self.id})
        if not _ccs:
            return []
        return [_cc["UserId"] for _cc in _ccs]

    def add_approvalto_user(self, user_id):
        """添加审查人员

        :rtype: str
        """
        logger.info("add approval user {} to project step {}".format(user_id, self.id))
        _apps = self.get("approval_user", filter = {"Object":"project_step", "LinkId":self.id})
        if _apps:
            _app = _apps[0]
            print(_app)
            _app["UserId"] = user_id
            self.put("approval_user", _app["Id"], _app)
        else:
            self.post(key = "approval_user", data = {"Object": "project_step","LinkId": self.id, "UserId": user_id, "Sort": 0})

    def add_cc_user(self, user_id):
        """添加抄送人员

        :rtype: str
        """
        logger.info("add cc user {} to project step {}".format(user_id, self.id))
        _ccs = self.get("cc_user", filter = {"Object":"project_step", "LinkId":self.id})
        if _ccs:
            _cc = _ccs[0]
            _cc["UserId"] = user_id
            self.put("cc_user", _cc["Id"], _cc)
        else:
            self.post(key = "cc_user", data = {"Object": "project_step","LinkId": self.id, "UserId": user_id, "Sort": 0})


    def output_attrs(self):
        """获取输出属性
        
        :rtype: str
        """
        _attrs = []
        for _attr_output in STEP_OUTPUTATTR_DATABASE:
            if self.id == _attr_output["ProjectStepId"]:
                _attrs.append(_attr_output)
        return _attrs

    def key_output_attr(self):
        """ 获取主输出属性
                目前先按 file 为主属性，之后换成 is_key 关键字
        """
        for _attr_output in STEP_OUTPUTATTR_DATABASE:
            if self.id == _attr_output["ProjectStepId"]:
                if _attr_output["Code"] == "file":
                    return _attr_output
        return None

    def input_attrs(self):
        """获取输入属性
        
        :rtype: str
        """
        _attrs = []
        for _attr_output in STEP_INPUTATTR_DATABASE:
            if self.id == _attr_output["ProjectStepId"]:
                _attrs.append(_attr_output)
        return _attrs

    def check_script(self):
        """get check script 

        :rtype: str        
        """
        return self.data["CheckScript"]

    def update_check_script(self, script):
        """ update project step check script
        
        :param script: 检查脚本
        :rtype: bool
        """
        self.data["CheckScript"] = script
        v = self.put("conn_project_step", self.data["Id"], self.data)
        if v:
            return True
        else:
            return False


class Step(object):
    global_dict = {}
    def __init__(self, id, data = None):
        self.id = id
        self.data = data

        if not self.global_dict.__contains__(self.id):
            if self.data:
                self.global_dict[self.id] = self.data
            else:
                #_data = self.get("step", filter = {"Id":self.id})
                _data = None
                for _step in STEP_DATABASE:
                    if id == _step["Id"]:
                        _data = _step
                if not _data:
                    logger.error("step id {0} not exists".format(self.id))
                    return
                self.data = _data
                self.global_dict[self.id] = _data
        else:
            if self.data:
                self.global_dict[self.id] = self.data
            else:
                self.data = self.global_dict[self.id]

    def color(self):
        """ return project step color
        """
        return self.data["Color"]

    def object(self):
        return "step"

    def name(self):
        return self.data["Name"]

    def code(self):
        return self.data["Code"]

    def name_code(self):
        return u"{}({})".format(self.name(),self.code())