#!/usr/bin/env python

import sys
from PySide import QtCore, QtGui
from mainwindow import Ui_MainWindow

class MainWindow(object):
    """This is the implementation of the generated UI of the MainWindow"""
    def __init__(self, ui):
        self.ui = ui
    

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    ui_mainwindow = Ui_MainWindow()
    ui_mainwindow.setupUi(window)
    main_window = MainWindow(ui_mainwindow)
    window.show()
    sys.exit(app.exec_())
