from PyQt6 import QtWidgets
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton

# Only needed for access to command line arguments
import sys
from random import choice

window_titles = [
    'My App',
    'My App',
    'Still My App',
    'Still My App',
    'What on Earth',
    'What on Earth',
    'This is suprising',
    'This is suprising',
    'Something went wrong'
]

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.n_times_clicked = 0

        self.button_is_checked = True

        self.setWindowTitle("My App")

        self.button = QPushButton("Press Me!")
        self.button.clicked.connect(self.the_button_was_clicked)

        self.windowTitleChanged.connect(self.window_title_changed)

        self.setMinimumSize(QSize(400,300))

        #Set central widget of the window
        self.setCentralWidget(self.button)

    def the_button_was_clicked(self):
        print("Clicked")
        new_window_title = choice(window_titles)
        print("Setting title: %s" % new_window_title)
        self.setWindowTitle(new_window_title)

    def window_title_changed(self, window_title):
        print("Window title changed: %s" % window_title)

        if window_title == 'Something went wrong':
            self.button.setDisabled(True)

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

