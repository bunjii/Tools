'''
Created on 2011/12/26

@author: troc
'''
from Node import *
from numpy import *
#from sets import Set # unnecessary to load in python 2.7 ?? need to confirm.

def createStiffnessMatrix2d(_nodes, _elements, _constraints):
    _numElem = len(_elements.elements)
    _numNode = len(_nodes.nodes)
    _stiffnessMatrix = zeros((2*_numNode, 2*_numNode))

    for i in range(_numElem):
        _tM = zeros((2*_numNode, 2*_numNode))
        _nI = _elements.elements[i].n1 # returns node id 1 (starting from 1,2,3,...)
        _nJ = _elements.elements[i].n2 # returns node id 2 
        
        #K11
        _tM[2*_nI-2, 2*_nI-2] = _elements.elements[i].k11
        _tM[2*_nI-2, 2*_nI-1] = _elements.elements[i].k12
        _tM[2*_nI-1, 2*_nI-2] = _elements.elements[i].k21
        _tM[2*_nI-1, 2*_nI-1] = _elements.elements[i].k22
        
        #K12
        _tM[2*_nI-2, 2*_nJ-2] = -1 * _elements.elements[i].k11
        _tM[2*_nI-2, 2*_nJ-1] = -1 * _elements.elements[i].k12
        _tM[2*_nI-1, 2*_nJ-2] = -1 * _elements.elements[i].k21
        _tM[2*_nI-1, 2*_nJ-1] = -1 * _elements.elements[i].k22
    
        #K21
        _tM[2*_nJ-2, 2*_nI-2] = -1 * _elements.elements[i].k11
        _tM[2*_nJ-2, 2*_nI-1] = -1 * _elements.elements[i].k12
        _tM[2*_nJ-1, 2*_nI-2] = -1 * _elements.elements[i].k21
        _tM[2*_nJ-1, 2*_nI-1] = -1 * _elements.elements[i].k22
        
        #K22
        _tM[2*_nJ-2, 2*_nJ-2] = _elements.elements[i].k11
        _tM[2*_nJ-2, 2*_nJ-1] = _elements.elements[i].k12
        _tM[2*_nJ-1, 2*_nJ-2] = _elements.elements[i].k21
        _tM[2*_nJ-1, 2*_nJ-1] = _elements.elements[i].k22
    
        
        _stiffnessMatrix = _stiffnessMatrix + _tM
#        print(type(_stiffnessMatrix)) # =numpy.ndarray
#        print(type(_tM)) # =numpy.ndarray
    
#    print (_stiffnessMatrix)
    
    # adding constraint conditions to the stiffness matrix       
    _numConst = len(_constraints.constraints)
    for i in range(_numConst):
        _tCMX = zeros((2*_numNode, 2*_numNode))
        _tCMY = zeros((2*_numNode, 2*_numNode))
        if (_constraints.constraints[i].cX == 1):
            _ncI = _constraints.constraints[i].nodeId
#            _temp = _stiffnessMatrix[2*_ncI-2, 2*_ncI-2]
            _stiffnessMatrix[2*_ncI-2, : ] = 0.0
            _stiffnessMatrix[: , 2*_ncI-2] = 0.0
            _stiffnessMatrix[2*_ncI-2, 2*_ncI-2] = 1.0
            
        if (_constraints.constraints[i].cY == 1):
            _ncI = _constraints.constraints[i].nodeId
#            _temp = _stiffnessMatrix[2*_ncI-1, 2*_ncI-1]
            _stiffnessMatrix[2*_ncI-1, : ] = 0.0
            _stiffnessMatrix[: , 2*_ncI-1] = 0.0
            _stiffnessMatrix[2*_ncI-1, 2*_ncI-1] = 1.0

#    print (_stiffnessMatrix)
    return _stiffnessMatrix

