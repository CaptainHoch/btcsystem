# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'result.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(861, 690)
        MainWindow.setStyleSheet("background-color: rgb(73, 88, 94);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.backButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.backButton.setMinimumSize(QtCore.QSize(40, 40))
        self.backButton.setMaximumSize(QtCore.QSize(40, 40))
        self.backButton.setBaseSize(QtCore.QSize(40, 40))
        self.backButton.setText("")
        self.backButton.setIconSize(QtCore.QSize(40, 40))
        self.backButton.setCheckable(False)
        self.backButton.setObjectName("backButton")
        self.horizontalLayout.addWidget(self.backButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(255, 255, 255);")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.resultWidget = QtWidgets.QListWidget(self.centralwidget)
        self.resultWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.resultWidget.setObjectName("resultWidget")
        self.verticalLayout.addWidget(self.resultWidget)
        self.pieBox = QtWidgets.QFrame(self.centralwidget)
        self.pieBox.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.pieBox.setFrameShadow(QtWidgets.QFrame.Raised)
        self.pieBox.setObjectName("pieBox")
        self.verticalLayout.addWidget(self.pieBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Web Crawler"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

