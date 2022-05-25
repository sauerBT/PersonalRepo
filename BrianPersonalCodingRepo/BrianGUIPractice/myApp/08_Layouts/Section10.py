import sys
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import (QApplication, 
QMainWindow,
QPushButton,
QDialog)

from layout_colorwidget import Color

# Only needed for access to command line arguments
import sys

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press me for dialog!")
        button.clicked.connect(self.button_clicked)

        self.setMinimumSize(QSize(300,200))

        #Set central widget of the window
        self.setCentralWidget(button)

    def button_clicked(self, s):
        print("click", s)

        dlg = QDialog(self)
        dlg.setWindowTitle("?")
        dlg.exec()



# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([])
# works too.
app = QApplication(sys.argv)

window = MainWindow()
window.show()

#Start the event loop
app.exec() 

# Your application won't reach here until you exit and the event
# loop has stopped.

