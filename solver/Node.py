"""
# First, and before importing any Enthought packages, set the ETS_TOOLKIT
# environment variable to qt4, to tell Traits that we will use Qt.
"""
import math

# ***** PROPERTY CLASS *****

class Node(object):

    def __init__(self, _id, _x, _y):
        self.id = _id
        self.x = _x
        self.y = _y

    def getId(self):
        return self.id

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def get_distance(self, _other):
        d = math.sqrt((self.x-_other.x)**2+(self.y-_other.y)**2)
        return d

    @staticmethod
    def getMidPointCoordinates(_n1, _n2):
        tx = (_n1.x+_n2.x)/2
        ty = (_n1.y+_n2.y)/2
        return [tx, ty]


class Node3d(object):

    def __init__(self, _id, _x, _y, _z):
        self.id = _id
        self.x = _x
        self.y = _y
        self.z = _z

    def getId(self):
        return self.id

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    def getDistance3d(self, _other):
        d = math.sqrt((self.x-_other.x)**2+(self.y-_other.y)**2+(self.z-_other.z)**2)
        return d
    
    @staticmethod
    def getMidPointCoordinates(_n1, _n2):
        tx = (_n1.x+_n2.x)/2
        ty = (_n1.y+_n2.y)/2
        tz = (_n1.z+_n2.z)/2 
        return [tx, ty, tz]

class Nodes(object):
    """
    Collection Classes
    """
    def __init__(self):
        self.nodes = []

    def append_node(self, _id, _x, _y):
        self.nodes.append(Node(_id, _x, _y))

    def appendNode3d(self, _id, _x, _y, _z):
        self.nodes.append(Node3d(_id, _x, _y, _z))

    def findNodeById(self, _id):
        for i in range(len(self.nodes)):
            if self.nodes[i].id == _id:
                return self.nodes[i]
            else: pass #exception

    def appendLoad(self, _loads):
        for i in range(len(self.nodes)):
            self.nodes[i].loadX = 0.0
            self.nodes[i].loadY = 0.0

        for i in range(len(_loads.loads)):
            temp_node_id = _loads.loads[i].nodeId # left-hand side returns node id
            self.findNodeById(temp_node_id).loadX = _loads.loads[i].loadX
            self.findNodeById(temp_node_id).loadY = _loads.loads[i].loadY

    def appendLoad2dR(self, _loads):
        for i in range(len(self.nodes)):
            self.nodes[i].loadX = 0.0
            self.nodes[i].loadY = 0.0
            self.nodes[i].moment = 0.0

        for i in range(len(_loads.loads)):
            tempNId = _loads.loads[i].nodeId # left-hand side returns node id
            self.findNodeById(tempNId).loadX = _loads.loads[i].loadX
            self.findNodeById(tempNId).loadY = _loads.loads[i].loadY

    def appendLoad3d(self, _loads):
        for i in range(len(self.nodes)):
            self.nodes[i].loadX = 0.0
            self.nodes[i].loadY = 0.0
            self.nodes[i].loadZ = 0.0

        for i in range(len(_loads.loads)):
            tempNId = _loads.loads[i].nodeId
            self.findNodeById(tempNId).loadX = _loads.loads[i].loadX
            self.findNodeById(tempNId).loadY = _loads.loads[i].loadY
            self.findNodeById(tempNId).loadZ = _loads.loads[i].loadZ

    def outputNodesInfo(self):
        _templines = str()
        for i in range(len(self.nodes)):
            _templines = '\n'.join([_templines, \
            ', '.join(["NODE", "{0: >5}".format(self.nodes[i].id), \
                               "{0:10.3f}".format(self.nodes[i].x), \
                               "{0:10.3f}".format(self.nodes[i].y)])])
        return _templines

    def outputNodesInfo3dTruss(self):
        _templines = str()
        for i in range(len(self.nodes)):
            _templines = '\n'.join([_templines, ', '.join([str(self.nodes[i].id),
                                                           str(self.nodes[i].x),
                                                           str(self.nodes[i].y),
                                                           str(self.nodes[i].z)])])
        return _templines

    def outputNodesResult(self):
        _templines = str()
        for i in range(len(self.nodes)):
            _templines = '\n'.join([_templines, \
            ', '.join(["NODE", "{0: >5}".format(self.nodes[i].id),\
            "{0:10.3f}".format(self.nodes[i].defX), \
            "{0:10.3f}".format(self.nodes[i].defY)])])
        return _templines

    def outputNodesResult3dTruss(self):
        _templines = str()
        for i in range(len(self.nodes)):
            _templines = '\n'.join([_templines, ', '.join([str(self.nodes[i].id),
                                                           str(self.nodes[i].defX),
                                                           str(self.nodes[i].defY),
                                                           str(self.nodes[i].defZ)])])
        return _templines

    def appendDeformation(self, _def):  # def: resulting vector

        for i in range(len(self.nodes)):
            self.nodes[i].defX = _def[2*i, 0]
            self.nodes[i].defY = _def[2*i+1, 0]

        return

    def appendDeformation3dTruss(self, _def):  # def: resulting vector

        for i in range(len(self.nodes)):
            self.nodes[i].defX = _def[3*i, 0]
            self.nodes[i].defY = _def[3*i+1, 0]
            self.nodes[i].defZ = _def[3*i+2, 0]

        return
