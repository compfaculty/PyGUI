from PyQt5 import QtGui, QtCore

try:
    from QtCore import QString
except ImportError:
    QString = bytes
import sys


class MyQProcess(QtCore.QProcess):
    def __init__(self, parent=None):
        # Call base class method
        super().__init__(parent)
        self.setProcessChannelMode(QtCore.QProcess.MergedChannels)

        # Define Slot Here
        self.connect(self, QtCore.SIGNAL("readyReadStandardOutput()"), self, QtCore.SLOT("readStdOutput()"))
        self.connect(self, QtCore.SIGNAL("finished()"), self.on_finished)

    @QtCore.pyqtSlot()
    def readStdOutput(self):
        text = QString(self.readAllStandardOutput())
        # print(text)
        # res  = text.replace('\r\n', "<br>")
        print(text.decode())
        # self.edit.insertPlainText(text.decode())

    def on_finished(self):
        # text = QString(self.readAllStandardOutput())
        # print(text)
        # res  = text.replace('\r\n', "<br>")
        # print(text.decode())
        print("finished")


def main():
    app = QtGui.QApplication(sys.argv)
    qProcess = MyQProcess()
    qProcess.ready
    qProcess.finished.connect(qProcess.on_finished)

    # qProcess.finished.connect(qProcess.on_finished)
    qProcess.start("ping localhost")

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
