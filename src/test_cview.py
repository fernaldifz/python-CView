from io import DEFAULT_BUFFER_SIZE
from sqlite3.dbapi2 import connect
from PyQt5.QtCore import *
import pytest
import unittest
import cview
import sqlite3

def test_welcomeScreen(qtbot):
    welcome = cview.welcomeScreen()
    qtbot.addWidget(welcome)
    qtbot.mouseClick(welcome.Login, Qt.LeftButton)
    qtbot.mouseClick(welcome.Signup, Qt.LeftButton)

def test_signup_fieldNotFilled_1(qtbot):
    signup = cview.signupAccScreen()
    qtbot.addWidget(signup)
    qtbot.mouseClick(signup.Signup, Qt.LeftButton)
    assert signup.error.text() == "Please fill in all inputs!"

def test_signup_fieldNotFilled_2(qtbot):
    signup = cview.signupAccScreen()
    qtbot.addWidget(signup)
    signup.input_email.setText("ff")
    qtbot.mouseClick(signup.Signup, Qt.LeftButton)
    assert signup.error.text() == "Please fill in all inputs!"

def test_signup_fieldNotFilled_3(qtbot):
    signup = cview.signupAccScreen()
    qtbot.addWidget(signup)
    signup.input_confirm.setText("ff")
    qtbot.mouseClick(signup.Signup, Qt.LeftButton)
    assert signup.error.text() == "Please fill in all inputs!"

def test_signup_fieldNotFilled_4(qtbot):
    signup = cview.signupAccScreen()
    qtbot.addWidget(signup)
    signup.input_password.setText("ff")
    qtbot.mouseClick(signup.Signup, Qt.LeftButton)
    assert signup.error.text() == "Please fill in all inputs!"

def test_signup_fieldNotFilled_5(qtbot):
    signup = cview.signupAccScreen()
    qtbot.addWidget(signup)
    signup.input_email.setText("ff")
    signup.input_confirm.setText("ff")
    qtbot.mouseClick(signup.Signup, Qt.LeftButton)
    assert signup.error.text() == "Please fill in all inputs!"

def test_signup_fieldNotFilled_6(qtbot):
    signup = cview.signupAccScreen()
    qtbot.addWidget(signup)
    signup.input_email.setText("ff")
    signup.input_password.setText("ff")
    qtbot.mouseClick(signup.Signup, Qt.LeftButton)
    assert signup.error.text() == "Please fill in all inputs!"

def test_signup_fieldNotFilled_7(qtbot):
    signup = cview.signupAccScreen()
    qtbot.addWidget(signup)
    signup.input_confirm.setText("ff")
    signup.input_password.setText("ff")
    qtbot.mouseClick(signup.Signup, Qt.LeftButton)
    assert signup.error.text() == "Please fill in all inputs!"

def test_signup_passNotMatch(qtbot):
    signup = cview.signupAccScreen()
    qtbot.addWidget(signup)
    signup.input_email.setText("ff")
    signup.input_confirm.setText("ff")
    signup.input_password.setText("f")
    qtbot.mouseClick(signup.Signup, Qt.LeftButton)
    assert signup.error.text() == "Password do not match!"

def test_signup_success(qtbot):
    signup = cview.signupAccScreen()
    qtbot.addWidget(signup)
    signup.input_email.setText("ff")
    signup.input_confirm.setText("ff")
    signup.input_password.setText("ff")
    qtbot.mouseClick(signup.Signup, Qt.LeftButton)

def test_login_fieldNotFilled_1(qtbot):
    login = cview.loginScreen()
    qtbot.addWidget(login)
    qtbot.mouseClick(login.Login, Qt.LeftButton)
    assert login.error.text() == "Please input all fields."

def test_login_fieldNotFilled_2(qtbot):
    login = cview.loginScreen()
    qtbot.addWidget(login)
    login.input_username.setText("ff")
    qtbot.mouseClick(login.Login, Qt.LeftButton)
    assert login.error.text() == "Please input all fields."

def test_login_fieldNotFilled_3(qtbot):
    login = cview.loginScreen()
    qtbot.addWidget(login)
    login.input_password.setText("ff")
    qtbot.mouseClick(login.Login, Qt.LeftButton)
    assert login.error.text() == "Please input all fields."

def test_login_passInvalid(qtbot):
    login = cview.loginScreen()
    qtbot.addWidget(login)
    login.input_username.setText("ff")
    login.input_password.setText("f")
    qtbot.mouseClick(login.Login, Qt.LeftButton)
    assert login.error.text() == "Invalid username or password."

def test_login_success(qtbot):
    login = cview.loginScreen()
    qtbot.addWidget(login)
    login.input_username.setText("ff")
    login.input_password.setText("ff")
    qtbot.mouseClick(login.Login, Qt.LeftButton)

def test_dashboard_beforePilihPaket(qtbot):
    dashboard = cview.userDashboard()
    qtbot.addWidget(dashboard)
    qtbot.mouseClick(dashboard.paket, Qt.LeftButton)
    qtbot.mouseClick(dashboard.report, Qt.LeftButton)
    assert dashboard.error.text() == "Order first to look your order report!"
    qtbot.mouseClick(dashboard.logout, Qt.LeftButton)

def test_paket_fieldNotFilled1(qtbot):
    paket = cview.pilihPaket()
    qtbot.addWidget(paket)
    qtbot.mouseClick(paket.konfirmasiButton, Qt.LeftButton)
    assert paket.error.text() == "Lengkapi seluruh data!"

