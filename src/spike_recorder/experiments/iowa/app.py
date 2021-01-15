# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

from spike_recorder.experiments.iowa.iowa_ui import Ui_main_window

class IowaMainWindow(QtWidgets.QMainWindow, Ui_main_window):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = IowaMainWindow(None)
    ui.showNormal()
    sys.exit(app.exec_())

