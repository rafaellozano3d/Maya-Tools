import sys
import maya.OpenMaya as om
import maya.OpenMayaMPx as omp

nodeTypeName = "vectorsAverageNode"
nodeTypeId = om.MTypeId(0x33334)


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


class vectorsAverageNode(omp.MPxNode):
    vectorArrayAttr = om.MObject()

    vOutput = om.MObject()
    vOx = om.MObject()
    vOy = om.MObject()
    vOz = om.MObject()

    def __init__(self):
        omp.MPxNode.__init__(self)

    def compute(self, plug, block):
        # Accedemos al VectorArray y a las componentes de salida
        try:
            vectorArray = om.MFnVectorArrayData(
                block.inputValue(
                    vectorsAverageNode.vectorArrayAttr).data()
                )

            vOx_dh = block.outputValue(vectorsAverageNode.vOx)
            vOy_dh = block.outputValue(vectorsAverageNode.vOy)
            vOz_dh = block.outputValue(vectorsAverageNode.vOz)

        except ImportError:
            sys.stderr.write("Failed to get MDataHandle")

        # Obtenemos la longitud del array e inicializamos los suamdores
        numVectors = vectorArray.length()

        averageX = 0.0
        averageY = 0.0
        averageZ = 0.0

        # Calculamos la suma de las componentes por separado
        for i in range(0, numVectors):
            vector = vectorArray.array()[i]

            averageX += vector.x
            averageY += vector.y
            averageZ += vector.z

        # Dividimos entre el total de elementos para calcular la media
        averageX = averageX / numVectors
        averageY = averageY / numVectors
        averageZ = averageZ / numVectors

        # Devolvemos el resultado
        vOx_dh.setFloat(averageX)
        vOy_dh.setFloat(averageY)
        vOz_dh.setFloat(averageZ)

        block.setClean(plug)


def nodeCreator():
    return omp.asMPxPtr(vectorsAverageNode())


def nodeInitializer():
    typedAttr = om.MFnTypedAttribute()

    # Crear atributo VectorArray de entrada
    vectorsAverageNode.vectorArrayAttr = typedAttr.create(
        "Vector Array",
        "vArray",
        om.MFnData.kVectorArray)

    MAKE_INPUT(typedAttr)
    vectorsAverageNode.addAttribute(vectorsAverageNode.vectorArrayAttr)

    # Crear atributo de salida compuesto
    nAttr = om.MFnNumericAttribute()
    cAttr = om.MFnCompoundAttribute()

    vectorsAverageNode.vOx = nAttr.create(
        "vOutput X",
        "vOx",
        om.MFnNumericData.kFloat)

    vectorsAverageNode.vOy = nAttr.create(
        "vOutput Y",
        "vOy",
        om.MFnNumericData.kFloat)

    vectorsAverageNode.vOz = nAttr.create(
        "vOutput Z",
        "vOz",
        om.MFnNumericData.kFloat)

    MAKE_OUTPUT(nAttr)

    vectorsAverageNode.vOutput = cAttr.create("vOutput", "vO")
    cAttr.addChild(vectorsAverageNode.vOx)
    cAttr.addChild(vectorsAverageNode.vOy)
    cAttr.addChild(vectorsAverageNode.vOz)

    vectorsAverageNode.addAttribute(vectorsAverageNode.vOutput)

    # Definir como afectan los atributos
    vectorsAverageNode.attributeAffects(
        vectorsAverageNode.vectorArrayAttr,
        vectorsAverageNode.vOutput)


def initializePlugin(obj):
    plugin = omp.MFnPlugin(obj)
    plugin.registerNode(nodeTypeName, nodeTypeId, nodeCreator,
                        nodeInitializer, omp.MPxNode.kDependNode)


def uninitializePlugin(obj):
    plugin = omp.MFnPlugin(obj)
    plugin.deregisterNode(nodeTypeId)
