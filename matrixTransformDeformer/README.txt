To use this script you only have to load it in Maya, for that, you can run this lines in a
python tab, in the Maya Script Editor:

import maya.cmds as cmds
cmds.loadPlugin(r'C:/Users/Rafa/Documents/maya/2017/scripts/matrixTransformDeformer/matrixTransformDeformer.py')

You have to replace the path for the path where you paste your matrixTransformDeformer.py file.

Them, you have to select a mesh, and run the command:

cmds.deformer(type="matrixTransformDeformer")

The node will appears in the node editor, and you will see an Matrix Attribute, here, you
can connect any transformation matrix, that will affect the mesh.

You can change the Envelope attribute to specify how much you want the modifier to affect the Mesh

(I included a scene where Envelope is set to 0.2)