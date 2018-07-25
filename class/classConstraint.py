
# ***** PROPERTY CLASS *****
class Constraint(object):
    
    def __init__(self, _id, _nodeId, _cX, _cY):
        self.id = _id
        self.nodeId = _nodeId
        self.cX = _cX
        self.cY = _cY
        
#class Constraint2dR(object):
#    
#    def __init__(self, _id, _nodeId, _cX, _cY, _angle, _rigidRatio):
#        self.id = _id
#        self.nodeId = _nodeId
#        self.cX = _cX
#        self.cY = _cY
#        self.angle = _angle
#        self.rigidRatio = _rigidRatio

class Constraint3d(object):
    
    def __init__(self, _id, _nodeId, _cX, _cY, _cZ):
        self.id = _id
        self.nodeId = _nodeId
        self.cX = _cX
        self.cY = _cY
        self.cZ = _cZ
    
class Constraints(object):
    
    def __init__(self):
        self.constraints = []
    
    def appendConstraint(self, _id, _nodeId, _cX, _cY):
        self.constraints.append(Constraint(_id, _nodeId, _cX, _cY))
        
#    def appendConstraint2dR(self, _id, _nodeId, _cX, _cY, _angle, _rigidRatio):
#        self.constraints.append(Constraint2dR(_id, _nodeId, _cX, _cY, _angle, _rigidRatio))

    def appendConstraint2dR(self, _id, _angle, _rigidRatio):
        for i in range(len(self.constraints)):
            if self.constraints[i].id == _id:
                self.constraints[i].angle = _angle
                self.constraints[i].rigidRatio = _rigidRatio
        
    def appendConstraint3d(self, _id, _nodeId, _cX, _cY, _cZ):
        self.constraints.append(Constraint3d(_id, _nodeId, _cX, _cY, _cZ))
        
        
    def outputConstraintsInfo(self):
        _templines = str()
        for i in range(len(self.constraints)):
            _templines = '\n'.join([_templines, ', '.join(["CONS", \
                "{0: >5}".format(self.constraints[i].id),
                "{0: >5}".format(self.constraints[i].nodeId),
                "{0: >5}".format(self.constraints[i].cX),
                "{0: >5}".format(self.constraints[i].cY)])])
    
        return _templines
    
    def outputConstraintsInfo3d(self):
        _templines = str()
        for i in range(len(self.constraints)):
            _templines = '\n'.join([_templines, ', '.join([str(self.constraints[i].id),
                                                           str(self.constraints[i].nodeId),
                                                           str(self.constraints[i].cX),
                                                           str(self.constraints[i].cY),
                                                           str(self.constraints[i].cZ)])])
        return _templines