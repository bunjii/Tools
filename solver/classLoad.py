import math

# ***** PROPERTY CLASS *****
class Load(object):
    
    def __init__(self, _id, _nodeId, _loadX, _loadY):
        self.id = _id
        self.nodeId = _nodeId
        self.loadX = _loadX
        self.loadY = _loadY
        self.vecLength = math.sqrt(_loadX ** 2 + _loadY ** 2)
        
class Load2dR(object):
    
    def __init__(self, _id, _nodeId, _loadX, _loadY, _moment):
        self.id = _id
        self.nodeId = _nodeId
        self.loadX = _loadX
        self.loadY = _loadY
        self.moment = _moment
        
class Load3d(object):
    
    def __init__(self, _id, _nodeId, _loadX, _loadY, _loadZ):
        self.id = _nodeId
        self.nodeId = _nodeId
        self.loadX = _loadX
        self.loadY = _loadY
        self.loadZ = _loadZ

class Loads(object):
    def __init__(self):
        self.loads = []
        self.maxLength = -999
        
    def appendLoad(self, _id, _nodeId, _loadX, _loadY):
        self.loads.append(Load(_id, _nodeId, _loadX, _loadY))
        if self.loads[-1].vecLength > self.maxLength:
            self.maxLength = self.loads[-1].vecLength
        
    def appendLoad2dR(self, _id, _nodeId, _loadX, _loadY, _moment):
        self.loads.append(Load2dR(_id, _nodeId, _loadX, _loadY, _moment))
        
    def appendLoad3d(self, _id, _nodeId, _loadX, _loadY, _loadZ):
        self.loads.append(Load3d(_id, _nodeId, _loadX, _loadY, _loadZ))
        
    def outputLoadsInfo(self):
        _templines = str()
        for i in range(len(self.loads)):
            _templines = '\n'.join([_templines, ', '.join(["LOAD", \
                "{0: >5}".format(self.loads[i].id),
                "{0: >5}".format(self.loads[i].nodeId),
                "{0:10.3f}".format(self.loads[i].loadX),
                "{0:10.3f}".format(self.loads[i].loadY)])])
    
        return _templines
    
    def outputLoadsInfo2dR(self):
        _templines = str()
        for i in range(len(self.loads)):
            _templines = '\n'.join([_templines, ', '.join([str(self.loads[i].id),
                                                           str(self.loads[i].nodeId),
                                                           str(self.loads[i].loadX),
                                                           str(self.loads[i].loadY),
                                                           str(self.loads[i].moment)])])
        return _templines
    
    def outputLoadsInfo3d(self):
        _templines = str()
        for i in range(len(self.loads)):
            _templines = '\n'.join([_templines, ', '.join([str(self.loads[i].id),
                                                           str(self.loads[i].nodeId),
                                                           str(self.loads[i].loadX),
                                                           str(self.loads[i].loadY),
                                                           str(self.loads[i].loadZ)])])
        return _templines