def createStiffnessMatrix2dR(_nodes, _elements, _constraints):
    
    _numElem = len(_elements.elements)
    _numNode = len(_nodes.nodes)
    _stiffnessMatrix = zeros((3*_numNode, 3*_numNode))

    for i in range(_numElem):
        _tM = zeros((3*_numNode, 3*_numNode))
        _nI = _elements.elements[i].n1 # returns node id 1 (starting from 1,2,3,...)
        _nJ = _elements.elements[i].n2 # returns node id 2 
        
        #K11 field
        _tM[3*_nI-3, 3*_nI-3] = _elements.elements[i].k11[0, 0]
        _tM[3*_nI-3, 3*_nI-2] = _elements.elements[i].k11[0, 1]
        _tM[3*_nI-3, 3*_nI-1] = _elements.elements[i].k11[0, 2]
        _tM[3*_nI-2, 3*_nI-3] = _elements.elements[i].k11[1, 0]
        _tM[3*_nI-2, 3*_nI-2] = _elements.elements[i].k11[1, 1]
        _tM[3*_nI-2, 3*_nI-1] = _elements.elements[i].k11[1, 2]
        _tM[3*_nI-1, 3*_nI-3] = _elements.elements[i].k11[2, 0]
        _tM[3*_nI-1, 3*_nI-2] = _elements.elements[i].k11[2, 1]
        _tM[3*_nI-1, 3*_nI-1] = _elements.elements[i].k11[2, 2]
        
        #K12 field
        _tM[3*_nI-3, 3*_nJ-3] = _elements.elements[i].k12[0, 0]
        _tM[3*_nI-3, 3*_nJ-2] = _elements.elements[i].k12[0, 1]
        _tM[3*_nI-3, 3*_nJ-1] = _elements.elements[i].k12[0, 2]
        _tM[3*_nI-2, 3*_nJ-3] = _elements.elements[i].k12[1, 0]
        _tM[3*_nI-2, 3*_nJ-2] = _elements.elements[i].k12[1, 1]
        _tM[3*_nI-2, 3*_nJ-1] = _elements.elements[i].k12[1, 2]
        _tM[3*_nI-1, 3*_nJ-3] = _elements.elements[i].k12[2, 0]
        _tM[3*_nI-1, 3*_nJ-2] = _elements.elements[i].k12[2, 1]
        _tM[3*_nI-1, 3*_nJ-1] = _elements.elements[i].k12[2, 2]
    
        #K21 field
        _tM[3*_nJ-3, 3*_nI-3] = _elements.elements[i].k21[0,0]
        _tM[3*_nJ-3, 3*_nI-2] = _elements.elements[i].k21[0,1]
        _tM[3*_nJ-3, 3*_nI-1] = _elements.elements[i].k21[0,2]
        _tM[3*_nJ-2, 3*_nI-3] = _elements.elements[i].k21[1,0]
        _tM[3*_nJ-2, 3*_nI-2] = _elements.elements[i].k21[1,1]
        _tM[3*_nJ-2, 3*_nI-1] = _elements.elements[i].k21[1,2]
        _tM[3*_nJ-1, 3*_nI-3] = _elements.elements[i].k21[2,0]
        _tM[3*_nJ-1, 3*_nI-2] = _elements.elements[i].k21[2,1]
        _tM[3*_nJ-1, 3*_nI-1] = _elements.elements[i].k21[2,2]
        
        #K22 field
        _tM[3*_nJ-3, 3*_nJ-3] = _elements.elements[i].k22[0,0]
        _tM[3*_nJ-3, 3*_nJ-2] = _elements.elements[i].k22[0,1]
        _tM[3*_nJ-3, 3*_nJ-1] = _elements.elements[i].k22[0,2]
        _tM[3*_nJ-2, 3*_nJ-3] = _elements.elements[i].k22[1,0]
        _tM[3*_nJ-2, 3*_nJ-2] = _elements.elements[i].k22[1,1]
        _tM[3*_nJ-2, 3*_nJ-1] = _elements.elements[i].k22[1,2]
        _tM[3*_nJ-1, 3*_nJ-3] = _elements.elements[i].k22[2,0]
        _tM[3*_nJ-1, 3*_nJ-2] = _elements.elements[i].k22[2,1]
        _tM[3*_nJ-1, 3*_nJ-1] = _elements.elements[i].k22[2,2]
        
        _stiffnessMatrix = _stiffnessMatrix + _tM
