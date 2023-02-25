import sys

import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget, \
    QAbstractItemView
from PyQt5 import uic


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Кофе")
        sql = """
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
        LEFT JOIN structures ON structures.ID = coffees.structure"""
        self.setCentralWidget(self.gridLayoutWidget)
        result = self.cur.execute(sql).fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        for y, coffee in enumerate(result):
            for x, param in enumerate(coffee):
                self.tableWidget.setItem(y, x, QTableWidgetItem(str(param)))
        self.tableWidget.setHorizontalHeaderLabels([el[0] for el in self.cur.description])
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.verticalHeader().setVisible(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())