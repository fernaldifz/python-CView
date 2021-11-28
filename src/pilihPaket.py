from sqlite3.dbapi2 import connect
import sys
from os import environ
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QTabWidget, QWidget
import sqlite3, random, time

class pilihPaket(QDialog):
    id_user = 1                 # untuk diintegrasikan dengan semua modul
    jumlah_CV = 0
    durasi = 0
    harga_paket = 0

    def __init__(self):
        super(pilihPaket, self).__init__()
        loadUi("pilihPaket.ui", self)
        self.JumlahCVcomboBox.setCurrentIndex(-1)
        self.durasicomboBox.setCurrentIndex(-1)
        self.lcdNumber.display("")        
        self.konfirmasiButton.clicked.connect(self.konfirmasiFunction)
        self.batalButton.clicked.connect(self.batalFunction)
        (self.JumlahCVcomboBox.currentIndexChanged and self.durasicomboBox.currentIndexChanged).connect(self.setLCDNumber)
        (self.durasicomboBox.currentIndexChanged and self.JumlahCVcomboBox.currentIndexChanged).connect(self.setLCDNumber)

    def konfirmasiFunction(self):
        fieldCondition = self.fieldCondition()

        if fieldCondition == "default":
            self.error.setText("Lengkapi seluruh data!")
        elif fieldCondition == "isiCV":
            self.error.setText("Lengkapi data durasi!")
        elif fieldCondition == "isiDurasi":
            self.error.setText("Lengkapi data jumlah CV!")
        elif fieldCondition == "complete":
            self.postData(pilihPaket.id_user, self.getID_Paket(pilihPaket.jumlah_CV, pilihPaket.durasi), pilihPaket.jumlah_CV, pilihPaket.durasi, pilihPaket.harga_paket)
            self.error.setText("")
            paketBerhasilWindow = pilihPaketBerhasil()
            widget.addWidget(paketBerhasilWindow)
            widget.setCurrentIndex(widget.currentIndex()+1)
            # tambahin post ke database  
        
    def batalFunction(self):      
        self.JumlahCVcomboBox.setCurrentIndex(-1)
        self.durasicomboBox.setCurrentIndex(-1)
        self.lcdNumber.display("")
        self.error.setText("")
        print("Kembali ke Dasboard")
        # belum kembali ke page dashboard
        # sesuaikan dengan modul sebelumnya

    def setLCDNumber(self):
        pilihPaket.jumlah_CV = self.JumlahCVcomboBox.currentText()
        pilihPaket.durasi = self.durasicomboBox.currentText()
        cv = pilihPaket.jumlah_CV
        durasi = pilihPaket.durasi
        result_harga = ""
        connect_db = sqlite3.connect("paket.db")
        cursor_db = connect_db.cursor()
        cursor_db.execute('SELECT * FROM paketTersedia WHERE jumlah_CV =? AND durasi =?', [cv, durasi])
        try:
            result_harga = cursor_db.fetchone()[3]
        except:
            None
        self.lcdNumber.display(result_harga)  

        cursor_db.close()
        connect_db.close()
        del cursor_db
        del connect_db

        pilihPaket.harga_paket = result_harga

    def getID_Paket(self, cv, durasi):
        id = 0
        connect_db = sqlite3.connect("paket.db")
        cursor_db = connect_db.cursor()
        cursor_db.execute('SELECT * FROM paketTersedia WHERE jumlah_CV =? AND durasi =?', [cv, durasi])
        try:
            id = cursor_db.fetchone()[0]
        except:
            None
        cursor_db.close()
        connect_db.close()
        del cursor_db
        del connect_db

        return id
        
    def fieldCondition(self):
        condition = "default"
        index_cv = self.JumlahCVcomboBox.currentIndex()
        index_durasi = self.durasicomboBox.currentIndex()

        if index_cv != -1 and index_durasi == -1:
            condition = "isiCV"
        elif index_cv == -1 and index_durasi != -1:
            condition = "isiDurasi"
        elif index_cv != -1 and index_durasi != -1:
            condition = "complete"

        return condition

    def postData(self, id_user, id_paket, jumlahCV, durasi, harga):
        try:
            connect_db = sqlite3.connect("paket.db")
            cursor_db = connect_db.cursor()
            # cursor_db.execute('CREATE TABLE IF NOT EXISTS "paket" ("ID_User"	INTEGER NOT NULL,"ID_Paket"	INTEGER NOT NULL,"Jumlah_CV"	INTEGER NOT NULL,"Durasi"	INTEGER NOT NULL,"Harga_Paket"	INTEGER NOT NULL,PRIMARY KEY("ID_User","ID_Paket"))')
            paket = [id_user, id_paket, jumlahCV, durasi, harga]
            cursor_db.execute('INSERT INTO paket (ID_User, ID_Paket, Jumlah_CV, Durasi, Harga_Paket) VALUES (?,?,?,?,?)', paket)
            connect_db.commit()
            cursor_db.close()
            connect_db.close()
            del cursor_db
            del connect_db
        except sqlite3.OperationalError:
            time.sleep(random.randint())

class pilihPaketBerhasil(QDialog):
    def __init__(self):
        super(pilihPaketBerhasil, self).__init__()
        loadUi("pilihPaketBerhasil.ui", self)      
        self.lanjutBayarButton.clicked.connect(self.pagePembayaranFunction)
    
    def pagePembayaranFunction(self):
        print("Lanjut ke Pembayaran")
        # sesuaikan dengan modul setelahnya

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

suppress_qt_warnings()
app = QApplication(sys.argv)
pilihPaketWindow = pilihPaket()
widget = QtWidgets.QStackedWidget()
widget.addWidget(pilihPaketWindow)
widget.setFixedHeight(512)
widget.setFixedWidth(720)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")