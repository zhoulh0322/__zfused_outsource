# coding:utf-8
#--author-- lanhua.zhou

import json
import os

__all__ = ['CONFIG_FILE', 'Config']

CONFIG_FILE = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))), "conf/app.json")


class Config(object):
    def __init__(self):
        self._file = CONFIG_FILE
        self._data = []
        with open(self._file, "r") as fileHandle:
            fileData = fileHandle.read()
            if fileData:
                self._data = json.loads(fileData)

    def address(self, address_name):
        _addresss = self.get()
        if _addresss:
            for _address in _addresss:
                if address_name == _address["name"]:
                    return _Address(_address)
        return None

    def ztranser_addr(self, address_name):
        """ get ztranser host and port

        :rtype: str
        """
        _data = self.address(address_name)
        return "{}:{}".format(_data.ztranser_host(),_data.ztranser_port())

    def get(self):
        return self._data

    def write(self, _key, _value):
        self._data[_key] = _value
        with open(self._file, "w") as handle:
            json.dump(data_old, handle, indent=4)


class _Address(object):
    def __init__(self, data={}):
        self._data = data

    def name(self):
        return self._data["name"]

    def host(self):
        return self._data["host"]

    def port(self):
        return self._data["port"]

    def python_path(self):
        return self._data["python_path"]

    def ztranser_host(self):
        return self._data["ztranser_host"]

    def ztranser_port(self):
        return self._data["ztranser_port"]


if __name__ == "__main__":
    print Config().get()