#        print(type(_stiffnessMatrix)) # =numpy.ndarray
#        print(type(_tM)) # =numpy.ndarray
    
    print (_stiffnessMatrix)
    # adding constraint conditions to the stiffness matrix       
    _numConst = len(_constraints.constraints)
    for i in range(_numConst):
#        _tCMX = zeros((3*_numNode, 3*_numNode))
#        _tCMY = zeros((3*_numNode, 3*_numNode))
        if (_constraints.constraints[i].cX == 1):
            _ncI = _constraints.constraints[i].nodeId
#            _temp = _stiffnessMatrix[2*_ncI-2, 2*_ncI-2]
            _stiffnessMatrix[3*_ncI-3, : ] = 0.0
            _stiffnessMatrix[: , 3*_ncI-3] = 0.0
            _stiffnessMatrix[3*_ncI-3, 3*_ncI-3] = 1.0
            
        if (_constraints.constraints[i].cY == 1):
            _ncI = _constraints.constraints[i].nodeId
#            _temp = _stiffnessMatrix[2*_ncI-1, 2*_ncI-1]
            _stiffnessMatrix[3*_ncI-2, : ] = 0.0
            _stiffnessMatrix[: , 3*_ncI-2] = 0.0
            _stiffnessMatrix[3*_ncI-2, 3*_ncI-2] = 1.0
            
        if (_constraints.constraints[i].angle ==1):
            _ncI = _constraints.constraints[i].nodeId
            

#    print (_stiffnessMatrix)
    return _stiffnessMatrix

