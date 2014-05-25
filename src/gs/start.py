#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
import xlrd, re

from gui import Form
from glossary import Glossary
from methods import MorphSearch
from languages import endings

def main():
    import sys, traceback
    app = QApplication(sys.argv)
    parent = QDialog()
    try:
        form = Form()
        form.show()
        parent = form
        form.initStorage(Glossary(MorphSearch(endings["korean"])))
        sys.exit(app.exec_())
    except Exception as e:
        QMessageBox.critical(parent, "Error", traceback.format_exc())
        sys.exit(app.quit())

if __name__ == '__main__':
    main()