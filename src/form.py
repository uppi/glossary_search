# -*- coding: utf-8 -*-

try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *

import traceback
from search_method import MorphSearch as SearchMethod

class Form(QMainWindow):
    def __init__(self, glossary, parent=None):
        super(Form, self).__init__(parent)
        self.glossary = glossary
        self.glossary.statusMessageSent.connect(self.showStatusMessage)
        self.curPlainText = ""

        inputLabel = QLabel("Input:")
        self.inputTextEdit = QTextEdit()
        resultLabel = QLabel("Results:")
        self.resultTable = QTableWidget()
        self.resultTable.setColumnCount(3)
        self.resultTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.resultTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.resultTable.setHorizontalHeaderLabels(["Translation", "Foreign word", "Matched"])

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
        text = unicode(self.inputTextEdit.toPlainText())
        sr = self.glossary.search(text)

        self.foundMatchObjects = {}
        searchResult = []
        for key, value in sr.iteritems():
            rich_regex = SearchMethod.make_regex(value, True)
            maxlen_val = ""
            if rich_regex:
                self.foundMatchObjects[key] = [x.group(0) for x in rich_regex.finditer(text)]
                for x in self.foundMatchObjects[key]:
                    if len(x) > len(maxlen_val):
                        maxlen_val = x
            else:
                self.foundMatchObjects[key] = []
            searchResult += [(key, value, maxlen_val)]

        searchResult = sorted(searchResult, cmp = lambda x, y : len(y[2]) - len(x[2]))

        self.resultTable.setRowCount(len(searchResult))
        for row in xrange(0, len(searchResult)):
            self.resultTable.setItem(row, 0, QTableWidgetItem(searchResult[row][0]))
            self.resultTable.setItem(row, 1, QTableWidgetItem(searchResult[row][1]))
            self.resultTable.setItem(row, 2, QTableWidgetItem(searchResult[row][2]))
        self.resultTable.resizeColumnsToContents()


    def showStatusMessage(self, message):
        self.statusBar().showMessage(message)
        QApplication.processEvents()

    def highlight(self, cur, prev):
        key_selected = unicode(self.resultTable.item(self.resultTable.currentRow(), 0).text())
        value_selected = unicode(self.resultTable.item(self.resultTable.currentRow(), 1).text())
        text = unicode(self.inputTextEdit.toPlainText())
        try:
            matches = self.foundMatchObjects[key_selected]
            ready_text = text
            for i in xrange(len(matches)):
                ready_text = ready_text.replace(matches[i], u"{{0}}".format(i), 1)
            print "after first:", ready_text
            matches_hl = [u'<font style="background:green">' + m + u'</font>' for m in matches]
            print matches_hl
            ready_text = unicode(ready_text).format(*matches_hl)
            self.inputTextEdit.setHtml(ready_text)
            """
            tohl = [(mo.start(0), mo.end(0)) for mo in matches if mo]
            tohltxts = [text[m[0]:m[1]] for m in tohl]
            hltxts = ['<font style="background:green">' + t + '</font>' for t in tohltxts]
            all_parts = [(0, 0)] + tohl + [(-1, -1)]
            simpletxts = []
            for i in xrange(1, len(all_parts)):
                simpletxts += [text[all_parts[i - 1][1]:all_parts[i][0]]]
            ready_text = "".join([hltxts[i] + simpletxts[i] for i in xrange(0, len(hltxts))]) + simpletxts[-1]
            print "tohl", tohl
            print "tohltxts", tohltxts
            print "hltxts", hltxts
            print "all_parts", all_parts
            print "simpletxts", simpletxts
            print "ready_text", ready_text 
            """
            #regex = SearchMethod.make_regex(value_selected, True)
            #mo = regex.search(text)
            #if mo:
            #    highlightedText = text[mo.start(0):mo.end(0)]
            """
            if highlightedText != value_selected:
                print "not equal!"
                ht = unicode(highlightedText).split()
                vs = unicode(value_selected).split()
                spaces = re.split('[^ ]+', highlightedText)
                if len(ht) != len(vs):
                    print "Life is hard."
                elif len(spaces) != len(ht):
                    print "Life is hard with spaces."
                    print spaces
                else:
                    for i in xrange(0, len(ht)):
                        if len(ht[i]) != len(vs[i]):
                            print "len!"
                            ht[i] += '<font style="background:red"> </font>'
                        elif ht[i][-1] != vs[i][-1]:
                            print "neq!"
                            ht[i] = ht[i][:-1] + '<font style="background:red">' + ht[i][-1] + '</font>'
                    for i in xrange(0, len(spaces)):
                        ht[i] += spaces[i]
                print "so the text is ready"
                highlightedText = "".join(ht)
            """
            #    text = text[:mo.start(0)] + '<font style="background:green">' + highlightedText + '</font>' + text[mo.end(0):]
            #    self.inputTextEdit.setHtml(text)
            #else:
            #    self.inputTextEdit.setPlainText(text)
        except Exception as e:
            traceback.print_exc()
            self.inputTextEdit.setPlainText(text)

    def initStorage(self):
        self.inputTextEdit.setDisabled(True);
        self.inputTextEdit.setPlainText("Initialization... ");
        fileName = './glossary_xls.xls'
        try:
            with open(fileName, "r") as f:
                pass
        except:
            fileName = QFileDialog.getOpenFileName(self, "Open glossary", ".", "glossary (*.xls *.xlsx)");
        if not fileName:
            raise Exception("You need to choose glossary file")
        if fileName is tuple:
            fileName = fileName[0]
        self.showStatusMessage("Parsing glossary file " + fileName)
        self.glossary.parse_xls(fileName)
        self.glossary.make_index()
        self.inputTextEdit.setPlainText("");
        self.inputTextEdit.setDisabled(False);
