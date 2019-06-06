 # coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os
import logging

import maya.cmds as cmds

import zfused_api
import zfused_maya.core.record as record
import zfused_maya.core.filefunc as filefunc
import zfused_maya.node.core.yeti as yeti
import zfused_maya.node.core.attr as attr
import zfused_maya.node.core.check as check
import zfused_maya.node.core.alembiccache as alembiccache
import zfused_maya.node.core.texture as texture
import zfused_maya.node.core.referencefile as referencefile
import zfused_maya.node.core.relatives as relatives

import zfused_login.core.util as util


logger = logging.getLogger(__file__)

def publish_file(link_object, link_id, project_step_id):
    """ publish file

    :rtype: bool
    """ 
    # _task_handle = zfused_api.task.Task(task_id)
    _link_handle = zfused_api.objects.Objects( link_object, 
                                               link_id )
    _project_step_handle = zfused_api.step.ProjectStep( project_step_id )
    _output_scripts = _project_step_handle.output_attrs()
    
    # # 检查
    # _check_script = _project_step_handle.check_script()
    # if not check.Check.value:
    #     exec(_check_script)
    # if check.Check.value == True:
    #     check.Check.value = False
    # else:
    #     return 

    # # 提交关联信息
    # relatives.create_relatives()

    # # 上传备份文件
    # _value = publish_backup(infomation)
    # if not _value:
    #     cmds.confirmDialog(message = u"上传备份文件失败")
    #     return

    # 运行自定义脚本
    if _output_scripts:
        for _output_script in _output_scripts:
            # run scrpt
            print(_output_script)
            exec( _output_script["Script"] )

    # # 此处获取信息 是主 file 文件
    # _key_output_attr = _project_step_handle.key_output_attr()
    # _file_suffix = _key_output_attr["Suffix"].replace(".", "")

    # _name = _link_handle.file_code()
    # _index = "%04d"%(_task_handle.last_version_index() + 1)
    # _file_name = "/{}.{}.{}".format(_name, _index, _file_suffix)
    # _video_file = infomation["video"]
    # _video_name = None
    # if _video_file:
    #     _video_suffix = os.path.splitext(_video_file)[-1]
    #     _video_name = "/%s.%s%s"%(_name, _index, _video_suffix)
    # _thumbnail_file = infomation["thumbnail"]
    # _thumbnail_suffix = os.path.splitext(_thumbnail_file)[-1]
    # _thumbnail_name = "/%s.%s%s"%(_name, _index, _thumbnail_suffix)
    # _v, _info = _task_handle.submit_approval("{}.{}".format(_name, _index),
    #                              _file_name,
    #                              _project_step_handle.approvalto_user_ids(),
    #                              _project_step_handle.cc_user_ids(),
    #                              _video_name,
    #                              _thumbnail_name,
    #                              infomation["description"])
    # if not _v:
    #     cmds.confirmDialog(message = u"上传数据库信息失败 {}".format(_info))
    #     return

    # #  发送通知信息
    # _user_id = zfused_api.zFused.USER_ID
    # zfused_api.im.submit_message( {"msgtype":"review",
    #                               "review":{"review_id":_v,
    #                               "title":"%s.%s"%(_name, _index)}},
    #                               "user",
    #                               _user_id,
    #                               _project_step_handle.approvalto_user_ids() + _project_step_handle.cc_user_ids())
    
    # # 修改任务状态为审查中
    # _review_ids = zfused_api.status.review_ids()
    # if _review_ids:
    #     _task_handle.update_status(_review_ids[0])

    # open new file
    # 打开空文件
    cmds.file(new = True, f = True)

    # 上传结果ui
    cmds.confirmDialog(message = u"上传成功")

