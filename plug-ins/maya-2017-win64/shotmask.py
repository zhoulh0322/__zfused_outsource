# coding:utf-8
# --author-- lanhua.zhou


"""
    custom maya mask 

"""

"""

PLUG_IN_NAME = "shotmask.py"
NODE_NAME = "shotmask"
TRANSFORM_NODE_NAME = "shotmask"
SHAPE_NODE_NAME = "shotmask_shape"

def create_mask():
    if not cmds.pluginInfo(PLUG_IN_NAME, q=True, loaded=True):
        try:
            cmds.loadPlugin(PLUG_IN_NAME)
        except:
            print("Failed to load ShotMask plug-in: {0}".format(PLUG_IN_NAME))
            return

    if not get_mask():
        transform_node = cmds.createNode("transform", name = TRANSFORM_NODE_NAME)
        cmds.createNode(NODE_NAME, name=SHAPE_NODE_NAME, parent=transform_node)

def delete_mask():
    mask = get_mask()
    if mask:
        transform = cmds.listRelatives(mask, fullPath=True, parent=True)
        if transform:
            cmds.delete(transform)
        else:
            cmds.delete(mask)

def get_mask():
    if cmds.pluginInfo(PLUG_IN_NAME, q=True, loaded=True):
        nodes = cmds.ls(type = NODE_NAME)
        if len(nodes) > 0:
            return nodes[0]
    return None

"""

import maya.api.OpenMaya as om
import maya.api.OpenMayaRender as omr
import maya.api.OpenMayaUI as omui

import maya.cmds as cmds


PLUGIN_NAME = "shotmask"
PLUGIN_TYPE_ID = om.MTypeId(0x0011A885)
DRAW_DB_CLASSIFICATION = "drawdb/geometry/shotmask"
DRAW_REGISTRANT_ID = "ShotMaskNode"

def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass


class ShotMaskLocator(omui.MPxLocatorNode):
    """
    """

    # TEXT_ATTRS = ["topLeftText", "tlt", "topCenterText", "tct", "topRightText", "trt",
    #               "bottomLeftText", "blt", "bottomCenterText", "bct", "bottomRightText", "brt"]

    def __init__(self):
        """
        """
        super(ShotMaskLocator, self).__init__()

    def excludeAsLocator(self):
        """
        """
        return False

    @classmethod
    def creator(cls):
        """
        """
        return ShotMaskLocator()

    @classmethod
    def initialize(cls):
        """
        """

        t_attr = om.MFnTypedAttribute()
        stringData = om.MFnStringData()
        obj = stringData.create("")
        camera_name = t_attr.create("camera", "cam", om.MFnData.kString, obj)
        t_attr.writable = True
        t_attr.storable = True
        t_attr.keyable = False
        ShotMaskLocator.addAttribute(camera_name)

        attr = om.MFnNumericAttribute()
        mask_width = attr.create("maskWidth", "mw", om.MFnNumericData.kShort, 10)
        attr.writable = True
        attr.storable = True
        attr.keyable = True
        # attr.setMin(0)
        # attr.setMax(6)
        ShotMaskLocator.addAttribute(mask_width)

        attr = om.MFnNumericAttribute()
        mask_height = attr.create("maskHeight", "mh", om.MFnNumericData.kShort, 10)
        attr.writable = True
        attr.storable = True
        attr.keyable = True
        # attr.setMin(0)
        # attr.setMax(6)
        ShotMaskLocator.addAttribute(mask_height)

        attr = om.MFnNumericAttribute()
        border_color = attr.createColor("borderColor", "bc")
        attr.default = (0.0, 0.0, 0.0)
        attr.writable = True
        attr.storable = True
        attr.keyable = True
        ShotMaskLocator.addAttribute(border_color)

        attr = om.MFnNumericAttribute()
        border_alpha = attr.create("borderAlpha", "ba", om.MFnNumericData.kFloat, 1.0)
        attr.writable = True
        attr.storable = True
        attr.keyable = True
        attr.setMin(0.0)
        attr.setMax(1.0)
        ShotMaskLocator.addAttribute(border_alpha)

        attr = om.MFnNumericAttribute()
        border_scale = attr.create("borderScale", "bs", om.MFnNumericData.kFloat, 1.0)
        attr.writable = True
        attr.storable = True
        attr.keyable = True
        attr.setMin(0.5)
        attr.setMax(2.0)
        ShotMaskLocator.addAttribute(border_scale)

        attr = om.MFnNumericAttribute()
        top_border = attr.create("topBorder", "tbd", om.MFnNumericData.kBoolean, True)
        attr.writable = True
        attr.storable = True
        attr.keyable = True
        ShotMaskLocator.addAttribute(top_border)

        attr = om.MFnNumericAttribute()
        bottom_border = attr.create("bottomBorder", "bbd", om.MFnNumericData.kBoolean, True)
        attr.writable = True
        attr.storable = True
        attr.keyable = True
        ShotMaskLocator.addAttribute(bottom_border)

        attr = om.MFnNumericAttribute()
        left_border = attr.create("leftBorder", "lbd", om.MFnNumericData.kBoolean, True)
        attr.writable = True
        attr.storable = True
        attr.keyable = True
        ShotMaskLocator.addAttribute(left_border)

        attr = om.MFnNumericAttribute()
        right_border = attr.create("rightBorder", "rbd", om.MFnNumericData.kBoolean, True)
        attr.writable = True
        attr.storable = True
        attr.keyable = True
        ShotMaskLocator.addAttribute(right_border)

