"""
# linear static solver for two-dimensional truss structure

"""
import os
#from pathlib import Path
from classConstraint import Constraints
from classElement import Elements
from classMaterial import Materials
from classSection import Sections
from classLoad import Loads
from classSolve import createStiffnessMatrix2d
from classSolve import createLoadVector2d
from classSolve import obtainInverseMatrix
from classSolve import obtainDefVector
from classSolve import obtainNormalForceStressStrain
from Node import Nodes
from DataIO import ReadInput, summaryInputData, resultTruss2d

# from numpy import *

# ****** VARIABLES ******
ns = Nodes()
elms = Elements()
mts = Materials()
secs = Sections()
consts = Constraints()
lds = Loads()

# ****** READ INPUT ******
osname = os.name
cwd = os.getcwd()
inputfilename = "input01.dat"
if osname == 'nt': # in case of Windows
    path = cwd+"\\"+inputfilename
else: # Mac, Linux
    path = cwd+"/"+inputfilename

ReadInput(path, ns, elms, mts, secs, consts, lds)

# ****** PREPROCESS ******
elms.appendElemLengthAngle(ns)
elms.appendLocalElementStiffnessMatrix(mts, secs)
elms.appendElementStiffnessMatrix2d()
ns.appendLoad(lds)

#elms.outputElemsStiffness()
summaryInputData(inputfilename, ns, elms, mts, secs, consts, lds)
# print (elms.outputElemsStiffness())

K = createStiffnessMatrix2d(ns, elms, consts)
# print (linalg.det(K))

KI = obtainInverseMatrix(K) # explicit method !!!

F = createLoadVector2d(ns, lds)

# ****** SOLVE ******
d = obtainDefVector(KI, F, ns) # d
obtainNormalForceStressStrain(ns, elms, secs, d) # u

# ****** OUTPUT ******
summaryInputData(inputfilename, ns, elms, mts, secs, consts, lds)
resultTruss2d(inputfilename, ns, elms)

# ****** HELPER FUNCTIONS ******
