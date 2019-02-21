#coding:utf-8
#--author-- lanhua.zhou

import os
import sys

__version__ = "2.2.4"

_resource = None

PATH = os.path.abspath(__file__)
DIRNAME = os.path.dirname(os.path.dirname(PATH))

sys.path.insert(0,os.path.dirname(PATH))
sys.path.insert(0,os.path.dirname(DIRNAME))
sys.path.insert(0,"{}/packages".format(DIRNAME))

RESOURCE_PATH = os.path.join(DIRNAME, "resources")

import core
import login

def version():
    """
    return the current version of the zfused client

    :rtype: sts
    """
    return __version__


def resource():
    """
    return a resource object for getting content from the resource folder

    :rtype: Resource
    """
    global _resource

    if not _resource:
        _resource = core.resource.Resource(RESOURCE_PATH)

    return _resource
