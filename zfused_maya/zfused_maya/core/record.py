# coding:utf-8
#--author-- lanhua.zhou

import os
import platform
import json
import ctypes
import logging

__all__ = ["Ui"]

logger = logging.getLogger(__name__)
# user app data path USER_CACHE_DIR

def current_project_id():
    _interface = Interface()
    _project_id = _interface.get("current_project_id")
    return _project_id if _project_id else 0

def current_task_id():
    _interface = Interface()
    _task_id = _interface.get("current_task_id")
    return _task_id if _task_id else 0

def current_project_step_id():
    _interface = Interface()
    _project_step_id = _interface.get("current_project_step_id")
    return _project_step_id if _project_step_id else 0

def current_link():
    _interface = Interface()
    _link = _interface.get("current_link")
    return _link if _link else ()

def _cache_dir():
    USER_CACHE_DIR = None
    if platform.system() == "Darwin":
        USER_CACHE_DIR = "%s/Applications/zfused/outsource/maya/ui_conf" % os.environ["HOME"]
    if platform.system() == "Windows":
        USER_CACHE_DIR = "%s/zfused/outsource/maya/ui_conf" % os.environ["APPDATA"]
    if not os.path.isdir(USER_CACHE_DIR):
        os.makedirs(USER_CACHE_DIR)
    return USER_CACHE_DIR

class _Json(object):
    def __init__(self, file):
        self.file = file
        self._data = {}
        '''
        if not os.path.isfile(self.file):
            with open(self.file, "w") as handle:
                json.dump({}, handle, indent=4)
        '''

    def write(self, _key, _value):
        data_old = self.get()
        data_old[_key] = _value
        with open(self.file, "w") as handle:
            json.dump(data_old, handle, indent=4)

    def save(self, data={}):
        data_old = self.get()
        if data_old == None:
            return
        data_old.update(data)
        with open(self.file, "w") as handle:
            json.dump(data_old, handle, indent=4)

    def get(self, key = None):
        try:
            with open(self.file, "r") as handle:
                data = handle.read()
                jsdata = json.loads(data)
            if key:
                return jsdata[key]
            else:
                return jsdata
        except Exception as e:
            logger.error("{} read error".format(self.file))
            return None

class Interface(_Json):
    pid = os.getpid()
    def __init__(self):
        super(Interface, self).__init__("%s/%s"%(_cache_dir(),os.getpid()))

        last_data = _get_last_data()
        pid = os.getpid()
        if not os.path.isfile(self.file):
            path = os.path.dirname(self.file)
            if not os.path.isdir(path):
                os.makedirs(path)
            with open(self.file, "w") as handle:
                if last_data:
                    json.dump(last_data, handle, indent = 4)
                else:
                    json.dump({}, handle, indent = 4)

    def __del__(self):
        _del_overdue_pid()


def _check_pid(pid):
    """
    检查pid是是否存在

    rtype: bool 
    """
    PROCESS_QUERY_INFROMATION = 0x1000
    processHandle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_INFROMATION, 0, pid)
    if processHandle == 0:
        return False
    else:
        ctypes.windll.kernel32.CloseHandle(processHandle)
    return True

def _del_overdue_pid():
    #get all pid file
    file_path = _cache_dir()
    all_pids = os.listdir(file_path)
    if all_pids:
        for pid in all_pids:
            if not _check_pid(int(pid)):
                os.remove(os.path.join(file_path,pid))

def _get_last_data():
    #get all pid file
    file_path = _cache_dir()
    if not os.path.isdir(file_path):
        return None
    all_pids = os.listdir(file_path)
    def compare(x, y):
        stat_x = os.stat(file_path + "/" + x)
        stat_y = os.stat(file_path + "/" + y)
        if stat_x.st_mtime < stat_y.st_mtime:
            return -1
        elif stat_x.st_mtime > stat_y.st_mtime:
            return 1
        else:
            return 0
    all_pids.sort(compare)
    try:
        all_pids.remove(str(os.getpid()))
    except Exception as e:
        logger.warning(e)
    if all_pids:
        last_pid = all_pids[-1]
        with open(os.path.join(file_path,last_pid), "r") as handle:
            data = handle.read()
            jsdata = json.loads(data)
        return jsdata 
    else:
        return None