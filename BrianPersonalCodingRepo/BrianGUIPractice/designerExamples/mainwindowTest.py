import random
import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QPalette, QColor
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
darkPalette = QPalette()
darkPalette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
darkPalette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor
.white)
darkPalette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole
.WindowText, QColor(127, 127, 127))
darkPalette.setColor(QPalette.ColorRole.Base, QColor(42, 42, 42))
darkPalette.setColor(QPalette.ColorRole.AlternateBase, QColor(66, 66,
66))
darkPalette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor
.white)
darkPalette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor
.white)
darkPalette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
darkPalette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole
.Text, QColor(127, 127, 127))
darkPalette.setColor(QPalette.ColorRole.Dark, QColor(35, 35, 35))
darkPalette.setColor(QPalette.ColorRole.Shadow, QColor(20, 20, 20))
darkPalette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
darkPalette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor
.white)
191
darkPalette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole
.ButtonText, QColor(127, 127, 127))
darkPalette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.
red)
darkPalette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
darkPalette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130,
218))
darkPalette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole
.Highlight, QColor(80, 80, 80))
darkPalette.setColor(QPalette.ColorRole.HighlightedText, Qt
.GlobalColor.white)
darkPalette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole
.HighlightedText, QColor(127, 127, 127))

app.setPalette(darkPalette)

w = MainWindow()

#Start the event loop
app.exec() 

# Your application won't reach here until you exit and the event
# loop has stopped.