# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function
from collections import defaultdict

import os
import json
import shutil
import datetime
import logging

import zfused_api
#from . import project
#from . import sequence

loggr = logging.getLogger(__name__)

# read database
DATABASE_PATH = os.path.dirname(os.path.dirname(__file__))
SHOT_DATABASE_FILE = "{}/database/shot.json".format(DATABASE_PATH)
with open(SHOT_DATABASE_FILE, 'r') as f:
    print("read")
    SHOT_DATABASE = json.load(f)

def project_shots(project_ids = []):
    """ get project assets
    """
    if not project_ids:
        return SHOT_DATABASE
    _all_shots = []
    for _shot in SHOT_DATABASE:
        if _shot["ProjectId"] in project_ids:
            _all_shots.append(_shot)
    return _all_shots

class Shot(object):
    global_dict = {}
    global_tasks = defaultdict(list)
    global_historys = defaultdict(list)
    global_tags = defaultdict(list)
    def __init__(self, id, data = None):
        self.id = id
        self.data = data

        if not self.global_dict.__contains__(self.id):
            if self.data:
                self.global_dict[self.id] = self.data
            else:
                _data = None
                for _shot in SHOT_DATABASE:
                    if id == _shot["Id"]:
                        _data = _shot
                if not _data:
                    logger.error("shot id {0} not exists".format(self.id))
                    return
                self.data = _data
                self.global_dict[self.id] = _data
        else:
            if self.data:
                self.global_dict[self.id] = self.data
            else:
                self.data = self.global_dict[self.id]

    def object(self):
        return "shot"

    def description(self):
        return self.data["Description"]

    def file_code(self):
        """ task version file name

        :rtype: str
        """
        return self.full_code().replace("/", "_")

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
        if self.data["SequenceId"]:
            _sequence_code = zfused_api.sequence.Sequence(self.data["SequenceId"]).full_code()
            return u"{}/{}".format(_sequence_code, _code)
        else:
            return _code

    def full_name(self):
        """
        get full path name

        rtype: str
        """
        _name = self.data["Name"]
        if self.data["SequenceId"]:
            _sequence_name = zfused_api.sequence.Sequence(self.data["SequenceId"]).full_name()
            return u"{}/{}".format(_sequence_name, _name)
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

    def start_frame(self):
        """ get start frame
        """
        return self.data["FrameStart"]

    def end_frame(self):
        """ get end frame
        """
        return self.data["FrameEnd"]

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
        """
        get shot production path

        rtype: str
        """
        _production_project_path = zfused_api.project.Project(self.data["ProjectId"]).config["Root"]
        _path = "{}/shot/{}".format(_production_project_path, self.full_code())
        return _path

    def backup_path(self):
        """
        get shot backup path

        rtype: str
        """
        _backup_project_path = zfused_api.project.Project(self.data["ProjectId"]).config["Publish"]
        _path = "{}/shot/{}".format(_backup_project_path, self.full_code())
        return _path

    def work_path(self):
        """
        get shot work path

        rtype: str
        """
        _work_project_path = zfused_api.project.Project(self.data["ProjectId"]).config["LocalRoot"]
        _path = "{}/shot/{}".format(_work_project_path, self.full_code())
        return _path

    def publish_path(self):
        """
        get shot publish path

        rtype: str
        """
        _publish_project_path = zfused_api.project.Project(self.data["ProjectId"]).config["LocalPublish"]
        _path = "{}/shot/{}".format(_publish_project_path, self.full_code())
        return _path

    def review_path(self):
        """
        get shot review path

        rtype: str
        """
        _review_project_path = zfused_api.project.Project(self.data["ProjectId"]).config["Review"]
        _path = "{}/shot/{}".format(_review_project_path, self.full_code())
        return _path

    def thumbnail(self):
        return self.global_dict[self.id]["Thumbnail"]
        
        return self.data["Thumbnail"]
        if self.id not in self.global_thumbnail.keys():
            return None
        return self.global_thumbnail[self.id]

    def get_thumbnail(self, is_version = False):
        if self.data.get("Thumbnail"):
            _thumbnail = self.data["Thumbnail"]
            _full_code = self.full_code()
            _production_path = zfused_api.project.Project(self.data["ProjectId"]).config["Root"]
            _production_file = "{0}/shot/{1}/{2}".format(_production_path, _full_code, _thumbnail)
            _local_path = zfused_api.project.Project(self.data["ProjectId"]).config["LocalRoot"]
            _local_file = "{0}/shot/{1}/{2}".format(_local_path, _full_code, _thumbnail)
            
            #return _production_file
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
                _versions = self.get("version", filter = {"LinkId":self.id,"Object":"shot"})
                if _versions:
                    _ver = _versions[-1]
                    import version
                    _ver_handle = version.Version(_ver["Id"], _ver)
                    return _ver_handle.GetThumbnail()
        return None

    def tag_ids(self):
        """ get asset link tag ids
        """
        if self.id not in self.global_tags.keys() or self.RESET:
            # _historys = self.get("tag_link", filter = {"TaskId":self.id}, sortby = ["ChangeTime"], order = ["asc"])
            _tag_links = self.get("tag_link", filter = {"LinkObject": "shot", "LinkId": self.id})
            self.global_tags[self.id] = [_tag_link["TagId"] for _tag_link in _tag_links]
        return self.global_tags[self.id]

    def versions(self):
        """ get task version
        
        :rtype: list
        """
        _versions = self.get("version", filter={"LinkId": self.id, "Object": "shot"},
                                        sortby = ["Index"], order = ["asc"])
        if not _versions:
            return []
        return _versions

    def history(self):
        """ get history

        :rtype: list
        """
        _history = self.get("shot_history", filter = {"ShotId":self.id}, sortby = ["ChangeTime"], order = ["asc"])
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
            if _key in self.global_tasks.keys():
                _tasks = self.global_tasks[_key]
            else:
                _tasks = self.get("task", filter = {"LinkId": self.id, 
                                                "Object": "shot", 
                                                "ProjectStepId__in": _ids})
                self.global_tasks[_key] = _tasks
        else:
            _tasks = self.get("task", filter = {"LinkId": self.id, 
                                                "Object": "shot"})
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
        v = self.put("shot", self.data["Id"], self.data)
        if v:
            return True
        else:
            return False

    def update_start_frame(self, start_frame):
        """ get start frame
        """
        self.global_dict[self.id]["FrameStart"] = start_frame
        self.data["FrameStart"] = start_frame
        v = self.put("shot", self.data["Id"], self.data)
        if v:
            return True
        else:
            return False

    def update_end_frame(self, end_frame):
        """ get end frame
        """
        self.global_dict[self.id]["FrameEnd"] = end_frame
        self.data["FrameEnd"] = end_frame
        v = self.put("shot", self.data["Id"], self.data)
        if v:
            return True
        else:
            return False