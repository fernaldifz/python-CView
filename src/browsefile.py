import sys
import sqlite3
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QDialog, QApplication, QPushButton, QFileDialog, QVBoxLayout) 

from PyQt5.uic import loadUi

from src.login import userDashboard


class MainWindow(QDialog):

    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("gui.ui",self)
        self.browse.clicked.connect(self.browsefiles)
        self.viewfile.clicked.connect(self.getfile)
        self.downloadfile.clicked.connect(self.gotoPostFile)
        self.upload.clicked.connect(self.uploadfile)
        self.deletefile.clicked.connect(self.delfile)
        self.gohome.clicked.connect(self.movetoDashboard)
    
    def browsefiles(self):
        global fname, _
        fname, _ =QFileDialog.getOpenFileName(self, 'Open file',  r"<Default dir>", "Image files (*.jpg *.jpeg *.gif)")
        self.idfile.setText("1")
        self.filename.setText(fname)
        #self.openfile.setPixmap(QPixmap(fname))
    
    def getfile(self):
	    #file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image File', r"<Default dir>", "Image files (*.jpg *.jpeg *.gif)")
	    self.openfile.setPixmap(QPixmap(fname))
    
    def gotoPostFile(self):
        postfile=PostFile()
        widget.addWidget(postfile)
        widget.setCurrentIndex(widget.currentIndex()+1) 
    
    def convertimg(self, filename):
        with open(fname,'rb') as file:
            photoimg = file.read()
        return photoimg

    def uploadfile(self):
        #file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image File', r"<Default dir>", "Image files (*.jpg *.jpeg *.gif)")
    
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute('SELECT * FROM Tuteers WHERE isActive = 1')
        id_user = cur.fetchone()[0]

        #for image in fname:
        insertimg = self.convertimg(fname)
        cur.execute('INSERT INTO cvupload (ID_User,cvname,cvfile) VALUES (?,?,?)', [id_user,fname,insertimg])

        conn.commit()
        conn.close()
        self.notif.setText("Upload Success!")

    def delfile(self):
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute('SELECT * FROM Tuteers WHERE isActive = 1')
        id_user = cur.fetchone()[0]
        
        #for image in fname:
        insertimg = self.convertimg(fname)
        cur.execute("DELETE FROM cvupload WHERE ID_User=? AND cvname=? AND cvfile=?", [id_user,fname,insertimg])

        conn.commit()
        conn.close()
        self.notif.setText("Delete Success!")

    def movetoDashboard(self):
        dashboard = userDashboard()
        widget.addWidget(dashboard)
        widget.setCurrentIndex(widget.currentIndex()+1)
       

class PostFile(QDialog):
    def __init__(self):
        super(PostFile,self).__init__()
        loadUi("postfile.ui",self)
        self.backbutton.clicked.connect(self.gotoMainWindow)

    def gotoMainWindow(self):
        mainwindow=MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1) 


app=QApplication(sys.argv)
mainwindow=MainWindow()
postfile=PostFile()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.addWidget(postfile)
widget.setFixedWidth(720)
widget.setFixedHeight(512)
widget.show()
sys.exit(app.exec_())