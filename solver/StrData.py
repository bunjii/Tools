from solver.classConstraint import Constraints
from solver.classElement import Elements
from solver.classMaterial import Materials
from solver.classSection import Sections
from solver.classLoad import Loads
from solver.classSolve import createStiffnessMatrix2d
from solver.classSolve import createLoadVector2d
from solver.classSolve import obtainInverseMatrix
from solver.classSolve import obtainDefVector
from solver.classSolve import obtainNormalForceStressStrain
from solver.Node import Nodes
 # from solver.DataIO import ReadInput, summaryInputData, resultTruss2d

class StructuralData():
    def __init__(self, _nds, _elems, _mats, _secs, _consts, _loads):
        Nodes = _nds
        Elems = _elems
        Mats = _mats
        Secs = _secs
        Consts = _consts
        Loads = _loads
