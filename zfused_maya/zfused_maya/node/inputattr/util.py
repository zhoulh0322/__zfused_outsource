 # coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os
import shutil
import logging
import datetime
import time

import maya.cmds as cmds

import zfused_api
import zfused_maya.core.record as record
import zfused_maya.core.filefunc as filefunc
import zfused_maya.node.core.alembiccache as alembiccache
import zfused_maya.node.core.texture as texture
import zfused_maya.node.core.referencefile as referencefile
import zfused_maya.node.core.attr as attr
import zfused_maya.node.core.element as element
import zfused_maya.node.core.relatives as relatives

logger = logging.getLogger(__file__)

def receive_file(argv_task_id, argv_attr_id, argv_attr_code, argv_attr_type, argv_attr_mode, argv_attr_local):
    """ receive file
        base receive file script
    
    :rtype: bool
    """

def receive_file(output_link_object, output_link_id,  output_attr_id, input_link_object, input_link_id, input_attr_id):
    '''import alembic cache
    '''

    _file_title = "shader/redshift"

    _output_attr_handle = zfused_api.outputattr.OutputAttr(output_attr_id)
    _project_step_id = _output_attr_handle.data["ProjectStepId"]
    _project_step_handle = zfused_api.step.ProjectStep(_project_step_id)
    _step_code = _project_step_handle.code()
    _software_code = zfused_api.software.Software(_project_step_handle.data["SoftwareId"]).code()

    _output_link_handle = zfused_api.objects.Objects(output_link_object, output_link_id)
    _output_link_production_path = _output_link_handle.production_path()
    _output_link_publish_path = _output_link_handle.publish_path()
    _file_code = _output_link_handle.file_code()
    _suffix = _output_attr_handle.suffix()
    _attr_code = _output_attr_handle.code()
    _output_link_production_file = "{}/{}/{}/{}/{}{}".format( _output_link_production_path, _step_code, _software_code, _attr_code, _file_code, _suffix )
    if not os.path.exists(_output_link_production_file):
        return False
    print( _output_link_production_file )

    # if not argv_task_id:
    #     return
    # _task_handle = zfused_api.task.Task(argv_task_id)
    # _version_id = _task_handle.last_version_id()
    # if not _version_id:
    #     return
    # _version_handle = zfused_api.version.Version(_version_id)
    # _production_file = _version_handle.production_file()
    _production_file = _output_link_production_file

    _input_attr_handle = zfused_api.inputattr.InputAttr(input_attr_id)
    _project_step_id = _input_attr_handle.data["ProjectStepId"]
    _project_step_handle = zfused_api.step.ProjectStep(_project_step_id)
    _step_code = _project_step_handle.code()
    _software_code = zfused_api.software.Software(_project_step_handle.data["SoftwareId"]).code()
    _input_link_handle = zfused_api.objects.Objects(input_link_object, input_link_id)
    _input_link_work_path = _input_link_handle.work_path()

    argv_attr_type = _input_attr_handle.data["Type"]
    argv_attr_local = _input_attr_handle.data["IsLocal"]
    # type 
    if argv_attr_type == "reference":
        if argv_attr_local:
            # reference local file
            #  download file
            _local_file = "{}/reference/{}".format(_input_link_work_path, os.path.basename(_production_file))
            _local_dir = os.path.dirname(_local_file)
            if not os.path.isdir(_local_dir):
                os.makedirs(_local_dir)
            # copy file
            filefunc.receive_file(_production_file, _local_file)
            rf = cmds.file(_local_file, r = True, ns = _file_code)
            rfn = cmds.referenceQuery(rf, rfn = True)
            # attr.set_node_attr(rfn, argv_attr_id, _version_id, "true")
        else:
            # reference server file
            rf = cmds.file(_production_file, r = True, ns = _file_code)
            rfn = cmds.referenceQuery(rf, rfn = True)
            # attr.set_node_attr(rfn, argv_attr_id, _version_id, "false")
    elif argv_attr_type == "import":
        rf = cmds.file(_production_file, i = True, namespace = ":", ra = True, ignoreVersion = True, mergeNamespacesOnClash = True, options = "v=0;", pr = True)
    elif argv_attr_type == "open":
        print("-------------------open file {}".format(_production_file))
        rf = cmds.file(_production_file, o = True, f = True, pr = True)

    elif argv_attr_type == "replace":
        # change reference step ...
        # get attr project step
        _project_steps = zfused_api.zFused.get("step_attr_output", filter = {"Id": argv_attr_id})
        if _project_steps:
            _project_step_id = _project_steps[0]["ProjectStepId"]
            # get scene elements
            _scene_elements = element.scene_elements()
            if _scene_elements:
                for _element in _scene_elements:
                    try:
                        element.replace_by_step(_element, _project_step_id)
                    except Exception as e:
                        logger.warning(e)
                # save local reference
                for _element in _scene_elements:
                    if _element.has_key("is_local"):
                        if _element["is_local"] == "true":
                            #保存本地二级参考
                            _file = cmds.referenceQuery(_element["reference_node"], f = True)
                            cmds.file(_file, f = True, saveReference = True)
    # elif argv_attr_type == "import":

    # frame
    _link_handle = zfused_api.objects.Objects( input_link_object, input_link_id )
    if isinstance( _link_handle, zfused_api.shot.Shot ):
        # start frame and end frame
        _start_frame = _link_handle.start_frame()
        _end_frame = _link_handle.end_frame()
        cmds.playbackOptions( min = _start_frame, max = _end_frame )

