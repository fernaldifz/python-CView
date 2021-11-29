from sqlite3.dbapi2 import connect
import sys
from os import environ
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QTabWidget, QWidget, QMessageBox, QPushButton, QFileDialog, QVBoxLayout
import sqlite3
import random
import time


class welcomeScreen(QDialog):
    def __init__(self):
        super(welcomeScreen, self).__init__()
        loadUi("welcome.ui", self)
        self.Login.clicked.connect(self.gotologin)
        self.Signup.clicked.connect(self.gotosignup)

    def gotologin(self):
        login = loginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotosignup(self):
        signup = signupAccScreen()
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex()+1)


class loginScreen(QDialog):
    def __init__(self):
        super(loginScreen, self).__init__()
        loadUi("login.ui", self)
        self.input_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Login.clicked.connect(self.loginFunction)
        self.create.clicked.connect(self.gotosignup)

    def gotosignup(self):
        signup = signupAccScreen()
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def loginFunction(self):
        username = self.input_username.text()
        password = self.input_password.text()

        if len(username) == 0 or len(password) == 0:
            self.error.setText("Please input all fields.")
        else:
            print(username)
            print(password)
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            cur.execute(
                'SELECT password FROM Tuteers WHERE username =\''+username+"\'")
            result_pass = cur.fetchone()[0]
            if result_pass == password:
                cur.execute(
                    'UPDATE Tuteers SET isActive = 1 WHERE username =\''+username+"\'")
                conn.commit()
                conn.close()
                self.error.setText("")
                dashboard = userDashboard()
                widget.addWidget(dashboard)
                widget.setCurrentIndex(widget.currentIndex()+1)

            else:
                self.error.setText("Invalid username or password.")


class signupAccScreen(QDialog):
    def __init__(self):
        super(signupAccScreen, self).__init__()
        loadUi("signup.ui", self)
        self.input_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_confirm.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Signup.clicked.connect(self.signupFunction)

    def signupFunction(self):
        user = self.input_email.text()
        password = self.input_password.text()
        confirmPassword = self.input_confirm.text()

        if len(user) == 0 or len(password) == 0 or len(confirmPassword) == 0:
            self.error.setText("Please fill in all inputs!")
        elif password != confirmPassword:
            self.error.setText("Password do not match!")
        else:
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            user_info = [user, password]
            cur.execute(
                'INSERT INTO Tuteers (username, password, isActive) VALUES (?,?,0)', user_info)
            conn.commit()
            conn.close()

            # fillProfile = fillProfileScreen()
            # widget.addWidget(fillProfile)
            # widget.setCurrentIndex(widget.currentIndex() + 1)\

            login = loginScreen()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)

    # def __init__(self):
    #     super(fillProfileScreen, self).__init__()
    #     loadUi("fillprofile.ui", self)
    #     self.skip.clicked.connect(self.gotologin)

    # def gotologin(self):
    #     login = loginScreen()
    #     widget.addWidget(login)
    #     widget.setCurrentIndex(widget.currentIndex()+1)


class userDashboard(QDialog):
    def __init__(self):
        super(userDashboard, self).__init__()
        loadUi("dashboard.ui", self)
        self.logout.clicked.connect(self.gotowelscreen)
        self.paket.clicked.connect(self.choosepaket)
        self.report.clicked.connect(self.movetoorderreport)

    def movetoorderreport(self):
        report = laporanPemesanan()
        widget.addWidget(report)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def choosepaket(self):
        paket = pilihPaket()
        widget.addWidget(paket)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotowelscreen(self):
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute('UPDATE Tuteers SET isActive = 0 WHERE isActive = 1')
        conn.commit()
        conn.close()
        welcome = welcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)