def createStiffnessMatrix3dTruss(_nodes, _elements, _constraints):
    
    _numElem = len(_elements.elements)
    _numNode = len(_nodes.nodes)
    _stiffnessMatrix = zeros((3*_numNode, 3*_numNode))

    for i in range(_numElem):
        _tM = zeros((3*_numNode, 3*_numNode))
        _nI = _elements.elements[i].n1 # returns node id 1 (starting from 1,2,3,...)
        _nJ = _elements.elements[i].n2 # returns node id 2 
        
        _tM[3*_nI-3, 3*_nI-3] = _elements.elements[i].k11
        _tM[3*_nI-3, 3*_nI-2] = _elements.elements[i].k12
        _tM[3*_nI-3, 3*_nI-1] = _elements.elements[i].k13
        _tM[3*_nI-2, 3*_nI-3] = _elements.elements[i].k21
        _tM[3*_nI-2, 3*_nI-2] = _elements.elements[i].k22
        _tM[3*_nI-2, 3*_nI-1] = _elements.elements[i].k23
        _tM[3*_nI-1, 3*_nI-3] = _elements.elements[i].k31
        _tM[3*_nI-1, 3*_nI-2] = _elements.elements[i].k32
        _tM[3*_nI-1, 3*_nI-1] = _elements.elements[i].k33
        
        _tM[3*_nJ-3, 3*_nJ-3] = _elements.elements[i].k11
        _tM[3*_nJ-3, 3*_nJ-2] = _elements.elements[i].k12
        _tM[3*_nJ-3, 3*_nJ-1] = _elements.elements[i].k13
        _tM[3*_nJ-2, 3*_nJ-3] = _elements.elements[i].k21
        _tM[3*_nJ-2, 3*_nJ-2] = _elements.elements[i].k22
        _tM[3*_nJ-2, 3*_nJ-1] = _elements.elements[i].k23
        _tM[3*_nJ-1, 3*_nJ-3] = _elements.elements[i].k31
        _tM[3*_nJ-1, 3*_nJ-2] = _elements.elements[i].k32
        _tM[3*_nJ-1, 3*_nJ-1] = _elements.elements[i].k33
    
        _tM[3*_nI-3, 3*_nJ-3] = -1 * _elements.elements[i].k11
        _tM[3*_nI-3, 3*_nJ-2] = -1 * _elements.elements[i].k12
        _tM[3*_nI-3, 3*_nJ-1] = -1 * _elements.elements[i].k13
        _tM[3*_nI-2, 3*_nJ-3] = -1 * _elements.elements[i].k21
        _tM[3*_nI-2, 3*_nJ-2] = -1 * _elements.elements[i].k22
        _tM[3*_nI-2, 3*_nJ-1] = -1 * _elements.elements[i].k23
        _tM[3*_nI-1, 3*_nJ-3] = -1 * _elements.elements[i].k31
        _tM[3*_nI-1, 3*_nJ-2] = -1 * _elements.elements[i].k32
        _tM[3*_nI-1, 3*_nJ-1] = -1 * _elements.elements[i].k33
    
        _tM[3*_nJ-3, 3*_nI-3] = -1 * _elements.elements[i].k11
        _tM[3*_nJ-3, 3*_nI-2] = -1 * _elements.elements[i].k12
        _tM[3*_nJ-3, 3*_nI-1] = -1 * _elements.elements[i].k13
        _tM[3*_nJ-2, 3*_nI-3] = -1 * _elements.elements[i].k21
        _tM[3*_nJ-2, 3*_nI-2] = -1 * _elements.elements[i].k22
        _tM[3*_nJ-2, 3*_nI-1] = -1 * _elements.elements[i].k23
        _tM[3*_nJ-1, 3*_nI-3] = -1 * _elements.elements[i].k31
        _tM[3*_nJ-1, 3*_nI-2] = -1 * _elements.elements[i].k32
        _tM[3*_nJ-1, 3*_nI-1] = -1 * _elements.elements[i].k33
        
        _stiffnessMatrix = _stiffnessMatrix + _tM
    
#    print (_stiffnessMatrix)
    
    # adding constraint conditions to the stiffness matrix       
    _numConst = len(_constraints.constraints)
    for i in range(_numConst):
        _tCMX = zeros((3*_numNode, 3*_numNode))
        _tCMY = zeros((3*_numNode, 3*_numNode))
        _tCMZ = zeros((3*_numNode, 3*_numNode))
        if (_constraints.constraints[i].cX == 1):
            _ncI = _constraints.constraints[i].nodeId
            _stiffnessMatrix[3*_ncI-3, : ] = 0.0
            _stiffnessMatrix[: , 3*_ncI-3] = 0.0
            _stiffnessMatrix[3*_ncI-3, 3*_ncI-3] = 1.0
            
        if (_constraints.constraints[i].cY == 1):
            _ncI = _constraints.constraints[i].nodeId
            _stiffnessMatrix[3*_ncI-2, : ] = 0.0
            _stiffnessMatrix[: , 3*_ncI-2] = 0.0
            _stiffnessMatrix[3*_ncI-2, 3*_ncI-2] = 1.0
            
        if (_constraints.constraints[i].cZ == 1):
            _ncI = _constraints.constraints[i].nodeId
            _stiffnessMatrix[3*_ncI-1, : ] = 0.0
            _stiffnessMatrix[: , 3*_ncI-1] = 0.0
            _stiffnessMatrix[3*_ncI-1, 3*_ncI-1] = 1.0

#    print (_stiffnessMatrix)
    return _stiffnessMatrix

def createStiffnessMatrix2drahmen(_nodes, _elements, _constraints):
    
    _numElem = len(_elements.elements)
    _numNode = len(_nodes.nodes)
    _stiffnessMatrix = zeros((3*_numNode, 3*_numNode))
    
    
    
    return _stiffnessMatrix

