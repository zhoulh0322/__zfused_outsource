# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

""" node 节点 """
from __future__ import print_function

import maya.cmds as cmds
import pymel as pm

NODE_ATTR = [ "translateX", 
              "translateY", 
              "translateZ",
              "rotateX", 
              "rotateY", 
              "rotateZ", 
              "scaleX",
              "scaleY",
              "scaleZ",
              "visibility" ]


class Node(object):
    def __init__(self, node, parent = None):
        self._node = node
    
        self._parent = parent
        self._child = []

        # node attr 
        self._object = cmds.nodeType(node)
        
    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, node):
        if isinstance(node, self.__class__):
            self._parent = node
            self._parent.append(self)
        else:
            return False

    def child(self):
        return self._child

    def append(self, node):
        if isinstance(node, self.__class__):
            if node not in self._child:
                self._child.append(node)

    def get_attr(self, attrs = NODE_ATTR, extra_attrs = []):
        """ return node attrs
        """
        _attr_data = {}
        for _attr in attrs:
            _attr_data[_attr] = {}
            # is animation
            _anim_curves = cmds.listConnections("{}.{}".format(self._node, _attr), type = "animCurve")
            if _anim_curves:
                _attr_data[_attr]["is_animation"] = True
                # _anim_curve = _anim_curves[0]
                # _anim_data = {}
                # _attr_list = ["weightedTangents", ""]
                # _anim_data["weightedTangents"] = 
                # _anim_data[""]
                _static_data = cmds.getAttr("{}.{}".format(self._node, _attr))
                _attr_data[_attr]["static_data"] = _static_data
            else:
                _attr_data[_attr]["is_animation"] = False
                # get data
                _value = cmds.getAttr("{}.{}".format(self._node, _attr))
                _attr_data[_attr]["static_data"] = _value

        return _attr_data

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other._node == self._node
        else:
            return Fasle