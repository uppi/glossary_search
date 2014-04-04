# -*- coding: utf-8 -*-

try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
    
import xlrd, re
from search_method import MorphSearch as SearchMethod

class Glossary(QObject):
    statusMessageSent = pyqtSignal(['QString'])

    def __init__(self):
        super(Glossary, self).__init__()
        self.dict = {}
        self.regexdict = {}

    def add_colpair(self, sheet, key_col_num, value_col_num):
        self.statusMessageSent.emit("Adding {0} {1}".format(key_col_num, value_col_num))
        for rownum in range(1, sheet.nrows):
            key = unicode(sheet.row_values(rownum)[key_col_num])
            data = unicode(sheet.row_values(rownum)[value_col_num])
            if not key and data:
                key = "no_data_col_" + str(key_col_num) + "_row_" + str(rownum)
            if key in self.dict and self.dict[key] != data:
                key = key + "_col_" + str(key_col_num) + "_row_" + str(rownum)
            self.dict[key] = data

    def parse_xls(self, path):
        rb = xlrd.open_workbook(path)
        sheet = rb.sheet_by_index(0)
        for colnum in xrange(0, sheet.ncols ,2):
            self.add_colpair(sheet, colnum + 1, colnum)

    def make_index(self):
        count = len(self.dict)
        done = 0
        errors = 0
        for key, value in self.dict.iteritems():
            if done % 200 == 0:
                self.statusMessageSent.emit("Compiled {0} of {1} messages ({2}%)".format(done, count, (100 * done) / count))
            regex = None
            try:
                regex = SearchMethod.make_regex(value)
            except Exception as e:
                errors += 1
                pass
            if regex:
                self.regexdict[key] = regex
            else:
                errors += 1
            done += 1
        self.statusMessageSent.emit("Done. Errors count: " + str(errors))

    def search(self, text):
        result = {}
        text = SearchMethod.prepare_text(text)
        for key, regex in self.regexdict.iteritems():
            if regex.search(text):
                result[key] = self.dict[key]
        return result
