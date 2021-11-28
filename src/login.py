import sys
from os import environ
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QTabWidget, QWidget
import sqlite3

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
            conn = sqlite3.connect("CView.db")
            cur = conn.cursor()
            query = 'SELECT password FROM Tuteers WHERE username =\''+username+"\'"
            cur.execute(query)
            result_pass = cur.fetchone()[0]
            print(result_pass)
            if result_pass == password:
                print("Successfully logged in.")
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
            conn = sqlite3.connect("CView.db")
            cur = conn.cursor()
            user_info = [user, password]
            cur.execute('INSERT INTO Tuteers (username, password) VALUES (?,?)', user_info)

            conn.commit()
            conn.close()

            # fillProfile = fillProfileScreen()
            # widget.addWidget(fillProfile)
            # widget.setCurrentIndex(widget.currentIndex() + 1)\

            login = loginScreen()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)

class fillProfileScreen(QDialog):
    def __init__(self):
        super(fillProfileScreen, self).__init__()
        loadUi("fillprofile.ui",self)
        self.skip.clicked.connect(self.gotologin)
    
    def gotologin(self):
        login = loginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
        

class userDashboard(QDialog):
    def __init__(self):
        super(userDashboard, self).__init__()
        loadUi("dashboard.ui", self)
        self.logout.clicked.connect(self.gotowelscreen)
    
    def gotowelscreen(self):
        welcome = welcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

suppress_qt_warnings()
app = QApplication(sys.argv)
welcome = welcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(512)
widget.setFixedWidth(720)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")