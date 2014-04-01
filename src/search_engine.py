try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
    
import xlrd, re

class SearchEngine(object):
    def __init__(self):
        self.dict = {}
        self.regexdict = {}

    @staticmethod
    def make_one_word_regex_part(word, rich=False):
        result = "(?:(?:^)|[ .+-])" + re.escape(word)
        if len(word) != 1:
            result += "?"
        if rich:
            return "(" + result + "[^ ]?" + ")"
        else:
            return result + "[^ ]?"

    @staticmethod
    def make_regex(value, rich=False):
        value = unicode(value)
        words = value.split()
        if words:
            return re.compile(u' *'.join(SearchEngine.make_one_word_regex_part(word, rich) for word in words), re.U) 
        return None

    def add_colpair(self, sheet, key_col_num, value_col_num):
        print "add", key_col_num, value_col_num
        for rownum in range(1, sheet.nrows):
            key = unicode(sheet.row_values(rownum)[key_col_num])
            data = unicode(sheet.row_values(rownum)[value_col_num])
            if not key and data:
                key = "no_data_col_" + str(key_col_num) + "_row_" + str(value_col_num)
            if key in self.dict and self.dict[key] != data:
                key = key + "_col_" + str(key_col_num) + "_row_" + str(value_col_num)
            self.dict[key] = data

    def parse_xls(self, path):
        rb = xlrd.open_workbook(path)
        sheet = rb.sheet_by_index(0)
        self.add_colpair(sheet, 3, 2)
        self.add_colpair(sheet, 5, 4)
        self.add_colpair(sheet, 7, 6)
        self.add_colpair(sheet, 9, 8)
        self.add_colpair(sheet, 11, 10)

    def make_index(self):    
        print "making index for", len(self.dict), "items"   
        errors = 0
        for key, value in self.dict.iteritems():
            regex = None
            try:
                regex = self.make_regex(value)
            except Exception as e:
                print str(e)
                errors += 1
                pass
            if regex:
                self.regexdict[key] = regex
        print errors

    def search(self, text):
        result = {}
        for key, regex in self.regexdict.iteritems():
            if regex.search(text):
                result[key] = self.dict[key]
        return result
