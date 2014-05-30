from parser import XlsParser, Row
from languages.korean import NOUN_ENDINGS
from methods.morph_search import MorphSearch

class LineageGlossaryParser(XlsParser):
    def __init__(self, fileName):
        XlsParser.__init__(self, fileName)
        self.sheet = self.workbook.sheet_by_index(0)
        self.colnum = 0
        self.rownum = 1
        self.dict = {}
        self.search_method = MorphSearch(NOUN_ENDINGS)

    def position(self):
        return u"col_" + unicode(self.colnum) + u"_row_" + unicode(self.rownum)

    def next(self):
        while True:
            if self.colnum >= self.sheet.ncols:
                return None
            elif self.rownum >= self.sheet.nrows:
                self.rownum = 1
                self.colnum += 2
            else:
                key = unicode(self.sheet.row_values(self.rownum)[self.colnum + 1])
                data = unicode(self.sheet.row_values(self.rownum)[self.colnum])
                if not key and data:
                    key = u"no_data_col_" + str(self.colnum + 1) + u"_row_" + str(self.rownum)
                elif key in self.dict and self.search_method.prepare_text(self.dict[key]) != self.search_method.prepare_text(data):
                    key = key + u"_col_" + str(self.colnum + 1) + u"_row_" + str(self.rownum)
                self.rownum += 1
                if data:
                    self.dict[key] = data
                    result = Row([key, data])
                    return result
