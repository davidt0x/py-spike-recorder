# -*- coding: utf-8 -*-

import sys
import os
import logging

import pandas as pd

from PyQt5 import QtCore, QtGui, QtWidgets

from spike_recorder.experiments.libet.libet_ui import Ui_Libet
from spike_recorder.experiments.libet.instructions_ui import Ui_dialog_instructions

from spike_recorder.experiments.libet.data import LibetData

# It seems I need to add this to get trace backs to show up on
# uncaught python exceptions.
def catch_exceptions(t, val, tb):
    old_hook(t, val, tb)
    sys.exit(-1)

old_hook = sys.excepthook
sys.excepthook = catch_exceptions


class IntroDialog(QtWidgets.QDialog, Ui_dialog_instructions):
    """
    The intro instructions dialog box. Allows selecting the output file.
    """
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.button_browse.clicked.connect(self.get_directory)

    def reject(self):
        """
        If the user clicks cancel, we can't proceeed, exit the app.

        Returns:
            None
        """
        sys.exit(0)

    def get_directory(self):
        dialog = QtWidgets.QFileDialog()
        foo_dir = dialog.getExistingDirectory(self, 'Select an output directory')

        # Add a slash at the end
        foo_dir = foo_dir + '/'

        self.textbox_file.setText(foo_dir)


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

        self.output_filename = None

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

        # Dump the data back out to file. We will just dump everything back out over and over again
        # so that if the user stops half way through, they have part of their data.
        if self.output_filename is not None:
            self.data.to_csv(self.output_filename)
        else:
            logging.warning("Output filename is not definied, results are not being saved.")

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

    # Show the instructions and ask for an output file name. Do some error
    # checking if the file isn't valid.
    fileNoGood = True
    while fileNoGood:
        # Try to open the output file for writing
        try:
            intro_d = IntroDialog()
            intro_d.show()
            intro_d.textbox_file.setFocus()
            intro_d.exec_()

            # Grab the filename from the textbox
            filename = intro_d.textbox_file.text()

            # Check if the file exists already, make sure they want to overwrite?
            if os.path.isfile(filename):
                qm = QtWidgets.QMessageBox
                retval = qm.question(intro_d, "", "This file already exists. "
                                                  "Are you sure you want it to be overwritten?",
                                     qm.Yes | qm.No)

                if retval == qm.No:
                    continue


            # Check if we can open the file. If so, we are ready to go
            with open(filename, 'w') as f:
                fileNoGood = False
                ui.output_filename = intro_d.textbox_file.text()

        except Exception as ex:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Output file could not be opened. Check the path.")
            msg.setDetailedText(f"{ex}")
            msg.setWindowTitle("Output File Error")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()



    sys.exit(app.exec_())