def createLoadVector2d(_nodes, _loads):
    
    _numNode = len(_nodes.nodes)
    _loadVec = zeros((2*_numNode, 1))
    for i in range(_numNode):
        _tempVec = zeros((2*_numNode, 1))
        
        _tempVec[2*i, 0] = _nodes.nodes[i].loadX
        _tempVec[2*i+1 , 0] = _nodes.nodes[i].loadY
        
        _loadVec = _loadVec + _tempVec
    
    return _loadVec

def createLoadVector3d(_nodes, _loads):
    
    _numNode = len(_nodes.nodes)
    _loadVec = zeros((3*_numNode, 1))
    for i in range(_numNode):
        _tempVec = zeros((3*_numNode, 1))
        
        _tempVec[3*i, 0] = _nodes.nodes[i].loadX
        _tempVec[3*i+1, 0] = _nodes.nodes[i].loadY
        _tempVec[3*i+2, 0] = _nodes.nodes[i].loadZ
        
        _loadVec = _loadVec + _tempVec
    
    return _loadVec

def GaussianElimination(self):

    # noch etwas hinzufuegen !!!
    
    return

def obtainInverseMatrix(self):
    
    return linalg.inv(self)

def obtainDefVector(_KI, _loadVec, _nodes):

    _defVec = dot(_KI, _loadVec)
    if isinstance(_nodes.nodes[0], Node):
        _nodes.appendDeformation(_defVec) ## need to move this part onto classNode
    
    elif isinstance(_nodes.nodes[0], Node3d):
        _nodes.appendDeformation3dTruss(_defVec) ## need to move this part onto classNode
    
    return _defVec

def obtainNormalForceStressStrain(_nodes, _elements, _sections, _defVec):
    
    for i in range(len(_elements.elements)):
        _k = _elements.elements[i].localStiffness
        _sn = _elements.elements[i].sinElem
        _cs = _elements.elements[i].cosElem
        _ar = _sections.getArea(_elements.elements[i].secNo)
        
        _dx1 = _nodes.findNodeById(_elements.elements[i].n1).defX
        _dy1 = _nodes.findNodeById(_elements.elements[i].n1).defY
        _dx2 = _nodes.findNodeById(_elements.elements[i].n2).defX
        _dy2 = _nodes.findNodeById(_elements.elements[i].n2).defY
    
        _elements.elements[i].fN = _k * (_cs * (float(_dx2 - _dx1)) + _sn * (float(_dy2 - _dy1)))
        _elements.elements[i].sigmaN = (_elements.elements[i].fN) / _ar
        _elements.elements[i].strain = (_elements.elements[i].fN) / _k
    
    return

def obtainNormalForceStressStrain3dTruss(_nodes, _elements, _sections, _defVec):
    
    for i in range(len(_elements.elements)):
        _k = _elements.elements[i].localStiffness
        
        _tL = _elements.elements[i].cosxx
        _tM = _elements.elements[i].cosxy
        _tN = _elements.elements[i].cosxz
        
        _ar = _sections.getArea(_elements.elements[i].secNo)
        
        _dx1 = float(_nodes.findNodeById(_elements.elements[i].n1).defX)
        _dy1 = float(_nodes.findNodeById(_elements.elements[i].n1).defY)
        _dz1 = float(_nodes.findNodeById(_elements.elements[i].n1).defZ)
        _dx2 = float(_nodes.findNodeById(_elements.elements[i].n2).defX)
        _dy2 = float(_nodes.findNodeById(_elements.elements[i].n2).defY)
        _dz2 = float(_nodes.findNodeById(_elements.elements[i].n2).defZ)
    
        _elements.elements[i].fN = _k * (_tL * (float(_dx2 - _dx1)) + _tM * (float(_dy2 - _dy1)) + _tN * (float(_dz2 - _dz1)))
        _elements.elements[i].sigmaN = (_elements.elements[i].fN) / _ar
        _elements.elements[i].strain = (_elements.elements[i].fN) / _k
    
    return
