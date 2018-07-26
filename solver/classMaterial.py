
# ***** PROPERTY CLASS *****
class Material(object):
    
    def __init__(self, _id, _name, _em):
        self.id = _id
        self.name = _name
        self.em = _em

    def assignEmToElem(self, _id):
        pass

class Materials(object):
    
    def __init__(self):
        self.materials = []
        
    def appendMaterial(self, _id, _name, _em):
        self.materials.append(Material(_id, _name, _em))
        
    def getEmod(self, _matNo):
        for i in range(len(self.materials)):
            if(self.materials[i].id == _matNo):
                return self.materials[i].em
            else: pass #exception

    def outputMaterialsInfo(self):
        _templines = str()
        for i in range(len(self.materials)):
            _templines = '\n'.join([_templines, ', '.join(["MAT", \
                "{0: >6}".format(self.materials[i].id),
                "{0: >5}".format(self.materials[i].name),
                "{0:10.3f}".format(self.materials[i].em)])])
        return _templines