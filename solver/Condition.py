class Conditions():
    def __init__(self):
        self.AnalysisType = -999
        
    def OutputConditions(self):
        _templines = str()

        _templines = '\n'.join([_templines, ', '.join(["ATYP", \
                "{0: >5}".format(self.AnalysisType) ])])

        return _templines