class ShotMaskData(om.MUserData):
    """
    """

    def __init__(self):
        """
        """
        super(ShotMaskData, self).__init__(False)  # don't delete after draw


class ShotMaskDrawOverride(omr.MPxDrawOverride):
    """
    """

    NAME = "zshotmask_draw_override"

    def __init__(self, obj):
        """
        """
        super(ShotMaskDrawOverride, self).__init__(obj, ShotMaskDrawOverride.draw)

    def supportedDrawAPIs(self):
        """
        """
        return (omr.MRenderer.kAllDevices)

    def isBounded(self, obj_path, camera_path):
        """
        """
        return False

    def boundingBox(self, obj_path, camera_path):
        """
        """
        return om.MBoundingBox()

    def prepareForDraw(self, obj_path, camera_path, frame_context, old_data):
        """
        """
        data = old_data
        if not isinstance(data, ShotMaskData):
            data = ShotMaskData()

        fnDagNode = om.MFnDagNode(obj_path)

        data.camera_name = fnDagNode.findPlug("camera", False).asString()

        data.mask_width = fnDagNode.findPlug("maskWidth", False).asInt()
        data.mask_height = fnDagNode.findPlug("maskHeight", False).asInt()

        r = fnDagNode.findPlug("borderColorR", False).asFloat()
        g = fnDagNode.findPlug("borderColorG", False).asFloat()
        b = fnDagNode.findPlug("borderColorB", False).asFloat()
        a = fnDagNode.findPlug("borderAlpha", False).asFloat()
        data.border_color = om.MColor((r, g, b, a))

        data.border_scale = fnDagNode.findPlug("borderScale", False).asFloat()

        data.top_border = fnDagNode.findPlug("topBorder", False).asBool()
        data.bottom_border = fnDagNode.findPlug("bottomBorder", False).asBool()
        data.left_border = fnDagNode.findPlug("leftBorder", False).asBool()
        data.right_border = fnDagNode.findPlug("rightBorder", False).asBool()

        return data

    def hasUIDrawables(self):
        """
        """
        return True

    def addUIDrawables(self, obj_path, draw_manager, frame_context, data):
        """
        """
        if not isinstance(data, ShotMaskData):
            return

        camera_path = frame_context.getCurrentCameraPath()
        camera = om.MFnCamera(camera_path)

        if data.camera_name and self.camera_exists(data.camera_name) and not self.is_camera_match(camera_path, data.camera_name):
            return

        camera_aspect_ratio = camera.aspectRatio()
        device_aspect_ratio = cmds.getAttr("defaultResolution.deviceAspectRatio")

        vp_x, vp_y, vp_width, vp_height = frame_context.getViewportDimensions()
        vp_half_width = 0.5 * vp_width
        vp_half_height = 0.5 * vp_height
        vp_aspect_ratio = vp_width / float(vp_height)

        scale = 1.0

        resolution_width = cmds.getAttr("defaultResolution.width")

        if camera.filmFit == om.MFnCamera.kHorizontalFilmFit:
            mask_width = vp_width / camera.overscan
            mask_height = mask_width / device_aspect_ratio

            _height = vp_width / camera.overscan / device_aspect_ratio
            _width = (vp_width / camera.overscan) * (data.mask_width / float(resolution_width))

        elif camera.filmFit == om.MFnCamera.kVerticalFilmFit:
            mask_height = vp_height / camera.overscan
            mask_width = mask_height * device_aspect_ratio


        elif camera.filmFit == om.MFnCamera.kFillFilmFit:
            if vp_aspect_ratio < camera_aspect_ratio:
                if camera_aspect_ratio < device_aspect_ratio:
                    scale = camera_aspect_ratio / vp_aspect_ratio
                else:
                    scale = device_aspect_ratio / vp_aspect_ratio
            elif camera_aspect_ratio > device_aspect_ratio:
                scale = device_aspect_ratio / camera_aspect_ratio

            mask_width = vp_width / camera.overscan * scale
            mask_height = mask_width / device_aspect_ratio

        elif camera.filmFit == om.MFnCamera.kOverscanFilmFit:
            if vp_aspect_ratio < camera_aspect_ratio:
                if camera_aspect_ratio < device_aspect_ratio:
                    scale = camera_aspect_ratio / vp_aspect_ratio
                else:
                    scale = device_aspect_ratio / vp_aspect_ratio
            elif camera_aspect_ratio > device_aspect_ratio:
                scale = device_aspect_ratio / camera_aspect_ratio

            mask_height = vp_height / camera.overscan / scale
            mask_width = mask_height * device_aspect_ratio
        else:
            om.MGlobal.displayError("[ZShotMask] Unknown Film Fit value")
            return

        mask_half_width = 0.5 * mask_width
        mask_x = vp_half_width - mask_half_width

        mask_half_height = 0.5 * mask_height
        mask_bottom_y = vp_half_height - mask_half_height
        mask_top_y = vp_half_height + mask_half_height

        border_height = int(0.05 * mask_height * data.border_scale)
        background_size = (int(mask_width), border_height)

        draw_manager.beginDrawable()
        # draw_manager.setFontName(data.font_name)
        # draw_manager.setFontSize(int((border_height - border_height * 0.15) * data.font_scale))
        # draw_manager.setColor(data.font_color)

        if data.left_border:
            # print("left---------------------")
            # print(mask_x, mask_bottom_y, (_width, _height))
            self.draw_border(draw_manager, om.MPoint(mask_x, mask_bottom_y), (int(_width), int(_height)), data.border_color )
        if data.right_border:
            # print("right----------------------")
            # print(mask_x, mask_bottom_y, (_width, _height))
            self.draw_border(draw_manager, om.MPoint(mask_x + mask_width - _width, mask_bottom_y), (int(_width), int(_height)), data.border_color )

        draw_manager.endDrawable()

    def draw_border(self, draw_manager, position, background_size, color):
        """
        """
        draw_manager.text2d(position, " ", alignment = omr.MUIDrawManager.kLeft, backgroundSize=background_size, backgroundColor=color)

    def draw_text(self, draw_manager, position, text, alignment, background_size):
        """
        """
        if(len(text) > 0):
            draw_manager.text2d(position, text, alignment=alignment, backgroundSize=background_size, backgroundColor=om.MColor((0.0, 0.0, 0.0, 0.0)))

    def camera_exists(self, name):
        """
        """
        # ---------------------------------------------------------------------
        # om.MItDependencyNodes is only supported in Maya 2016.5 and newer
        # ---------------------------------------------------------------------
        # dg_iter = om.MItDependencyNodes(om.MFn.kCamera)
        # while not dg_iter.isDone():
        #     if dg_iter.thisNode().hasFn(om.MFn.kDagNode):
        #         camera_path = om.MDagPath.getAPathTo(dg_iter.thisNode())
        #         if self.is_camera_match(camera_path, name):
        #             return True
        #     dg_iter.next()
        # return False

        return name in cmds.listCameras()

    def is_camera_match(self, camera_path, name):
        """
        """
        path_name = camera_path.fullPathName()
        split_path_name = path_name.split('|')
        if len(split_path_name) >= 1:
            if split_path_name[-1] == name:
                return True
        if len(split_path_name) >= 2:
            if split_path_name[-2] == name:
                return True

        return False

    @staticmethod
    def creator(obj):
        """
        """
        return ShotMaskDrawOverride(obj)

    @staticmethod
    def draw(context, data):
        """
        """
        return


