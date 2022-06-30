import random
import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QApplication, 
QMainWindow,
QLabel,
QPushButton,
QMenu,
QWidget,
QTextEdit)

from MainWindow import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.show()

        # you can still override from you UI file within your code, 
        # but if possible, set them in Qt Creator.  See the properties panel

        f = self.label.font() # <---- start interaction with existing object from Ui_MainWindow
        f.setPointSize(25)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.label.setFont(f)

        #signals from UI widgets can be connected as normal
        self.pushButton.pressed.connect(self.update_label) # create signal that interacts with Ui_MainWindow object "pushButton"

    def update_label(self):
        n = random.randint(1, 6)
        self.label.setText("%d" % n)

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([])
# works too.
app = QApplication(sys.argv)
app.setStyle("Fusion")

w = MainWindow()

#Start the event loop
app.exec() 

# Your application won't reach here until you exit and the event
# loop has stopped.