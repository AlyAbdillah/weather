import time
from PyQt6.QtWidgets import QApplication,QGridLayout, QWidget,QLabel
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QThread,QObject, pyqtSignal,Qt,pyqtSlot
from firebase_admin import db
from sys import exit, argv
from ard import init ,data
from threading import Thread
from geoloc import get_loc , date_time,cache

init()

@cache

def get_data(n,m):
    ref = db.reference('/')
    t = ref.child("Climat").child(n).child(m).get()
    return t
class job(Thread):

    def run(self):
        while(True):
            if exitflag:
                break
            try:
                data()
            except:
                pass

exitflag = False
job=job()
job.start()
exitflag = True

class Worker(QObject):
    label1_ch = pyqtSignal(str)
    label2_ch = pyqtSignal(str)
    label3_ch = pyqtSignal(str)
    labelmap_ch = pyqtSignal(str)
    labeldate_ch = pyqtSignal(str)
    labeltime_ch = pyqtSignal(str)
    finished = pyqtSignal()

    @pyqtSlot()
    def run(self):
        self.isRunning = True
        while self.isRunning:
            try:
                file = open("count.txt", "r")
                n = int(file.read())-1
                m=str(n)
                t = get_data(m, "Temperature")
                h = get_data(m, "Humidité")
                p = get_data(m, "Pluie")
                file.close()
                self.label1_ch.emit(t)
                self.label2_ch.emit(h)
                self.label3_ch.emit(p)
                self.labelmap_ch.emit(get_loc())
                self.labeldate_ch.emit(date_time()[0])
                self.labeltime_ch.emit(date_time()[1])
                file.close()
            except OSError:
                pass
        self.finished.emit()

class Window(QWidget):
    def __init__(self):
        super(Window,self).__init__()
        self.label1 = QLabel("Température")
        self.label2 = QLabel("Humidité")
        self.label3 = QLabel("Pluie")
        self.labelmap = QLabel("Localisation")
        self.labeldate = QLabel("Date")
        self.labeltime = QLabel("Heure")

        self.grid = QGridLayout(self)
        self.setLayout(self.grid)

        self.obj = Worker()
        self.thread = QThread()

        self.obj.label1_ch.connect(self.label1.setText)
        self.obj.label2_ch.connect(self.label2.setText)
        self.obj.label3_ch.connect(self.label3.setText)
        self.obj.labelmap_ch.connect(self.labelmap.setText)
        self.obj.labeldate_ch.connect(self.labeldate.setText)
        self.obj.labeltime_ch.connect(self.labeltime.setText)

        self.obj.moveToThread(self.thread)
        self.obj.finished.connect(self.thread.quit)
        self.thread.started.connect(self.obj.run)
        self.thread.start()

        self.initUI()
    def initUI(self):
        self.setWindowTitle("Météo")
        self.setFixedSize(600,400)
        self.bk = QLabel(self)
        self.bk.setProperty("class","back")
        self.bk.resize(600,400)
        self.setWindowIcon(QIcon("image/logo.png"))

        self.pic1 = QLabel(self)
        self.pic1.setPixmap(QPixmap("image/temp1.png"))

        self.pic2 = QLabel(self)
        self.pic2.setPixmap(QPixmap("image/hum1.png"))

        self.pic3 = QLabel(self)
        self.pic3.setPixmap(QPixmap("image/rain1.png"))

        self.grid.addWidget(self.label1,2,0,Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.pic1, 1, 0, Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.label2, 2, 1, Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.pic2, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.label3, 2, 2, Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.pic3, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.labelmap, 0, 0, Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.labeldate, 0, 1, Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.labeltime, 0, 2, Qt.AlignmentFlag.AlignCenter)
        self.grid.setRowStretch(0,2)
        self.grid.setRowStretch(1,2)
        self.grid.setRowStretch(2,1)
if __name__ == '__main__':
    app = QApplication(argv)
    app.setStyleSheet(open('style.qss','r').read())
    window = Window()
    window.show()
    exit(app.exec())