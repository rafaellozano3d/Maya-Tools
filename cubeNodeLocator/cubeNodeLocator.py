import maya.OpenMaya as om
import maya.OpenMayaMPx as omp
import maya.OpenMayaRender as omr
import maya.OpenMayaUI as omui

nodeTypeName = "cubeNodeLocator"
nodeTypeId = om.MTypeId(0x33333)

'''
To work with OpenGL, we must defines the variables
glRender and glFT, which will provide us with the
tools with which we can, later, to define aspects
such as vertices of the cube, or the method of fusion
with which the object will be represented in the scene
'''
glRenderer = omr.MHardwareRenderer.theRenderer()
glFT = glRenderer.glFunctionTable()


# We define the cubeNodeLocator class, which inherits
# from the omp.MPxLocatorNode class
class cubeNodeLocator(omp.MPxLocatorNode):

    '''
    These variables will be useful to define directly
    the values of the attributes, that we add to our node
    '''
    colorObj = om.MObject()
    kColorAttrLongName = 'color'
    kColorAttrName = 'col'

    sizeObj = om.MObject()
    kSizeAttrLongName = 'size'
    kSizeAttrName = 'siz'

    def __init__(self):
        omp.MPxLocatorNode.__init__(self)

    def compute(self, plug, block):
        pass

    # We define the draw method
    def draw(self, view, path, style, status):
        thisNode = self.thisMObject()

        # We obtain the value of the Color Plug
        colorPlug = om.MPlug(thisNode, self.colorObj)
        color = colorPlug.asMDataHandle().asFloat3()

        # We obtain the value of the Plug Size
        sizePlug = om.MPlug(thisNode, self.sizeObj)
        size = sizePlug.asMDataHandle().asInt()

        # We initialize OpenGL
        view.beginGL()
        glFT.glPushAttrib(omr.MGL_CURRENT_BIT)

        # We define the color for the display status kDormant
        if status == omui.M3dView.kDormant:
            glFT.glColor3f(color[0], color[1], color[2])

        # We define the way in which we want the object to appear
        # in the scene
        glFT.glEnable(omr.MGL_BLEND)
        glFT.glBlendFunc(omr.MGL_SRC_ALPHA,
                         omr.MGL_ONE_MINUS_SRC_ALPHA)
        glFT.glDepthFunc(omr.MGL_LESS)

        # We create a polygon to define our cube
        glFT.glBegin(omr.MGL_POLYGON)

        # We set the length of the side
        sideSize = 0.5*size

        # We define all the points of the triangles set
        # that define our cube
        glFT.glVertex3f(-sideSize, sideSize, sideSize)
        glFT.glVertex3f(-sideSize, sideSize, -sideSize)
        glFT.glVertex3f(sideSize, sideSize, -sideSize)
        glFT.glVertex3f(sideSize, sideSize, sideSize)
        glFT.glVertex3f(-sideSize, sideSize, sideSize)
        glFT.glVertex3f(-sideSize, -sideSize, sideSize)
        glFT.glVertex3f(-sideSize, -sideSize, -sideSize)
        glFT.glVertex3f(-sideSize, sideSize, -sideSize)
        glFT.glVertex3f(-sideSize, sideSize, sideSize)
        glFT.glVertex3f(-sideSize, -sideSize, sideSize)
        glFT.glVertex3f(sideSize, -sideSize, sideSize)
        glFT.glVertex3f(sideSize, sideSize, sideSize)
        glFT.glVertex3f(sideSize, sideSize, -sideSize)
        glFT.glVertex3f(sideSize, -sideSize, -sideSize)
        glFT.glVertex3f(sideSize, -sideSize, sideSize)
        glFT.glVertex3f(sideSize, -sideSize, -sideSize)
        glFT.glVertex3f(-sideSize, -sideSize, -sideSize)
        glFT.glEnd()

        # We define the colors for the different states
        if status == view.kActive:
            glFT.glColor4f(0.2, 0.5, 0.1, 1)
        elif status == view.kLead:
            glFT.glColor4f(0.5, 0.2, 0.1, 1)

        # Disable Blend mode and restore state
        glFT.glDisable(omr.MGL_BLEND)
        glFT.glPopAttrib()
        view.endGL()

    @staticmethod
    def nodeCreator():
        return omp.asMPxPtr(cubeNodeLocator())

    @staticmethod
    def nodeInitializer():
        nAttr = om.MFnNumericAttribute()

        # We create a color attribute
        cubeNodeLocator.colorObj = nAttr.createColor(
            cubeNodeLocator.kColorAttrLongName,
            cubeNodeLocator.kColorAttrName)

        # We define the parameters of the attribute
        nAttr.setDefault(1.0, 1.0, 1.0)
        nAttr.setKeyable(True)
        nAttr.setReadable(True)
        nAttr.setWritable(True)
        nAttr.setStorable(True)
        nAttr.setUsedAsColor(True)

        # And we add it
        cubeNodeLocator.addAttribute(cubeNodeLocator.colorObj)

        # We create an Int attribute
        cubeNodeLocator.sizeObj = nAttr.create(
            cubeNodeLocator.kSizeAttrLongName,
            cubeNodeLocator.kSizeAttrLongName,
            om.MFnNumericData.kInt, 3)

        # We define the parameters of the attribute
        nAttr.setHidden(False)
        nAttr.setKeyable(True)
        nAttr.setReadable(True)
        nAttr.setWritable(True)
        nAttr.setStorable(True)

        # And we add it
        cubeNodeLocator.addAttribute(cubeNodeLocator.sizeObj)

    def postConstructor(self):
        # Rename the node
        om.MFnDependencyNode(self.thisMObject()).setName("cubeNodeLocator#")


def initializePlugin(obj):
    plugin = omp.MFnPlugin(obj)

    plugin.registerNode(nodeTypeName, nodeTypeId,
                        cubeNodeLocator.nodeCreator,
                        cubeNodeLocator.nodeInitializer,
                        omp.MPxNode.kLocatorNode)


def uninitializePlugin(obj):
    plugin = omp.MFnPlugin(obj)
    plugin.deregisterNode(nodeTypeId)
