from PySide2.QtWidgets import QApplication
from datasearch.graphics.ui_p5 import Ui_MainWaindow
import p5
import sys


def run():
    qapp = QApplication([])
    if len(sys.argv) > 1:
        win = Ui_MainWaindow(sys.argv[1])
        win.show()
        p5.redraw()
        p5.run_sketch()
        qapp.run()
        win.hide()
        return win

    else:
        print('Cant')


if __name__ == '__main__':
    run()
