class Conditions():
    def __init__(self):
        self.analysisType = -999
        self.unit = -999
        
    def OutputConditions(self):
        _templines = ""

        _templines += '\n'.join([_templines, ', '.join(["ATYP", \
                "{0: >5}".format(self.analysisType) ])])
        
        _templines += '\n'.join([_templines, ', '.join(["UNIT", \
        "{0: >5}".format(self.unit) ])])

        return _templines
