import sys

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt

from MainWindow import Ui_MainWindow

# tag::model[]
class ToDoModel(QtCore.QAbstractListModel):
    def __init__(self, todos=None):
        super().__init__()
        self.todos = todos or []

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            status, text = self.todos[index.row()]
            return text

    def rowCount(self, index):
        return len(self.todos)
# end::model[]

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.model = ToDoModel(todos=[(False, 'my first todo')])
        self.todoView.setModel(self.model)
        self.addButton.pressed.connect(self.add)

    def add(self):
        """
        Add items to the rodo list, getting the text from the QLineEdit .todoEdit
        and then clearing it.
        """
        text = self.todoEdit.text()
        text = text.strip() # Remove whitespace from the ends of the string
        if text: # Dont add empty strings
            #Access the list via the model
            self.model.todos.append((False, text))
            # Trigger refresh
            self.model.layoutChanged.emit()
            # Empty the input
            self.todoEdit.setText("")

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
