import xlrd

class Row(object):
    def __init__(self, columns=None, main_col=1, key_col=0):
        self.columns = columns
        self.main_col = main_col
        self.key_col = key_col

    def key(self):
        return self.columns[self.key_col]

    def val(self):
        return self.columns[self.main_col]

class Parser(object):
    def __init__(self):
        pass

    def next(self):
        return None

    def status(self):
        return ""

    def progress(self):
        return 0

    @staticmethod
    def get(filePath):
        from lin_glossary_parser import LineageGlossaryParser
        from dp_glossary_parser import DPGlossaryParser
        if filePath.find("DP_Glossary") != -1:
            return DPGlossaryParser(filePath)
        return LineageGlossaryParser(filePath)

class XlsParser(Parser):
    def __init__(self, filePath):
        Parser.__init__(self)
        self.wb = xlrd.open_workbook(filePath)
