To run this plugin, you can to load it running this lines in a python tab, in your Maya Script Editor:

import maya.cmds as cmds
cmds.loadPlugin(r'C:/Users/Rafa/Documents/maya/2017/scripts/cubeNodeLocator/cubeNodeLocator.py')

Them, you can create a cube locator node running this python command:

cmds.createNode("cubeNodeLocator");

You have to be in Legacy Viewport to see the cube locator, and you can go to the Maya Attribute
Editor, in Extra Attributes, and set the locator, where you could change the size of the cube
(set to 3 by default) and the cube color