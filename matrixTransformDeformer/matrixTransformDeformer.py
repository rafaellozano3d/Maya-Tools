import sys
import maya.OpenMaya as om
import maya.OpenMayaMPx as omp

nodeTypeName = "matrixTransformDeformer"
nodeTypeId = om.MTypeId(0x33339)


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
    # Main methods and node attributes
    inputMatrix = om.MObject()

    def __init__(self):
        omp.MPxDeformerNode.__init__(self)

    def deform(self, block, geoIterator, matrix, geometryIndex):
        # Configure mesh and get all inputs attributes
        kInput = omp.cvar.MPxGeometryFilter_input
        inputArray_dh = block.outputArrayValue(kInput)
        inputArray_dh.jumpToElement(geometryIndex)
        inputElement_dh = inputArray_dh.outputValue()

        kInputGeom = omp.cvar.MPxGeometryFilter_inputGeom
        inputGeom_dh = inputElement_dh.child(kInputGeom)
        inMesh = inputGeom_dh.asMesh()

        kEnvelope = omp.cvar.MPxGeometryFilter_envelope
        dataHandleEnvelope = block.inputValue(kEnvelope)
        envelope_value = dataHandleEnvelope.asFloat()

        # Getting custom inputs attributes data handles
        try:
            inputMatrix_dh = block.inputValue(noiseDeformer.inputMatrix)
        except ImportError:
            sys.stderr.write("Failed to get MDataHandle")

        # Getting values of custom inputs attributes through data handles
        inputMatrix_value = inputMatrix_dh.asMatrix()

        # Getting translation of input transform matrix
        mTransMatrix = om.MTransformationMatrix(inputMatrix_value)
        inputMatrixTranslation_value = mTransMatrix.getTranslation(
            om.MSpace.kObject)

        # Get mesh normals
        mFloatVectorArray_normal = om.MFloatVectorArray()
        mFnMesh = om.MFnMesh(inMesh)
        mFnMesh.getVertexNormals(False,
                                 mFloatVectorArray_normal,
                                 om.MSpace.kObject)

        # Temporal array to save all vertices modified
        mPointArray_meshVertex = om.MPointArray()

        # Iterate around all vertices
        while(not geoIterator.isDone()):
            pointPosition = geoIterator.position()

            # Get the painted weights of the mesh
            weight = self.weightValue(block, geometryIndex,
                                      geoIterator.index())

            # Create a new vertex position
            pointPosition.x = pointPosition.x + (
                inputMatrixTranslation_value[0]
                * mFloatVectorArray_normal[geoIterator.index()].x
                * envelope_value
                * weight)
            pointPosition.y = pointPosition.y + (
                inputMatrixTranslation_value[1]
                * mFloatVectorArray_normal[geoIterator.index()].y
                * envelope_value
                * weight)
            pointPosition.z = pointPosition.z + (
                inputMatrixTranslation_value[2]
                * mFloatVectorArray_normal[geoIterator.index()].z
                * envelope_value
                * weight)

            # Save the new position in the temporal array
            mPointArray_meshVertex.append(pointPosition)
            geoIterator.next()

        # When the iterator finish, we replace its vertices values with the
        # temporal array
        geoIterator.setAllPositions(mPointArray_meshVertex)


def deformerCreator():
    nodePtr = omp.asMPxPtr(noiseDeformer())
    return nodePtr


def nodeInitializer():
    # Create input attributes
    mFnMatrixAttr = om.MFnMatrixAttribute()
    noiseDeformer.inputMatrix = mFnMatrixAttr.create(
        "MatrixAttribute",
        "matAttr")

    mFnMatrixAttr.setStorable(False)
    mFnMatrixAttr.setConnectable(True)
    MAKE_INPUT(mFnMatrixAttr)

    # add attributes
    noiseDeformer.addAttribute(noiseDeformer.inputMatrix)

    outputGeom = omp.cvar.MPxGeometryFilter_outputGeom

    noiseDeformer.attributeAffects(noiseDeformer.inputMatrix, outputGeom)

    # Make the node paintable
    om.MGlobal.executeCommand("makePaintable -attrType multiFloat"
                              + "-sm deformer matrixTransformDeformer weights")


def initializePlugin(mobject):
    mplugin = omp.MFnPlugin(mobject, "rafaellozano3d.com/devBlog", "1.0")
    try:
        mplugin.registerNode(nodeTypeName, nodeTypeId,
                             deformerCreator,
                             nodeInitializer,
                             omp.MPxNode.kDeformerNode)
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
