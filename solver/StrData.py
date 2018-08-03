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
from solver.Condition import Conditions
from solver.Node import Nodes
 # from solver.DataIO import ReadInput, summaryInputData, resultTruss2d

class StructuralData():
    def __init__(self, _nds, _elems, _mats, _secs, _consts, _loads, _conds):

        self.Nodes = _nds
        self.Elems = _elems
        self.Mats = _mats
        self.Secs = _secs
        self.Consts = _consts
        self.Loads = _loads
        self.Conds = _conds

    def ResetStrData(self):
        
        self.Nodes = Nodes()
        self.Elems = Elements()
        self.Mats = Materials()
        self.Secs = Sections()
        self.Consts = Constraints()
        self.Loads = Loads()
        self.conds = Conditions()

        """
        self.Nodes.nodes = []
        self.Elems.elements = []
        self.Mats.materials = []
        self.Secs.sections = []
        self.Consts.constraints = []
        self.Loads.loads = []
        self.Conds = -999
        """