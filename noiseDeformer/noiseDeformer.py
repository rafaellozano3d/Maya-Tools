import sys
import random
import maya.OpenMaya as om
import maya.OpenMayaMPx as omp
import maya.cmds as cmds

nodeTypeName = "noiseDeformer"
nodeTypeId = om.MTypeId(0x33338)

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


class noiseDeformer(omp.MPxDeformerNode):

    vector = om.MObject()
    vectorX = om.MObject()
    vectorY = om.MObject()
    vectorZ = om.MObject()

    min = om.MObject()
    max = om.MObject()

    def __init__(self):
        omp.MPxDeformerNode.__init__(self)

    def deform(self, block, geoIterator, matrix, geometryIndex):
        # Mesh attributes
        print "ok1"
        kApiVersion = cmds.about(apiVersion=True)

        kInput = omp.cvar.MPxGeometryFilter_input
        inputArray_dh = block.inputArrayValue(kInput)
        inputArray_dh.jumpToElement(geometryIndex)
        inputElement_dh = inputArray_dh.inputValue()

        kInputGeom = omp.cvar.MPxGeometryFilter_inputGeom
        inputGeom_dh = inputElement_dh.child(kInputGeom)
        inMesh = inputGeom_dh.asMesh()

        kEnvelope = omp.cvar.MPxGeometryFilter_envelope
        dataHandleEnvelope = block.inputValue(kEnvelope)
        envelope_value = dataHandleEnvelope.asFloat()

        # Custom attributes
        try:
            vectorX_dh = block.inputValue(noiseDeformer.vectorX)
            vectorY_dh = block.inputValue(noiseDeformer.vectorY)
            vectorZ_dh = block.inputValue(noiseDeformer.vectorZ)
            min_dh = block.inputValue(noiseDeformer.min)
            max_dh = block.inputValue(noiseDeformer.max)
        except ImportError:
            sys.stderr.write("Failed to get MDataHandle")

        min_value = min_dh.asFloat()
        max_value = max_dh.asFloat()

        # Get mesh normals
        mFloatVectorArray_normal = om.MFloatVectorArray()
        mFnMesh = om.MFnMesh(inMesh)
        mFnMesh.getVertexNormals(False, mFloatVectorArray_normal, om.MSpace.kObject)


        while(not geoIterator.isDone()):
            pointPosition = geoIterator.position()
            vectorX_dh.setFloat(random.uniform(min_value, max_value))
            vectorY_dh.setFloat(random.uniform(min_value, max_value))
            vectorZ_dh.setFloat(random.uniform(min_value, max_value))

            vectorX_value = vectorX_dh.asFloat()
            vectorY_value = vectorY_dh.asFloat()
            vectorZ_value = vectorZ_dh.asFloat()

            # print "vertex = ", pointPosition.x, ",", pointPosition.y, ",", pointPosition.z
            pointPosition.x = pointPosition.x + vectorX_value * envelope_value
            pointPosition.y = pointPosition.y + vectorY_value * envelope_value
            pointPosition.z = pointPosition.z + vectorZ_value * envelope_value

            geoIterator.setPosition(pointPosition)
            geoIterator.next()

        print "sale"

def deformerCreator():
    nodePtr = omp.asMPxPtr(noiseDeformer())
    return nodePtr

def nodeInitializer():
    nAttr = om.MFnNumericAttribute()
    cAttr = om.MFnCompoundAttribute()

    # Create input attributes
    noiseDeformer.vectorX = nAttr.create("v1 X", "v1x",
                                               om.MFnNumericData.kFloat)
    MAKE_INPUT(nAttr)
    nAttr.setWritable(False)
    noiseDeformer.vectorY = nAttr.create("v1 Y", "v1y",
                                               om.MFnNumericData.kFloat)
    MAKE_INPUT(nAttr)
    nAttr.setWritable(False)
    noiseDeformer.vectorZ = nAttr.create("v1 Z", "v1z",
                                               om.MFnNumericData.kFloat)
    MAKE_INPUT(nAttr)
    nAttr.setWritable(False)

    noiseDeformer.min = nAttr.create("minRange", "min", om.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    noiseDeformer.max = nAttr.create("maxRange", "max", om.MFnNumericData.kFloat, 10.0)
    MAKE_INPUT(nAttr)

    # create compound attributes
    noiseDeformer.vector = cAttr.create("vector", "v")
    cAttr.addChild(noiseDeformer.vectorX)
    cAttr.addChild(noiseDeformer.vectorY)
    cAttr.addChild(noiseDeformer.vectorZ)

    # add attributes
    noiseDeformer.addAttribute(noiseDeformer.vector)
    noiseDeformer.addAttribute(noiseDeformer.min)
    noiseDeformer.addAttribute(noiseDeformer.max)

    kApiVersion = cmds.about(apiVersion=True)
    if kApiVersion < 201600:
        outputGeom = omp.cvar.MPxDeformerNode_outputGeom
    else:
        outputGeom = omp.cvar.MPxGeometryFilter_outputGeom

    noiseDeformer.attributeAffects(noiseDeformer.vector, outputGeom)
    noiseDeformer.attributeAffects(noiseDeformer.min, outputGeom)
    noiseDeformer.attributeAffects(noiseDeformer.max, outputGeom)

def initializePlugin(mobject):
    mplugin = omp.MFnPlugin(mobject, "rafaellozano3d.com/devBlog", "1.0")
    try:
        mplugin.registerNode(nodeTypeName, nodeTypeId, deformerCreator, nodeInitializer, omp.MPxNode.kDeformerNode)
    except Exception:
        sys.stderr.write("Failed to register node")
        raise


def uninitializePlugin(mobject):
    mplugin = omp.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(nodeTypeId)
    except Exception:
        sys.stderr.write("Failed to deregister node")
        raise
