from datetime import datetime
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):

        if role == Qt.ItemDataRole.BackgroundRole and index.column() == 2: # <----- Makes row three blue
            # see below for data structure
            return QtGui.QColor(Qt.GlobalColor.blue)

        if role == Qt.ItemDataRole.DisplayRole:
            # get the raw value
            value = self._data[index.row()][index.column()]

            # Perform per-type checks and render accordingly.
            if isinstance(value, datetime):
                # render time to YYY-MM-DD
                return value.strftime("%Y-%m-%d")

            if isinstance(value, float):
                # render float to 2 dp
                return "%.2f" % value
            
            if isinstance(value, str):
                # render strings with quotes
                return '"%s"' % value

            # Default (anything not captured above: e.g. int)
            return value


    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QtWidgets.QTableView()

        data = [
            [4, 1, 'hello', 3, 7],
            [9, 1, 5, 3, 8],
            [2, 1, 5, datetime(2017,10,1), 9],
        ]

        self.model = TableModel(data)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
