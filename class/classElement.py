
from numpy import *
import math 
from Node import Node, Nodes

# ***** PROPERTY CLASS *****
class Element(object):
    
    def __init__(self, _id, _n1, _n2, _matNo, _secNo):
        self.id = _id
        self.n1 = _n1
        self.n2 = _n2
        self.matNo = _matNo
        self.secNo = _secNo
    
    def getElemLength(self):
        return self.elemLength


class Elements(object):
    
    def __init__(self):
        self.elements = []
    
    def appendElement(self, _id, _n1, _n2, _matNo, _secNo):
        self.elements.append(Element(_id, _n1, _n2, _matNo, _secNo))
        
    def appendElemLengthAngle(self, _nodes):
        for i in range(len(self.elements)):
            nI = _nodes.findNodeById(self.elements[i].n1)
            nJ = _nodes.findNodeById(self.elements[i].n2)
            self.elements[i].elemLength = float(nI.get_distance(nJ))
            self.elements[i].sinElem = (float(nJ.y)-float(nI.y)) / float(nI.get_distance(nJ))
            self.elements[i].cosElem = (float(nJ.x)-float(nI.x)) / float(nI.get_distance(nJ))
            
    def appendElemLengthAngle3d(self, _nodes):
        for i in range(len(self.elements)):
            nI = _nodes.findNodeById(self.elements[i].n1)
            nJ = _nodes.findNodeById(self.elements[i].n2)
            self.elements[i].elemLength = float(nI.getDistance3d(nJ))
            
            self.elements[i].cosxx = (float(nJ.x)-float(nI.x)) / self.elements[i].elemLength
            self.elements[i].cosxy = (float(nJ.y)-float(nI.y)) / self.elements[i].elemLength
            self.elements[i].cosxz = (float(nJ.z)-float(nI.z)) / self.elements[i].elemLength
            
#            self.elements[i].lambdaValue = float(math.sqrt((self.elements[i].cosxx)**2+(self.elements[i].cosxy)**2))
            
    
    def appendLocalElementStiffnessMatrix(self, _materials, _sections):
        for i in range(len(self.elements)):
            Em = _materials.getEmod(self.elements[i].matNo)
            Ar = _sections.getArea(self.elements[i].secNo)
            self.elements[i].localStiffness = Em * Ar / self.elements[i].elemLength
    
            
    def appendElementStiffnessMatrix2d(self):
        for i in range(len(self.elements)):
            tempMatrix = zeros((2,2))
            tS = self.elements[i].sinElem
            tC = self.elements[i].cosElem
            tK = self.elements[i].localStiffness
            tempMatrix = array([[(tC)**2, tC * tS],
                                [tC * tS, (tS)**2]])
            self.elements[i].elemStiffness = tK * tempMatrix
            self.elements[i].k11 = tK * ((tC) ** 2)
            self.elements[i].k12 = tK * (tC * tS)
            self.elements[i].k21 = tK * (tC * tS)
            self.elements[i].k22 = tK * ((tS) ** 2)
        
        return
    
    def appendElementStiffnessMatrix2dRahmen(self, _materials, _sections):
        for i in range(len(self.elements)):
            
            # sub-elements of element stiffness matrix
            k11 = zeros((3,3))
            k12 = zeros((3,3))
            k21 = zeros((3,3))
            k22 = zeros((3,3))
            
            # element stiffness matrix
            ke = zeros((6,6))
            
            tS = self.elements[i].sinElem
            tC = self.elements[i].cosElem
            tI = _sections.getI(self.elements[i].secNo)
