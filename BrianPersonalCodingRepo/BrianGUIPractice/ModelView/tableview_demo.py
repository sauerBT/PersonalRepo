from datetime import datetime
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.TextAlignmentRole:
            value = self._data[index.row()][index.column()]

            if isinstance(value, int) or isinstance(value, float):
                # Align right, vertical middle
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter

        if role == Qt.ItemDataRole.BackgroundRole:
            value = self._data[index.row()][index.column()]
            COLORS = ['#ffffcc','#ffeda0','#fed976','#feb24c','#fd8d3c','#fc4e2a','#e31a1c','#bd0026','#800026'] # <----- Define custom color gradient

            if isinstance(value, int) or isinstance(value, float):
                value = int(value) # Convert to integer for indexing

                # Limit to range -5 .... +5, then convert to 0...10
                value = max(-5, value) #values <-5 become -5
                value  = min(3, value) # values >5 become 5
                value = value + 5 # -5 becomes 0, +5 becomes +10
                print(value)

                return QtGui.QColor(COLORS[value])
        
        if role == Qt.ItemDataRole.ForegroundRole:
            value = self._data[index.row()][index.column()]

            if (isinstance(value, int) or isinstance(value, float)):
                return QtGui.QColor("white")

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
            [-5, 1, 'hello', -2, 7],
            [9, -3, 5, 3, 8],
            [2, 1, 5, datetime(2017,10,1), -4],
        ]

        self.model = TableModel(data)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
