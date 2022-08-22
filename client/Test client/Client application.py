import sys
import os
import Client_application_new
import serial.tools.list_ports


from PyQt6.QtWidgets import (QApplication, QWidget, QMainWindow)
from sock_module import *
from uart_module import *
from genericpath import isfile
from tkinter import filedialog
from time import localtime
from multiprocessing import Process

class AppLogic(QMainWindow, Client_application_new.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        ser_list = serial.tools.list_ports.comports()
        for port, desc, hwid in ser_list:
            self.portChooser.addItem("{}".format(port))

        self.ip_con.clicked.connect(self.clientCon)
        self.ip_dcon.clicked.connect(self.clientDcon)

        self.portConBtn.clicked.connect(self.portConnect)
        self.portDConBtn.clicked.connect(self.portDConnect)

        Baud_S = ["300", "1200", "2400", "4800", "9600", "19200", "38400", "57600", "74880", "115200", "230400", "250000", "500000", "1000000", "2000000"]
        for baud in Baud_S:
            self.baudChooser.addItem(baud)
        self.baudChooser.setCurrentIndex(4)

        self.sendTextBtn.clicked.connect(self.message_send)
        self.clearTextBtn.clicked.connect(self.clearFunc)

        self.entMessageField.returnPressed.connect(self.sendTextBtn.click)

        self.changer_mode.valueChanged.connect(self.chooserMode)

        self.profRead()
        self.ipPoffileSave.clicked.connect(self.profSave)
        self.ipProfileLoad.clicked.connect(self.profLoad)
        self.ipProfileDel.clicked.connect(self.profDelete)

        self.picBrowseBtn.clicked.connect(self.imageSelector)
        

    def chooserMode(self, s_pos):
            self.stackedWidget.setCurrentIndex(s_pos)
            if s_pos == 0:
                self.portDConBtn.click
            else:
                self.ip_dcon.click

    def clearFunc(self):
        self.messageArea.clear()

    def clientCon(self):
        ip = self.ent_ip.text()
        ip_port = self.ent_port.text()
        try:
            self.sock = Socket(ip, int(ip_port))
            self.consoleArea.appendPlainText("Client connected with "+ip)
        except:
            self.consoleArea.appendPlainText("Trouble with connection! Client not connected!") 

    def clientDcon(self):
        try:
            self.sock.s.close()
            self.consoleArea.appendPlainText("Client disconnected")
        except:
            self.consoleArea.appendPlainText("Client already disconnected or troubled") 

    def portConnect(self):

        #self.ser_rxp.join()
        #try:
        PORT = self.portChooser.currentText()
        BAUD = self.baudChooser.currentText()

        self.uart = Uart(PORT,BAUD)

        def ser_rx():
            while True:
                self.messageArea.appendPlainText(self.uart.rx())

        ser_rxp = Process(target=ser_rx)
        ser_rxp.start()

        self.consoleArea.appendPlainText("Connected to " + PORT)
        #except:
            #self.consoleArea.appendPlainText("Trouble with connection to COM!")

    def portDConnect(self):
        try:
            self.uart.ser.close()
            self.consoleArea.appendPlainText("Port disconnected")
        except:
            self.consoleArea.appendPlainText("Port already discconected or not found!")

    # Messages part -----------------------------------------------------------------------------------------------------------------------------------
    def message_send(self):
        tm = localtime()
        text = self.entMessageField.text()
        string = str(tm.tm_hour)+":"+str(tm.tm_min)+":"+str(tm.tm_sec) + " << " + text
        self.messageArea.appendPlainText(string)
        self.entMessageField.clear()
        try:
            self.uart.tx(text)
        except:
            pass

    # Profiles part ------------------------------------------------------------------------------------------------------------------------------------
    def profSave(self):
        conDat = [self.ent_ip.text(), self.ent_port.text()]
        f = open(self.ipProfileField.text()+".conf", 'w')
        for i in range(len(conDat)):
            f.writelines(conDat[i]+"\n")
        f.close()
        self.profRead()
    
    def profLoad(self):
        path = "D:/Test_clientApp/"
        try:
            data = str(self.listWidget.currentItem().text())
            if os.path.isfile(path+data):
                f = open(path+data, 'r')
                self.ent_ip.setText(f.readline())  
                self.ent_port.setText(f.__next__())
                f.close()
            else:
                self.consoleArea.appendPlainText("Profile not found!")
        except:
            self.consoleArea.appendPlainText("Profile not selected")

    def profDelete(self):
        path = "D:/Test_clientApp/"
        data = str(self.listWidget.currentItem().text())
        if os.path.isfile(path+data):
            os.remove(path+data)
            self.consoleArea.appendPlainText("Profile was deleted!")
            self.profRead()
        else:
            self.consoleArea.appendPlainText("Profile not found!")

    def profRead(self):
        path = "D:/Test_clientApp/"
        self.listWidget.clear()
        for file in os.listdir(path):
            if file.endswith(".conf"):
                self.listWidget.addItem(file)

    # Image part-----------------------------------------------------------------------------------------------------------------------------------
    def imageSelector(self):
        filetypes = (("Text file", "*.txt"),("Image", "*.jpg *.png"), ("Any", "*"))
        filename = filedialog.askopenfilename(title="Open file", initialdir="/", filetypes=filetypes)
        if filename:
            self.picField.setText(filename)


def main():
    app = QApplication(sys.argv)
    window = AppLogic()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()