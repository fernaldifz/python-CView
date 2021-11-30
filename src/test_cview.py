from PyQt5.QtCore import *
import pytest
import unittest
# from time import sleep
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

# def test_laporanPemesanan(qtbot):
    