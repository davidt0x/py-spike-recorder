# -*- coding: utf-8 -*-
import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets

from spike_recorder.experiments.iowa.instructions_ui import Ui_dialog_instructions
from spike_recorder.experiments.iowa.iowa_ui import Ui_main_window

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

        # Lets prepopulate the output file name with something
        index = 1
        filename = f"iowa_output{index}.csv"
        while os.path.isfile(filename):
            index = index + 1
            filename = f"iowa_output{index}.csv"

        self.textbox_file.setText(filename)

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


class IowaMainWindow(QtWidgets.QMainWindow, Ui_main_window):
    """
    The main window GUI for the Iowa Gambling task experiment.
    """

    # The maximum number of deck pulls to allow the user.
    MAX_DECK_PULLS = 100

    MAX_WINNINGS = MAX_DECK_PULLS * 350

    MAX_LOSSES = MAX_DECK_PULLS * 350

    # The starting winnings
    INITIAL_WINNINGS = 2000

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        # Setup the exerpiment status variables
        self.winnings = self.INITIAL_WINNINGS
        self.losses = 0
        self.last_win = 0
        self.last_loss = 0
        self.deck_pull_index = 0

        self.progress_winnings.setMaximum(self.MAX_WINNINGS)
        self.progress_losses.setMaximum(self.MAX_LOSSES)

        # Update the status
        self.update_status()

    def update_status(self):
        """
        Update any status fields with the current state of the experiment.

        Returns:
            None
        """
        self.label_last_win.setText(f'Winnings on last trial: <font color="#0571b0">${self.last_win}</font>')
        self.label_last_loss.setText(f'Losses on last trial: <font color="#ca0020">${self.last_loss}</font>')
        net = self.last_win - self.last_loss
        color = "#0571b0" if net >= 0 else "#ca0020"
        self.label_net_win.setText(f'Net Winnings: <font color="{color}">${net}</font>')

        # Update the progress bars
        self.progress_winnings.setValue(self.winnings)
        self.progress_winnings.setFormat(f"${self.winnings}")
        self.progress_losses.setValue(self.losses)
        self.progress_losses.setFormat(f"${self.losses}")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = IowaMainWindow(None)
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

            # Check if we can open the file. If so, set the output file on the main app
            # and we are ready to go!
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

    # Run the main app
    sys.exit(app.exec_())

