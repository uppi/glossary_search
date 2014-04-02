#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
import xlrd, re

from form import Form
from glossary import Glossary

def main():
    import sys

    glossary = Glossary()
 
    app = QApplication(sys.argv)
 
    form = Form(glossary)
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
            glossary.parse_xls(fileName)
        except:
            glossary.parse_xls(fileName[0])
        glossary.make_index()
        form.inputTextEdit.setPlainText("");
        form.inputTextEdit.setDisabled(False);
    except Exception as e:
        form.inputTextEdit.setPlainText("Error: " + str(e));
        raise
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()