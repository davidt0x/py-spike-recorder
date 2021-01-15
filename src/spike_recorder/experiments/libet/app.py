# -*- coding: utf-8 -*-

import sys

import pandas as pd

from PyQt5 import QtCore, QtGui, QtWidgets

from spike_recorder.experiments.libet.libet_ui import Ui_Libet
from spike_recorder.experiments.libet.data import LibetData

# It seems I need to add this to get trace backs to show up on
# uncaught python exceptions.
def catch_exceptions(t, val, tb):
    old_hook(t, val, tb)
    sys.exit(-1)

old_hook = sys.excepthook
sys.excepthook = catch_exceptions

class LibetMainWindow(QtWidgets.QMainWindow, Ui_Libet):
    """
    The main application class for the Libet experiement.
    """

    NUM_PRACTICE_TRIALS = 2

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        # adding action to a buttons
        self.button_next.clicked.connect(self.next_trial_click)
        self.button_retry.clicked.connect(self.retry_trial_click)

        self.data = LibetData()

    def update_status(self):
        """
        Update any status fields with the current state of the experiment.

        Returns:
            None
        """
        self.label_status.setText(f"Trial: {self.data.num_trials()+1}")

    def restart_trial(self):
        """
        Restart the current trial.

        Returns:
            None
        """
        self.clock_widget.reset_clock()
        self.clock_widget.start_clock()
        self.button_next.setText("Stop")
        self.button_next.setStyleSheet("background-color : red;")
        self.button_retry.setEnabled(False)

        self.update_status()

    def stop_trial(self):
        """
        Stop the trial.

        Returns:

        """
        self.clock_widget.stop_clock()
        self.button_next.setText("Next Trial")
        self.button_next.setStyleSheet("")
        self.button_retry.setEnabled(True)

        # Store the trial data
        self.data.add_trial(stop_time_msecs=self.clock_widget.msecs_elapsed())

    def next_trial_click(self):
        """
        When the next trial button is clicked. This can also be the stop clock button when the trial is running.

        Returns:
            None
        """

        if not self.clock_widget.clock_stopped:
            self.stop_trial()
        else:
            self.restart_trial()

    def retry_trial_click(self):
        """
        Retry the trial, don't save the last trials results.

        Returns:
            None
        """

        # Don't keep the last trials data
        self.data.remove_last_trial()

        self.restart_trial()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = LibetMainWindow(None)
    ui.showNormal()
    sys.exit(app.exec_())

