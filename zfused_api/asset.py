# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os
import json
import datetime
import shutil
import logging

import zfused_api

# read database
DATABASE_PATH = os.path.dirname(os.path.dirname(__file__))
ASSET_DATABASE_FILE = "{}/database/asset.json".format(DATABASE_PATH)
with open(ASSET_DATABASE_FILE, 'r') as f:
    print("read")
    ASSET_DATABASE = json.load(f)

logger = logging.getLogger(__name__)


def project_assets(project_ids = []):
    """ get project assets
    """
    if not project_ids:
        return ASSET_DATABASE
    _all_assets = []
    for _asset in ASSET_DATABASE:
        if _asset["ProjectId"] in project_ids:
            _all_assets.append(_asset)
    return _all_assets


class Asset(object):
    global_dict = {}
    task_dict = {}
    def __init__(self, id, data = None):
        self.id = id
        self.data = data

        if not self.global_dict.__contains__(self.id):
            if self.data:
                self.global_dict[self.id] = self.data
            else:
                _data = None
                for _asset in ASSET_DATABASE:
                    if id == _asset["Id"]:
                        _data = _asset
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

    @classmethod
    def reset(cls):
        cls.task_dict = {}
        cls.global_dict = {}

    def object(self):
        return "asset"

    def id(self):
        return self.id

    def description(self):
        return self.data["Description"]

    def file_code(self):
        """ task version file name

        :rtype: str
        """
        return self.code().replace("/", "_")

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
        return u"{}({})".format(self.name(), self.code())

    def full_code(self):
        """
        get full path code

        rtype: str
        """
        _code = self.data["Code"]
        if self.data["TypeId"]:
            _step_code = zfused_api.types.Types(self.data["TypeId"]).data["Code"]
            return u"{}/{}".format(_step_code, _code)
        else:
            return _code

    def full_name(self):
        """
        get full path name

        rtype: str
        """
        _name = self.data["Name"]
        if self.data["TypeId"]:
            _step_name = zfused_api.types.Types(self.data["TypeId"]).data["Name"]
            return u"{}/{}".format(_step_name, _name)
        else:
            return _name

    def full_name_code(self):
        """
        get full path name and code

        rtype: str
        """
        return u"{}({})".format(self.full_name(), self.full_code())

    def project_id(self):
        """ get project id

        """
        return self.data["ProjectId"]

    def status_id(self):
        """ get status id 
        
        """
        return self.data["StatusId"]

    def start_time(self):
        """ get start time

        rtype: datetime.datetime
        """
        _time_text = self.data["StartTime"]
        if _time_text.startswith("0001"):
            return None
        _time_text = _time_text.split("+")[0].replace("T", " ")
        return datetime.datetime.strptime(_time_text, "%Y-%m-%d %H:%M:%S")

    def end_time(self):
        """ get end time

        rtype: datetime.datetime
        """
        _time_text = self.data["EndTime"]
        if _time_text.startswith("0001"):
            return None
        _time_text = _time_text.split("+")[0].replace("T", " ")
        return datetime.datetime.strptime(_time_text, "%Y-%m-%d %H:%M:%S")

    def create_time(self):
        """ get create time

        """
        _time_text = self.data["CreateTime"]
        if _time_text.startswith("0001"):
            return None
        _time_text = _time_text.split("+")[0].replace("T", " ")
        return datetime.datetime.strptime(_time_text, "%Y-%m-%d %H:%M:%S")

    def production_path(self):
        """ get asset production path

        rtype: str
        """
        _production_project_path = zfused_api.project.Project(
            self.data["ProjectId"]).config["Root"]
        _path = "{}/asset/{}".format(_production_project_path,
                                     self.full_code())
        return _path

    def backup_path(self):
        """ get asset backup path

        rtype: str
        """
        _backup_project_path = zfused_api.project.Project(
            self.data["ProjectId"]).config["Publish"]
        _path = "{}/asset/{}".format(_backup_project_path, self.full_code())
        return _path

    def work_path(self):
        """ get asset work path

        rtype: str
        """
        _work_project_path = zfused_api.project.Project(
            self.data["ProjectId"]).config["LocalRoot"]
        _path = "{}/asset/{}".format(_work_project_path, self.full_code())
        return _path

    def publish_path(self):
        """ get asset publish path

        rtype: str
        """
        _publish_project_path = zfused_api.project.Project(
            self.data["ProjectId"]).config["LocalPublish"]
        _path = "{}/asset/{}".format(_publish_project_path, self.full_code())
        return _path

    def review_path(self):
        """ get asset review path

        rtype: str
        """
        _review_project_path = zfused_api.project.Project(
            self.data["ProjectId"]).config["Review"]
        _path = "{}/asset/{}".format(_review_project_path, self.full_code())
        return _path

    def thumbnail(self):
        """ get thumbnail file
        """
        return self.data["Thumbnail"]

    def get_thumbnail(self, is_version=False):
        if self.data.get("Thumbnail"):
            _thumbnail = self.data["Thumbnail"]
            _full_code = self.full_code()
            _production_path = zfused_api.project.Project(self.data["ProjectId"]).config["Root"]
            _production_file = "{0}/asset/{1}/{2}".format(_production_path, _full_code, _thumbnail)
            _local_path = zfused_api.project.Project(self.data["ProjectId"]).config["LocalRoot"]
            _local_file = "{0}/asset/{1}/{2}".format(_local_path, _full_code, _thumbnail)

            # return _production_file
            # 是否需要宝贝到本机
            if os.path.exists(_production_file):
                if not os.path.isfile(_local_file):
                    _path = os.path.dirname(_local_file)
                    if not os.path.isdir(_path):
                        os.makedirs(_path)
                    shutil.copy(_production_file, _local_file)
                return _local_file
            else:
                return None
        else:
            if is_version:
                _versions = self.get("version", filter={
                                     "LinkId": self.id, "Object": "asset"})
                if _versions:
                    _ver = _versions[-1]
                    import version
                    _ver_handle = version.Version(_ver["Id"], _ver)
                    return _ver_handle.GetThumbnail()
        return None

    def versions(self):
        """ get task version
        
        :rtype: list
        """
        _versions = self.get("version", filter={"LinkId": self.id, "Object": "asset"},
                                        sortby = ["Index"], order = ["asc"])
        if not _versions:
            return []
        return _versions

    def history(self):
        """ get history

        :rtype: list
        """
        _history = self.get("asset_history", filter = {"AssetId":self.id}, sortby = ["ChangeTime"], order = ["asc"])
        if _history:
            return _history
        else:
            return []

    def tasks(self, project_step_id_list = []):
        """ get task 
        """
        if project_step_id_list:
            _ids = "|".join([str(_step_id) for _step_id in project_step_id_list])
            _key = "{}_{}".format(self.id, _ids)
            if _key in self.task_dict.keys():
                _tasks = self.task_dict[_key]
            else:
                _tasks = self.get("task", filter = {"LinkId": self.id, 
                                                "Object": "asset", 
                                                "ProjectStepId__in": _ids})
                self.task_dict[_key] = _tasks
        else:
            _tasks = self.get("task", filter = {"LinkId": self.id, 
                                                "Object": "asset"})
        if not _tasks:
            return []
        return _tasks

    def update_status(self, status_id):
        """ update project step check script
        
        :param status_id: 状态id
        :rtype: bool
        """
        self.global_dict[self.id]["StatusId"] = status_id
        self.data["StatusId"] = status_id
        v = self.put("asset", self.data["Id"], self.data)
        if v:
            return True
        else:
            return False


    def create_default_task(self, project_step_id):
        """ create default task

        """
        # get default status id
        pass
