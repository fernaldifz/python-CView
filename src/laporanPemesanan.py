import sys
from os import environ
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QTabWidget, QWidget
import sqlite3

class laporanPemesanan(QDialog):
    def __init__(self):
        super(laporanPemesanan, self).__init__()
        loadUi("laporanPemesanan.ui", self)
        self.detailPaket.clicked.connect(self.gotopaket)
        self.detailBayar.clicked.connect(self.gotobayar)
        self.detailCV.clicked.connect(self.gotocv)
        self.tabelPemesanan.setColumnWidth(0, 50)
        self.tabelPemesanan.setColumnWidth(1, 100)
        self.tabelPemesanan.setHorizontalHeaderLabels(["ID", "Tanggal"])
        # self.loadData()
    
    def gotopaket(self):
        paket = detailPaket()
        widget.addWidget(paket)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotobayar(self):
        bayar = detailBayar()
        widget.addWidget(bayar)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotocv(self):  
        cv = detailCV()
        widget.addWidget(cv)
        widget.setCurrentIndex(widget.currentIndex()+1)

    # def loadData(self):
    #     conn = sqlite3.connect("CView.db")
    #     cur = conn.cursor()
    #     query = "SELECT * FROM 'Order' LIMIT 5"

    #     tableRow = 0
    #     for row in cur.execute(query):
    #         self.tabelPemesanan.setItem(tableRow, 1, QtWidgets.QTablelWidgetItem(row[0]))
    #         self.tabelPemesanan.setItem(tableRow, 2, QtWidgets.QTablelWidgetItem(row[1]))
    #         tableRow += 1

class detailPaket(QDialog):
    def __init__(self):
        super(detailPaket, self).__init__()
        loadUi("detailPaket.ui", self)
        self.Back.clicked.connect(self.gotoback)

    def gotoback(self):  
        Order = laporanPemesanan()
        widget.addWidget(Order)
        widget.setCurrentIndex(widget.currentIndex()+1)

class detailCV(QDialog):
    def __init__(self):
        super(detailCV, self).__init__()
        loadUi("detailCV.ui", self)
        self.Back.clicked.connect(self.gotoback)

    def gotoback(self):  
        Order = laporanPemesanan()
        widget.addWidget(Order)
        widget.setCurrentIndex(widget.currentIndex()+1)

class detailBayar(QDialog):
    def __init__(self):
        super(detailBayar, self).__init__()
        loadUi("detailBayar.ui", self)
        self.Back.clicked.connect(self.gotoback)

    def gotoback(self):  
        Order = laporanPemesanan()
        widget.addWidget(Order)
        widget.setCurrentIndex(widget.currentIndex()+1)

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

suppress_qt_warnings()
app = QApplication(sys.argv)
laporanPemesananWindow = laporanPemesanan()
widget = QtWidgets.QStackedWidget()
widget.addWidget(laporanPemesananWindow)
widget.setFixedHeight(512)
widget.setFixedWidth(720)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")