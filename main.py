import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QHeaderView

HEADERS = ["Title", "Roast", "Ground", "Taste", "Price, rub.", "Volume, g"]


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.tableWidget.setColumnCount(len(HEADERS))
        self.tableWidget.setHorizontalHeaderLabels(HEADERS)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(HEADERS.index("Taste"), QHeaderView.Stretch)
        self.load_base()

    def load_base(self):
        cursor = self.connection.cursor()
        result = cursor.execute(
            """SELECT coffee.title, roasts.title, coffee.ground,
            coffee.taste, coffee.price, coffee.pack
            FROM coffee JOIN roasts ON coffee.roast == roasts.id""").fetchall()
        self.tableWidget.setRowCount(len(result))
        for (i, row) in enumerate(result):
            for (j, elem) in enumerate(row):
                if j == HEADERS.index("Ground"):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(bool(elem))))
                else:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
