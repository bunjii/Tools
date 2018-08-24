"""
# linear static solver for two-dimensional truss structure

"""
import os
#from pathlib import Path
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
from solver.DataIO import ReadInput, summaryInputData, resultTruss2d


class solve_2d_truss():
    @staticmethod
    def truss2d(_strdata, _filepath):
        ns = _strdata.Nodes
        elms = _strdata.Elems
        mts = _strdata.Mats
        secs = _strdata.Secs
        consts = _strdata.Consts
        lds = _strdata.Loads
        conds = _strdata.Conds

        # ****** PREPROCESS ******
        elms.appendElemLengthAngle(ns)
        elms.appendLocalElementStiffnessMatrix(mts, secs)
        elms.appendElementStiffnessMatrix2d()
        ns.appendLoad(lds)

        # elms.outputElemsStiffness()
        # summaryInputData(inputfilename, ns, elms, mts, secs, consts, lds)
        # print (elms.outputElemsStiffness())

        K = createStiffnessMatrix2d(ns, elms, consts)
        # print (linalg.det(K))

        KI = obtainInverseMatrix(K) # explicit method !!!

        F = createLoadVector2d(ns, lds)

        # ****** SOLVE ******
        d = obtainDefVector(KI, F, ns) # d
        obtainNormalForceStressStrain(ns, elms, secs, d) # u

        # ****** OUTPUT ******
        # summaryInputData(inputfilename, ns, elms, mts, secs, consts, lds)
        # resultTruss2d(os.path.basename(_filepath), ns, elms)

        return _strdata