class pilihPaket(QDialog):
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
        (self.JumlahCVcomboBox.currentIndexChanged and self.durasicomboBox.currentIndexChanged).connect(
            self.setLCDNumber)
        (self.durasicomboBox.currentIndexChanged and self.JumlahCVcomboBox.currentIndexChanged).connect(
            self.setLCDNumber)

    def konfirmasiFunction(self):
        fieldCondition = self.fieldCondition()

        if fieldCondition == "default":
            self.error.setText("Lengkapi seluruh data!")
        elif fieldCondition == "isiCV":
            self.error.setText("Lengkapi data durasi!")
        elif fieldCondition == "isiDurasi":
            self.error.setText("Lengkapi data jumlah CV!")
        elif fieldCondition == "complete":
            self.postData(pilihPaket.jumlah_CV,
                          pilihPaket.durasi, pilihPaket.harga_paket)
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
        self.backtoDasboard()
    
    def backtoDasboard(self):
        dashboardWindow = userDashboard()
        widget.addWidget(dashboardWindow)
        widget.setCurrentIndex(widget.currentIndex()+1) 

    def setLCDNumber(self):
        pilihPaket.jumlah_CV = self.JumlahCVcomboBox.currentText()
        pilihPaket.durasi = self.durasicomboBox.currentText()
        cv = pilihPaket.jumlah_CV
        durasi = pilihPaket.durasi
        result_harga = ""
        connect_db = sqlite3.connect("database.db")
        cursor_db = connect_db.cursor()
        cursor_db.execute(
            'SELECT * FROM paketTersedia WHERE jumlah_CV =? AND durasi =?', [cv, durasi])
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

    def postData(self, jumlahCV, durasi, harga):
        try:
            connect_db = sqlite3.connect("database.db")

            cursor_db = connect_db.cursor()
            cursor_db.execute('SELECT * FROM Tuteers WHERE isActive = 1')
            id_user = cursor_db.fetchone()[0]
            cursor_db.close()
            del cursor_db
            # id_user = 1

            cursor_db = connect_db.cursor()
            cursor_db.execute(
                'SELECT * FROM paketTersedia WHERE jumlah_CV =? AND durasi =?', [jumlahCV, durasi])
            id_paket = cursor_db.fetchone()[0]
            cursor_db.close()
            del cursor_db

            cursor_db = connect_db.cursor()
            # cursor_db.execute('CREATE TABLE IF NOT EXISTS "Paket" ("ID"	INTEGER,"ID_User"	INTEGER NOT NULL,"ID_Paket" INTEGER NOT NULL,"Jumlah_CV"	INTEGER,"Durasi"	INTEGER,"Harga"	INTEGER),  FOREIGN KEY("ID_Paket") REFERENCES "paketTersedia"("id_paket"), FOREIGN KEY("ID_User") REFERENCES "Tuteers"("id"), PRIMARY KEY("ID" AUTOINCREMENT)')
            paket = [id_user, id_paket, jumlahCV, durasi, harga]
            cursor_db.execute(
                'INSERT INTO Paket (ID_User, ID_Paket, Jumlah_CV, Durasi, Harga) VALUES (?,?,?,?,?)', paket)
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

        self.lanjutBayarButton.clicked.connect(self.movetoPagePembayaran)

    def movetoPagePembayaran(self):
        pembayaranWindow = modulMetodePembayaran()
        widget.addWidget(pembayaranWindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"


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
            'SELECT * FROM Paket WHERE ID_User = ? ORDER BY ID DESC LIMIT 1', (id_user,))
        jumlahCV = cur.fetchone()[3]
        conn.commit()
        del cur

        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM Paket WHERE ID_User = ? ORDER BY ID DESC LIMIT 1', (id_user,))
        durasiPaket = cur.fetchone()[4]
        conn.commit()
        del cur

        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM Paket WHERE ID_User = ? ORDER BY ID DESC LIMIT 1', (id_user,))
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

        if(len(jumlahUang) == 0):
            jumlahUang = 0

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

            self.movetoUploadCV()

        else:
            errorMessage = QMessageBox()
            errorMessage.setIcon(QMessageBox.Critical)
            errorMessage.setText("Jumlah uang tersedia tidak cukup")
            errorMessage.setWindowTitle("Error")
            errorMessage.exec_()

    def movetoUploadCV(self):
        mainWindow = MainWindow()
        widget.addWidget(mainWindow)
        widget.setCurrentIndex(widget.currentIndex()+1)


