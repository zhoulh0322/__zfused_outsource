# coding:utf-8
# --author-- lanhua.zhou

""" 文件操作函数集合 """

import os
import sys
import re
import time
import shutil
import subprocess
import tempfile
import hashlib
import locale
import json
import logging

import zfused_api
import zfused_login
import zfused_maya

import record

# will ???
REPLACE = {
    "P:":"C:/ClusterStorage/Volume1/Shares/Workspace",
}

logger = logging.getLogger(__name__)

def receive_file(src, dst):
    """ 获取文件
        类似拷贝服务器文件
        返回是否领取成功
    :pargarms: src 源文件
    :pargarms: dst 目标文件
    
    :rtype: str
    """
    if not os.path.isfile(src):
        return False
    _dst_path = os.path.dirname(dst)
    if not os.path.isdir(_dst_path):
        os.makedirs(_dst_path)
    shutil.copy(src, dst)
    if os.path.isfile(dst):
        return True
    return False

def publish_file(src, dst, del_src = False):
    """ 上传文件
    
    :pargarms: src 源文件
    :pargarms: dst 目标文件
    :pargarms: del_src 是否删除源文件,默认不删除

    :rtype: bool
    """
    _resource = zfused_maya.resource()
    _publish_exe = _resource.get("plugins/ztranser", "client.exe")
    if not os.path.isfile(_publish_exe):
        return False
    # get ztranser server addr
    """
    _login = zfused_login.core.record.Login()
    _address_name = _login.address_name()
    _config = zfused_login.core.config.Config()
    _ztranser_addr = _config.ztranser_addr(_address_name)
    """
    _ztranser_addr = zfused_login.core.util.ztranser_server_addr()
    # ???
    _dst_file = dst.replace("P:",REPLACE["P:"])

    # copy dst file to temp file
    _temp_dir = tempfile.gettempdir()
    _temp_file = "%s/%s%s"%(_temp_dir, time.time(), os.path.splitext(src)[-1]) 
    logger.info("temp file {}".format(_temp_file))   
    # copy src to temp file
    try:
        shutil.copy(src, _temp_file)
    except Exception as e:
        logger.error(e)
        return False

    # publish args
    arg = u"{} {} send {} {}".format(_publish_exe, _ztranser_addr, _temp_file, _dst_file)
    logger.info(arg)
    arg = arg.encode(locale.getdefaultlocale()[1])

    # publish info temp
    _publish_temp = tempfile.SpooledTemporaryFile(bufsize = 1024)
    _file_no = _publish_temp.fileno()
    _obj = subprocess.Popen(arg, stdout = _file_no, stderr = _file_no, shell = True)
    _obj.wait()
    _publish_temp.seek(0)
    _logger_data = _publish_temp.readlines()
    _dst_size = os.path.getsize(_temp_file)

    # remove temp file
    os.remove(_temp_file)
    # remove src file
    if del_src:
        os.remove(src)

    for i in _logger_data:
        if "send over " in i:
            if int(i.split(" ")[-1]) == _dst_size:
                return True
            else:
                return False
    return False