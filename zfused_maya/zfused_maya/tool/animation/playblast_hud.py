# coding:utf-8
# author binglu.wang
import os
import maya.cmds as cmds
import maya.mel as mm
import json
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import getpass,time
from functools import partial
import zfused_maya
import zfused_api
import zfused_maya.node.core.shotmask as shotmask

try:
    import zfused_login
    # record.User().name()
except ImportError:
    # 线下项目设置
    HUDProject = "BKM2"

def get_maya_hud():
    _project_id = zfused_maya.core.record.current_project_id()
    if _project_id:
        _project_handle = zfused_api.project.Project(_project_id)
        _dir = _project_handle.config["Root"]
        _file = "{}/setup/MAYA_HUD.json".format(_dir)
        print _file
        if os.path.isfile(_file):
            return _file
        return None
    return None

def get_maya_shotmask():
    _project_id = zfused_maya.core.record.current_project_id()
    if _project_id:
        _project_handle = zfused_api.project.Project(_project_id)
        _dir = _project_handle.config["Root"]
        _file = "{}/setup/MAYA_SHOTMASK.json".format(_dir)
        if os.path.isfile(_file):
            return _file
        return None
    return None

class HUD(object):
    viewInfoState = False
    def __init__(self, jsonPath):
        self.jsonPath = jsonPath
        self._HUDCompany   = u"苏州星龙传媒"
        #纵向边距"bs": "medium","small","large" 不能手动设置
        self._Company = {}
        self._Project = {}
        self._CUT = {}
        self._Timer = {}
        self._ImageSize = {}
        self._Camera_Name = {}
        self._Camera_Near = {}
        self._Camera_Far = {}
        self._Camera_Focal = {}
        self._Camera_Film = {}
        self._FrameInfo = {}
        self._DefaultList = []
        self._set_hud_info()

    def _get_config(self):
        # jsonPath = (r"%s\\%s.json"%(filePath,fileName)).replace("\\","/")
        # print jsonPath
        if os.path.exists(self.jsonPath):
            try:
                with open(self.jsonPath, 'r') as info:
                    dataInfo = json.load(info)
                    info.close()
                return dataInfo
            except ValueError:
                return None
        else:
            return None

    def _set_hud_info(self):
        self._Company["c"] = self._get_company
        self._Project["c"] = self._get_project_user_str
        self._CUT["c"] = self._get_file_name
        self._Timer["c"] = self._get_time
        self._ImageSize["c"] = self._get_image_size
        self._Camera_Name["c"] = self._get_camera_name
        self._Camera_Near["c"] = partial(self._get_camera_attr,"nearClipPlane")
        self._Camera_Far["c"] = partial(self._get_camera_attr,"farClipPlane")
        self._Camera_Focal["c"] = partial(self._get_camera_attr,"focalLength")
        self._Camera_Film["c"] = partial(self._get_camera_attr,"filmFit")
        self._FrameInfo["c"] = self._get_frame_str
        alltype = {
                    "_Company" : self._Company,
                    "_Project" : self._Project,
                    "_CUT" : self._CUT,
                    "_Timer" : self._Timer,
                    "_ImageSize" : self._ImageSize,
                    "_Camera_Name" : self._Camera_Name,
                    "_Camera_Near" : self._Camera_Near,
                    "_Camera_Far" : self._Camera_Far,
                    "_Camera_Focal" : self._Camera_Focal,
                    "_Camera_Film" : self._Camera_Film,
                    "_FrameInfo" : self._FrameInfo
                }
        # print alltype
        _config_info = self._get_config()
        # print _config_info
        if _config_info:
            self._DefaultList = [_i for _i in _config_info.keys()]
            for _k,_v in _config_info.items():
                for _key, _value in _v.items():
                    alltype[_k][_key] = _value
        else:
            print "Can't find config file"


    # 获取当前项目
    def _get_project(self):
        try:
            # uiConfigHandle = user.UiConfig()
            # uiConfigData = uiConfigHandle.Get()
            # #load task
            # project_id = uiConfigData["current_project_id"]
            # projectHandle = api.project.Project(project_id)
            # return projectHandle.data["Code"]
            _project_id = zfused_maya.core.record.current_project_id()
            _project_handle = zfused_api.project.Project(_project_id)
            return _project_handle.code()
        except:
            global HUDProject
            return HUDProject

    # 获取相机名字
    def _get_camera_name(self):
        view = OpenMayaUI.M3dView.active3dView()
        camDag = OpenMaya.MDagPath()
        view.getCamera(camDag)
        camera = camDag.fullPathName()
        _name = cmds.listRelatives(camera, parent = True)[0]
        return "            Camera:     %s"%(_name)

    # 获取当前相机焦距
    def _get_camera_attr(self,attr_name):
        view = OpenMayaUI.M3dView.active3dView()
        camDag = OpenMaya.MDagPath()
        view.getCamera(camDag)
        camera = camDag.fullPathName()
        try:
            # print "%s.%s"%(camera,attr_name)
            value = "%.3f"%cmds.getAttr("%s.%s"%(camera,attr_name))
            return "            %s:     %s"%(attr_name,str(value))
        except:
            return "            %s:     "%attr_name

    # 获取帧数段
    def _get_frame_str(self):
        z_StartFrame = int(cmds.playbackOptions(q = True, min = True))
        z_EndFrame = int(cmds.playbackOptions(q = True, max = True))
        format = "%0" + str(len(str(z_EndFrame))) + "d"
        z_CurrentFrame = format%int(cmds.currentTime(q = True))
        return "%s|%s-%s"%(z_CurrentFrame,z_StartFrame,z_EndFrame)
        # return "%s"%z_CurrentFrame + " | " + "%s-%s"%(z_StartFrame,z_EndFrame)

    # 获取当前时间
    def _get_time(self):
        import time
        time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        return str(time)

    # 获取项目制作人
    def _get_user(self):
        try:
            # userHandle = user.User()
            # userData = userHandle.Get()
            # # if not userData.has_key("account"):
            # #     return "robot"
            # _user_handle = api.user.User(userData["id"])
            # #return userData["account"]
            # return _user_handle.profile["NameCn"]
            return zfused_login.core.record.User().name()
        except:
            return self.GetUser()

    # 获取电脑账户
    def GetUser(self):
        import getpass
        hostName = getpass.getuser()    
        return hostName

    # 获取公司名
    # @property
    def _get_company(self):
        return "Company: %s"%self._HUDCompany

    # 组合项目信息
    def _get_project_user_str(self):
        #get user
        user = self._get_user()
        project = self._get_project()
        return "%s | %s"%(project,user)

    # 获取文件名
    def _get_file_name(self):
        _file = cmds.file(q = True, sn = True)
        if _file:
            _name = os.path.basename(os.path.splitext(_file)[0])
            return _name
        else:
            return ""

    # 获取图像大小
    def _get_image_size(self):
        _size = "%sx%s"%(cmds.getAttr("defaultResolution.width"),cmds.getAttr("defaultResolution.height"))
        return _size

    def _get_show_info(self,*args):
        from collections import Counter
        showInfo = {}
        blockindex = []
        for preProject in args:
            preProjectAttr = eval("self.%s"%preProject)
            print preProjectAttr
            blockindex.append(preProjectAttr["s"])
            current = Counter(blockindex)
            preProjectAttr["b"] = current[preProjectAttr["s"]]-1
            showInfo[preProject] = self._complete_info(**preProjectAttr)
        return showInfo

    def _complete_info(self,**kwargs):
        # 参数全简称对照:
        # section = s
        # block = b
        # blockAlignment = ba
        # blockSize = bs
        # dataFontSize = dfs
        # labelFontSize = lfs
        # padding = p
        # command = c
        # attachToRefresh = atr
        allAttr = {"atr":True,"b":0,"ba":"left","bs":"small","c":None,"dfs":"large","lfs":"large","p":0,"s":0,"da":"left","lw":0}
        outdict = {}
        for attr in allAttr.keys():
            if kwargs.has_key(attr):
                outdict[attr] = kwargs[attr]
            else:
                outdict[attr] = allAttr[attr]
        return outdict

    def displayMode(self,type):
        # allattr
        # ["nurbsCurves","nurbsSurfaces","cv","hulls","polymeshes","subdivSurfaces","planes",
        # "lights","cameras","imagePlane","joints","ikHandles","deformers","dynamics",
        # "particleInstancers","fluids","hairSystems","follicles","nCloths","nParticles",
        # "nRigids","dynamicConstraints","locators","dimensions","pivots","handles",
        # "textures","strokes","motionTrails","pluginShapes","clipGhosts","greasePencils","pluginObjects",]
        # 拍屏预设
        if "playblast" in type:
            hidekeys = ["nurbsCurves","cv","hulls","subdivSurfaces","planes","lights",
                        "cameras","imagePlane","joints","ikHandles","deformers","dynamics",
                        "particleInstancers","fluids","hairSystems","follicles","nCloths",
                        "nParticles","nRigids","dynamicConstraints","locators","dimensions",
                        "pivots","handles","motionTrails","clipGhosts","greasePencils"]
        # 中期制作预设
        elif "mediumTerm" in type:
            hidekeys = ["cv","hulls","subdivSurfaces","planes","lights","imagePlane",
                        "joints","ikHandles","particleInstancers","nParticles","dimensions",
                        "pivots","handles","motionTrails","clipGhosts","greasePencils"]
        # 原始预设
        else:
            hidekeys = ['nc','pl','lt','ca','joints','ikh','df','ha','follicles','hairSystems',
                        'strokes','motionTrails','dimensions','locators','motionTrails']
        #Display smoothness low
        modelPanels=cmds.getPanel(typ="modelPanel")
        for currentPanel in modelPanels:
            for item in hidekeys:
                eval("cmds.modelEditor(\'"+currentPanel+"\',e=True,"+item+"=0)")

    def show(self):
        import zfused_maya.core.restricted as restricted
        import maya.cmds as cmds
        _has_per, _info = restricted.restricted()
        if not _has_per:
            cmds.confirmDialog(message = _info)
            return False
        return True


    # 获取和修改显示信息的字体颜色
    @property
    def color(self):
        return cmds.displayColor("headsUpDisplayLabels", q = True)

    @color.setter
    def color(self, num = 16):
        cmds.displayColor("headsUpDisplayLabels", num, dormant = True)
        cmds.displayColor("headsUpDisplayValues", num, dormant = True)

    def AnimationHUD(self):
        if self.show():
            self.displayMode("playblast")
            # self._resize_font()
            displayLayout = self._get_show_info(*self._DefaultList)
            #mili heads up display sets
            self.removeHUD()
            # self.color = 16
            #----- Company Name ------ 
            #left top(section 0, block 0)
            for display in displayLayout.keys():
                dis = displayLayout[display]
                cmds.headsUpDisplay(display, s = dis["s"], b = dis["b"], ba = dis["ba"],p = dis["p"],
                                        lfs = dis["lfs"], dfs = dis["dfs"], blockSize = dis["bs"], 
                                        c = dis["c"], atr = dis["atr"],da = dis["da"],lw = dis["lw"])

    def removeHUD(self):
        huds = cmds.headsUpDisplay(lh = True)
        if huds:
            for item in huds:
                cmds.headsUpDisplay(item, rem = True)

    def restInitHUD(self):
        self.removeHUD()
        mm.eval("source initHUD.mel")

    def _resize_font(self):
        scalemode = cmds.mayaDpiSetting(q = 1,mode = 1)
        if scalemode == 0:
            print u"error:当前ui缩放模式不正确"
            return
        else:
            hudScale = cmds.mayaDpiSetting(q = 1,scaleValue = 1)
            font_size = int(15/hudScale)
            print font_size
            current_font_size= cmds.displayPref(q = 1,dfs = 1)
            if font_size != current_font_size:
                if font_size == 15:
                    cmds.displayPref(dfs = 16)
                else:
                    cmds.displayPref(dfs = font_size)

    def change_hud_state(self):
        print HUD.viewInfoState
        isshow = cmds.headsUpDisplay(lh = True)
        if not HUD.viewInfoState:
            self.color = 16
            self.AnimationHUD()

            # read shot mask profile
            _mask_json = get_maya_shotmask()
            if _mask_json:
                # shot mask
                shotmask.create_mask()
                _mask = shotmask.get_mask()
                with open(_mask_json, 'r') as info:
                    dataInfo = json.load(info)
                    if dataInfo:
                        for _key, _value in dataInfo.items():
                            cmds.setAttr("{}.{}".format(_mask, _key), _value)

            HUD.viewInfoState = True
        else:
            self.removeHUD()
            self.restInitHUD()

            # remove shot mask
            shotmask.delete_mask()

            HUD.viewInfoState = False

        return
        #if isshow and "self._Project" in isshow:
        #    self.viewInfoState = True
        self.viewInfoState = not self.viewInfoState
        # print self.viewInfoState
        if self.viewInfoState:
            self.color = 16
            self.AnimationHUD()
        else:
            self.removeHUD()
            self.restInitHUD()



if __name__ == '__main__':
    viewInfo = HUD(get_maya_hud())
    viewInfo.AnimationHUD()
