'''
Created on 12 dic. 2017

@author: rafaellozano3d.com
'''

import maya.OpenMaya as om
import maya.OpenMayaMPx as omp

nodeTypeName = "angleBetweenVectorsNode"
nodeTypeId = om.MTypeId(0x33333)


def MAKE_INPUT(attr):
    attr.setKeyable(True)
    attr.setStorable(True)
    attr.setReadable(True)
    attr.setWritable(True)


def MAKE_OUTPUT(attr):
    attr.setKeyable(False)
    attr.setStorable(False)
    attr.setReadable(True)
    attr.setWritable(False)

class angleBetweenVectorsNode(omp.MPxNode):

    def __init__(self):
        print "> angleBetweenVectorsNode.__init__"
        omp.MPxNode.__init__(self)

    def compute(self, plug, block):
        print "> compute"


def nodeCreator():
    return omp.asMPxPtr(angleBetweenVectorsNode())


def nodeInitializer():
    print "> nodeInitializer"
    #Create V1 Plug
    cmpV1Attr = om.MFnCompoundAttribute()
    v1CmpAttr = cmpV1Attr.create("v1", "v1")

    nAttr = om.MFnNumericAttribute()
    v1XAttr = nAttr.create("v1X", "v1X", om.MFnNumericData.kFloat)
    cmpV1Attr.addChild(v1XAttr)

    nAttr = om.MFnNumericAttribute()
    v1YAttr = nAttr.create("v1Y", "v1Y", om.MFnNumericData.kFloat)
    cmpV1Attr.addChild(v1YAttr)

    nAttr = om.MFnNumericAttribute()
    v1ZAttr = nAttr.create("v1Z", "v1Z", om.MFnNumericData.kFloat)
    cmpV1Attr.addChild(v1ZAttr)

    angleBetweenVectorsNode.addAttribute(v1CmpAttr)

    cmpV1Attr.setKeyable(True)
    cmpV1Attr.setStorable(True)
    cmpV1Attr.setWritable(True)

    # Create V2 Plug
    cmpV2Attr = om.MFnCompoundAttribute()
    v2CmpAttr = cmpV2Attr.create("v2", "v2")

    nAttr = om.MFnNumericAttribute()
    v2XAttr = nAttr.create("v2X", "v2X", om.MFnNumericData.kFloat)
    cmpV2Attr.addChild(v2XAttr)

    nAttr = om.MFnNumericAttribute()
    v2YAttr = nAttr.create("v2Y", "v2Y", om.MFnNumericData.kFloat)
    cmpV2Attr.addChild(v2YAttr)

    nAttr = om.MFnNumericAttribute()
    v2ZAttr = nAttr.create("v2Z", "v2Z", om.MFnNumericData.kFloat)
    cmpV2Attr.addChild(v2ZAttr)

    angleBetweenVectorsNode.addAttribute(v2CmpAttr)

    cmpV2Attr.setKeyable(True)
    cmpV2Attr.setStorable(True)
    cmpV2Attr.setWritable(True)

    # Create V3 Plug
    cmpV3Attr = om.MFnCompoundAttribute()
    v3CmpAttr = cmpV3Attr.create("v3", "v3")

    nAttr = om.MFnNumericAttribute()
    v3XAttr = nAttr.create("v3X", "v3X", om.MFnNumericData.kFloat)
    cmpV3Attr.addChild(v3XAttr)

    nAttr = om.MFnNumericAttribute()
    v3YAttr = nAttr.create("v3Y", "v3Y", om.MFnNumericData.kFloat)
    cmpV3Attr.addChild(v3YAttr)

    nAttr = om.MFnNumericAttribute()
    v3ZAttr = nAttr.create("v3Z", "v3Z", om.MFnNumericData.kFloat)
    cmpV3Attr.addChild(v3ZAttr)

    angleBetweenVectorsNode.addAttribute(v3CmpAttr)

    cmpV3Attr.setKeyable(True)
    cmpV3Attr.setStorable(True)
    cmpV3Attr.setWritable(True)

    angleBetweenVectorsNode.attributeAffects(v1CmpAttr, cmpV3Attr)
    angleBetweenVectorsNode.attributeAffects(v2CmpAttr, cmpV3Attr)


def initializePlugin(obj):
    print "> initializePlugin"
    # Aqui se registra el nodo
    plugin = omp.MFnPlugin(obj)
    plugin.registerNode(nodeTypeName, nodeTypeId, nodeCreator,
                        nodeInitializer, omp.MPxNode.kDependNode)


def uninitializePlugin(obj):
    print ">_uninitializePlugin"
    # Aqui se elimina del registro
    plugin = omp.MFnPlugin(obj)
    plugin.deregisterNode(nodeTypeId)
