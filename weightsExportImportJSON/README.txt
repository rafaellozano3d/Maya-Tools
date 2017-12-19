To run this file, we only have to set the path where we want that Maya save our weights.json file,
to do that, copy all file in a python tab, in the Maya Script Editor, and in the line numer 216,
change it for any directory you want, in my case, i put int in "C:\\Users\\Rafa\\Desktop\\weights.json"

Now, you only have to run all the code to be able to call the weightAccess method, for example,
you can run this lines:


dictionaryWeights = {}
dictionaryWeights = weightsAccess(True, False)
weightsAccess(False, True, dictionaryWeights)

print dictionaryWeights



NOTE: Before call weightAccess, you have to select the mesh to analyze