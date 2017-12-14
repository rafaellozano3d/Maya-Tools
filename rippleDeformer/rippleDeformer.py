import sys
import math
import maya.OpenMaya as om
import maya.OpenMayaMPx as omp

nodeTypeName = "rippleDeformer"
nodeTypeId = om.MTypeId(0x33332)


class rippleNode(omp.MPxDeformerNode):

    mObj_Amplitude = om.MObject()
    mObj_Displace = om.MObject()

    def __init__(self):
        omp.MPxDeformerNode.__init__(self)

    def deform(self, dataBlock, geoIterator, matrix, geometryIndex):

        input = omp.cvar.MPxGeometryFilter_input
        dataHandleInputArray = dataBlock.inputArrayValue(input)
        dataHandleInputArray.jumpToElement(geometryIndex)
        dataHandleInputElement = dataHandleInputArray.inputValue()

        inputGeom = omp.cvar.MPxGeometryFilter_inputGeom
        dataHandleInputGeom = dataHandleInputElement.child(inputGeom)
        inMesh = dataHandleInputGeom.asMesh()

        envelope = omp.cvar.MPxGeometryFilter_envelope
        dataHandleEnvelope = dataBlock.inputValue(envelope)
        envelopeValue = dataHandleEnvelope.asFloat()

        dataHandleAmplitude = dataBlock.inputValue(rippleNode.mObj_Amplitude)
        amplitudeValue = dataHandleAmplitude.asFloat()

        dataHandleDisplace = dataBlock.inputValue(rippleNode.mObj_Displace)
        displaceValue = dataHandleDisplace.asFloat()

        mFloatVectorArray_normal = om.MFloatVectorArray()
        mFnMesh = om.MFnMesh(inMesh)
        mFnMesh.getVertexNormals(False, mFloatVectorArray_normal, om.MSpace.kObject)

        while(not geoIterator.isDone()):
            pointPosition = geoIterator.position()
            pointPosition.x = pointPosition.x + math.sin(geoIterator.index() + displaceValue) * amplitudeValue * mFloatVectorArray_normal[geoIterator.index()].x * envelopeValue
            pointPosition.y = pointPosition.y + math.sin(geoIterator.index() + displaceValue) * amplitudeValue * mFloatVectorArray_normal[geoIterator.index()].y * envelopeValue
            pointPosition.z = pointPosition.z + math.sin(geoIterator.index() + displaceValue) * amplitudeValue * mFloatVectorArray_normal[geoIterator.index()].z * envelopeValue
            geoIterator.setPosition(pointPosition)
            geoIterator.next()

def deformerCreator():
    nodePtr = omp.asMPxPtr(rippleNode())
    return nodePtr

def nodeInitializer():
    mFnAttr = om.MFnNumericAttribute()
    rippleNode.mObj_Amplitude = mFnAttr.create("AttributeValue", "AttrVal", om.MFnNumericData.kFloat, 0.0)
    mFnAttr.setKeyable(1)
    mFnAttr.setMin(0.0)
    mFnAttr.setMax(1.0)

    rippleNode.mObj_Displace = mFnAttr.create("DisplaceValue", "DispVal", om.MFnNumericData.kFloat, 0.0)
    mFnAttr.setKeyable(1)
    mFnAttr.setMin(0.0)
    mFnAttr.setMax(10.0)

    rippleNode.addAttribute(rippleNode.mObj_Amplitude)
    rippleNode.addAttribute(rippleNode.mObj_Displace)

    outputGeom = omp.cvar.MPxGeometryFilter_outputGeom
    rippleNode.attributeAffects(rippleNode.mObj_Amplitude, outputGeom)
    rippleNode.attributeAffects(rippleNode.mObj_Displace, outputGeom)

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
