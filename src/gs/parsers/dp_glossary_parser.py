from parser import XlsParser, Row
from methods.simple_search import SimpleSearch

class DPGlossaryParser(XlsParser):
    def __init__(self, fileName):
        XlsParser.__init__(self, fileName)
        self.sheet = self.wb.sheet_by_index(0)
        self.rownum = 1
        self.dict = {}
        self.search_method = SimpleSearch()

    def position(self):
        return unicode(self.rownum)

    def next(self):
        while(True):
            if self.rownum < self.sheet.nrows:
                key = unicode(self.sheet.row_values(self.rownum)[0])
                if key[:3] == "SYS" and key[-5:] == "_NAME":
                    key = key[3:-5]
                t = unicode(self.sheet.row_values(self.rownum)[1])
                data = unicode(self.sheet.row_values(self.rownum)[2])
                en =  unicode(self.sheet.row_values(self.rownum)[3])
                tr1 =  unicode(self.sheet.row_values(self.rownum)[4])
                tr2 =  unicode(self.sheet.row_values(self.rownum)[5])
                if not key and data:
                    key = u"no_data_row_" + str(self.rownum)
                self.rownum += 1
                if data:
                    result = Row([en, key, t, data, tr1, tr2], main_col=3)
                    return result
            else:
                return None