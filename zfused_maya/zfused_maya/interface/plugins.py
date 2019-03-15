# coding:utf-8
# --author-- lanhua.zhou

"""
    load maya plugins

"""

import os

import zfused_maya

def set_plugin_path():
    _path = zfused_maya.PLUGIN_PATH
    scriptsPath = os.environ.get('MAYA_PLUG_IN_PATH')
    if os.path.exists(_path):
        if not _path in scriptsPath:
            os.environ['MAYA_PLUG_IN_PATH'] += '%s%s' % (os.pathsep, _path)