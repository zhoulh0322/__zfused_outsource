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
PROJECT_DATABASE_FILE = "{}/database/project.json".format(DATABASE_PATH)
PROJECT_CONFIG_DATABASE_FILE = "{}/database/project_config.json".format(DATABASE_PATH)
PROJECT_PROFILE_DATABASE_FILE = "{}/database/project_profile.json".format(DATABASE_PATH)



with open(PROJECT_DATABASE_FILE, 'r') as f:
    print("read")
    PROJECT_DATABASE = json.load(f)
with open(PROJECT_CONFIG_DATABASE_FILE, 'r') as f:
    print("read")
    PROJECT_CONFIG_DATABASE = json.load(f)
with open(PROJECT_PROFILE_DATABASE_FILE, 'r') as f:
    print("read")
    PROJECT_PROFILE_DATABASE = json.load(f)

def all_projects():
    """ get all projects
    """
    return PROJECT_DATABASE


logger = logging.getLogger(__name__)


class Project(object):
    global_dict = {}
    config_dict = {}
    profile_dict = {}

    def __init__(self, id, data = None, config = None, profile = None):
        self.id = id
        self.data = data
        self.config = config
        self.profile = profile

        if not self.global_dict.__contains__(self.id):
            _datas = None
            for _project in PROJECT_DATABASE:
                if id == _project["Id"]:
                    _datas = _project
                    break
            if not _datas:
                logger.error("project id {0} is not exists".format(self.id))
                return
            self.data = _datas
            _profiles = None
            for _project_profile in PROJECT_PROFILE_DATABASE:
                if id ==  _project_profile["ProjectId"]:
                    _profiles = _project_profile
                    break
            if not _profiles:
                logger.error("project id {0} is not exists".format(self.id))
                return
            self.profile = _profiles
            _configs = None
            for _project_config in PROJECT_CONFIG_DATABASE:
                if id == _project_config["ProjectId"]:
                    _configs = _project_config
                    break
            if not _configs:
                logger.error("project id {0} is not exists".format(self.id))
                return
            self.config = _configs
            self.global_dict[self.id] = self.data
            self.profile_dict[self.id] = self.profile
            self.config_dict[self.id] = self.config
        else:
            self.data = self.global_dict[self.id]
            self.profile = self.profile_dict[self.id]
            self.config = self.config_dict[self.id]

    def color(self):
        """ return project color

        """
        return self.profile["Color"]

    def object(self):
        return "project"

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

    def full_code(self):
        """get full path code

        :rtype: str
        """
        return u"{}".format(self.data["Code"])

    def full_name(self):
        """get full path name

        :rtype: str
        """
        return u"{}".format(self.data["Name"])

    def full_name_code(self):
        """get full path name and code

        :rtype: str
        """
        return u"{}({})".format(self.full_name(), self.full_code())

    def status_id(self):
        """ get status id 
        
        """
        return self.data["StatusId"]

    def start_time(self):
        """
        get start time

        rtype: datetime.datetime
        """
        _time_text = self.profile["StartTime"]
        if _time_text.startswith("0001"):
            return None
        _time_text = _time_text.split("+")[0].replace("T", " ")
        return datetime.datetime.strptime(_time_text, "%Y-%m-%d %H:%M:%S")

    def end_time(self):
        """ get end time

        rtype: datetime.datetime
        """
        _time_text = self.profile["EndTime"]
        if _time_text.startswith("0001"):
            return None
        _time_text = _time_text.split("+")[0].replace("T", " ")
        return datetime.datetime.strptime(_time_text, "%Y-%m-%d %H:%M:%S")

    def project_step_ids(self):
        """ get asset task step id

        :rtype: list
        """
        _steps = self.get("conn_project_step", 
                          filter = {"ProjectId": self.id},
                          sortby = ["Sort"], order = ["asc"])
        if _steps:
            return [_step["Id"] for _step in _steps]
        return []

    def task_step_ids(self, object):
        """ get task step id by object

        :rtype: list
        """
        _project_steps = zfused_api.step.project_steps()
        #_steps = self.get("conn_project_step", 
        #                  filter = {"ProjectId": self.id, "Object": object},
        #                  sortby = ["Sort"], order = ["asc"])
        _steps = []
        if _project_steps:
            for _step in _project_steps:
                if _step["Object"] == object:
                    _steps.append(_step["Id"])
        return _steps

    def asset_type_ids(self):
        """get asset type

        :rtype: list
        """
        _project_types = zfused_api.types.project_types([self.id])
        #_types = self.get("conn_project_type", filter = {"ProjectId": self.id}) 
        if _project_types:
            return [_type["TypeId"] for _type in _project_types]
        return []

    def assembly_attributes(self):
        """ get is assembly attrs
        
        :rtype: list
        """
        _steps = self.get("conn_project_step", filter = {"ProjectId": self.id})
        if not _steps:
            return []
        _step_ids = [str(_step["Id"]) for _step in _steps]
        _attrs = self.get("step_attr_output", filter = {"ProjectStepId__in": "|".join(_step_ids),
                                                        "IsAssembly__gte": 1},
                                              sortby = ["IsAssembly"], order = ["desc"])

        if not _attrs:
            return []
        return _attrs

    def assembly_attribute_ids(self):
        """ get is assembly attr ids
        
        :rtype: list
        """
        _steps = self.get("conn_project_step", filter = {"ProjectId": self.id})
        if not _steps:
            return []
        _step_ids = [str(_step["Id"]) for _step in _steps]
        _attrs = self.get("step_attr_output", filter = {"ProjectStepId__in": "|".join(_step_ids),
                                                        "IsAssembly__gte": 1},
                                              sortby = ["IsAssembly"], order = ["desc"])

        if not _attrs:
            return []
        return [_attr["Id"] for _attr in _attrs]
