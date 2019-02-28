# coding:utf-8
# author binglu.wang

import os
import re
import maya.cmds as cmds
import time

TEXT_NODE = ["file", "imagePlane", "RedshiftNormalMap","RedshiftCameraMap"]
TEXTURE_ATTR_DICT = {
    "file" : "fileTextureName",
    "imagePlane": "imageName",
    "RedshiftNormalMap":"tex0",
    "RedshiftCameraMap":"tex0",
}

class CheckShader(object):
    def __init__(self):
        self.ture_sg_name = {}
        self.ture_mat_name = {}
        self.ture_tex_name = {}
        self.unuseSG = []

        self.sgfilters = [["M"],["sg"]]
        self.matfilters = [["M"],["mat"]]
        self.texfilters = [["T"]]
        # ,["col","spe","nor","bump","dis"]]
        self.layerfilters =["RedshiftMaterialBlender","layeredShader"]

        self.defalut_mats = ["lambert1","particleCloud1"]
        self.defalut_SGs = ["initialParticleSE", "initialShadingGroup"]

        self.allmats = self._get_mat()
        self.assetname = ""
        self.assettype = ""

    def _get_asset_name(self):
        for i in cmds.ls(type = "transform"):
            if cmds.objExists("%s.treeName"%i):
                self.assetname = cmds.getAttr("%s.treeName"%i)

    def _get_mat(self):
        return [i for i in cmds.ls(mat = 1) if i not in self.defalut_mats]

    def _set_true_name(self,meshstr):
        _t_sg_name = "M_%s_sg"%meshstr
        _t_mat_name = "M_%s_mat"%meshstr
        _t_tex_name = "T_%s"%meshstr
        return _t_sg_name,_t_mat_name,_t_tex_name

    def _set_filter(self,meshstr):
        _ture = meshstr.split("{}_{}".format(self.assettype,self.assetname))[-1]
        if _ture.startswith("_"):
            _ture = _ture[1:]
        return "{}_{}".format(self.assetname,_ture)

    def check_mesh(self,sg_c):
        mesh_c = cmds.listConnections(sg_c,scn = 1,type = "mesh")
        if not mesh_c:
            if sg_c not in self.defalut_SGs:
                _info = u"Error link SG node:  %s\n"%sg_c
                # errorlist.append(_info)
                self.unuseSG.append(sg_c)
                return _info,None
            else:
                return None,None
        mesh_c = list(set(mesh_c))
        # print mesh_c
        if len(mesh_c) > 1:
            _temps = []
            for _i in mesh_c:
                if re.findall("\.f\[\d+\]",_i):
                    _i = _i.replace(re.findall("\.f\[\d+\]",_i)[0],"")
                if re.findall("\.f\[\d+.\d+\]",_i):
                    _i = _i.replace(re.findall("\.f\[\d+.\d+\]",_i)[-1],"")
                _temps.append(self._set_filter(_i))
        else:
            _temps = [self._set_filter(mesh_c[0])]
        if not _temps:
            _info = u"SGnode isn't same with mesh:  %s\n"%sg_c
            return _info,None
        strlist = []
        for _s in _temps:
            if _s[-1].isdigit():
                _num = len(re.findall("\d+",_s)[-1])
                _s = _s[:-_num]
                if _s.endswith("_"):
                    _s = _s[:-1]
            strlist.append(_s)
        return None,strlist

    def check_sg(self,sg_c,mesh_filters):
        mesh_c = cmds.listConnections(sg_c,scn = 1,type = "mesh")
        if mesh_c and sg_c in self.defalut_SGs:
            _info = u"Use default material mesh:  %s\n"%"\n                            ".join(mesh_c)
            return _info
        if not self.check_filters(sg_c,*self.sgfilters):
            _info = u"Wrong name SG node:  %s\n"%sg_c
            return _info
        true_n = [i for i in mesh_filters if i in sg_c]
        if not true_n:
            _info = u"SGnode isn't same with mesh:  %s\n"%sg_c
            return _info
        return None

    def check_mat(self,sg_c,mesh_filters):
        mat_c = cmds.listConnections("%s.surfaceShader"%sg_c)
        if mat_c:
            for _c in mat_c:
                self.ture_mat_name[_c] = "M_{}_mat".format(mesh_filters[0])
                if _c in self.allmats:
                    self.allmats.remove(_c)
                # else:
                #     if _c not in self.defalut_mats:
                #         _info = u"Error material type:  %s\n"%_c
                #         return _info
                if not self.check_filters(_c,*self.matfilters):
                    _info = u"Wrong name material node:  %s\n"%_c
                    return _info
                true_n = [i for i in mesh_filters if i in _c.split(":")[-1]]
                if not true_n:
                    _info = u"Material name isn't same with mesh:  %s\n"%_c
                    return _info
        return None

    def check_secondary_mat(self):
        _info = []
        for _mat in self.allmats:
            _sg = self._get_node(_mat,"shadingEngine",True,"transform","mesh")
            if not _sg:
                _info.append(u"Error link material:  %s\n"%_mat)
                continue
            if self.ture_sg_name.has_key(_sg[0]):
                _filter = "_".join(self.ture_sg_name[_sg[0]].split("_")[1:-1])
            else:
                _filter = "_".join(_sg[0].split("_")[1:-1])
            self.ture_mat_name[_mat] = "M_{}_mat".format(_filter)
            if not self.check_filters(_mat,*self.matfilters):
                _info.append(u"Wrong name material node:  %s\n"%_mat)
            if not _filter in _mat.split(":")[-1]:
                _info.append(u"Material name isn't same with mesh:  %s\n"%_mat)
        return _info


    def check_filters(self,node,*filters):
        """
        判断字符串是否符合过滤条件
        """
        if len(filters) == 1:
            _F = filters[0]
            _L = None
        else :
            _F,_L = filters
        if ":" in node:
            node = node.split(":")[-1]
        _node_ele = node.split("_")

        if len(_node_ele) < 2:
            return False
        _index = re.findall("\d+",_node_ele[-1])
        if _index:
            if _node_ele[-1].find(_index[0]) < 1:
                return False
            _node_l_str = _node_ele[-1].replace(_index[0],"")
            if _node_l_str not in _node_ele[-1]:
                return False
            if _node_ele[0] in _F and (not _L or _node_l_str in _L):
                return True
            else:
                return False
        else:
            if _node_ele[0] in _F and (not _L or _node_ele[-1] in _L):
                return True
            else:
                return False

    def _get_node(self,node,nodetype,io = False,*args):
        # 获取上下游指定类型的链接节点
        _c_node = node
        filenode_list = []
        i = 0
        # 防止死循环
        while i < 10:
            _c_list = cmds.listConnections(_c_node,d = io, s = not io,scn = 1)
            if _c_list:
                _c_list = list(set(_c_list))
                for j in _c_list:
                    if cmds.nodeType(j) == nodetype:
                        filenode_list.append(j)
                    if args and cmds.nodeType(j) in args:
                        _c_list.remove(j)
                _c_node = _c_list
            else:
                break
            i += 1
        if filenode_list:
            filenode_list = list(set(filenode_list))
        return filenode_list

    def _get_file_dict(self):
        file_dict = {}
        self._get_asset_name()
        def set_value(node,path,name):
            if file_dict.has_key(path):
                _value = file_dict[path]
                _value["node"].append(node)
            else:
                _value = {"node":[node],"name":name}
            return _value
        _files = cmds.ls(type = TEXT_NODE)
        if _files:
            for _file in _files:
                _type = cmds.nodeType(_file)
                _path = cmds.getAttr("{}.{}".format(_file,TEXTURE_ATTR_DICT[_type]))
                if _type == "file":
                    _mode = cmds.getAttr("%s.uvTilingMode"%_file)
                    _ani = cmds.getAttr("%s.useFrameExtension"%_file)
                else:
                    _mode,_ani = None,None
                if _path and os.path.exists(_path):
                    _p,_n = os.path.split(_path)
                    _n = os.path.splitext(_n)[0]
                    if _n[-1].isdigit():
                        if re.findall("\.\d+",_n):
                            _num = len(re.findall("\.\d+",_n)[-1])
                            _n = _n[:-_num]
                            # _n = _n.replace(re.findall("\.\d+",_n)[-1],"")
                        else:
                            # _n = _n.replace(re.findall("\d+",_n)[-1],"")
                            _num = len(re.findall("\d+",_n)[-1])
                            _n = _n[:-_num]
                        if _n.endswith("_"):
                            _n = _n[:-1]
                    _key = "_>v<_".join([_path,str(_mode),str(_ani)])
                    file_dict[_key] = set_value(_file,_key,_n)
                else:
                    _key = "_>v<_".join([_path,str(_mode),str(_ani)])
                    file_dict[_key] = set_value(_file,_key,None)
                    continue
        return file_dict

    def check_texture(self):
        file_dict = self._get_file_dict()
        _info = []
        for _path in file_dict.keys():
            if not file_dict[_path]["name"]:
                _info.append(u"Error filenode:  %s\n"%"\n".join(file_dict[_path]["node"]))
                continue
            # _filter = file_dict[_path]["filter"]
            _name = file_dict[_path]["name"]
            _nodes = file_dict[_path]["node"]
            _real_path = _path.split("_>v<_")[0]
            if not self.check_filters(_name,*self.texfilters):
                _info.append(u"Wrong name Texture:  %s\n"%_real_path)
                continue
            _sgs = self._get_node(_nodes,"shadingEngine",True,"transform","mesh")
            if not _sgs:
                _info.append(u"Error link file node:  %s\n"%"\n".join(_nodes))
                continue
            _meshs  = cmds.listConnections(_sgs,scn = 1,type = "mesh")
            if not _meshs:
                continue
            strlist = []
            for i in _meshs:
                _f = self._set_filter(i)
                if _f[-1].isdigit():
                    _num = len(re.findall("\d+",_f)[-1])
                    _f = _f[:-_num]
                    if _f.endswith("_"):
                        _f = _f[:-1]
                if _f in _name:
                    strlist.append(_f)
            if not strlist:
                _info.append(u"Texture name isn't same with mesh:  %s\n"%_real_path)
            texname = os.path.basename(_real_path)
            _same = [_i for _i in file_dict.keys() if texname in _i]
            if len(_same) > 1:
                _showlist = [_i.split("_>v<_")[0] for _i in _same]
                _info.append(u"Has same Texture:  %s\n"%"<==>".join(_showlist))
        _info = list(set(_info))
        return _info

    def check_shader(self):
        info = []
        self._get_asset_name()
        if self.assetname:
            allSGs = cmds.ls(type = "shadingEngine")
            for SG_c in allSGs:
                _,_mesh_f = self.check_mesh(SG_c)
                if _mesh_f:
                    # print SG_c
                    _info = self.check_sg(SG_c,_mesh_f)
                    if _info:
                        self.ture_sg_name[SG_c] = "M_{}_sg".format(_mesh_f[0])
                        info.append(_info)
                    _info = self.check_mat(SG_c,_mesh_f)
                    info.append(_info)
                else:
                    info.append(_)
            if self.allmats:
                _info = self.check_secondary_mat()
                info.extend(_info)
        else:
            info = []
        info = list(set(info))
        if None in info:
            info.remove(None)
        return info

    def _set_name(self,_dict):
        for k,v in _dict.items():
            if k != v:
                try:
                    print "rename {} to {}".format(k,v)
                    cmds.rename(k,v)
                except:
                    pass

    def repair(self):
        self.check_shader()
        if self.ture_sg_name:
            self._set_name(self.ture_sg_name)
        if self.ture_mat_name:
            self._set_name(self.ture_mat_name)




if __name__ == '__main__':
    a = CheckShader()
    time_s = time.time()
    print a.check_shader()
    print a.check_texture()
    # print a.repair()
    # a._get_file_dict()
    time_e = time.time()
    print time_e-time_s
    # a.repair()