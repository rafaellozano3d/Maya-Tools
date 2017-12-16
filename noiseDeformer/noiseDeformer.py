import sys
import random
import maya.OpenMaya as om
import maya.OpenMayaMPx as omp

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
    # Main methods and node attributes
    seed = om.MObject()
    min = om.MObject()
    max = om.MObject()
    locatorMatrix = om.MObject()
    mesh = om.MObject()

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
            seed_dh = block.inputValue(noiseDeformer.seed)
            min_dh = block.inputValue(noiseDeformer.min)
            max_dh = block.inputValue(noiseDeformer.max)
            matrix_dh = block.inputValue(noiseDeformer.locatorMatrix)
        except ImportError:
            sys.stderr.write("Failed to get MDataHandle")

        # Getting values of custom inputs attributes through data handles
        seed_value = seed_dh.asFloat()
        min_value = min_dh.asFloat()
        max_value = max_dh.asFloat()
        locatorMatrix_value = matrix_dh.asMatrix()

        # Getting locator transform matrix
        mTransMatrix = om.MTransformationMatrix(locatorMatrix_value)
        locatorTranslation_value = mTransMatrix.getTranslation(
            om.MSpace.kObject)

        # Getting locator coordinates
        locatorPoint = om.MPoint(om.MVector(locatorTranslation_value[0],
                                            locatorTranslation_value[1],
                                            locatorTranslation_value[2]))

        meshVector = om.MVector(
            om.MFnDependencyNode(noiseDeformer.mesh).
            findPlug("translateX").asFloat(),
            om.MFnDependencyNode(noiseDeformer.mesh).
            findPlug("translateY").asFloat(),
            om.MFnDependencyNode(noiseDeformer.mesh).
            findPlug("translateZ").asFloat())

        meshPoint = om.MPoint(meshVector)

        distance = meshPoint.distanceTo(locatorPoint)

        # Get mesh normals
        mFloatVectorArray_normal = om.MFloatVectorArray()
        mFnMesh = om.MFnMesh(inMesh)
        mFnMesh.getVertexNormals(False,
                                 mFloatVectorArray_normal,
                                 om.MSpace.kObject)

        # Generate a random seed
        randomVector = om.MVector()
        random.seed(seed_value)

        # Temporal array to save all vertices modified
        mPointArray_meshVertex = om.MPointArray()

        # Iterate around all vertices
        while(not geoIterator.isDone()):
            pointPosition = geoIterator.position()

            # Setting random vector with random values
            randomVector.x = random.uniform(min_value, max_value)
            randomVector.y = random.uniform(min_value, max_value)
            randomVector.z = random.uniform(min_value, max_value)

            # Create a new vertex position
            pointPosition.x = pointPosition.x + (randomVector.x *
                                                 envelope_value * distance/10)
            pointPosition.y = pointPosition.y + (randomVector.y *
                                                 envelope_value * distance/10)
            pointPosition.z = pointPosition.z + (randomVector.z *
                                                 envelope_value * distance/10)

            # Save the new position in the temporal array
            mPointArray_meshVertex.append(pointPosition)
            geoIterator.next()

        # When the iterator finish, we replace its vertices values with the
        # temporal array
        geoIterator.setAllPositions(mPointArray_meshVertex)

    def accessoryNodeSetup(self, dagModifier):
        # We create a extra node of type "locator"
        locator = dagModifier.createNode("locator")

        # Get the locator transform matrix plug
        mFnDependLocator = om.MFnDependencyNode(locator)
        mPlugWorld = mFnDependLocator.findPlug("worldMatrix")
        worldAttr = mPlugWorld.attribute()

        # Connect the plug with our custom node matrix transform plug
        mStatusConnect = dagModifier.connect(locator, worldAttr,
                                             self.thisMObject(),
                                             noiseDeformer.locatorMatrix)
        return mStatusConnect

    def accessoryAttribute(self):
        return noiseDeformer.locatorMatrix


def deformerCreator():
    # Get dag path from selected object when create the node
    selected = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(selected)
    selected.getDependNode(0, noiseDeformer.mesh)

    nodePtr = omp.asMPxPtr(noiseDeformer())
    return nodePtr


def nodeInitializer():
    nAttr = om.MFnNumericAttribute()

    # Create input attributes
    noiseDeformer.seed = nAttr.create("Seed", "seed",
                                      om.MFnNumericData.kFloat,
                                      0.0)
    MAKE_INPUT(nAttr)

    noiseDeformer.min = nAttr.create("rangeA", "rngA",
                                     om.MFnNumericData.kFloat,
                                     0.0)
    MAKE_INPUT(nAttr)

    noiseDeformer.max = nAttr.create("rangeB", "rngB",
                                     om.MFnNumericData.kFloat,
                                     1.0)
    MAKE_INPUT(nAttr)

    mFnMatrixAttr = om.MFnMatrixAttribute()
    noiseDeformer.locatorMatrix = mFnMatrixAttr.create("MatrixAttribute",
                                                        "matAttr")
    mFnMatrixAttr.setStorable(False)
    mFnMatrixAttr.setConnectable(True)

    # add attributes
    noiseDeformer.addAttribute(noiseDeformer.seed)
    noiseDeformer.addAttribute(noiseDeformer.min)
    noiseDeformer.addAttribute(noiseDeformer.max)
    noiseDeformer.addAttribute(noiseDeformer.locatorMatrix)

    outputGeom = omp.cvar.MPxGeometryFilter_outputGeom

    noiseDeformer.attributeAffects(noiseDeformer.seed, outputGeom)
    noiseDeformer.attributeAffects(noiseDeformer.min, outputGeom)
    noiseDeformer.attributeAffects(noiseDeformer.max, outputGeom)
    noiseDeformer.attributeAffects(noiseDeformer.locatorMatrix, outputGeom)


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
