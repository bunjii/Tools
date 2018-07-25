
# ***** PROPERTY CLASS *****
class Section(object):
    
    def __init__(self, _id, _area, _inertia):
        self.id = _id
        self.area = _area
        self.inertia = _inertia

class Sections(object):
    
    def __init__(self):
        self.sections = []
        
    def appendSection(self, _id, _area, _inertia):
        self.sections.append(Section(_id, _area, _inertia))
        
    def getArea(self, _id):
        for i in range(len(self.sections)):
            if (self.sections[i].id == _id):
                return self.sections[i].area
    
    def getI(self, _secNo):
        for i in range(len(self.sections)):
            if (self.sections[i].id == _secNo):
                return self.sections[i].inertia
        
    def outputSectionsInfo(self):
        _templines = str()
        for i in range(len(self.sections)):
            _templines = '\n'.join([_templines, ', '.join(["SEC", \
                "{0: >6}".format(self.sections[i].id),
                "{0:10.3f}".format(self.sections[i].area),
                "{0:10.3f}".format(self.sections[i].inertia)])])
        return _templines