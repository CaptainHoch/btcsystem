import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QFrame

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class Pie(QDialog):
    def __init__(self, frame):

        # a figure instance to plot on
        self.figure = plt.figure()
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(frame)
        self.plot()

    def plot(self):
        # random data
        labels = 'Python.org', 'winAPI.org', 'Ruby.org', 'oracle.Java.org'
        sizes = [20, 25, 30, 25]
        colors = ['#006FF6']
        explode = (0.05, 0.05, 0.05, 0.05)  # explode slices

        # instead of ax.hold(False)
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        # ax.hold(False) # deprecated, see above

        # plot data
        ax.pie(sizes, explode=explode, labels=labels, colors=colors,
               autopct='%1.1f%%', shadow=True, startangle=90)
        ax.set_title('precentage')

        # refresh canvas
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # main = Window()
    # main.show()

    sys.exit(app.exec_())
