# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'w_alert.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, uic


class AlertWidget(QtWidgets.QWidget):
    def __init__(self, info):
        self.info = info
        super().__init__()
        uic.loadUi("UI/w_alert.ui", self)
        self.save.clicked.connect(lambda: self.save_alert("INFO"))
        self.delete_2.clicked.connect(self.delete_alert)
        self.retranslateUi(info)
        QtCore.QMetaObject.connectSlotsByName(self)

    def save_alert(self, info):
        alerts = open("saved_alert.txt", "r").readlines()
        open("saved_alerts.txt").close()
        alerts.append(info + "\n")
        t = ""
        for line in alerts:
            t += line

        open("saved_alerts.txt", "w").write(t)
        open("saved_alerts.txt").close()

    def delete_alert(self):
        del (self)

    def retranslateUi(self, info):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.text.setText(_translate("Form", info))
        self.save.setText(_translate("Form", "SAVE"))

