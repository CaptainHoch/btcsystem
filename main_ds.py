from PySide2.QtWidgets import QApplication, QMessageBox, QDialog
from datasearch.graphics.ui_p5 import Ui_MainWaindow
from datasearch.networking.client import graph_from_server, setup_client
import p5
import sys


def showDialog():
   msgBox = QMessageBox()
   msgBox.setIcon(QMessageBox.Warning)
   msgBox.setText("Can't find that address")
   msgBox.setWindowTitle("Error")
   msgBox.setStandardButtons(QMessageBox.Ok)
   msgBox.buttonClicked.connect(lambda: msgBox.close())

   returnValue = msgBox.exec()
   if returnValue == QMessageBox.Ok:
      print('OK clicked')


def not_work(app):
    showDialog()


def run():
    qapp = QApplication([])
    if len(sys.argv) > 1:
        try:
            setup_client()
            first_center = sys.argv[1]
            g = graph_from_server(first_center)

            if len(g) <= 1:
                not_work(qapp)
                return

            win = Ui_MainWaindow(first_center, g)
            win.show()
            p5.redraw()
            p5.run_sketch()

            qapp.exec_()
            return win
        except:
            not_work(qapp)

    else:
        not_work(qapp)


if __name__ == '__main__':
    run()
