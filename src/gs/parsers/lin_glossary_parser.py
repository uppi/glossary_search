from parser import XlsParser, Row
from languages.korean import noun_endings
from methods.morph_search import MorphSearch

class LineageGlossaryParser(XlsParser):
    def __init__(self, fileName):
        XlsParser.__init__(self, fileName)
        self.sheet = self.wb.sheet_by_index(0)
        self.colnum = 0
        self.rownum = 1
        self.currentGen = None
        self.dict = {}
        self.search_method = MorphSearch(noun_endings)

    def position(self):
        return u"col_" + unicode(self.colnum) + u"_row_" + unicode(self.rownum)

    def next(self):
        while(True):
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

"""
    def add_colpair(self, sheet, key_col_num, value_col_num):
        self.statusMessageSent.emit("Adding {0} {1}".format(key_col_num, value_col_num))
        for rownum in range(1, sheet.nrows):
            key = unicode(sheet.row_values(rownum)[key_col_num])
            data = unicode(sheet.row_values(rownum)[value_col_num])
            if not key and data:
                key = u"no_data_col_" + str(key_col_num) + u"_row_" + str(rownum)
            elif key in self.dict and self.search_method.prepare_text(self.dict[key].val()) != self.search_method.prepare_text(data):
                key = key + u"_col_" + str(key_col_num) + u"_row_" + str(rownum)
            self.dict[key] = Row([key, data])

    def parse_xls(self, path):
        rb = xlrd.open_workbook(path)
        sheet = rb.sheet_by_index(0)
        for colnum in xrange(0, sheet.ncols ,2):
            self.add_colpair(sheet, colnum + 1, colnum)
"""