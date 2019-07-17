import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QFrame

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.left = 100
        self.top = 100
        self.title = 'PyQt5 matplotlib example'
        self.width = 640
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.wid = QFrame(self)
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.plot()
        self.m = FigureCanvas(self.figure)
        self.m.setSizePolicy(QSizePolicy.Expanding,
                             QSizePolicy.Expanding)
        self.m.updateGeometry()
        self.m.setParent(self.wid)
        self.m.draw()
        self.show()

    def plot(self):
        labels = 'Python.org', 'winAPI.org', 'Ruby.org', 'oracle.Java.org'
        sizes = [20, 25, 30, 25]
        colors = ['#006FF6']
        explode = (0.05, 0.05, 0.05, 0.05)  # explode slices
        ax = self.figure.add_subplot(111)
        ax.pie(sizes, explode=explode, labels=labels, colors=colors,
               autopct='%1.1f%%', shadow=True, startangle=90)
        ax.set_title('precentage')

    def foo(self):
        print("foo")


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        labels = 'Python.org', 'winAPI.org', 'Ruby.org', 'oracle.Java.org'
        sizes = [20, 25, 30, 25]
        colors = ['#006FF6']
        explode = (0.05, 0.05, 0.05, 0.05)  # explode 1st slice
        ax = self.figure.add_subplot(111)
        ax.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
        ax.set_title('precentage')
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
