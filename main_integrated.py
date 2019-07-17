# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

# from datasearch import run as run_datasearch
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
import crawler
import crawlerResult
from alert import AlertWidget
import json
from PyQt5.QtGui import QMovie as QMovie
from PyQt5.QtCore import QByteArray as QByteArray


class Ui_Dialog(QtWidgets.QMainWindow):
    sig = QtCore.pyqtSignal()

    def add_item(self, widget, info):
        form = AlertWidget(info)
        a = QtWidgets.QListWidgetItem()
        a.setSizeHint(form.sizeHint())
        widget.insertItem(0, a)
        widget.setItemWidget(a, form)

    def __init__(self):
        super().__init__()
        uic.loadUi("UI/MainWindow.ui", self)
        self.searchButton.clicked.connect(self.crawler_search)
        self.movie = QMovie("loading.gif", QByteArray(), self.lblLogo)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setSpeed(100)
        self.lblLogo.setMovie(self.movie)
        self.dw = None

        alerts = open("alerts.txt", "r").readlines()
        for line in alerts:
            print(line[:-1])
            self.add_item(self.newListWidget, line)

        with open('history\history.txt', 'r') as fl:
            dict = json.load(fl)
            for key in dict.keys():
                s = ""
                for c in dict[key]:
                    s += c + "\n"
                self.add_item(self.webListWidget, key)

        self.show()

    def resultScreen(self):
        self.matchResult = crawlerResult.MatchGui((self.res[0], "alias"), self.res[1])
        self.matchResult.show()
        self.movie.stop()

    def setresult(self, res):
        self.res = res

    def crawler_search(self):
        if self.dataButton.isChecked():
            # data search = daniel hoch
            print("Hello")
            self.close()
            import os
            os.system('python main_ds.py %s' % str(self.searchEdit.text()))
        elif self.webButton.isChecked():
            # web search = dor salomon
            # replace
            self.movie.start()
            print(self.movie.state())
            self.sig.connect(self.resultScreen)
            self.t = Thread(self)
            self.t.start()
            self.show()

            '''if self.searchEdit.text() == "~test":
                self.matchResult = crawlerResult.MatchGui((self.searchEdit.text(), "alias"),
                                                          ['python', 'java', 'C', 'C++', 'python'])
            else:
                p = crawler.CrawlerQueue(ttl=150, query=self.searchEdit.text())
                p.config()
                p.start()
                result = p.output()
                self.matchResult = crawlerResult.MatchGui((self.searchEdit.text(), "alias"), result)
                self.matchResult.show()
                print("window!")
                with open('history\history.txt', 'r') as fl:
                    log = json.load(fl)
                log[self.searchEdit.text()] = result
                with open('history\history.txt', 'w') as fl:
                    json.dump(log, fl)'''

# new class


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
        if self.trigger.searchEdit.text() not in ['~test']:
            p = crawler.CrawlerQueue(query=self.trigger.searchEdit.text(), ttl=150)
            if self.trigger.searchEdit.text() == '~resume':
                p.resume()
            else:
                p.start()
            self.res = ['', '']
            self.res[0] = self.trigger.searchEdit.text()
            self.res[1] = p.output()
            print("out")
            self.trigger.sig.emit()
            self.trigger.setresult(self.res)
        else:
            self.trigger.sig.emit()
            self.trigger.setresult(['test', ['python', 'java', 'C', 'C++', 'python']])


if __name__ == "__main__":
    print("this is it")
    app = QtWidgets.QApplication(sys.argv)
    m = Ui_Dialog()
    sys.exit(app.exec_())
