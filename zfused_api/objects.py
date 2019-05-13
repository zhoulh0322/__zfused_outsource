# coding:utf-8
# --author-- lanhua.zhou

import zfused_api

OBJECT = {
    "asset": zfused_api.asset.Asset,
    # "episode": zfused_api.episode.Episode,
    "shot": zfused_api.shot.Shot,
    "sequence": zfused_api.sequence.Sequence,
    # "task": zfused_api.task.Task,
    "types": zfused_api.types.Types,
    "step": zfused_api.step.Step,
    "status": zfused_api.status.Status,
    # "user": zfused_api.user.User,
    "project": zfused_api.project.Project,
    # "version": zfused_api.version.Version,
}

def reset():
    for _, _api in OBJECT.items():
        _api.global_dict = {}

def Objects(obj, id, data=None):
    return OBJECT[obj](id, data)

def refresh(obj, object_id):
    """ 刷新对象
        
    """
    zfused_api.zFused.RESET = True
    OBJECT[obj].global_dict.pop(object_id)
    OBJECT[obj](object_id)
    zfused_api.zFused.RESET = True