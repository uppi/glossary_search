try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *

from search_engine import SearchEngine

class Form(QWidget):
    def __init__(self, storage, parent=None):
        super(Form, self).__init__(parent)
        self.storage = storage
        self.curPlainText = ""

        inputLabel = QLabel("Input:")
        self.inputTextEdit = QTextEdit()
        resultLabel = QLabel("Results:")
        self.resultTable = QTableWidget()
        self.resultTable.setColumnCount(2)
        self.resultTable.setSelectionBehavior(QAbstractItemView.SelectRows)

        mainLayout = QVBoxLayout()

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
        mainLayout.addWidget(mainSplitter)

        self.inputTextEdit.textChanged.connect(self.handleTextChanged)
        self.resultTable.currentItemChanged.connect(self.highlight)

        self.setLayout(mainLayout)
        self.setWindowTitle("Search")

    def handleTextChanged(self):
        newText = u" ".join(unicode(self.inputTextEdit.toPlainText()).split())
        if self.curPlainText != newText:
            self.curPlainText = newText
            self.search()
        else:
            pass
 
    def search(self):
        searchResult = self.storage.search(
            unicode(self.inputTextEdit.toPlainText())).items()
        searchResult = sorted(searchResult, cmp = lambda x, y : len(y[1]) - len(x[1]))
        self.resultTable.setRowCount(len(searchResult))
        for row in xrange(0, len(searchResult)):
            self.resultTable.setItem(row, 0, QTableWidgetItem(searchResult[row][0]))
            self.resultTable.setItem(row, 1, QTableWidgetItem(searchResult[row][1]))

    def highlight(self, cur, prev):
        value_selected = self.resultTable.item(self.resultTable.currentRow(), 1).text()
        text = self.inputTextEdit.toPlainText()
        try:
            regex = SearchEngine.make_regex(value_selected, True)
            mo = regex.search(text)
            if mo:
                highlightedText = text[mo.start(0):mo.end(0)]
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
                text = text[:mo.start(0)] + '<font style="background:green">' + highlightedText + '</font>' + text[mo.end(0):]
                self.inputTextEdit.setHtml(text)
            else:
                self.inputTextEdit.setPlainText(text)
        except Exception as e:
            self.inputTextEdit.setPlainText(text)