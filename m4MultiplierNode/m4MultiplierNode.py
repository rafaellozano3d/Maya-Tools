import sys
import maya.OpenMaya as om
import maya.OpenMayaMPx as omp

nodeTypeName = "m4MultiplierNode"
nodeTypeId = om.MTypeId(0x33331)


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


class m4MultiplierNode(omp.MPxNode):
    # Main Class and node attributes
    m1 = om.MObject()
    m2 = om.MObject()
    mOutput = om.MObject()

    def __init__(self):
        omp.MPxNode.__init__(self)

    def printMatrix(self, matrix):
        """Auxiliar extra method to print an input matrix

        Args:
            matrix (MMatrix): Input matrix to print
        """
        result = ('% .2f % .2f % .2f % .2f\n% .2f % .2f % .2f % .2f\n'
                  + '% .2f % .2f % .2f % .2f\n% .2f % .2f % .2f % .2f\n')

        print result % (matrix(0, 0), matrix(0, 1), matrix(0, 2), matrix(0, 3),
                        matrix(1, 0), matrix(1, 1), matrix(1, 2), matrix(1, 3),
                        matrix(2, 0), matrix(2, 1), matrix(2, 2), matrix(2, 3),
                        matrix(3, 0), matrix(3, 1), matrix(3, 2), matrix(3, 3))

    def compute(self, plug, block):
        """We need three attributes, two for matrix inputs, and one
        for the matrix output. We create one data handle for each one and,
        through them, get and set its values

        """
        try:
            m1_dh = block.inputValue(m4MultiplierNode.m1)
            m2_dh = block.inputValue(m4MultiplierNode.m2)
            mO_dh = block.outputValue(m4MultiplierNode.mOutput)
        except ImportError:
            sys.stderr.write("Failed to get MDataHandle")

        m1_value = m1_dh.asMatrix()
        m2_value = m2_dh.asMatrix()
        mO_value = mO_dh.asMatrix()

        # Multiplication of matrices
        for x in range(4):
            for y in range(4):
                sumatory = 0.0

                for z in range(4):
                    sumatory = sumatory + m1_value(x, z) * m2_value(z, y)

                om.MScriptUtil.setDoubleArray(mO_value[x], y, sumatory)

        """"Matrix multiplication could be done with:
        outMatrix = m1_value * m2_value
        """

        block.setClean(plug)


def nodeCreator():
    return omp.asMPxPtr(m4MultiplierNode())


def nodeInitializer():
    # Attributes input definition
    mAttr1 = om.MFnMatrixAttribute()
    m4MultiplierNode.m1 = mAttr1.create("matrix1", "m1",
                                        om.MFnMatrixAttribute.kDouble)
    MAKE_INPUT(mAttr1)
    m4MultiplierNode.addAttribute(m4MultiplierNode.m1)

    mAttr2 = om.MFnMatrixAttribute()
    m4MultiplierNode.m2 = mAttr2.create("matrix2", "m2",
                                        om.MFnMatrixAttribute.kDouble)
    MAKE_INPUT(mAttr2)
    m4MultiplierNode.addAttribute(m4MultiplierNode.m2)

    mAttr3 = om.MFnMatrixAttribute()
    m4MultiplierNode.mOutput = mAttr3.create("matrixOutput", "mO",
                                             om.MFnMatrixAttribute.kDouble)
    MAKE_OUTPUT(mAttr3)
    m4MultiplierNode.addAttribute(m4MultiplierNode.mOutput)

    m4MultiplierNode.attributeAffects(m4MultiplierNode.m1,
                                      m4MultiplierNode.mOutput)
    m4MultiplierNode.attributeAffects(m4MultiplierNode.m2,
                                      m4MultiplierNode.mOutput)


def initializePlugin(obj):
    # Node register
    plugin = omp.MFnPlugin(obj)
    plugin.registerNode(nodeTypeName, nodeTypeId, nodeCreator,
                        nodeInitializer, omp.MPxNode.kDependNode)


def uninitializePlugin(obj):
    # Node unregister
    plugin = omp.MFnPlugin(obj)
    plugin.deregisterNode(nodeTypeId)
