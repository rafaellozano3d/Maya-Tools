'''
Created on 12 dic. 2017

@author: rafaellozano3d.com
'''

import maya.OpenMaya as om
import maya.OpenMayaMPx as omp

nodeTypeName = "myNode"
nodeTypeId = om.MTypeId(0x33333)

class myNode(omp.MPxNode):
    def __init__(self):
        print "> myNode.__init__"
        omp.MPxNode.__init__(self)

    def compute(self, plug, block):
        print "> compute"
        """
        Aqui definiremos que operaciones realizara nuestro
        nodo cuando un determinado plug varie
        """


def nodeCreator():
    """
    Si necesitamos que al crear un nodo se cree algo en
    nuestra es escena, es aqui donde deberiamos de realizar
    esos preoperaciones iniciales, es importante retornar
    un MPxPtr de la clase de nuestro nodo
    """
    return omp.asMPxPtr(myNode())


def nodeInitializer():
    print "> nodeInitializer"
    """
    Aqui sera donde definamos los atributos y conexiones que
    tendra nuestro nodo
    """


def initializePlugin(obj):
    print "> initializePlugin"
    # Aqui se registra el nodo
    plugin = omp.MFnPlugin(obj)
    plugin.registerNode(nodeTypeName, nodeTypeId, nodeCreator,
                        nodeInitializer, omp.MPxNode.kDependNode)


def uninitializePlugin(obj):
    print ">_uninitializePlugin"
    # Aqui se elimina del registro
    plugin = omp.MFnPlugin(obj)
    plugin.deregisterNode(nodeTypeId)
