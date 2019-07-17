# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'index.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie as QMovie
from PyQt5.QtCore import QByteArray as QByteArray
import crawler
import os
import entry
import history
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import threading
import json

plt.rcParams.update({'text.color': '#FFFFFF'})
LEN = 10


class Ui_MainWindow(QtCore.QObject):
    sig = QtCore.pyqtSignal()
    def setupresUi(self):
        print(threading.enumerate())
        print(self.res)
        output = self.res[1]

        with open('history\history.txt', 'r') as fl:
            log = json.load(fl)
        log[self.res[0]] = output
        with open('history\history.txt', 'w') as fl:
            json.dump(log, fl)

        self.t.exit()
        # with open('history\history.txt', 'w') as json_file:
        #    json.dump(log, json_file)
        MainWindow = self.MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(861, 690)
        MainWindow.setStyleSheet("background-color: rgb(255,255,255);")
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
        self.MainWindow = MainWindow
        self.backButton.clicked.connect(self.setupUi)
        self.horizontalLayout.addWidget(self.backButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setStyleSheet("color: rgb(0, 0, 0);\n"
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

        '''plot area'''
        plt.rcParams.update({'font.size': 14})
        # a figure instance to plot on
        self.figure = plt.figure(figsize=(2, 2), facecolor='#FFFFFF')
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self.pieBox)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas)
        self.pieBox.setLayout(layout)
        dict = {}
        mask = {}
        for url in output:
            b = url
            url = url.split('://')[-1].split("?")[0].split('/')[0].split(':')[0].lower()
            mask[url] = b
            if url in dict.keys():
                dict[url] += 1
            else:
                dict[url] = 1
        sorted(dict)
        i = 1
        for item in list(dict.keys())[0:LEN]:
            form = QtWidgets.QWidget()
            a = QtWidgets.QListWidgetItem()
            ui = entry.Ui_Entry()
            ui.setupUi(form, "#" + str(i) + " - " + item, mask[item])
            a.setSizeHint(form.sizeHint())
            self.resultWidget.insertItem(-1, a)
            self.resultWidget.setItemWidget(a, form)
            i += 1

        def enum_list(lst):
            i = 1
            ans = []
            for it in lst:
                ans.append("No. " + str(i))
                i += 1
            return ans

        labels = enum_list(dict.keys())[0:LEN]
        print(type(dict.values()))
        sizes = list(dict.values())[0:LEN]
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        plt.tight_layout()
        y_pos = [0]*len(labels)
        for i in range(0, len(labels)):
            y_pos[i] = i
        # plot data
        ax.bar(y_pos, sizes, align='center', alpha=0.5)
        ax.set_title('Hits by website')
        plt.xticks(y_pos, labels)
        plt.ylabel('Amount of matches')
        # refresh canvas
        self.canvas.draw()

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Search result - " + self.res[0]))
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setMain(self, Main):
        self.MainWindow = Main

    def setupUi(self):
        try:
            os.remove('cache.ch')
        except:
            pass
        MainWindow = self.MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)
        MainWindow.resize(871, 697)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("SEO_sign-512.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(25, 0))
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                 "border-color: rgb(0, 0, 0);")
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2.addWidget(self.frame)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.titleLbl = QtWidgets.QLabel(self.centralwidget)
        self.titleLbl.setStyleSheet("font: 26pt \"Tahoma\";\n"
                                    "color: rgb(0, 0, 0);")
        self.titleLbl.setObjectName("titleLbl")
        self.verticalLayout.addWidget(self.titleLbl)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.searchBarEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.searchBarEdit.setMinimumSize(QtCore.QSize(0, 40))
        self.searchBarEdit.setStyleSheet("font: 16pt \"Tahoma\";\n"
                                         "color: rgb(0, 0, 0);")
        self.searchBarEdit.setObjectName("searchBarEdit")
        self.horizontalLayout.addWidget(self.searchBarEdit)
        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchButton.setStyleSheet("font: 16pt \"Tahoma\";\n"
                                        "background-color: rgb(255, 255, 255);\n"
                                        "color: rgb(0, 0, 0);")
        self.searchButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.searchButton.setIcon(icon1)
        self.searchButton.setIconSize(QtCore.QSize(40, 40))
        self.searchButton.setObjectName("searchButton")
        self.MainWindow = MainWindow
        self.searchButton.clicked.connect(self.search)
        self.horizontalLayout.addWidget(self.searchButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)

        self.radioButton_3 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_3.setStyleSheet("font: 14pt \"Tahoma\";\n"
                                         "color: rgb(0, 0, 0);")
        self.radioButton_3.setObjectName("radioButton_3")
        self.horizontalLayout_3.addWidget(self.radioButton_3)

        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setStyleSheet("font: 14pt \"Tahoma\";\n"
                                         "color: rgb(0, 0, 0);")
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout_3.addWidget(self.radioButton_2)
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setStyleSheet("font: 14pt \"Tahoma\";\n"
                                       "color: rgb(0, 0, 0);")
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout_3.addWidget(self.radioButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.loading = QtWidgets.QLabel(self.centralwidget)
        self.loading.setText("")
        self.loading.setObjectName("loading")
        self.verticalLayout.addWidget(self.loading, 0, QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        self.movie = QMovie("loading.gif", QByteArray(), self.loading)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setSpeed(100)
        self.loading.setMovie(self.movie)
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Web Crawler"))
        self.titleLbl.setText(_translate("MainWindow", "Web Crawler"))
        self.radioButton_2.setText(_translate("MainWindow", "Web search"))
        self.radioButton.setText(_translate("MainWindow", "Site search"))

        self.srchBtn = QtWidgets.QPushButton(self.centralwidget)
        self.srchBtn.setMaximumSize(QtCore.QSize(250, 16777215))
        self.srchBtn.setStyleSheet("font: 16pt \"Tahoma\";")
        self.srchBtn.setObjectName("pushButton")
        self.srchBtn.clicked.connect(self.history)
        self.verticalLayout.addWidget(self.srchBtn, 0, QtCore.Qt.AlignHCenter)
        self.srchBtn.setText(_translate("MainWindow", "Search History"))
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def history(self):
        self.w = history.Ui_History()
        self.w.show()

    def search(self):
        self.movie.start()
        print(self.movie.state())
        self.sig.connect(self.setupresUi)
        self.t = Thread(self)
        self.t.start()
        self.MainWindow.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Web Crawler"))
        self.titleLbl.setText(_translate("MainWindow", "Web Crawler"))
        self.radioButton_3.setText(_translate("MainWindow", "DarkNet search"))
        self.radioButton_2.setText(_translate("MainWindow", "Web search"))
        self.radioButton.setText(_translate("MainWindow", "Site search"))

    def setresult(self, res):
        self.res = res


class Thread(QtCore.QThread):
    def __init__(self, trigger):
        QtCore.QThread.__init__(self)
        self.res = []
        self.trigger = trigger
        self.setObjectName('QThread Main')

    def __del__(self):
        self.wait()

    def result(self):
        return self.res

    def run(self):
        if self.trigger.searchBarEdit.text() not in ['~test']:
            if self.trigger.radioButton.isChecked():
                self.res = ['', '']
                self.res[0] = self.trigger.searchBarEdit.text()
                self.res[1] = crawler.site_sweep(self.trigger.searchBarEdit.text())
                self.trigger.sig.emit()
                self.trigger.setresult(self.res)
            elif self.trigger.radioButton_2.isChecked():
                p = crawler.CrawlerQueue(query=self.trigger.searchBarEdit.text(), ttl=150)
                if self.trigger.searchBarEdit.text() == '~resume':
                    p.resume()
                else:
                    p.start()
                self.res = ['', '']
                self.res[0] = self.trigger.searchBarEdit.text()
                self.res[1] = p.output()
                print("out")
                self.trigger.sig.emit()
                self.trigger.setresult(self.res)
            else:
                p = crawler.DarkCrawler(query=self.trigger.searchBarEdit.text(), ttl=150)
                if self.trigger.searchBarEdit.text() == '~resume':
                    p.resume()
                else:
                    p.start()
                self.res = ['', '']
                self.res[0] = self.trigger.searchBarEdit.text()
                self.res[1] = p.output()
                print("out")
                self.trigger.sig.emit()
                self.trigger.setresult(self.res)
        else:
            self.trigger.sig.emit()
            self.trigger.setresult(['test', ['python', 'java', 'C', 'C++', 'python']])


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setMain(MainWindow)
    ui.setupUi()
    MainWindow.show()
    sys.exit(app.exec_())

