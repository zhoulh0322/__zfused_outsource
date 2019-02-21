# coding:utf-8
# toolName：Check Skin Weight
# Author：wangbinglu

from functools import partial
import maya.cmds as cmds
import maya.api.OpenMaya as om

wrongInfo = {}

def WBLUI():
    def show():
        import zfused_maya.core.restricted as restricted
        import maya.cmds as cmds
        _has_per, _info = restricted.restricted()
        if not _has_per:
            cmds.confirmDialog(message = _info)
            return False
        return True

    if show():
        name = u'CheckSkinWeight'
        version = "0.1"
        if cmds.window(name,exists = True):
            cmds.deleteUI(name,window = True)
        cmds.window(name,t = "%s_%s"%(name,version),w = 450)
        layout1 = cmds.columnLayout(w = 455,h = 350,bgc = (0.2,0.2,0.2))
        layout2 = cmds.formLayout(w = 455,h = 350,p = layout1)
        meshTextUI     = cmds.text(w = 220,l = u'蒙皮超标模型',al = "center",p = layout2,fn = "fixedWidthFont")
        verticesTextUI = cmds.text(w = 220,l = u'对应模型的点',al = "center",p = layout2,fn = "fixedWidthFont")
        meshInfoUI     = cmds.textScrollList(w = 220,p = layout2)
        verticesInfoUI = cmds.textScrollList(w = 220,p = layout2,ams = 1)
        checkBtnUI     = cmds.button(w = 445,h = 30,l = "Do Check", c = lambda x:WBLdoCheck(meshInfoUI,verticesInfoUI),p = layout2,bgc = (0.2,0.3,0.3))
        cmds.formLayout(layout2, e = 1, af = [(meshTextUI,"top",5),(meshTextUI,"left",5),
                                              (verticesTextUI,"top",5),(verticesTextUI,"right",5),
                                              (meshInfoUI,"left",5),(verticesInfoUI,"right",5),
                                              (checkBtnUI,"bottom",5),(checkBtnUI,"left",5),(checkBtnUI,"right",5)],
                                        ac = [(meshInfoUI, "top", 5, meshTextUI),
                                              (verticesInfoUI, "top", 5, verticesTextUI),
                                              (verticesTextUI, "left", 5, meshTextUI),
                                              (verticesInfoUI, "left", 5, meshInfoUI),
                                              (verticesInfoUI, "bottom", 5, checkBtnUI),
                                              (meshInfoUI, "bottom", 5, checkBtnUI)])
        cmds.textScrollList(meshInfoUI, e=1, sc=partial(WBLSelectMesh, meshInfoUI,verticesInfoUI))
        cmds.textScrollList(verticesInfoUI, e=1, sc=partial(WBLSelectVer,verticesInfoUI))
        #if arg(verticesInfoUI,meshInfoUI) == False:
        cmds.showWindow(name)

def WBLSelectMesh(meshInfoUI,verticesInfoUI,*args):
    sels = cmds.textScrollList(meshInfoUI, q=1, si=1)
    cmds.select(sels, r=1)
    cmds.textScrollList(verticesInfoUI, e = 1,ra = 1)
    for sel in sels:
        WBLwrongVerInfo(verticesInfoUI,sel)
        
def WBLSelectVer(verticesInfoUI,*args):
    sels = cmds.textScrollList(verticesInfoUI, q=1, si=1)
    cmds.select(sels,r=1)
    
def WBLgetMeshVer(shapename):
    verName = []
    trans = cmds.listRelatives(shapename,p = 1,pa = 1)[0]
    mSel = om.MSelectionList()
    mDagPath = om.MDagPath()
    mSel.clear()
    mSel.add(trans)
    mDagPath = mSel.getDagPath(0)
    mFnMesh = om.MFnMesh(mDagPath)
    vertices = mFnMesh.numVertices
    for i in xrange(vertices):
        verName.append("%s.vtx[%s]"%(trans,i))
    return verName

def WBLcheckSkinWeight():
    verticesName = []
    allskinClusters = cmds.ls(type = "skinCluster")
    for skinClusters in allskinClusters:
        objShapeName = cmds.skinCluster(skinClusters,q = 1,g = 1)
        if cmds.nodeType(objShapeName) == "mesh":
            allvertices = WBLgetMeshVer(objShapeName)
            if allvertices:
                for vertices in allvertices:
                    weightlist = set(cmds.skinPercent(skinClusters,vertices,q = 1,v = 1))
                    try:
                        weightlist.remove(0.0)
                    except:
                        pass
                    if len(weightlist) > 4:
                        verticesName.append(vertices)
    if verticesName:
        for verticeName in verticesName:
            wrongInfo[verticeName.split(".")[0]] = []
        for key in wrongInfo.keys():
            tempList = []
            for index in verticesName:
                if key in index:
                    tempList.append(index)
            wrongInfo[key] = tempList
    # return wrongInfo

def WBLwrongVerInfo(verticesInfoUI,*args):
    if wrongInfo:
        if not args:
            firstElement = wrongInfo.keys()[0]
            for i in wrongInfo[firstElement]:
                cmds.textScrollList(verticesInfoUI, e=1, a = i)
        else:
            for index in wrongInfo[args[0]]:
                cmds.textScrollList(verticesInfoUI, e=1, a = index)
    else:
        cmds.confirmDialog(title = '',message = u'权重未发现异常')
        #     return wrongInfo
        # else:
        #     return False

def WBLshowInfo(meshInfoUI):
    if wrongInfo:
        for key in wrongInfo.keys():
            cmds.textScrollList(meshInfoUI, e=1, a = key)

def WBLdoCheck(meshInfoUI,verticesInfoUI):
    cmds.textScrollList(meshInfoUI, e=1, ra = 1)
    cmds.textScrollList(verticesInfoUI, e=1, ra = 1)
    try:
        WBLcheckSkinWeight()
        WBLshowInfo(meshInfoUI)
        WBLwrongVerInfo(verticesInfoUI)
    except:
        cmds.confirmDialog(title = '',message = u'运行失败，请检查文件内是否存在绑定模型')
# print WBLcheckSkinWeight()
if __name__ == '__main__':
    WBLUI()