def receive_version_file(version_id):
    """ receive version file 
        if not has versions,assembly new file
    
    :rtype: bool
    """
    # 按照版本领取文件
    print("version id {}".format(version_id))
    _version_handle = zfused_api.version.Version(version_id)
    _version_backup_file = _version_handle.backup_file()
    _version_work_file = _version_handle.work_file()

    # BACKUP FILE
    # 
    _backup_file(_version_work_file)

    # copy backup file to work file
    _version_work_dir = os.path.dirname(_version_work_file)
    if not os.path.isdir(_version_work_dir):
        os.makedirs(_version_work_dir)
    shutil.copy(_version_backup_file, _version_work_file)
    import maya.cmds as cmds
    
    try:
        # open file
        cmds.file(_version_work_file, o = True, f = True)
    except:
        pass
        
    # local reference file
    _task_handle = zfused_api.task.Task(_version_handle.data["TaskId"])
    _work_path = _task_handle.work_path()
    _files = referencefile.files()
    if _files:
        _path_set = referencefile.paths(_files)[0]
        _intersection_path = max(_path_set)
        referencefile.local_file(_files, _intersection_path, _work_path + "/reference")
        _file_nodes = referencefile.nodes()
        if _file_nodes:
            referencefile.change_node_path(_file_nodes, _intersection_path, _work_path + "/reference")

    # local texture
    _task_handle = zfused_api.task.Task(_version_handle.data["TaskId"])
    _work_path = _task_handle.work_path()
    _texture_files = texture.files()
    if _texture_files:
        _path_set = texture.paths(_texture_files)[0]
        _intersection_path = max(_path_set)
        texture.local_file(_texture_files, _intersection_path, _work_path + "/texture")
        _file_nodes = texture.nodes()
        if _file_nodes:
            texture.change_node_path(_file_nodes, _intersection_path, _work_path + "/texture")

    # local alembic cache
    _alembic_files = alembiccache.files()
    if _alembic_files:
        _path_set = alembiccache.paths(_alembic_files)[0]
        _intersection_path = max(_path_set)
        alembiccache.local_file(_alembic_files, _intersection_path, _work_path + "/cache/alembic")
        _file_nodes = alembiccache.nodes()
        if _file_nodes:
            alembiccache.change_node_path(_file_nodes, _intersection_path, _work_path + "/cache/alembic")

    # wireframe
    viewport = cmds.getPanel( withFocus = True)
    if 'modelPanel' in viewport:
        cmds.modelEditor( viewport, edit = True, displayAppearance = "wireframe" )

    # create relatives
    relatives.create_relatives()

    return True

