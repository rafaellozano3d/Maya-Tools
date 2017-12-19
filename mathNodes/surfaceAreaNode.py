import maya.OpenMaya as om
import maya.OpenMayaMPx as omp
from maya.app.type.typeToolSetup import connectTypeAdjustDeformer

nodeTypeName = "surfaceAreaNode"
nodeTypeId = om.MTypeId(0x33333)


def MAKE_INPUT(attr):
    # Macro to define an attribute as input attribute
    attr.setKeyable(True)
    attr.setStorable(True)
    attr.setReadable(False)
    attr.setWritable(True)


def MAKE_OUTPUT(attr):
    # Macro to define an attribute as input attribute
    attr.setKeyable(False)
    attr.setStorable(False)
    attr.setReadable(True)
    attr.setWritable(False)


class surfaceAreaNode(omp.MPxNode):

    meshNode = om.MFnMesh()
    meshObj = om.MObject()
    meshDepNode = om.MFnDependencyNode()
    meshDagPath = om.MDagPath()

    inputMeshAttr = om.MObject()
    areaAttr = om.MObject()

    def __init__(self):
        omp.MPxNode.__init__(self)

    def compute(self, plug, block):
        print "> compute"


def nodeCreator():
    return omp.asMPxPtr(surfaceAreaNode())


def nodeInitializer():
    # Create DepNode from current mesh selected
    selected = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(selected)
    surfaceAreaNode.meshDagPath = om.MDagPath()
    selected.getDagPath(0, surfaceAreaNode.meshDagPath)
    surfaceAreaNode.meshDagPath.extendToShape()
    selected.clear()
    selected.add(surfaceAreaNode.meshDagPath)
    selected.getDependNode(0, surfaceAreaNode.meshObj)
    surfaceAreaNode.meshDepNode = om.MFnDependencyNode(surfaceAreaNode.meshObj)

    print "name = ", surfaceAreaNode.meshDepNode.name()
    surfaceAreaNode.meshNode = om.MFnMesh(surfaceAreaNode.meshDagPath.node())

    # Create Attributes
    typedAttr = om.MFnTypedAttribute()
    surfaceAreaNode.inputMeshAttr = typedAttr.create("inputMesh",
                                                     "inMesh",
                                                     om.MFnNumericData.kMesh)

    nAttr = om.MFnNumericAttribute()
    surfaceAreaNode.areaAttr = nAttr.create("area",
                                            "area",
                                            om.MFnNumericData.kFloat)
    MAKE_OUTPUT(nAttr)

    # Add Attributes
    surfaceAreaNode.addAttribute(surfaceAreaNode.inputMeshAttr)
    surfaceAreaNode.addAttribute(surfaceAreaNode.areaAttr)

    surfaceAreaNode.attributeAffects(surfaceAreaNode.inputMeshAttr, surfaceAreaNode.areaAttr)

    dgMod = om.MDGModifier()
    thisDepNode = om.MFnDependencyNode(surfaceAreaNode.inputMeshAttr)
    print "thisdepnode = ", thisDepNode.name()

def initializePlugin(obj):
    plugin = omp.MFnPlugin(obj)
    plugin.registerNode(nodeTypeName, nodeTypeId, nodeCreator,
                        nodeInitializer, omp.MPxNode.kDependNode)


def uninitializePlugin(obj):
    plugin = omp.MFnPlugin(obj)
    plugin.deregisterNode(nodeTypeId)
