# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import webbrowser


class Ui_Entry(object):
    def setupUi(self, Form, link, realLink):
        Form.setObjectName("Form")
        Form.resize(779, 41)
        Form.setMaximumSize(QtCore.QSize(1677215, 80))
        Form.setStyleSheet("background-color: rgb(255,255,255);")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.visitButton = QtWidgets.QPushButton(Form)
        self.visitButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.visitButton.setStyleSheet("color: rgb(0, 0, 0);")
        self.visitButton.setObjectName("visitButton")
        self.visitButton.clicked.connect(lambda: webbrowser.open(realLink))
        self.horizontalLayout.addWidget(self.visitButton)
        self.linkLbl = QtWidgets.QLabel(Form)
        self.linkLbl.setText(link)
        self.linkLbl.setStyleSheet("font: 14pt \"Tahoma\";\n"
                                   "color: rgb(0, 0, 0);")
        self.linkLbl.setObjectName("linkLbl")
        self.horizontalLayout.addWidget(self.linkLbl)
        self.link = link
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.visitButton.setText(_translate("Form", "Go"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Entry()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

