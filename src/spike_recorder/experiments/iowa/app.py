# -*- coding: utf-8 -*-
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from spike_recorder.experiments.iowa.iowa_ui import Ui_main_window

# It seems I need to add this to get trace backs to show up on
# uncaught python exceptions.
def catch_exceptions(t, val, tb):
    old_hook(t, val, tb)
    sys.exit(-1)

old_hook = sys.excepthook
sys.excepthook = catch_exceptions

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

