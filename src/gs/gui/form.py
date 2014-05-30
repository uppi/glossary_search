# -*- coding: utf-8 -*-

try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except ImportError:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *

import traceback, operator

class Form(QMainWindow):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.glossary = None
        self.cur_plain_text = ""
        input_label = QLabel("Input:")
        self.input_text_edit = QTextEdit()
        result_label = QLabel("Results:")
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(3)
        self.result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.result_table.setHorizontalHeaderLabels(["Translation", "Foreign word", "Matched"])
        self.search_result = []
        main_splitter = QSplitter(Qt.Vertical)

        splitter_top = QWidget()
        splitter_top_layout = QVBoxLayout()

        splitter_top_layout.addWidget(input_label)
        splitter_top_layout.addWidget(self.input_text_edit)
        splitter_top.setLayout(splitter_top_layout)

        splitter_bottom = QWidget()
        splitter_bottom_layout = QVBoxLayout()

        splitter_bottom_layout.addWidget(result_label)
        splitter_bottom_layout.addWidget(self.result_table)
        splitter_bottom.setLayout(splitter_bottom_layout)

        main_splitter.addWidget(splitter_top)
        main_splitter.addWidget(splitter_bottom)

        self.input_text_edit.textChanged.connect(self.handle_text_changed)
        self.result_table.currentItemChanged.connect(self.highlight)

        self.setCentralWidget(main_splitter)
        self.setWindowTitle("Search")

        self.statusBar().showMessage("")

        screen_size = QDesktopWidget().availableGeometry(self)
        self.setMinimumSize(QSize(screen_size.width() * 0.4, screen_size.height() * 0.3))

    def handle_text_changed(self):
        new_text = u" ".join(unicode(self.input_text_edit.toPlainText()).split())
        if self.cur_plain_text != new_text:
            self.cur_plain_text = new_text
            self.search()
        else:
            pass

    def search(self):
        if not self.glossary:
            return
        text = unicode(self.input_text_edit.toPlainText())
        res = self.glossary.search(text)
        if not res:
            self.search_result = []
            self.result_table.setRowCount(0)
            self.result_table.setColumnCount(0)
        else:
            for i in xrange(len(res)):
                rich_regex = self.glossary.search_method.make_regex(res[i].val(), True)
                maxlen_val = ""
                if rich_regex:
                    res[i].found_match_objects = [x.group(0) for x in rich_regex.finditer(text)]
                    for m_obj in res[i].found_match_objects:
                        if len(m_obj) > len(maxlen_val):
                            maxlen_val = m_obj
                else:
                    print "regex failed"
                    res[i].found_match_objects = []
                res[i].maxlen_val = maxlen_val
                res[i].maxlen = len(maxlen_val)
            res = list(reversed(sorted(res, key=operator.attrgetter("maxlen"))))
            self.search_result = res
            self.result_table.setRowCount(len(res))
            self.result_table.setColumnCount(len(res[0].columns) + 1)
            self.result_table.setHorizontalHeaderLabels(([""] * (len(res[0].columns))) + ["Matched"])
            for row in xrange(len(res)):
                for col in xrange(len(res[row].columns)):
                    self.result_table.setItem(row, col, QTableWidgetItem(res[row].columns[col]))
                self.result_table.setItem(row, len(res[row].columns), QTableWidgetItem(res[row].maxlen_val))

            self.result_table.resizeColumnsToContents()


    def show_status_message(self, message):
        self.statusBar().showMessage(message)
        QApplication.processEvents()

    def highlight(self):
        if self.search_result:
            matches = self.search_result[self.result_table.currentRow()].found_match_objects
            text = unicode(self.input_text_edit.toPlainText())
            try:
                ready_text = text
                for i in xrange(len(matches)):
                    ready_text = ready_text.replace(matches[i], u"{{0}}".format(i), 1)
                matches_hl = [u'<font style="background:green">' + m + u'</font>' for m in matches]
                ready_text = unicode(ready_text).format(*matches_hl)
                self.input_text_edit.setHtml(ready_text)
            except Exception:
                traceback.print_exc()
                self.input_text_edit.setPlainText(text)

    def init_storage(self, glossary):
        self.input_text_edit.setDisabled(True)
        self.input_text_edit.setPlainText("Initialization... ")
        file_name = u'./glossary_xls.xls'
        try:
            with open(file_name, "r"):
                pass
        except (IOError, OSError):
            file_name = QFileDialog.getOpenFileName(self, u"Open glossary", u".", u"glossary (*.xls *.xlsx)")
        if not file_name:
            raise Exception("You need to choose glossary file")
        if isinstance(file_name, tuple):
            file_name = file_name[0]
        file_name = unicode(file_name)
        self.show_status_message("Parsing glossary file " + file_name)
        self.glossary = glossary
        self.glossary.status_message_sent.connect(self.show_status_message)
        self.glossary.parse(file_name)
        self.glossary.make_index()
        self.input_text_edit.setPlainText("")
        self.input_text_edit.setDisabled(False)
