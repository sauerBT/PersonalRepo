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
        self.deleteButton.pressed.connect(self.delete)
        self.completeButton.pressed.connect(self.complete)


    def add(self):
        """
        Add items to the todo list, getting the text from the QLineEdit .todoEdit
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

    def delete(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            # Indexes is a list of a single item in single-select mode
            index = indexes[0]
            # remove item and refresh view
            del self.model.todos[index.row()]
            self.model.layoutChanged.emit()
            # clear the selection (as it is no longer valid)
            self.todoView.clearSelection()

    def complete(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row() # <-- index in this case is a type of Qt opject and row() is a method
            status, text = self.model.todos[row]
            self.model.todos[row] = (True, text)
            #.dataChanged takes top-left and bottom right, which are equal
            #for a single selection
            self.model.dataChanged.emit(index, index)
            # clear the selection (as it is no longer valid)..
            self.todoView.clearSelection()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
