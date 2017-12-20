import sys
import maya.OpenMaya as om
import maya.OpenMayaMPx as omp

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

    inputMeshAttr = om.MObject()
    areaAttr = om.MObject()

    def __init__(self):
        omp.MPxNode.__init__(self)

    def compute(self, plug, block):
        '''La mesh de entrada a conectar debera ser el World Mesh, ya que
        si conectamos el Out Mesh no se vera afectado por atributos como
        la escala a la hora de calcular el area
        '''
        try:
            inMesh_dh = block.inputValue(surfaceAreaNode.inputMeshAttr)
            outArea_dh = block.outputValue(surfaceAreaNode.areaAttr)
        except ImportError:
            sys.stderr.write("Failed to get MDataHandle")

        inMesh = inMesh_dh.asMesh()

        faceIt = om.MItMeshPolygon(inMesh)

        # Definir un objeto tipo double
        areaParam = om.MScriptUtil()
        areaParam.createFromDouble(0.0)
        areaPtr = areaParam.asDoublePtr()

        # Iteramos por todos los poligonos y hacemos un sumatorio del area
        totalArea = 0.0
        while not faceIt.isDone():
            faceIt.getArea(areaPtr, om.MSpace.kWorld)
            area = om.MScriptUtil(areaPtr).asDouble()
            totalArea += area
            faceIt.next()

        # Conectamos el output Area al valor calculado para devolverlo
        outArea_dh.setFloat(totalArea)

        block.setClean(plug)


def nodeCreator():
    return omp.asMPxPtr(surfaceAreaNode())


def nodeInitializer():
    # Create Attributes
    nAttr = om.MFnNumericAttribute()
    surfaceAreaNode.areaAttr = nAttr.create("area",
                                            "area",
                                            om.MFnNumericData.kFloat)
    MAKE_OUTPUT(nAttr)

    typedAttr = om.MFnTypedAttribute()
    surfaceAreaNode.inputMeshAttr = typedAttr.create("inputMesh",
                                                     "inMesh",
                                                     om.MFnNumericData.kMesh)
    MAKE_INPUT(typedAttr)

    # Add Attributes
    surfaceAreaNode.addAttribute(surfaceAreaNode.inputMeshAttr)
    surfaceAreaNode.addAttribute(surfaceAreaNode.areaAttr)

    surfaceAreaNode.attributeAffects(surfaceAreaNode.inputMeshAttr,
                                     surfaceAreaNode.areaAttr)


def initializePlugin(obj):
    plugin = omp.MFnPlugin(obj)
    plugin.registerNode(nodeTypeName, nodeTypeId, nodeCreator,
                        nodeInitializer, omp.MPxNode.kDependNode)


def uninitializePlugin(obj):
    plugin = omp.MFnPlugin(obj)
    plugin.deregisterNode(nodeTypeId)
