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
    import sys, traceback
    app = QApplication(sys.argv)
    parent = QDialog()
 
    try:
        glossary = Glossary()
        form = Form(glossary)
        form.show()
        parent = form

        form.inputTextEdit.setDisabled(True);
        form.inputTextEdit.setPlainText("Parsing... ");
        fileName = './glossary_xls.xls'
        try:
            with open(fileName, "r") as f:
                pass
        except:
            fileName = QFileDialog.getOpenFileName(form, "Open glossary", ".", "glossary (*.xls *.xlsx)");
            try:
                glossary.parse_xls(fileName)
            except:
                glossary.parse_xls(fileName[0])
            glossary.make_index()
            form.inputTextEdit.setPlainText("");
            form.inputTextEdit.setDisabled(False);
        sys.exit(app.exec_())
    except Exception as e:
        QMessageBox.critical(parent, "Error", traceback.format_exc())
        sys.exit(app.quit())

if __name__ == '__main__':
    main()