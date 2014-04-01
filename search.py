#!/usr/bin/python

try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
import xlrd, re

class Storage(object):
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
            return re.compile(u' *'.join(Storage.make_one_word_regex_part(word, rich) for word in words), re.U) 
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
            regex = Storage.make_regex(value_selected, True)
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

def main():
    import sys

    storage = Storage()

 
    app = QApplication(sys.argv)
 
    form = Form(storage)
    form.show()

    form.inputTextEdit.setDisabled(True);
    form.inputTextEdit.setPlainText("Parsing... ");
    fileName = './glossary_xls.xls'
    try:
        with open(fileName, "r") as f:
            pass
    except:
        fileName = QFileDialog.getOpenFileName(form, "Open glossary", ".", "glossary (*.xls)");
    try:
        try:
            storage.parse_xls(fileName)
        except:
            storage.parse_xls(fileName[0])
        storage.make_index()
        form.inputTextEdit.setPlainText("");
        form.inputTextEdit.setDisabled(False);
    except Exception as e:
        form.inputTextEdit.setPlainText("Error: " + str(e));
        raise
    sys.exit(app.exec_())

def test():
    print  Storage.make_regex("a      b   c").pattern

if __name__ == '__main__':
    main()
    test()