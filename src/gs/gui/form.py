# -*- coding: utf-8 -*-

try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *

import traceback

class Form(QMainWindow):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.curPlainText = ""
        inputLabel = QLabel("Input:")
        self.inputTextEdit = QTextEdit()
        resultLabel = QLabel("Results:")
        self.resultTable = QTableWidget()
        self.resultTable.setColumnCount(3)
        self.resultTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.resultTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.resultTable.setHorizontalHeaderLabels(["Translation", "Foreign word", "Matched"])
        self.searchResult = []
        mainSplitter = QSplitter(Qt.Vertical)

        splitterTop = QWidget()
        splitterTopLayout = QVBoxLayout()

        splitterTopLayout.addWidget(inputLabel)
        splitterTopLayout.addWidget(self.inputTextEdit)
        splitterTop.setLayout(splitterTopLayout)
        
        splitterBottom = QWidget()
        splitterBottomLayout = QVBoxLayout()

        splitterBottomLayout.addWidget(resultLabel)
        splitterBottomLayout.addWidget(self.resultTable)
        splitterBottom.setLayout(splitterBottomLayout)

        mainSplitter.addWidget(splitterTop)
        mainSplitter.addWidget(splitterBottom)

        self.inputTextEdit.textChanged.connect(self.handleTextChanged)
        self.resultTable.currentItemChanged.connect(self.highlight)

        self.setCentralWidget(mainSplitter)
        self.setWindowTitle("Search")

        self.statusBar().showMessage("")

        dw = QDesktopWidget()
        screenSize = dw.availableGeometry(self)
        self.setMinimumSize(QSize(screenSize.width() * 0.4, screenSize.height() * 0.3))

    def handleTextChanged(self):
        newText = u" ".join(unicode(self.inputTextEdit.toPlainText()).split())
        if self.curPlainText != newText:
            self.curPlainText = newText
            self.search()
        else:
            pass
 
    def search(self):
        if not hasattr(self, "glossary"):
            return
        text = unicode(self.inputTextEdit.toPlainText())
        sr = self.glossary.search(text)
        if not sr:
            self.searchResult = []
            self.resultTable.setRowCount(0)
            self.resultTable.setColumnCount(0)
        else:
            for i in xrange(len(sr)):
                rich_regex = self.glossary.search_method.make_regex(sr[i].val(), True)
                maxlen_val = ""
                if rich_regex:
                    sr[i].foundMatchObjects = [x.group(0) for x in rich_regex.finditer(text)]
                    for x in sr[i].foundMatchObjects:
                        if len(x) > len(maxlen_val):
                            maxlen_val = x
                else:
                    print "regex failed"
                    sr[i].foundMatchObjects = []
                sr[i].maxlen_val = maxlen_val
            sr = sorted(sr, cmp = lambda x, y : len(y.maxlen_val) - len(x.maxlen_val))
            self.searchResult = sr
            self.resultTable.setRowCount(len(sr))
            self.resultTable.setColumnCount(len(sr[0].columns) + 1)
            self.resultTable.setHorizontalHeaderLabels(([""] * (len(sr[0].columns))) + ["Matched"])
            for row in xrange(len(sr)):
                for col in xrange(len(sr[row].columns)):
                    self.resultTable.setItem(row, col, QTableWidgetItem(sr[row].columns[col]))
                self.resultTable.setItem(row, len(sr[row].columns), QTableWidgetItem(sr[row].maxlen_val))

            self.resultTable.resizeColumnsToContents()


    def showStatusMessage(self, message):
        self.statusBar().showMessage(message)
        QApplication.processEvents()

    def highlight(self, cur, prev):
        if self.searchResult:
            matches = self.searchResult[self.resultTable.currentRow()].foundMatchObjects
            text = unicode(self.inputTextEdit.toPlainText())
            try:
                ready_text = text
                for i in xrange(len(matches)):
                    ready_text = ready_text.replace(matches[i], u"{{0}}".format(i), 1)
                matches_hl = [u'<font style="background:green">' + m + u'</font>' for m in matches]
                ready_text = unicode(ready_text).format(*matches_hl)
                self.inputTextEdit.setHtml(ready_text)
            except Exception as e:
                traceback.print_exc()
                self.inputTextEdit.setPlainText(text)

    def initStorage(self, glossary):
        self.inputTextEdit.setDisabled(True);
        self.inputTextEdit.setPlainText("Initialization... ");
        fileName = u'./glossary_xls.xls'
        try:
            with open(fileName, "r") as f:
                pass
        except:
            fileName = QFileDialog.getOpenFileName(self, u"Open glossary", u".", u"glossary (*.xls *.xlsx)");
        if not fileName:
            raise Exception("You need to choose glossary file")
        if isinstance(fileName, tuple):
            fileName = fileName[0]
        fileName = unicode(fileName)
        self.showStatusMessage("Parsing glossary file " + fileName)
        self.glossary = glossary
        self.glossary.statusMessageSent.connect(self.showStatusMessage)
        self.glossary.parse(fileName)
        self.glossary.make_index()
        self.inputTextEdit.setPlainText("");
        self.inputTextEdit.setDisabled(False);
