#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except ImportError:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *

from gui import Form
from glossary import Glossary

def main():
    import sys, traceback
    app = QApplication(sys.argv)
    parent = QDialog()
    try:
        form = Form()
        form.show()
        parent = form
        form.init_storage(Glossary())
        sys.exit(app.exec_())
    except Exception:
        QMessageBox.critical(parent, "Error (please send a report!)", traceback.format_exc())
        sys.exit(app.quit())

if __name__ == '__main__':
    main()
