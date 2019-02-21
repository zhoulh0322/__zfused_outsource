# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os

import config 
import record

def ztranser_server_addr():
    _login = record.Login()
    _address_name = _login.address_name()
    _config = config.Config()
    _ztranser_addr = _config.ztranser_addr(_address_name)
    return _ztranser_addr

def zfused_server_addr():
    _login = record.Login()
    _address_name = _login.address_name()
    _config = config.Config()
    _handle = _config.address(_address_name)
    return "{}:{}".format(_handle.host(),_handle.port())
    #return _ztranser_addr