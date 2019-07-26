import sys

from PyQt5 import QtGui
from mainwindow2 import Ui_MainWindow


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, QWidget_parent=None):
        super().__init__(QWidget_parent)
        self.setupUi(self)
        self.retranslateUi(self)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