class MainWindow(QDialog):
    upload = False
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("gui.ui", self)
        self.browse.clicked.connect(self.browsefiles)
        self.viewfile.clicked.connect(self.getfile)
        self.downloadfile.clicked.connect(self.gotoPostFile)
        self.upload.clicked.connect(self.uploadfile)
        self.deletefile.clicked.connect(self.delfile)
        

    def browsefiles(self):
        global fname, _
        fname, _ = QFileDialog.getOpenFileName(
            self, 'Open file',  r"<Default dir>", "Image files (*.jpg *.jpeg *.gif)")
        self.idfile.setText("1")
        self.filename.setText(fname)
        # self.openfile.setPixmap(QPixmap(fname))

    def getfile(self):
        #file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image File', r"<Default dir>", "Image files (*.jpg *.jpeg *.gif)")
        self.openfile.setPixmap(QPixmap(fname))

    def gotoPostFile(self):
        postfile = PostFile()
        widget.addWidget(postfile)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def convertimg(self, filename):
        with open(fname, 'rb') as file:
            photoimg = file.read()
        return photoimg

    def uploadfile(self):
        #file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image File', r"<Default dir>", "Image files (*.jpg *.jpeg *.gif)")

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute('SELECT * FROM Tuteers WHERE isActive = 1')
        id_user = cur.fetchone()[0]

        # for image in fname:
        insertimg = self.convertimg(fname)
        cur.execute('INSERT INTO cvupload (ID_User,cvname,cvfile) VALUES (?,?,?)', [
                    id_user, fname, insertimg])

        conn.commit()
        conn.close()
        self.notif.setText("Upload Success!")
        self.upload = True
        if self.upload:
            self.gohome.clicked.connect(self.movetoDashboard)
            self.upload = False

    def delfile(self):
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute('SELECT * FROM Tuteers WHERE isActive = 1')
        id_user = cur.fetchone()[0]

        # for image in fname:
        insertimg = self.convertimg(fname)
        cur.execute("DELETE FROM cvupload WHERE ID_User=? AND cvname=? AND cvfile=?", [
                    id_user, fname, insertimg])

        conn.commit()
        conn.close()
        self.notif.setText("Delete Success!")
        if self.upload == False:
            self.gohome.clicked.connect(self.movetoself)
   
    def movetoDashboard(self):
        dashboard = userDashboard()
        widget.addWidget(dashboard)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def movetoself(self):
        mainwd = MainWindow()
        widget.addWidget(mainwd)
        widget.setCurrentIndex(widget.currentIndex()+1)

class PostFile(QDialog):
    def __init__(self):
        super(PostFile, self).__init__()
        loadUi("postfile.ui", self)
        self.backbutton.clicked.connect(self.gotoMainWindow)

    def gotoMainWindow(self):
        mainwindow = MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

class laporanPemesanan(QDialog):
    def __init__(self):
        super(laporanPemesanan, self).__init__()
        loadUi("laporanPemesanan.ui", self)
        self.Home.clicked.connect(self.movetoPagePembayaran)
        self.detailPaket.clicked.connect(self.gotopaket)
        self.detailBayar.clicked.connect(self.gotobayar)
        self.detailCV.clicked.connect(self.gotocv)
        self.tabelPemesanan.setColumnWidth(0, 50)
        self.tabelPemesanan.setColumnWidth(1, 100)
        # self.loadData()

    def movetoPagePembayaran(self):
        dashboard = userDashboard()
        widget.addWidget(dashboard)
        widget.setCurrentIndex(widget.currentIndex()+1)
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
        conn = sqlite3.connect("CView.db")
        cur = conn.cursor()
        qdate = 'SELECT "Order"."Tanggal Pemesanan" FROM "Order", Pembayaran as P  WHERE P.ID_Order = "Order".ID'
        cur.execute(qdate)
        date = cur.fetchone()[0]
        self.LTanggal.setText(date)

        qpaket = 'SELECT P.ID FROM "Order", Paket as P  WHERE P.ID_Order = "Order".ID'
        cur.execute(qpaket)
        paket = cur.fetchone()[0]
        self.LPaket.setText("Paket " + str(paket))

        qdurasi = 'SELECT P.Durasi FROM "Order", Paket as P  WHERE P.ID_Order = "Order".ID'
        cur.execute(qdurasi)
        durasi = cur.fetchone()[0]
        self.LDurasi.setText(str(durasi) + " Hari")

        qCV = 'SELECT P.Jumlah_CV FROM "Order", Paket as P  WHERE P.ID_Order = "Order".ID'
        cur.execute(qCV)
        CV = cur.fetchone()[0]
        self.LJumlah.setText(str(CV))

        qharga = 'SELECT P.Harga FROM "Order", Paket as P  WHERE P.ID_Order = "Order".ID'
        cur.execute(qharga)
        harga = cur.fetchone()[0]
        self.LHarga.setText("Rp " + str(harga))

    def gotoback(self):  
        Order = laporanPemesanan()
        widget.addWidget(Order)
        widget.setCurrentIndex(widget.currentIndex()+1)

