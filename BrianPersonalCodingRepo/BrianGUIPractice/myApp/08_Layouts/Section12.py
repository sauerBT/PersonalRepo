# Only needed for access to command line arguments
import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (QApplication, 
QMainWindow,
QLabel,
QWidget,
QTextEdit)

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Click in this window")
        self.setMinimumSize(QSize(300,200))
        self.setCentralWidget(self.label)

    def mouseMoveEvent(self, e): # <--------- New Commit
        self.label.setText("mouseMoveEvent")

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            # handle the left-button press in here
            self.label.setText("mousePressEvent LEFT")
        
        elif e.button() == Qt.MouseButton.MiddleButton:
            #handle the middle-button press in here
            self.label.setText("mousePressEvent MIDDLE")

        elif e.button() == Qt.MouseButton.RightButton:
            # handle the right-button press in here
            self.label.setText("mousePressEvent RIGHT")

    def mouseReleaseEvent(self, e):  # <--------- New Commit
        if e.button() == Qt.MouseButton.LeftButton:
            # handle the left-button press in here
            self.label.setText("mouseReleaseEvent LEFT")
        
        elif e.button() == Qt.MouseButton.MiddleButton:
            #handle the middle-button press in here
            self.label.setText("mouseReleaseEvent MIDDLE")

        elif e.button() == Qt.MouseButton.RightButton:
            # handle the right-button press in here
            self.label.setText("mouseReleaseEvent RIGHT")

    def mouseDoubleClickEvent(self, e):  # <--------- New Commit
        if e.button() == Qt.MouseButton.LeftButton:
            # handle the left-button press in here
            self.label.setText("mouseDoubleClickEvent LEFT")
        
        elif e.button() == Qt.MouseButton.MiddleButton:
            #handle the middle-button press in here
            self.label.setText("mouseDoubleClickEvent MIDDLE")

        elif e.button() == Qt.MouseButton.RightButton:
            # handle the right-button press in here
            self.label.setText("mouseDoubleClickEvent RIGHT")


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

