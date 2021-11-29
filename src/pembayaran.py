import sys
from os import environ
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QTabWidget, QWidget, QMessageBox
import sqlite3


class modulMetodePembayaran(QDialog):
    paymentMethodSelected = "*"

    def __init__(self):
        super(modulMetodePembayaran, self).__init__()
        loadUi("metodePembayaran.ui", self)
        self.emoneyButton_1.setChecked(True)

        self.confirmButton.clicked.connect(self.gotoKonfirmasiPembayaran)

    def gotoKonfirmasiPembayaran(self):
        if self.emoneyButton_1.isChecked():
            modulMetodePembayaran.paymentMethodSelected = self.emoneyButton_1.text()
        elif self.emoneyButton_2.isChecked():
            modulMetodePembayaran.paymentMethodSelected = self.emoneyButton_2.text()
        elif self.emoneyButton_3.isChecked():
            modulMetodePembayaran.paymentMethodSelected = self.emoneyButton_3.text()
        elif self.bankingButton_1.isChecked():
            modulMetodePembayaran.paymentMethodSelected = self.bankingButton_1.text()
        elif self.bankingButton_2.isChecked():
            modulMetodePembayaran.paymentMethodSelected = self.bankingButton_2.text()
        elif self.cardButton_1.isChecked():
            modulMetodePembayaran.paymentMethodSelected = self.cardButton_1.text()
        elif self.cardButton_2.isChecked():
            modulMetodePembayaran.paymentMethodSelected = self.cardButton_2.text()
        elif self.codButton.isChecked():
            modulMetodePembayaran.paymentMethodSelected = self.codButton.text()
        print("metode pembayaran yang dipilih adalah " +
              modulMetodePembayaran.paymentMethodSelected)

        konfirmasiPembayaranWindow = modulKonfirmasiPembayaran()
        widget.addWidget(konfirmasiPembayaranWindow)
        widget.setCurrentIndex(widget.currentIndex()+1)


class modulKonfirmasiPembayaran(QDialog):
    id_user = 0

    def __init__(self):
        super(modulKonfirmasiPembayaran, self).__init__()
        loadUi("konfirmasiPembayaran.ui", self)

        conn = sqlite3.connect("database.db")

        cur = conn.cursor()
        cur.execute('SELECT id FROM Tuteers WHERE isActive = 1')
        id_user = cur.fetchone()[0]
        conn.commit()
        del cur

        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM Paket WHERE ID = ? ORDER BY ID DESC', (id_user,))
        # cur.execute('SELECT * FROM Paket WHERE ID = ?', (id_user,))
        jumlahCV = cur.fetchone()[3]
        conn.commit()
        del cur

        cur = conn.cursor()
        cur.execute('SELECT * FROM Paket WHERE ID = ?', (id_user,))
        durasiPaket = cur.fetchone()[4]
        conn.commit()
        del cur

        cur = conn.cursor()
        cur.execute('SELECT * FROM Paket WHERE ID = ?', (id_user,))
        hargaPaket = cur.fetchone()[5]
        conn.commit()

        conn.close()
        del cur
        del conn

        metodePembayaran = modulMetodePembayaran.paymentMethodSelected

        validator = QtGui.QIntValidator()
        self.lineEdit.setValidator(validator)

        self.label_6.setText("Jumlah CV adalah " + str(jumlahCV) +
                             " dengan durasi " + str(durasiPaket) + " hari")
        self.label_7.setText(metodePembayaran)
        self.label_8.setText(str(hargaPaket))

        self.confirmButton.clicked.connect(lambda: self.confirmPayment(
            jumlahCV, durasiPaket, metodePembayaran, hargaPaket))

    def confirmPayment(self, jumlahCV, durasiPaket, metodePembayaran, hargaPaket):
        jumlahUang = self.lineEdit.text()

        if(int(jumlahUang) >= int(hargaPaket)):
            print("jumlah CV adalah " + str(jumlahCV))
            print("durasi paket adalah " + str(durasiPaket))
            print("metode pembayaran adalah " + str(metodePembayaran))
            print("jumlah uang pengguna tersedia adalah " + str(jumlahUang))
            print("jumlah harga paket adalah " + str(hargaPaket))

            conn = sqlite3.connect("database.db")
            cur = conn.cursor()

            cur.execute('SELECT id FROM Tuteers WHERE isActive = 1')
            modulMetodePembayaran.id_user = cur.fetchone()[0]

            cur.execute('CREATE TABLE IF NOT EXISTS "Pembayaran" ("ID_Pembayaran" INTEGER NOT NULL, "ID_User" INTEGER NOT NULL, "Metode_Pembayaran"	TEXT NOT NULL, "Jumlah_Pembayaran" INTEGER NOT NULL, "Status_Pembayaran" INTEGER NOT NULL, FOREIGN KEY("ID_User") REFERENCES "Tuteers"("ID"), PRIMARY KEY("ID_Pembayaran" AUTOINCREMENT))')

            statusPembayaran = 1
            pembayaran = [modulMetodePembayaran.id_user, metodePembayaran,
                          hargaPaket, statusPembayaran]
            cur.execute(
                'INSERT INTO Pembayaran (ID_User, Metode_Pembayaran, Jumlah_Pembayaran, Status_Pembayaran) VALUES (?,?,?,?)', pembayaran)
            conn.commit()
            conn.close()
        else:
            errorMessage = QMessageBox()
            errorMessage.setIcon(QMessageBox.Critical)
            errorMessage.setText("Jumlah uang tersedia tidak cukup")
            errorMessage.setWindowTitle("Error")
            errorMessage.exec_()


def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"


if __name__ == "__main__":
    suppress_qt_warnings()
    app = QApplication(sys.argv)
    metodePembayaranWindow = modulMetodePembayaran()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(metodePembayaranWindow)
    widget.setFixedHeight(512)
    widget.setFixedWidth(720)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")