class detailCV(QDialog):
    def __init__(self):
        super(detailCV, self).__init__()
        loadUi("detailCV.ui", self)
        self.Back.clicked.connect(self.gotoback)
        conn = sqlite3.connect("CView.db")
        cur = conn.cursor()
        qdate = 'SELECT "Order"."Tanggal Pemesanan" FROM "Order", CV  WHERE CV.ID_Order = "Order".ID'
        cur.execute(qdate)
        date = cur.fetchone()[0]
        self.LTanggal.setText(date)

        qCV = 'SELECT CV.Jumlah_CV FROM "Order", CV  WHERE CV.ID_Order = "Order".ID'
        cur.execute(qCV)
        CV = cur.fetchone()[0]
        self.LCV.setText(str(CV))

        qStatus = 'SELECT CV.Status FROM "Order", CV  WHERE CV.ID_Order = "Order".ID'
        cur.execute(qStatus)
        Status = cur.fetchone()[0]
        self.LStatus.setText(Status)

    def gotoback(self):  
        Order = laporanPemesanan()
        widget.addWidget(Order)
        widget.setCurrentIndex(widget.currentIndex()+1)

class detailBayar(QDialog):
    def __init__(self):
        super(detailBayar, self).__init__()
        loadUi("detailBayar.ui", self)
        self.Back.clicked.connect(self.gotoback)
        conn = sqlite3.connect("CView.db")
        cur = conn.cursor()
        qdate = 'SELECT "Order"."Tanggal Pemesanan" FROM "Order", Pembayaran as P  WHERE P.ID_Order = "Order".ID'
        cur.execute(qdate)
        date = cur.fetchone()[0]
        self.LTanggal.setText(date)

        qmethod = 'SELECT P.Metode FROM "Order", Pembayaran as P  WHERE P.ID_Order = "Order".ID'
        cur.execute(qmethod)
        method = cur.fetchone()[0]
        self.LMetode.setText(method)

        qbayar = 'SELECT P.Total_Bayar FROM "Order", Pembayaran as P  WHERE P.ID_Order = "Order".ID'
        cur.execute(qbayar)
        bayar = cur.fetchone()[0]
        self.LBayar.setText("Rp " + str(bayar))

        qstatus = 'SELECT P.Status FROM "Order", Pembayaran as P  WHERE P.ID_Order = "Order".ID'
        cur.execute(qstatus)
        status = cur.fetchone()[0]
        self.LStatus.setText(status)

    def gotoback(self):  
        Order = laporanPemesanan()
        widget.addWidget(Order)
        widget.setCurrentIndex(widget.currentIndex()+1)


def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"


def run():
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute('UPDATE Tuteers SET isActive = 0 WHERE isActive = 1')
        conn.commit()
        conn.close()
        print("Exiting")


suppress_qt_warnings()
app = QApplication(sys.argv)
pilihPaketWindow = welcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(pilihPaketWindow)
widget.setFixedHeight(512)
widget.setFixedWidth(720)