def assembly_file(link_object, link_id, project_step_id):
    """ assembly new task file

    :rtype: None
    """
    import maya.cmds as cmds
    cmds.file(new = True, f = True)

    # 本地制作文件路劲
    _project_step_handle = zfused_api.step.ProjectStep(project_step_id)
    _step_code = _project_step_handle.code()
    _software_code = zfused_api.software.Software( _project_step_handle.data["SoftwareId"] ).code()
    _object_handle = zfused_api.objects.Objects( link_object, link_id )
    _work_path = "{}/{}/{}".format(_object_handle.work_path(), _step_code, _software_code)
    _name = "%s.0001"%(_object_handle.file_code())
    if link_object == "asset":
        _format = "mayaBinary"
        _file_name = "%s/%s.mb"%(_work_path, _name)
    else:    
        _format = "mayaAscii"
        _file_name = "%s/%s.ma"%(_work_path, _name)
    _file_dir = os.path.dirname(_file_name)
    if not os.path.isdir(_file_dir):
        os.makedirs(_file_dir)
    cmds.file(rename = _file_name)

    _input_scripts = _project_step_handle.input_attrs()

    for _input_script in _input_scripts:
        print(_input_script)
        if _input_script["Mode"] == "direct":
            _argvs = {
                "output_link_object": link_object, 
                "output_link_id": link_id,  
                "output_attr_id": _input_script["StepAttrId"], 
                "input_link_object" : link_object, 
                "input_link_id": link_id, 
                "input_attr_id": _input_script["Id"] 
            }
            exec( _input_script["Script"], _argvs)

    # frame
    # _link_handle = zfused_api.objects.Objects( _task_handle.data["Object"], _task_handle.data["LinkId"])
    if isinstance( _object_handle, zfused_api.shot.Shot ):
        # start frame and end frame
        _start_frame = _object_handle.start_frame()
        _end_frame = _object_handle.end_frame()
        cmds.playbackOptions( min = _start_frame, max = _end_frame )
        cmds.currentTime(_start_frame)

    return

    # get input task
    _input_tasks = _task_handle.input_tasks()
    #if _input_tasks:
    if _input_tasks:
        for _input_attr_id, _task_list in _input_tasks.items():
            # get code script ...
            logger.info("{}".format(_input_attr_id))
            _input_attr_handle = zfused_api.inputattr.InputAttr(_input_attr_id)
            _script = _input_attr_handle.data["Script"]
            for _task in _task_list:
                _task_id = _task["Id"]
                _argv = {
                    "argv_task_id" : _task_id,
                    "argv_attr_id" : _input_attr_handle.data["StepAttrId"],
                    "argv_attr_code" : _input_attr_handle.data["Code"], 
                    "argv_attr_type" : _input_attr_handle.data["Type"], 
                    "argv_attr_mode" : _input_attr_handle.data["Mode"],
                    "argv_attr_local": _input_attr_handle.data["IsLocal"]
                }
                # will do
                print("========================================")
                print(_script)
                # 动态创建类
                exec(_script, _argv)

    cmds.file(rename = _file_name)
    # wireframe
    viewport = cmds.getPanel( withFocus = True)
    if 'modelPanel' in viewport:
        cmds.modelEditor( viewport, edit = True, displayAppearance = "wireframe" )

    cmds.file(save = True, options = "v=0;", f = True, type = _format)

    # create relatives
    # 先取消记录 关联关系 后期领取总是判定错误
    # relatives.create_relatives()
    return True

def _backup_file(ori_file):
    """ backup files

    """
    if not os.path.isfile(ori_file):
        return

    _dir = os.path.dirname(ori_file)
    _backup_dir = "{}/backup".format(_dir)
    if not os.path.isdir(_backup_dir):
        os.makedirs(_backup_dir)
    # copy file and rename 
    _file_name = os.path.basename(ori_file)
    _suffix = os.path.splitext(_file_name)
    # new name
    _time_str = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    _new_name = "{}.{}.{}".format(_suffix[0], _time_str, _suffix[-1])
    _new_file = "{}/{}".format(_backup_dir, _new_name)

    shutil.copy(ori_file, _new_file)