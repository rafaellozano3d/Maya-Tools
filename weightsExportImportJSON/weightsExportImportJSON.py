import maya.OpenMaya as om
import maya.OpenMayaAnim as oma
import json

'''
The idea is to make an initial dictionary, that we will
use as database, which will use as key the index that
identify the bones.

Next, we will create a new dictionary with a key that
represents the index of each vertex, and its value will
will be the dictionary created previously, with the bone
index as key and the weight assigned as value.

We see now an example with a geometry with 8 vertex with
3 bones


{
  "0": {
    "0": 0.9997786579426335,
    "1": 0.0002083107833012753,
    "2": 1.0185354279407606e-05
  },
  "1": {
    "0": 0.9996507763613539,
    "1": 0.00032854589599395846,
    "2": 1.6158465717394537e-05
  },
  "2": {
    "0": 0.9994543861300254,
    "1": 0.0005130804485717589,
    "2": 2.5416323872270777e-05
  },
  "3": {
    "0": 0.9992652528303488,
    "1": 0.0006906883887673361,
    "2": 3.4413059598642316e-05
  },
  "4": {
    "0": 0.9991860108441455,
    "1": 0.0007650737121918432,
    "2": 3.8203363857932757e-05
  },
  "5": {
    "0": 0.9992652529348223,
    "1": 0.0006906882906864528,
    "2": 3.4413054609262334e-05
  },
  "6": {
    "0": 0.99945438629511,
    "1": 0.0005130802935036854,
    "2": 2.541631605218632e-05
  },
  "7": {
    "0": 0.9996507765994861,
    "1": 0.00032854567215906855,
    "2": 1.615845455056239e-05
  },
  "8": {
    "0": 0.9997786581127507,
    "1": 0.00020831062331107982,
    "2": 1.0185346367431276e-05
  }
}
'''


def weightsAccess(read=False, write=False, dictionary=None):
    """
    weightAccess method allow us to access to all vertices weights,
    and create the dictionary with all the information.

    Args:
        read: True if we call this method to read weights and create
            the JSON file with the dictionary
        write: True if we call this method to write the current weights
            with the dictionary new values
        dictionary: if we call this method to write new weights, we use
            this dictionary to specify the new weights
    """
    # --------  To get the skincluster of the selected element  -------- #
    selectionList = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(selectionList)

    # First, we will obtain the shape node through the dag path of the
    # selected element
    selectedDagPath = om.MDagPath()
    selectionList.getDagPath(0, selectedDagPath)

    selectedDagPath.extendToShape()

    shapeNode = om.MFnDependencyNode(selectedDagPath.node())

    # Now, we can get the skin node connected to the shape

    allPlugsConnected = om.MPlugArray()
    shapeNode.findPlug("inMesh").connectedTo(allPlugsConnected, True, False)

    skinNode = om.MFnDependencyNode(allPlugsConnected[0].node())

    # We could see the skin node name with the next line:
    # print "skinNode = "+skinNode.name()

    # -----------  To get the skin node weights  ----------- #

    mfnSkin = oma.MFnSkinCluster(allPlugsConnected[0].node())

    # Now we will get all the dag paths of the bones that affect
    # the shape
    jointsDagsPaths = om.MDagPathArray()
    mfnSkin.influenceObjects(jointsDagsPaths)

    # We create the initial dictionary with the index of the bones
    # that affect the shape
    jointStructureDictionary = {}

    for i in xrange(jointsDagsPaths.length()):
        # And the index of each bone
        infId = int(mfnSkin.indexForInfluenceObject(jointsDagsPaths[i]))

        # And we add the index to the initial dictionary
        jointStructureDictionary[infId] = i

    # We could see the initial dictionary structure with this line
    # print "dictionaryStructure: ", jointStructureDictionary

    '''
    We already have the list of all bones that affect the object stored
    in a dictionary, sorted as if it were a database.

    Now, we have to create the final dictionary, in which the IDs of vertices
    will be the keys, and the initial dictionary will be the value, which will
    have in each key the value of the corresponding weight
    '''
    weightPlug = skinNode.findPlug("weights")

    jointsIdsList = om.MIntArray()

    # Final dictionary that we have to fill if we are reading
    weights = {}

    # We iterate all affected vertices
    for vertexId in xrange(skinNode.findPlug("weightList").numElements()):
        # We create an auxiliar dictionary, which will be added to the
        # corresponding key position (usefull if we are reading)
        vertexWeights = {}

        # We select the "vertexID" position in the attribute list of the
        # weights vertices
        weightPlug.selectAncestorLogicalIndex(
            vertexId, skinNode.findPlug("weightList").attribute())

        # Once the vertex is selected in the list, we obtain the list of
        # bones that affect said vertex
        weightPlug.getExistingArrayAttributeIndices(jointsIdsList)

        # We will need a plug copy to work
        vertexAndJointWeight = om.MPlug(weightPlug)

        # We iterate over all the bones that affect the vertex
        for jointId in jointsIdsList:
            vertexAndJointWeight.selectAncestorLogicalIndex(
                jointId, skinNode.findPlug("weights").attribute())

            try:
                if (read is True):
                    # If we are reading, we fill the dictionary with the
                    # weights reads
                    vertexWeights[
                        jointStructureDictionary[
                            jointId]] = vertexAndJointWeight.asDouble()

                if (write is True):
                    # If we are writing, we configure the weights with respect
                    # to the input dictionary

                    # You can print the input dictionary with this lines:
                    # print "vertex ID",str(vertexId)," joint ID"
                    # str(jointId)," = ", str(dictionary[vertexId][jointId])
                    vertexAndJointWeight.setDouble(
                        dictionary[vertexId][jointId])

            except KeyError:
                pass

            # We keep in the position of the corresponding vertex, in the
            # general dictionary, the data that we have just extracted
            weights[vertexId] = vertexWeights

    # If we are reading, we create the JSON file with the dictionary
    if (read is True):
        convertDictionaryToJSON(weights)

    return weights


def convertDictionaryToJSON(dictionary):
    """
    convertDictionaryToJSON method allow us to generate the JSON
    file

    Args:
        dictionary: the dictionary from which we want to create the
            JSON file
    """
    dictJSON = json.dumps(
        dictionary, sort_keys=True,
        indent=2,
        separators=(',', ': '))

    stockPath = "C:\\Users\\Rafa\\Desktop\\weights.json"
    with open(stockPath, "w") as myFile:
        json.dump(dictionary, myFile, indent=2, sort_keys=True)

    return dictJSON
