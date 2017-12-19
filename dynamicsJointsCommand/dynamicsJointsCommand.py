import maya.cmds as cmds
import maya.mel as mel

selected = cmds.ls(sl=True)

# Obtener la cadena inicial de joints (jointListA)

jointListA = cmds.listRelatives(ad=True, f=True)
jointListA = jointListA[0]

jointListA = jointListA.split('|')
jointListA = jointListA[1:len(jointListA)]

# Duplicamos la cadena (jointListB)

jointListB = cmds.duplicate(jointListA[0], rc=True)

# Hacemos un parent constraint de cada hueso A a B

for jntA, jntB in zip(jointListA, jointListB):
    cmds.parentConstraint(jntA, jntB, mo=False)

# Creamos un IK Spline para la cadena jointListA y jointListB

ikReturn = cmds.ikHandle(sj=jointListA[0],
                         ee=jointListA[len(jointListA)-1],
                         sol="ikSplineSolver")
curveA = ikReturn[2]

ikReturn = cmds.ikHandle(sj=jointListB[0],
                         ee=jointListB[len(jointListB)-1],
                         sol="ikSplineSolver")
curveB = ikReturn[2]

# Hacemos dinamica la curvaA

cmds.select(curveA)
mel.eval('makeCurvesDynamic 2 { "1", "0", "1", "1", "0"};')

'''
Ya tenemos jointListA, su curva curveA, jointListB ysu curva curveB

Ahora necesitamos llegar al nodo de la curva que lleva la dinamica
aplicada, al haber realizado el makeCurvesDynamic, el nuevo elemento
seleccionado por defecto sera el hairSystem, asi que podemos aprovecharlo
para acceder a traves de el
'''

# Obtener curveDyn

# Primero, a traves del hairSystem, obtenemos el follicle transform node
hairSystem = cmds.ls(sl=True)
follicle = cmds.listConnections(hairSystem, type="follicle")[0]

# Mediante el folicle transform node obtenemos el follicle shape
cmds.select(follicle)
selected_items = cmds.ls(selection=True)
follicleShape = cmds.listRelatives(selected_items[0], shapes=True)[0]
cmds.setAttr(follicleShape+".pointLock", 1)

# Por ultimo, obtenemos la curva conectada al follicle shape
curveDyn = cmds.listConnections(follicleShape)[-1]

# Ya solo queda agregar curveDyn como blendshape a curveB
cmds.blendShape(curveDyn, curveB)
