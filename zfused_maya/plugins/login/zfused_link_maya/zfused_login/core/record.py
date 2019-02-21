# coding:utf-8
# --author-- lanhua.zhou

import os
import platform
import json

__all__ = ["LoginType", "Login", "User"]

# user app data path USER_CACHE_DIR
class LoginType:
    if platform.system() == "Darwin":
        login_dir = "%s/Applications/zfused/login/maya" % os.environ["HOME"]
    if platform.system() == "Windows":
        login_dir = "%s/zfused/login/maya" % os.environ["APPDATA"]
    login_file = "{}/login_type".format(login_dir)
    if not os.path.isdir(login_dir):
        os.makedirs(login_dir)
        with open(login_file, "w") as handle:
            json.dump({"login_type": 0}, handle, indent=4)

    @classmethod
    def set_login_type(cls, login_type):
        with open(cls.login_file, "w") as handle:
            json.dump({"login_type": login_type}, handle, indent=4)

    @classmethod
    def login_type(cls):
        with open(cls.login_file, "r") as handle:
            data = handle.read()
            jsdata = json.loads(data)
            LOGIN_TYPE = jsdata["login_type"]
            return LOGIN_TYPE

def _cache_dir():
    USER_CACHE_DIR = None
    if LoginType.login_type() == 0:
        if platform.system() == "Darwin":
            USER_CACHE_DIR = "%s/Applications/zfused/link/maya/login_conf" % os.environ["HOME"]
        if platform.system() == "Windows":
            USER_CACHE_DIR = "%s/zfused/link/maya/login_conf" % os.environ["APPDATA"]
    elif LoginType.login_type() == 1:
        if platform.system() == "Darwin":
            USER_CACHE_DIR = "%s/Applications/zfused/outsource/maya/login_conf" % os.environ["HOME"]
        if platform.system() == "Windows":
            USER_CACHE_DIR = "%s/zfused/outsource/maya/login_conf" % os.environ["APPDATA"]
    if not os.path.isdir(USER_CACHE_DIR):
        os.makedirs(USER_CACHE_DIR)
    return USER_CACHE_DIR


class useJson(object):
    def __init__(self, file):
        self.file = file
        self._data = {}
        if not os.path.isfile(self.file):
            with open(self.file, "w") as handle:
                json.dump({}, handle, indent=4)

    def write(self, _key, _value):
        data_old = self.get()
        # if data_old == None:
        #    data_old = []
        # data_old.update(data)
        data_old[_key] = _value
        with open(self.file, "w") as handle:
            json.dump(data_old, handle, indent=4)

    def save(self, data={}):
        data_old = self.get()
        if data_old == None:
            return
        # for key in data.keys():
        data_old.update(data)
        with open(self.file, "w") as handle:
            json.dump(data_old, handle, indent=4)

    def get(self):
        try:
            with open(self.file, "r") as handle:
                data = handle.read()
                jsdata = json.loads(data)
            return jsdata
        except:
            return {}


class Login(useJson):
    def __init__(self):
        super(Login, self).__init__("%s/login.json" % _cache_dir())

    def login_type(self):
        _data = self.get()
        if _data:
            if "login_type" in _data:
                return _data["login_type"]
        return 0

    def set_login_type(self, type_id):
        """ set login type

        """
        self.write("login_type", type_id)

    def address_name(self):
        """
        get address name

        """
        _data = self.get()
        if _data:
            if "address_name" in _data:
                return _data["address_name"]
        return None

    def set_address_name(self, name):
        """ set address name

        """
        self.write("address_name", name)

    def set_outsource_path(self, path):
        """ outsource path
        
        """
        self.write("outsource_path", path)

    def outsource_path(self):
        """ outsource path

        """
        _data = self.get()
        if _data:
            if "outsource_path" in _data:
                return _data["outsource_path"]
        return None

    def remember(self):
        """ get is remember

        """
        _data = self.get()
        if _data:
            if "remember" in _data:
                return _data["remember"]
        return False

    def autoload(self):
        """
        get auto load

        """
        _data = self.get()
        if _data:
            if "autoload" in _data:
                return _data["autoload"]
        return False

    def set_remember(self, _v=True):
        """
        set remember

        """
        self.write("remember", _v)


    def set_autoload(self, _v=True):
        """
        set auto load

        """
        self.write("autoload", _v)


class User(useJson):
    def __init__(self):
        super(User, self).__init__("%s/user.json" % _cache_dir())

    def name(self):
        _data = self.get()
        if "name" in _data:
            return _data["name"]
        return None

    def password(self):
        _data = self.get()
        if "password" in _data:
            return _data["password"]
        return None

    def set_name(self, _v):
        """
        set remember

        """
        self.write("name", str(_v))

    def set_password(self, _v):
        """
        set remember

        """
        self.write("password", _v)


'''
class UiConfig(useJson):
    def __init__(self):
        super(UiConfig, self).__init__("%s/uiConfig.json"%_cache_dir())
'''
