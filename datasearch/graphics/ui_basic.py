# ui_basic.py

from PySide2.QtWidgets import QMainWindow
from PySide2 import QtGui, QtUiTools


class Ui(QMainWindow):
    def __init__(self, uifile=None):
        QMainWindow.__init__(self)

        if uifile is not None:
            loader = QtUiTools.QUiLoader()
            self.win = loader.load("datasearch/ui/" + uifile)
            self.win.closeEvent = self.closeEvent

        self._running = True

    def show(self):
        self.win.show()

    def running(self):
        return self._running

    def stop_running(self):
        self._running = False

    def closeEvent(self, *args, **kwargs):
        QMainWindow.close(self.win)
        self.stop_running()


def main():
    app = QtGui.QApplication([])
    win = Ui()
    win.show()
    app.exec_()


if __name__ == "__main__":
    main()
