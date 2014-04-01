#!/usr/bin/python

try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
import xlrd, re

from form import Form
from search_engine import SearchEngine

def main():
    import sys

    storage = SearchEngine()
 
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
            raise
            storage.parse_xls(fileName[0])
        storage.make_index()
        form.inputTextEdit.setPlainText("");
        form.inputTextEdit.setDisabled(False);
    except Exception as e:
        form.inputTextEdit.setPlainText("Error: " + str(e));
        raise
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()