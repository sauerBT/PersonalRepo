from random import randint
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import (QApplication, 
QMainWindow,
QPushButton,
QVBoxLayout,
QWidget,
QLabel,
QLineEdit)

# Only needed for access to command line arguments
import sys

from matplotlib import container

class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.w = AnotherWindow() # Create persistent instance of the second window
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.toggle_window)
        self.setMinimumSize(QSize(300,200))

        self.input = QLineEdit()
        self.input.textChanged.connect(self.w.label.setText)
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.input)
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def toggle_window(self, checked):
        if self.w.isVisible():
            self.w.hide()
        else:
            self.w.show()

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

