import sys
import sqlite3
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, \
    QHeaderView, QMessageBox, QDialog, QFileDialog
from mainUI import Ui_MainWindow
from addEditCoffeeForm import Ui_Dialog

HEADERS = ["ID", "Title", "Roast", "Ground", "Taste", "Price, rub.", "Volume, g"]


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        database = QFileDialog.getOpenFileName(
            self, 'Select coffee database', '',
            'Database (*.sqlite);;All files(*)')[0]
        self.connection = sqlite3.connect(database)
        self.edit_window = EditWindow(self.connection)
        self.add_window = AddWindow(self.connection)
        self.tableWidget.setColumnCount(len(HEADERS))
        self.tableWidget.setHorizontalHeaderLabels(HEADERS)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(HEADERS.index("Taste"), QHeaderView.Stretch)
        self.load_base()
        self.newPushButton.clicked.connect(self.new_button)
        self.editPushButton.clicked.connect(self.edit_button)

    def new_button(self):
        cursor = self.connection.cursor()
        ids = set(x[0] for x in cursor.execute('SELECT id FROM coffee').fetchall())
        self.add_window.idLineEdit.setText(str(max(ids) + 1))
        self.add_window.titleLineEdit.clear()
        self.add_window.roastComboBox.setCurrentIndex(0)
        self.add_window.groundCheckBox.setChecked(False)
        self.add_window.tasteLineEdit.clear()
        self.add_window.priceDoubleSpinBox.setValue(0)
        self.add_window.volumeSpinBox.setValue(100)
        self.add_window.exec()
        self.load_base()

    def edit_button(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        if len(rows) > 1:
            QMessageBox.warning(self, "Warning", "Can't edit multiple items")
            return
        if len(rows) == 0:
            QMessageBox.warning(self, "Warning", "Select an item")
            return
        row = rows[0]
        coffee_id = int(self.tableWidget.item(row, 0).text())
        cursor = self.connection.cursor()
        record = cursor.execute(f"""SELECT coffee.id, coffee.title, roasts.title,
            coffee.ground, coffee.taste, coffee.price, coffee.pack
            FROM coffee JOIN roasts ON coffee.roast == roasts.id
            WHERE coffee.id = {coffee_id}""").fetchall()[0]
        self.edit_window.idLineEdit.setText(str(record[0]))
        self.edit_window.titleLineEdit.setText(record[1])
        self.edit_window.roastComboBox.setCurrentText(record[2])
        self.edit_window.groundCheckBox.setChecked(record[3])
        self.edit_window.tasteLineEdit.setText(record[4])
        self.edit_window.priceDoubleSpinBox.setValue(record[5])
        self.edit_window.volumeSpinBox.setValue(record[6])
        self.edit_window.exec()
        self.load_base()

    def load_base(self):
        cursor = self.connection.cursor()
        result = cursor.execute(
            """SELECT coffee.id, coffee.title, roasts.title, coffee.ground,
            coffee.taste, coffee.price, coffee.pack
            FROM coffee JOIN roasts ON coffee.roast == roasts.id""").fetchall()
        self.tableWidget.setRowCount(len(result))
        for (i, row) in enumerate(result):
            for (j, elem) in enumerate(row):
                if j == HEADERS.index("Ground"):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(bool(elem))))
                else:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))


class RecordWindow(QDialog, Ui_Dialog):
    def __init__(self, connection):
        super(RecordWindow, self).__init__()
        self.connection = connection
        self.setupUi(self)
        cursor = self.connection.cursor()
        roasts = cursor.execute("SELECT * FROM roasts").fetchall()
        self.roasts = {x[1]: x[0] for x in roasts}
        self.roastComboBox.addItems(self.roasts.keys())

    def form_query(self, add=True):
        if add:
            query = f'INSERT INTO coffee VALUES('
            query += str(self.idLineEdit.text()) + ', '
            query += "'" + self.titleLineEdit.text() + "', "
            query += str(self.roasts[self.roastComboBox.currentText()]) + ', '
            query += str(int(self.groundCheckBox.isChecked())) + ', '
            query += "'" + self.tasteLineEdit.text() + "', "
            query += str(self.priceDoubleSpinBox.value()) + ', '
            query += str(self.volumeSpinBox.value()) + ')'
        else:
            query = f'UPDATE coffee SET '
            query += f"title = '{self.titleLineEdit.text()}', "
            query += f'roast = {self.roasts[self.roastComboBox.currentText()]}, '
            query += f'ground = {int(self.groundCheckBox.isChecked())}, '
            query += f"taste = '{self.tasteLineEdit.text()}', "
            query += f'price = {self.priceDoubleSpinBox.value()}, '
            query += f'pack = {self.volumeSpinBox.value()} '
            query += f'WHERE id = {self.idLineEdit.text()}'
        return query


class EditWindow(RecordWindow):
    def __init__(self, connection):
        super(EditWindow, self).__init__(connection)
        self.pushButton.clicked.connect(self.save)

    def save(self):
        self.connection.cursor().execute(self.form_query(add=False))
        self.connection.commit()
        self.close()


class AddWindow(RecordWindow):
    def __init__(self, connection):
        super(AddWindow, self).__init__(connection)
        self.pushButton.clicked.connect(self.save)

    def save(self):
        if not self.titleLineEdit.text():
            QMessageBox.warning(self, "Warning", "Title shouldn't be empty")
            return
        self.connection.cursor().execute(self.form_query())
        self.connection.commit()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
