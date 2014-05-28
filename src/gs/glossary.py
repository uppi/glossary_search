# -*- coding: utf-8 -*-

try:
    from PyQt4.QtCore import *
except:
    from PyQt5.QtCore import *
    
import re
from parsers import Parser, Row

class Glossary(QObject):
    statusMessageSent = pyqtSignal(['QString'])

    def __init__(self):
        super(Glossary, self).__init__()
        self.rows = []

    def parse(self, path):
        parser = Parser.get(path)
        self.search_method = parser.search_method # todo: fix
        row = parser.next()
        while row:
            self.rows.append(row)
            row = parser.next()

    def make_index(self):
        count = len(self.rows)
        print count
        done = 0
        errors = 0
        for i in xrange(len(self.rows)):
            if done % 200 == 0:
                self.statusMessageSent.emit("Compiled {0} of {1} messages ({2}%)".format(done, count, (100 * done) / count))
            regex = None
            try:
                regex = self.search_method.make_regex(self.rows[i].val())
            except Exception as e:
                print e
                pass
            if not regex:
                errors += 1
            self.rows[i].regex = regex
            done += 1
        self.rows = [row for row in self.rows if row.regex]
        self.statusMessageSent.emit("Done. Errors count: " + str(errors))

    def search(self, text):
        result = []
        text = self.search_method.prepare_text(text)
        for row in self.rows:
            if row.regex.search(text):
                result.append(row)
        return result
