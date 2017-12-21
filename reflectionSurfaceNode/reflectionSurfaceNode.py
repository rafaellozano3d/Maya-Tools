import sys
import maya.OpenMaya as om
import maya.OpenMayaMPx as omp

nodeTypeName = "reflectionSurfaceNode"
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


class reflectionSurfaceNode(omp.MPxNode):
    # Main Class and node attributes
    pointPAttr = om.MObject()
    inputMatrixAttr = om.MObject()

    outputVectorAttr = om.MObject()

    def __init__(self):
        omp.MPxNode.__init__(self)

    def compute(self, plug, block):
        try:
            pointPAttr_dh = block.inputValue(
                reflectionSurfaceNode.pointPAttr)

            inputMatrixAttr_dh = block.inputValue(
                reflectionSurfaceNode.inputMatrixAttr)

            outputVectorAttr_dh = block.outputValue(
                reflectionSurfaceNode.outputVectorAttr)
        except ImportError:
            sys.stderr.write("Failed to get MDataHandle")

        pointPAttr_value = pointPAttr_dh.asFloatVector()
        inputMatrixAttr_value = inputMatrixAttr_dh.asMatrix()

        '''Vamos a definir tres puntos:
            puntoP : punto en el que se situa el locator
            puntoQ : punto del locator afectado por el reflejo
            puntoR : punto del plano donde reflejara el puntoP
        '''

        pointP = om.MVector(pointPAttr_value)

        # Obtener la normal del plano usando, por ejemplo, la coordenada Y
        # hara que refleje desde el plano horizontal, podeis probar reflejar
        # desde un plano X o un plano Z
        planeNormal = om.MVector(
            inputMatrixAttr_value(1, 0),
            inputMatrixAttr_value(1, 1),
            inputMatrixAttr_value(1, 2)).normal()

        # Obtenemos el punto central del plano, que definira pointR
        pointR = om.MVector(
            inputMatrixAttr_value(3, 0),
            inputMatrixAttr_value(3, 1),
            inputMatrixAttr_value(3, 2))

        # Calculamos el vector que va de pointR a pointP
        RPVector = pointP - pointR

        # Invertimos nuestro vector PR
        RPVectorInverse = (RPVector * -1.0) + pointR

        # Proyeccion del vector RP sobre la normal del plano
        '''Por otro lado, necesitamos la proyeccion del vector RP sobre
        la normal, que lo obtenemos mediante el producto escalar
        '''
        projectRPNormal = planeNormal * (RPVector * planeNormal)

        # Sumamos el doble de esta proyeccion (distancia) al vector
        # RP invertido
        auxVectorToAdd = (projectRPNormal * 2) + RPVectorInverse

        RQVector = (auxVectorToAdd - pointR) + pointR

        # Establecemos el valor de salida
        outputVector = om.MFloatVector(RQVector.x, RQVector.y, RQVector.z)
        outputVectorAttr_dh.setMFloatVector(outputVector)

        block.setClean(plug)


def nodeCreator():
    return omp.asMPxPtr(reflectionSurfaceNode())


def nodeInitializer():
    # Inputs Attributes
    nAttr = om.MFnNumericAttribute()

    reflectionSurfaceNode.pointPAttr = nAttr.createPoint(
        "inputVector",
        "inV")
    MAKE_INPUT(nAttr)
    reflectionSurfaceNode.addAttribute(
        reflectionSurfaceNode.pointPAttr)

    mAttr = om.MFnMatrixAttribute()

    reflectionSurfaceNode.inputMatrixAttr = mAttr.create(
        "inputMatrix",
        "inM")
    MAKE_INPUT(mAttr)
    reflectionSurfaceNode.addAttribute(reflectionSurfaceNode.inputMatrixAttr)

    # Output Attributes
    reflectionSurfaceNode.outputVectorAttr = nAttr.createPoint(
        "outputVecto",
        "outV")
    MAKE_OUTPUT(nAttr)
    reflectionSurfaceNode.addAttribute(reflectionSurfaceNode.outputVectorAttr)

    # Attributes Affects
    reflectionSurfaceNode.attributeAffects(
        reflectionSurfaceNode.pointPAttr,
        reflectionSurfaceNode.outputVectorAttr)

    reflectionSurfaceNode.attributeAffects(
        reflectionSurfaceNode.inputMatrixAttr,
        reflectionSurfaceNode.outputVectorAttr)


def initializePlugin(obj):
    # Node register
    plugin = omp.MFnPlugin(obj)
    plugin.registerNode(nodeTypeName, nodeTypeId, nodeCreator,
                        nodeInitializer, omp.MPxNode.kDependNode)


def uninitializePlugin(obj):
    # Node unregister
    plugin = omp.MFnPlugin(obj)
    plugin.deregisterNode(nodeTypeId)
