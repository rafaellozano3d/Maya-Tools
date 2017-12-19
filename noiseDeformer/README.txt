To use this script you only have to load it in Maya, for that, you can run this lines in a
python tab, in the Maya Script Editor:

import maya.cmds as cmds
cmds.loadPlugin(r'C:/Users/Rafa/Documents/maya/2017/scripts/noiseDeformer/noiseDeformer.py')

You have to replace the path for the path where you paste your noiseDeformer.py file.

Them, you have to select a mesh, and run the command:

cmds.deformer(type="noiseDeformer")

You can modify four parameters:

- Envelope: it change how many affect the deformer to the mesh
- Seed: change the seed of the random vector that affect the mesh
- Range A: the min displacement of any vertex
- Range B: the max displacement of any vertex

You can also get the generated locator, and the further away from the Mesh, the more the
modifier affects