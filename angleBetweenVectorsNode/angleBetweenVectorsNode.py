import sys
import math
import maya.OpenMaya as om
import maya.OpenMayaMPx as omp

nodeTypeName = "angleBetweenVectorsNode"
nodeTypeId = om.MTypeId(0x33333)


def MAKE_INPUT(attr):
    # Macro to define an attribute as input attribute
    attr.setKeyable(True)
    attr.setStorable(True)
    attr.setReadable(True)
    attr.setWritable(True)


def MAKE_OUTPUT(attr):
    # Macro to define an attribute as input attribute
    attr.setKeyable(False)
    attr.setStorable(False)
    attr.setReadable(True)
    attr.setWritable(False)


class angleBetweenVectorsNode(omp.MPxNode):
    """Class to define the node methods and
    attributes. We almost compute the output
    in compute method
    """

    v1 = om.MObject()
    v1x = om.MObject()
    v1y = om.MObject()
    v1z = om.MObject()

    v2 = om.MObject()
    v2x = om.MObject()
    v2y = om.MObject()
    v2z = om.MObject()

    v3 = om.MObject()
    v3x = om.MObject()
    v3y = om.MObject()
    v3z = om.MObject()

    def __init__(self):
        omp.MPxNode.__init__(self)

    def compute(self, plug, block):
        # Get dataHandle to get and set the attributes
        try:
            v1x_dh = block.inputValue(angleBetweenVectorsNode.v1x)
            v1y_dh = block.inputValue(angleBetweenVectorsNode.v1y)
            v1z_dh = block.inputValue(angleBetweenVectorsNode.v1z)

            v2x_dh = block.inputValue(angleBetweenVectorsNode.v2x)
            v2y_dh = block.inputValue(angleBetweenVectorsNode.v2y)
            v2z_dh = block.inputValue(angleBetweenVectorsNode.v2z)

            v3x_dh = block.inputValue(angleBetweenVectorsNode.v3x)
            v3y_dh = block.inputValue(angleBetweenVectorsNode.v3y)
            v3z_dh = block.inputValue(angleBetweenVectorsNode.v3z)

        except ImportError:
            sys.stderr.write("Failed to get MDataHandle")

        v1x_value = v1x_dh.asFloat()
        v1y_value = v1y_dh.asFloat()
        v1z_value = v1z_dh.asFloat()

        v2x_value = v2x_dh.asFloat()
        v2y_value = v2y_dh.asFloat()
        v2z_value = v2z_dh.asFloat()

        # Create two vectors with the input values
        v1_vector = om.MVector()
        v1_vector.x = v1x_value
        v1_vector.y = v1y_value
        v1_vector.z = v1z_value

        v2_vector = om.MVector()
        v2_vector.x = v2x_value
        v2_vector.y = v2y_value
        v2_vector.z = v2z_value

        v1_vector.normalize()
        v2_vector.normalize()

        # Calculate the angle between two vectors
        v3_vector = v1_vector ^ v2_vector

        v3x_dh.setFloat(math.degrees(v3_vector.x))
        v3y_dh.setFloat(math.degrees(v3_vector.y))
        v3z_dh.setFloat(math.degrees(v3_vector.z))


def nodeCreator():
    return omp.asMPxPtr(angleBetweenVectorsNode())


def nodeInitializer():
    nAttr = om.MFnNumericAttribute()
    cAttr = om.MFnCompoundAttribute()

    # Create input attributes
    angleBetweenVectorsNode.v1x = nAttr.create("v1 X", "v1x",
                                               om.MFnNumericData.kFloat)
    MAKE_INPUT(nAttr)
    angleBetweenVectorsNode.v1y = nAttr.create("v1 Y", "v1y",
                                               om.MFnNumericData.kFloat)
    MAKE_INPUT(nAttr)
    angleBetweenVectorsNode.v1z = nAttr.create("v1 Z", "v1z",
                                               om.MFnNumericData.kFloat)
    MAKE_INPUT(nAttr)

    angleBetweenVectorsNode.v2x = nAttr.create("v2 X", "v2x",
                                               om.MFnNumericData.kFloat)
    MAKE_INPUT(nAttr)
    angleBetweenVectorsNode.v2y = nAttr.create("v2 Y", "v2y",
                                               om.MFnNumericData.kFloat)
    MAKE_INPUT(nAttr)
    angleBetweenVectorsNode.v2z = nAttr.create("v2 Z", "v2z",
                                               om.MFnNumericData.kFloat)
    MAKE_INPUT(nAttr)

    # Create output attribute
    angleBetweenVectorsNode.v3x = nAttr.create("v3 X", "v3x",
                                               om.MFnNumericData.kFloat)
    angleBetweenVectorsNode.v3y = nAttr.create("v3 Y", "v3y",
                                               om.MFnNumericData.kFloat)
    angleBetweenVectorsNode.v3z = nAttr.create("v3 Z", "v3z",
                                               om.MFnNumericData.kFloat)
    MAKE_OUTPUT(nAttr)

    # create compound attributes
    angleBetweenVectorsNode.v1 = cAttr.create("v1", "v1")
    cAttr.addChild(angleBetweenVectorsNode.v1x)
    cAttr.addChild(angleBetweenVectorsNode.v1y)
    cAttr.addChild(angleBetweenVectorsNode.v1z)

    angleBetweenVectorsNode.v2 = cAttr.create("v2", "v2")
    cAttr.addChild(angleBetweenVectorsNode.v2x)
    cAttr.addChild(angleBetweenVectorsNode.v2y)
    cAttr.addChild(angleBetweenVectorsNode.v2z)

    angleBetweenVectorsNode.v3 = cAttr.create("v3", "v3")
    cAttr.addChild(angleBetweenVectorsNode.v3x)
    cAttr.addChild(angleBetweenVectorsNode.v3y)
    cAttr.addChild(angleBetweenVectorsNode.v3z)

    # add attributes
    angleBetweenVectorsNode.addAttribute(angleBetweenVectorsNode.v1)
    angleBetweenVectorsNode.addAttribute(angleBetweenVectorsNode.v2)
    angleBetweenVectorsNode.addAttribute(angleBetweenVectorsNode.v3)

    # Setup which attributes affect each other
    angleBetweenVectorsNode.attributeAffects(angleBetweenVectorsNode.v1,
                                             angleBetweenVectorsNode.v3)
    angleBetweenVectorsNode.attributeAffects(angleBetweenVectorsNode.v2,
                                             angleBetweenVectorsNode.v3)


def initializePlugin(obj):
    # Register node
    plugin = omp.MFnPlugin(obj)
    plugin.registerNode(nodeTypeName, nodeTypeId, nodeCreator,
                        nodeInitializer, omp.MPxNode.kDependNode)


def uninitializePlugin(obj):
    # Unregister node
    plugin = omp.MFnPlugin(obj)
    plugin.deregisterNode(nodeTypeId)
