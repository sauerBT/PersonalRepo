import sys

from PyQt6 import QtWidgets, uic

app = QtWidgets.QApplication(sys.argv)

window = uic.loadUi("C:/Users/brian/iCloudDrive/GIT/BrianPersonalCodingRepo/BrianGUIPractice/designerExamples/mainwindowTest.ui")
window.show()
app.exec()