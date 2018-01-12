import sys
import maya.OpenMaya as om
import maya.OpenMayaMPx as omp

nodeTypeName = "smoothLaplacianDeformer"
nodeTypeId = om.MTypeId(0x33355)


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


class smoothLaplacianDeformer(omp.MPxDeformerNode):

    iter = om.MObject()
    lamb = om.MObject()
    dagPath = om.MDagPath()
    infComponentList = om.MObject()
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
            iter_dh = block.inputValue(smoothLaplacianDeformer.iter)
            lamb_dh = block.inputValue(smoothLaplacianDeformer.lamb)
        except ImportError:
            sys.stderr.write("Failed to get MDataHandle")

        # Getting values of custom inputs attributes through data handles
        iter_value = iter_dh.asInt()
        lamb_value = lamb_dh.asFloat()

        # Create vertex iterator
        vIt = om.MItMeshVertex(inMesh)

        # We need to get the average
        avg = om.MVector()

        # Custom variables for iterations
        connected = om.MIntArray()
        currentVertex = om.MPoint()
        newPoint = om.MPoint()

        # Temporal array to save all vertices modified
        mPointArray_meshVertex = om.MPointArray()

        # Iterate around all vertices
        while not vIt.isDone():
            # Get connected and current vertices
            vIt.getConnectedVertices(connected)
            currentVertex = vIt.position(om.MSpace.kWorld)

            avg.x = 0.0
            avg.y = 0.0
            avg.z = 0.0

            # Compute the neighbors average
            for neighbor in connected:
                vertex = om.MPoint()
                meshFn = om.MFnMesh(inMesh)

                meshFn.getPoint(neighbor, vertex, om.MSpace.kWorld)

                # Set the weight with which the deformer affects
                weight = (1.0) / (len(connected))

                for i in range(iter_value):
                    avg.x += weight * (vertex.x - currentVertex.x) * envelope_value
                    avg.y += weight * (vertex.y - currentVertex.y) * envelope_value
                    avg.z += weight * (vertex.z - currentVertex.z) * envelope_value

            # The new point will be the sum of its position plus the new vector
            # multiplied by the lambda variable
            newPoint.x = currentVertex.x + (lamb_value * avg.x)
            newPoint.y = currentVertex.y + (lamb_value * avg.y)
            newPoint.z = currentVertex.z + (lamb_value * avg.z)

            # Save the new position in the temporal array
            mPointArray_meshVertex.append(newPoint)
            vIt.next()

        # At the end, we set the new positions
        geoIterator.setAllPositions(mPointArray_meshVertex)


def deformerCreator():
    # Get dag path from selected object when create the node
    selected = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(selected)
    selected.getDependNode(0, smoothLaplacianDeformer.mesh)
    selected.getDagPath(0, smoothLaplacianDeformer.dagPath)

    nodePtr = omp.asMPxPtr(smoothLaplacianDeformer())
    return nodePtr


def nodeInitializer():
    nAttr = om.MFnNumericAttribute()

    # Define custom attributes
    smoothLaplacianDeformer.iter = nAttr.create(
        "Iterations",
        "Iter",
        om.MFnNumericData.kInt,
        1)

    MAKE_INPUT(nAttr)
    nAttr.setMin(0)
    nAttr.setMax(3)

    smoothLaplacianDeformer.lamb = nAttr.create(
        "Lambda",
        "lamb",
        om.MFnNumericData.kFloat,
        0.333)

    MAKE_INPUT(nAttr)
    nAttr.setMin(-1.0)
    nAttr.setMax(1.0)

    # We agree the attribute to the node
    smoothLaplacianDeformer.addAttribute(smoothLaplacianDeformer.iter)
    smoothLaplacianDeformer.addAttribute(smoothLaplacianDeformer.lamb)

    outputGeom = omp.cvar.MPxGeometryFilter_outputGeom

    smoothLaplacianDeformer.attributeAffects(smoothLaplacianDeformer.iter, outputGeom)
    smoothLaplacianDeformer.attributeAffects(smoothLaplacianDeformer.lamb, outputGeom)


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
