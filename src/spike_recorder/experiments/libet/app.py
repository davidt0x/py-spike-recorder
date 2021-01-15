# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\spike_recorder\experiments\libet\libet.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.clock_widget = LibetClock(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clock_widget.sizePolicy().hasHeightForWidth())
        self.clock_widget.setSizePolicy(sizePolicy)
        self.clock_widget.setStyleSheet("background-color:black;")
        self.clock_widget.setObjectName("clock_widget")
        self.verticalLayout.addWidget(self.clock_widget)
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setObjectName("grid_layout")
        self.button_next = QtWidgets.QPushButton(self.centralwidget)
        self.button_next.setObjectName("button_next")
        self.grid_layout.addWidget(self.button_next, 1, 0, 1, 1)
        self.button_retry = QtWidgets.QPushButton(self.centralwidget)
        self.button_retry.setObjectName("button_retry")
        self.grid_layout.addWidget(self.button_retry, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.grid_layout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button_next.setText(_translate("MainWindow", "Next Trial"))
        self.button_retry.setText(_translate("MainWindow", "Retry"))

from spike_recorder.experiments.libet.clock import LibetClock

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