def test_paket_fieldNotFilled2(qtbot):
    paket = cview.pilihPaket()
    qtbot.addWidget(paket)
    durasi = "3"
    qtbot.keyClicks(paket.durasicomboBox, durasi)
    qtbot.mouseClick(paket.konfirmasiButton, Qt.LeftButton)
    assert paket.error.text() == "Lengkapi data jumlah CV!"

def test_paket_fieldNotFilled3(qtbot):
    paket = cview.pilihPaket()
    qtbot.addWidget(paket)
    cv = "1"
    qtbot.keyClicks(paket.JumlahCVcomboBox, cv)
    qtbot.mouseClick(paket.konfirmasiButton, Qt.LeftButton)
    assert paket.error.text() == "Lengkapi data durasi!"

def test_paket_success(qtbot):
    paket = cview.pilihPaket()
    qtbot.addWidget(paket)
    paket.JumlahCVcomboBox.clear()
    paket.durasicomboBox.clear()
    cv = "1"
    durasi = "3"
    harga = 70000
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute('UPDATE Tuteers SET isActive = 1 WHERE username = "ff"')
    conn.commit()
    conn.close()
    qtbot.keyClicks(paket.JumlahCVcomboBox, cv)
    qtbot.keyClicks(paket.durasicomboBox, durasi)
    paket.postData(cv, durasi, harga)
    qtbot.mouseClick(paket.konfirmasiButton, Qt.LeftButton)
    # dilakukan karena tidak mengetahui syntax yang tepat di PyTest untuk upload ComboBox Button supaya berhasil terupload datanya ke database

def test_paket_back_to_dashboard(qtbot):
    batalPaket = cview.pilihPaket()
    qtbot.addWidget(batalPaket)
    qtbot.mouseClick(batalPaket.batalButton, Qt.LeftButton)

def test_paket_next(qtbot):
    nextPaket = cview.pilihPaketBerhasil()
    qtbot.addWidget(nextPaket)
    qtbot.mouseClick(nextPaket.lanjutBayarButton, Qt.LeftButton)
    

def test_metode_pembayaran_1(qtbot):
    pembayaran = cview.modulMetodePembayaran()
    qtbot.addWidget(pembayaran)
    qtbot.mouseClick(pembayaran.confirmButton, Qt.LeftButton)

def test_metode_pembayaran_2(qtbot):
    pembayaran = cview.modulMetodePembayaran()
    qtbot.addWidget(pembayaran)
    qtbot.mouseClick(pembayaran.cardButton_2, Qt.LeftButton)
    qtbot.mouseClick(pembayaran.confirmButton, Qt.LeftButton)

def test_konfirmasi_pembayaran(qtbot):
    confirmBayar = cview.modulKonfirmasiPembayaran()
    qtbot.addWidget(confirmBayar)
    qtbot.mouseClick(confirmBayar.confirmButton, Qt.LeftButton)
    confirmBayar.lineEdit.setText("10000")
    qtbot.mouseClick(confirmBayar.confirmButton, Qt.LeftButton)    
    confirmBayar.lineEdit.setText("100000")
    qtbot.mouseClick(confirmBayar.confirmButton, Qt.LeftButton)

def test_browse_File(qtbot):
    cv = cview.MainWindow()
    qtbot.addWidget(cv)
    qtbot.mouseClick(cv.browse, Qt.LeftButton)
    qtbot.mouseClick(cv.viewfile, Qt.LeftButton)
    qtbot.mouseClick(cv.upload, Qt.LeftButton)
    qtbot.mouseClick(cv.downloadfile, Qt.LeftButton)

def test_delete_File(qtbot):
    delete = cview.MainWindow()
    qtbot.addWidget(delete)
    qtbot.mouseClick(delete.browse, Qt.LeftButton)
    qtbot.mouseClick(delete.upload, Qt.LeftButton)
    qtbot.mouseClick(delete.deletefile, Qt.LeftButton)

def test_gohome_File(qtbot):
    gohome = cview.MainWindow()
    qtbot.addWidget(gohome)
    qtbot.mouseClick(gohome.browse, Qt.LeftButton)
    qtbot.mouseClick(gohome.upload, Qt.LeftButton)
    qtbot.mouseClick(gohome.gohome, Qt.LeftButton)

def test_laporan_pemesanan(qtbot):
    report = cview.laporanPemesanan()
    qtbot.addWidget(report)
    qtbot.mouseClick(report.detailPaket, Qt.LeftButton)
    qtbot.mouseClick(report.detailBayar, Qt.LeftButton)
    qtbot.mouseClick(report.detailCV, Qt.LeftButton)
    qtbot.mouseClick(report.Home, Qt.LeftButton)

def test_detail_paket(qtbot):
    Paket = cview.detailPaket()
    qtbot.addWidget(Paket)
    qtbot.mouseClick(Paket.Back, Qt.LeftButton)

def test_detail_bayar(qtbot):
    Bayar = cview.detailBayar()
    qtbot.addWidget(Bayar)
    qtbot.mouseClick(Bayar.Back, Qt.LeftButton)

def test_detail_CV(qtbot):
    cv = cview.detailCV()
    qtbot.addWidget(cv)
    qtbot.mouseClick(cv.Back, Qt.LeftButton)

def test_dashboard_afterPilihPaket(qtbot):
    dashboard = cview.userDashboard()
    qtbot.addWidget(dashboard)
    qtbot.mouseClick(dashboard.report, Qt.LeftButton)
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute('DELETE FROM Pemesanan')
    conn.commit()
    cur.execute('DELETE FROM Paket')
    conn.commit()
    cur.execute('DELETE FROM Pembayaran')
    conn.commit()
    cur.execute('DELETE FROM cvupload')
    conn.commit()
    cur.execute('DELETE FROM Tuteers WHERE username = "ff"')
    conn.commit()
    conn.close()