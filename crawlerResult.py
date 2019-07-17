from PyQt5 import QtCore, QtGui, QtWidgets, uic
import entry
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import sys
import webbrowser

LEN = 10
def show_link(link):
    print(link[5:])
    try:
        webbrowser.open(link[5:])
    except Exception as e:
        print(e)


class MatchGui(QtWidgets.QMainWindow):
    def __init__(self, name, result):
        super().__init__()
        _translate = QtCore.QCoreApplication.translate
        uic.loadUi('UI/SearchResults.ui', self)
        self.TitleLbl.setText("Web Search - %s (%s)" % (name[0], name[1]))
        print(plt.rcParams.keys())
        plt.rcParams.update({'font.size': 14, 'axes.facecolor':'#2A5491', 'figure.facecolor':'#2A5491',
                             'text.color':'white', 'axes.labelcolor':'white',
                             'xtick.color':'white', 'ytick.color':'white'})
        # a figure instance to plot on
        self.figure = plt.figure(figsize=(2, 2))
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self.pieBox)
        im = plt.imread('Facade.jpg')
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas)
        self.pieBox.setLayout(layout)
        dict = {}
        mask = {}
        for url in result:
            b = url
            url = url.split('://')[-1].split("?")[0].split('/')[0].split(':')[0].lower()
            mask[url] = b
            if url in dict.keys():
                dict[url] += 1
            else:
                dict[url] = 1
        sorted(dict)
        print(dict)
        labels = []
        i = 1
        for var in list(dict.keys())[0:LEN]:
            form = QtWidgets.QWidget()
            form.setStyleSheet("background-color: rgb(0, 255, 0);")

            a = QtWidgets.QListWidgetItem()
            ui = Ui_Entry()
            ui.setupUi(form, "#" + str(i) + " - " + var, mask[var][:5]+mask[var][8:])
            a.setSizeHint(form.sizeHint())
            self.resultWidget.insertItem(-1, a)
            self.resultWidget.setItemWidget(a, form)
            labels.append("#" + str(i))
            i += 1
        
        print(type(dict.values()))
        sizes = list(dict.values())[0:LEN]
        ax = self.figure.add_subplot(111)
        plt.tight_layout()
        y_pos = [0]*len(labels)
        for i in range(0, len(labels)):
            y_pos[i] = i
        # plot data
        ax.bar(y_pos, sizes, align='center', alpha=0.5, color=(1, 1, 1, 1))
        ax.set_title('Hits by website')
        plt.xticks(y_pos, labels)
        plt.ylabel('Amount of Hits')
        # refresh canvas
        self.canvas.draw()
        self.setWindowTitle(_translate("Dialog", "Information - " + name[0]))
        
        self.show()

class Ui_Entry(object):
    def setupUi(self, Form, link, mask):
        self.mask = mask
        Form.setStyleSheet("color: rgb(0, 255, 0);")
        Form.setObjectName("Form")
        Form.resize(779, 41)
        Form.setMaximumSize(QtCore.QSize(1677215, 80))
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.visitButton = QtWidgets.QPushButton(Form)
        self.visitButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.visitButton.setStyleSheet("color: rgb(255, 255, 255);")
        self.visitButton.setObjectName("visitButton")
        self.visitButton.clicked.connect(lambda: show_link(self.mask))
        self.horizontalLayout.addWidget(self.visitButton)
        self.linkLbl = QtWidgets.QLabel(Form)
        self.linkLbl.setText(link)
        self.linkLbl.setStyleSheet("font: 14pt \"Tahoma\";\n"
                                   "color: rgb(255, 255, 255);")
        self.linkLbl.setObjectName("linkLbl")
        self.horizontalLayout.addWidget(self.linkLbl)
        self.link = link
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.visitButton.setText(_translate("Form", "Go"))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    m = MatchGui('aa', 'www.google.com')
    sys.exit(app.exec_())
