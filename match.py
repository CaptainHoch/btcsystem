# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'match.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, uic
import entry
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

LEN = 10


class MatchGui(QtWidgets.QMainWindow):
    def __init__(self, item, lst):
        super().__init__()
        _translate = QtCore.QCoreApplication.translate
        uic.loadUi('UI/result.ui', self)
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
        print("llll  ",lst)
        for url in lst:
            b = url
            url = url.split('://')[-1].split("?")[0].split('/')[0].split(':')[0].lower()
            mask[url] = b
            if url in dict.keys():
                dict[url] += 1
            else:
                dict[url] = 1
        sorted(dict)
        print(dict)
        i = 1

        for var in list(dict.keys())[0:LEN]:
            form = QtWidgets.QWidget()
            a = QtWidgets.QListWidgetItem()
            ui = entry.Ui_Entry()
            ui.setupUi(form, "#" + str(i) + " - " + var, mask[var])
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
        self.setWindowTitle(_translate("Dialog", "Information - " + item))
        self.show()
