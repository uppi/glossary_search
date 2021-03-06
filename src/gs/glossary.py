# -*- coding: utf-8 -*-

try:
    from PyQt4.QtCore import *
except ImportError:
    from PyQt5.QtCore import *

import re
from parsers import Parser

class Glossary(QObject):
    status_message_sent = pyqtSignal(['QString'])
    errors = 0

    def __init__(self):
        super(Glossary, self).__init__()
        self.rows = []
        self.search_method = None

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
        self.errors = 0
        for i in xrange(len(self.rows)):
            if done % 200 == 0:
                self.status_message_sent.emit("Compiled {0} of {1} messages ({2}%)".format(done, count, (100 * done) / count))
            regex = None
            try:
                regex = self.search_method.make_regex(self.rows[i].val())
            except re.error:
                pass
            if not regex:
                self.errors += 1
            self.rows[i].regex = regex
            done += 1
        self.rows = [row for row in self.rows if row.regex]
        self.status_message_sent.emit("Done. Errors count: " + str(self.errors))

    def search(self, text):
        result = []
        text = self.search_method.prepare_text(text)
        for row in self.rows:
            if row.regex.search(text):
                result.append(row)
        return result
