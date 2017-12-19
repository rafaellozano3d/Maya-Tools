To use this script you have to load it in Maya, you can run this lines for that, in a
python tab, in your Maya Script Editor:

import maya.cmds as cmds
cmds.loadPlugin(r'C:/Users/Rafa/Documents/maya/2017/scripts/m4MultiplierNode/m4MultiplierNode.py')

You have to change this path to your path where you copy the m4MultiplierNode.py file. Them, you
can write cmds.createNode("m4MultiplierNode") to create the node.

For use it, you only have to connect the matrix 1 and 2 in the Matrix 1 and Matrix 2 plugs,
the result can be obtained in the Matrix Output plug.