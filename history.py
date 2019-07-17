# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'history.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import json
import match


class Ui_History(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        with open('history\history.txt') as json_file:
            self.history = json.load(json_file)
        self.setObjectName("History")
        self.resize(871, 697)
        self.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 15pt \"Tahoma\";")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.historyWidget = QtWidgets.QListWidget(self.centralwidget)
        self.historyWidget.setObjectName("historyWidget")
        self.verticalLayout.addWidget(self.historyWidget)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.filterEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.filterEdit.setObjectName("filterEdit")
        self.verticalLayout.addWidget(self.filterEdit)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.filterBtn = QtWidgets.QPushButton(self.centralwidget)
        self.filterBtn.setObjectName("filterBtn")
        self.horizontalLayout.addWidget(self.filterBtn, 0, QtCore.Qt.AlignBottom)
        self.setCentralWidget(self.centralwidget)

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("History", "History"))
        self.label.setText(_translate("History", "Search History"))
        self.label_2.setText(_translate("History", "Filter"))
        self.filterBtn.setText(_translate("History", "Filter"))

        self.btnLst = []
        for item in self.history.keys():
            form = QtWidgets.QPushButton()
            form.setText(_translate("History", item))
            form.clicked.connect(self.info(item))
            print(item)
            self.btnLst.append(form)
            a = QtWidgets.QListWidgetItem()
            a.setSizeHint(form.sizeHint())
            self.historyWidget.insertItem(0, a)
            self.historyWidget.setItemWidget(a, form)
        self.filterBtn.clicked.connect(self.filter)
        QtCore.QMetaObject.connectSlotsByName(self)

    def filter(self):
        _translate = QtCore.QCoreApplication.translate
        self.historyWidget.clear()
        self.btnLst =[]
        for item in self.history.keys():
            if item.find(self.filterEdit.text()) != -1:
                form = QtWidgets.QPushButton()
                form.setText(_translate("History", item))
                form.clicked.connect(self.info(item))
                self.btnLst.append(form)
                a = QtWidgets.QListWidgetItem()
                a.setSizeHint(form.sizeHint())
                self.historyWidget.insertItem(0, a)
                self.historyWidget.setItemWidget(a, form)
        self.show()

    def info(self, item):
        def inon():
            try:
                with open('history\history.txt', 'r') as fl:
                    dict = json.load(fl)
                self.wnd = match.MatchGui(item, dict[item])
            except Exception as e:
                self.wnd = match.MatchGui("error", e)
        return inon