#            print('tI of '+ str(self.elements[i].id) + '= ' + str(tI))
            tE = _materials.getEmod(self.elements[i].matNo)
            tL = self.elements[i].elemLength
            
            tk1 = self.elements[i].localStiffness
            tk2 = 12*tE*tI/(tL**3)
            tk3 = 6*tE*tI/(tL**2)
            tk4 = 4*tE*tI/tL
            tk5 = 2*tE*tI/tL
            
            # k11 to be
            ke[0,0] = (tC**2) * tk1 + (tS**2) * tk2
            ke[0,1] = tS*tC*(tk1-tk2)
            ke[1,1] = (tS**2)*tk1 + (tC**2) * tk2
            ke[2,0] = -tk3 * tS
            ke[2,1] = tk3 * tC
            ke[2,2] = tk4
            
            # k21 to be
            ke[3,0] = -tk1*(tC**2) - tk2*(tS**2)
            ke[3,1] = (-tk1+tk2)*tC*tS
            ke[3,2] = tk3*tS
            ke[4,0] = (-tk1+tk2)*tC*tS
            ke[4,1] = (-tk1)*(tS**2)-tk2*(tC**2)
            ke[4,2] = -tk3*tC
            ke[5,0] = -tk3*tS
            ke[5,1] = tk3*tC
            ke[5,2] = tk5
            
            # k22 to be
            ke[3,3] = tk1*(tC**2)
            ke[4,3] = (tk1-tk2)*tC*tS
            ke[4,4] = tk1*(tS**2)+tk2*(tC**2)
            ke[5,3] = tk3*tS
            ke[5,4] = -tk3*tC
            ke[5,5] = tk4
            
            for j in range(0,6):
                for k in range(j,6):
                    ke[j,k] = ke[k,j]
            
            print (ke)
            
            for j in range(0,3):
                for k in range(0,3):
                    k11[j,k] = ke[j,k]
                    k12[j,k] = ke[j,k+3]
                    k21[j,k] = ke[j+3,k]
                    k22[j,k] = ke[j+3,k+3]
            
            self.elements[i].k11 = k11
            self.elements[i].k12 = k12
            self.elements[i].k21 = k21
            self.elements[i].k22 = k22
            self.elements[i].ke = ke
        
        
        return
    
    def appendElementStiffnessMatrix3dTruss(self, _nodes):
        for i in range(len(self.elements)):
            tempMatrix = zeros((3,3))
            tK = self.elements[i].localStiffness
            
            '''
            method 1 by prof.Fujii to obtain tL, tM & tN
            '''
            tL = self.elements[i].cosxx
            tM = self.elements[i].cosxy
            tN = self.elements[i].cosxz

            '''
            method 2 by prof.Horibe to obtain tL, tM & tN
            '''
#            nI = _nodes.findNodeById(self.elements[i].n1)
#            nJ = _nodes.findNodeById(self.elements[i].n2)
#            
#            tLen = self.elements[i].elemLength
#            tL = (nJ.x - nI.x) / tLen 
#            tM = (nJ.y - nI.y) / tLen
#            tN = (nJ.z - nI.z) / tLen
            
            tempMatrix = array([[tL**2, tL * tM, tL * tN],
                                [tL * tM, tM**2, tM * tN],
                                [tL * tN, tM * tN, tN**2]])
            
            self.elements[i].elemStiffness = tK * tempMatrix
            
            self.elements[i].k11 = tK * (tL**2)
            self.elements[i].k12 = tK * (tL * tM)
            self.elements[i].k13 = tK * (tL * tN)
            
            self.elements[i].k21 = tK * (tL * tM)
            self.elements[i].k22 = tK * (tM**2)
            self.elements[i].k23 = tK * (tM * tN)
            
            self.elements[i].k31 = tK * (tL * tN)
            self.elements[i].k32 = tK * (tM * tN)
            self.elements[i].k33 = tK * (tN**2)
        
        return


    def findElemById(self, _id):
        for i in range(len(self.elements)):
            if(self.elements[i].id == _id):
                return self.elements[i]
            else: pass #exception

    def outputElemsInfo(self):
        _templines = str()
        for i in range(len(self.elements)):
            _templines = '\n'.join([_templines, ', '.join(["ELEM", \
                "{0: >5}".format(self.elements[i].id), \
                "{0: >5}".format(self.elements[i].n1), \
                "{0: >5}".format(self.elements[i].n2), \
                "{0: >5}".format(self.elements[i].matNo), \
                "{0: >5}".format(self.elements[i].secNo), \
                "{0:10.3f}".format(self.elements[i].elemLength), \
                "{0:10.3f}".format(self.elements[i].sinElem), \
                "{0:10.3f}".format(self.elements[i].cosElem), \
                "{0:10.3f}".format(self.elements[i].localStiffness)])])
        return _templines

    def outputElemsResult(self):
        _templines = str()
        for i in range(len(self.elements)):
            _templines = '\n'.join([_templines, ', '.join(["ELEM", \
            "{0: >5}".format(self.elements[i].id), \
            "{0:10.3f}".format(self.elements[i].fN), \
            "{0:10.3f}".format(self.elements[i].sigmaN), \
            "{0:10.3f}".format(self.elements[i].strain)])])
        return _templines

    def outputElemsStiffness(self):
        for i in range(len(self.elements)):
            _temp = self.elements[i].elemStiffness
            print (_temp)
        return 
    
    