def initializePlugin(obj):
    """
    """
    pluginFn = om.MFnPlugin(obj, "lanhua.zhou", "1.0.2", "Any")

    try:
        pluginFn.registerNode(PLUGIN_NAME,
                              PLUGIN_TYPE_ID,
                              ShotMaskLocator.creator,
                              ShotMaskLocator.initialize,
                              om.MPxNode.kLocatorNode,
                              DRAW_DB_CLASSIFICATION)
    except:
        om.MGlobal.displayError("Failed to register node: {0}".format(PLUGIN_NAME))

    try:
        omr.MDrawRegistry.registerDrawOverrideCreator(DRAW_DB_CLASSIFICATION,
                                                      DRAW_REGISTRANT_ID,
                                                      ShotMaskDrawOverride.creator)
    except:
        om.MGlobal.displayError("Failed to register draw override: {0}".format(PLUGIN_NAME))


def uninitializePlugin(obj):
    """
    """
    pluginFn = om.MFnPlugin(obj)

    try:
        omr.MDrawRegistry.deregisterDrawOverrideCreator(DRAW_DB_CLASSIFICATION, DRAW_REGISTRANT_ID)
    except:
        om.MGlobal.displayError("Failed to deregister draw override: {0}".format(PLUGIN_NAME))

    try:
        pluginFn.deregisterNode(PLUGIN_TYPE_ID)
    except:
        om.MGlobal.displayError("Failed to unregister node: {0}".format(PLUGIN_NAME))


if __name__ == "__main__":

    cmds.file(f=True, new=True)

    plugin_name = "shotmask.py"
    cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
    cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(plugin_name))

    cmds.evalDeferred('cmds.createNode("zshotmask")')
