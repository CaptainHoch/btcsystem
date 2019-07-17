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
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import threading
plt.rcParams.update({'text.color': '#FFFFFF'})


class Ui_MainWindow(QtCore.QObject):
    sig = QtCore.pyqtSignal()
    def setupresUi(self):
        print(threading.enumerate())
        output = self.res
        self.t.exit()
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
        for item in output:
            form = QtWidgets.QWidget()
            a = QtWidgets.QListWidgetItem()
            ui = entry.Ui_Entry()
            ui.setupUi(form, item)
            a.setSizeHint(form.sizeHint())
            self.resultWidget.insertItem(0, a)
            self.resultWidget.setItemWidget(a, form)
        self.verticalLayout.addWidget(self.resultWidget)
        self.pieBox = QtWidgets.QFrame(self.centralwidget)
        self.pieBox.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.pieBox.setFrameShadow(QtWidgets.QFrame.Raised)
        self.pieBox.setObjectName("pieBox")
        self.verticalLayout.addWidget(self.pieBox)

        '''plot area'''
        plt.rcParams.update({'font.size': 14})
        # a figure instance to plot on
        self.figure = plt.figure(figsize=(2, 2), facecolor='#696969')
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self.pieBox)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas)
        self.pieBox.setLayout(layout)
        dict = {}
        for url in output:
            url = url.split('://')[-1].split("?")[0].split('/')[0].split(':')[0].lower()
            if url in dict.keys():
                dict[url] += 1
            else:
                dict[url] = 1
        print(dict)
        labels = dict.keys()
        sizes = dict.values()
        colors = ['#006FF6']
        explode = [0.05] * len(sizes)  # explode slices
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # plot data
        ax.pie(sizes, explode=explode, labels=labels, colors=colors,
               autopct='%1.1f%%', shadow=True, startangle=90)
        ax.set_title('precentage by website')

        # refresh canvas
        self.canvas.draw()

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Web Crawler"))
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
        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

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
                self.res = crawler.site_sweep(self.trigger.searchBarEdit.text())
                self.trigger.sig.emit()
                self.trigger.setresult(self.res)
            else:
                p = crawler.CrawlerQueue(query=self.trigger.searchBarEdit.text(), ttl=150)
                if self.trigger.searchBarEdit.text() == '~resume':
                    p.resume()
                else:
                    p.start()
                self.res = p.output()
                print("out")
                self.trigger.sig.emit()
                self.trigger.setresult(self.res)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setMain(MainWindow)
    ui.setupUi()
    MainWindow.show()
    sys.exit(app.exec_())

