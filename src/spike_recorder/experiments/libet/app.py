# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

from spike_recorder.experiments.libet.libet_ui import Ui_Libet

class LibetMainWindow(QtWidgets.QMainWindow, Ui_Libet):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        # adding action to a button
        self.button_next.clicked.connect(self.next_trial_click)

    def next_trial_click(self):
        if not self.clock_widget.clock_stopped:
            self.clock_widget.stop_clock()
        else:
            self.clock_widget.reset_clock()
            self.clock_widget.start_clock()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = LibetMainWindow(None)
    ui.showNormal()
    sys.exit(app.exec_())

