from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (QApplication, 
QMainWindow, 
QHBoxLayout,
QLabel,
QPushButton,
QVBoxLayout,
QStackedLayout, 
QWidget)

from layout_colorwidget import Color

# Only needed for access to command line arguments
import sys

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        pageLayout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.stackLayout = QStackedLayout()

        pageLayout.addLayout(button_layout)
        pageLayout.addLayout(self.stackLayout)

        btn = QPushButton("red")
        btn.pressed.connect(self.activate_tab_1)
        button_layout.addWidget(btn)
        self.stackLayout.addWidget(Color("red"))

        btn = QPushButton("green")
        btn.pressed.connect(self.activate_tab_2)
        button_layout.addWidget(btn)
        self.stackLayout.addWidget(Color("green"))

        btn = QPushButton("yellow")
        btn.pressed.connect(self.activate_tab_3)
        button_layout.addWidget(btn)
        self.stackLayout.addWidget(Color("yellow"))

        widget = QWidget()
        widget.setLayout(pageLayout)

        self.setMinimumSize(QSize(300,200))

        #Set central widget of the window
        self.setCentralWidget(widget)

    def activate_tab_1(self):
        self.stackLayout.setCurrentIndex(0)

    def activate_tab_2(self):
        self.stackLayout.setCurrentIndex(1)
    
    def activate_tab_3(self):
        self.stackLayout.setCurrentIndex(2)

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

