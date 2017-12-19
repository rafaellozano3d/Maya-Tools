To load this script you only have to import it in Maya, you can run this lines in a
python tab to do that:

import maya.cmds as cmds
cmds.loadPlugin(r'C:/Users/Rafa/Documents/maya/2017/scripts/angleBetweenVectorsNode/angleBetweenVectorsNode.py')

Where the loadPlugin path must be the path where you have your angleBetweenVectorsNode.py
(in my case that)

Them, only have to call cmds.createNode("angleBetweenVectorsNode") and you will have one
in your node editor.

You can connect one vector output to the V1 input vector, and another to the V2 input. The
result can be obtained in the V3 output.