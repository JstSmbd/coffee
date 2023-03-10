import sys

import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from release.main_window import MainWindow
from release.edit_form import EditForm


class MyWidget(QMainWindow, MainWindow):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect("release/data/coffee.sqlite")
        self.cur = self.con.cursor()
        self.result = None
        self.setupUi(self)
        self.update_table()

    def update_table(self):
        self.result = self.cur.execute("""
        SELECT 
            coffees.ID, 
            coffees.name,
            roastings.roasting,
            structures.structure,
            coffees.taste,
            coffees.cost,
            coffees.volume
        FROM 
            coffees
        LEFT JOIN roastings ON roastings.ID = coffees.roasting 
        LEFT JOIN structures ON structures.ID = coffees.structure""").fetchall()
        self.tableWidget.setRowCount(len(self.result))
        if len(self.result) > 0:
            self.tableWidget.setColumnCount(len(self.result[0]))
        for y, coffee in enumerate(self.result):
            for x, param in enumerate(coffee):
                self.tableWidget.setItem(y, x, QTableWidgetItem(str(param)))
        self.tableWidget.setHorizontalHeaderLabels([el[0] for el in self.cur.description])
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.resizeColumnsToContents()

    def change(self, item):
        self.change_form = ChangeForm(self.result[item.row()], self.con, 1, self)
        self.change_form.show()

    def add(self):
        self.change_form = ChangeForm(None, self.con, 0, self)
        self.change_form.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            for index in self.tableWidget.selectedIndexes():
                self.cur.execute("""DELETE FROM coffees WHERE ID = ?""",
                                 (self.result[index.row()][0],))
            self.con.commit()
            self.update_table()


class ChangeForm(QMainWindow, EditForm):
    def __init__(self, items, con, mode, main_window):
        super().__init__()
        self.main_window = main_window
        self.mode = mode
        if self.mode:
            self.id = items[0]
            self.name = items[1]
            self.roasting = items[2]
            self.structure = items[3]
            self.taste = items[4]
            self.cost = items[5]
            self.volume = items[6]
        self.con = con
        self.cur = self.con.cursor()
        self.setupUi(self)

    def get_click(self, btn):
        if btn.text() == "OK":
            if self.mode:
                self.cur.execute("""
                UPDATE coffees 
                SET name = ?,
                roasting = ?,
                structure = ?,
                taste = ?,
                cost = ?,
                volume = ?
                WHERE ID = ?""", (self.lineEdit.text(),
                                  self.roastings.index(self.comboBox.currentText()) + 1,
                                  self.structures.index(self.comboBox_2.currentText()) + 1,
                                  self.plainTextEdit.toPlainText(),
                                  self.doubleSpinBox.value(),
                                  self.doubleSpinBox_2.value(),
                                  self.id))
            else:
                self.cur.execute("""
                                INSERT INTO coffees(name, roasting, structure, taste, cost, volume) 
                                VALUES (?, ?, ?, ?, ?, ?)""",
                                 (self.lineEdit.text(),
                                  self.roastings.index(
                                      self.comboBox.currentText()) + 1,
                                  self.structures.index(
                                      self.comboBox_2.currentText()) + 1,
                                  self.plainTextEdit.toPlainText(),
                                  self.doubleSpinBox.value(),
                                  self.doubleSpinBox_2.value()))
            self.con.commit()
            self.main_window.update_table()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
