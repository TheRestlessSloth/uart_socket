import socket
import os
import serial.tools.list_ports

from uart_module import *
from genericpath import isfile
from time import localtime

from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 400)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777214))

        font = QtGui.QFont()
        font.setKerning(True)
        MainWindow.setFont(font)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(180, 180, 180)")
        MainWindow.setDockNestingEnabled(False)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(440, 175, 352, 144))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.ConsoleAndButtonsLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.ConsoleAndButtonsLayout.setContentsMargins(0, 0, 0, 0)
        self.ConsoleAndButtonsLayout.setObjectName("ConsoleAndButtonsLayout")
        self.EntMessageFieldLayout = QtWidgets.QHBoxLayout()
        self.EntMessageFieldLayout.setObjectName("EntMessageFieldLayout")

        self.entMessageField = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.entMessageField.setStyleSheet("background-color: white")
        self.entMessageField.setObjectName("entMessageField")
        self.EntMessageFieldLayout.addWidget(self.entMessageField)

        self.clearTextBtn = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.clearTextBtn.setStyleSheet("background-color: rgb(255, 94, 94)")
        self.clearTextBtn.setObjectName("clearTextBtn")
        self.EntMessageFieldLayout.addWidget(self.clearTextBtn)
        self.ConsoleAndButtonsLayout.addLayout(self.EntMessageFieldLayout)

        self.SendButtonLayout = QtWidgets.QHBoxLayout()
        self.SendButtonLayout.setObjectName("SendButtonLayout")
        self.sendTextBtn = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.sendTextBtn.setMaximumSize(QtCore.QSize(350, 16777215))
        self.sendTextBtn.setStyleSheet("background-color: rgb(51, 215, 0)")
        self.sendTextBtn.setObjectName("sendTextBtn")
        self.SendButtonLayout.addWidget(self.sendTextBtn)
        self.ConsoleAndButtonsLayout.addLayout(self.SendButtonLayout)

        self.consoleArea = QtWidgets.QPlainTextEdit(self.verticalLayoutWidget_2)
        self.consoleArea.setMinimumSize(QtCore.QSize(350, 80))
        self.consoleArea.setMaximumSize(QtCore.QSize(350, 16777215))
        self.consoleArea.setStyleSheet("background-color: white")
        self.consoleArea.setObjectName("consoleArea")
        self.ConsoleAndButtonsLayout.addWidget(self.consoleArea)

        self.changer_mode = QtWidgets.QSlider(self.centralwidget)
        self.changer_mode.setGeometry(QtCore.QRect(385, 10, 40, 20))
        self.changer_mode.setMouseTracking(True)
        self.changer_mode.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.changer_mode.setAutoFillBackground(False)
        self.changer_mode.setStyleSheet("")
        self.changer_mode.setMaximum(1)
        self.changer_mode.setSliderPosition(0)
        self.changer_mode.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.changer_mode.setObjectName("changer_mode")
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(10, 330, 781, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.horizontalLayoutWidget_5.setFont(font)
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")

        self.Authors_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.Authors_layout.setContentsMargins(0, 0, 0, 0)
        self.Authors_layout.setObjectName("Authors_layout")
        self.progTitle = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.progTitle.setFont(font)
        self.progTitle.setObjectName("progTitle")
        self.Authors_layout.addWidget(self.progTitle)
        self.authorsTitle = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        
        self.authorsTitle.setFont(font)
        self.authorsTitle.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.authorsTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.authorsTitle.setObjectName("authorsTitle")
        
        self.Authors_layout.addWidget(self.authorsTitle)

        self.messageArea = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.messageArea.setGeometry(QtCore.QRect(440, 9, 350, 161))
        self.messageArea.setStyleSheet("background-color: white")
        self.messageArea.setObjectName("messageArea")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 270, 361, 58))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        
        self.PicCentralLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.PicCentralLayout.setContentsMargins(0, 0, 0, 0)
        self.PicCentralLayout.setObjectName("PicCentralLayout")
        
        self.TransmitLayout = QtWidgets.QVBoxLayout()
        self.TransmitLayout.setObjectName("TransmitLayout")
        
        self.BrowseWayLayout = QtWidgets.QHBoxLayout()
        self.BrowseWayLayout.setObjectName("BrowseWayLayout")

        self.picField = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.picField.setStyleSheet("background-color: white")
        self.picField.setObjectName("picField")
        
        self.BrowseWayLayout.addWidget(self.picField)

        self.picBrowseBtn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.picBrowseBtn.setStyleSheet("background-color: rgb(186, 102, 255)")
        self.picBrowseBtn.setObjectName("picBrowseBtn")
        
        self.BrowseWayLayout.addWidget(self.picBrowseBtn)
        self.TransmitLayout.addLayout(self.BrowseWayLayout)

        self.picTransBtn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.picTransBtn.setStyleSheet("background-color: rgb(255, 215, 0)")
        self.picTransBtn.setObjectName("picTransBtn")
        
        self.TransmitLayout.addWidget(self.picTransBtn)
        
        self.PicCentralLayout.addLayout(self.TransmitLayout)

        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(10, 0, 360, 145))
        self.stackedWidget.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.stackedWidget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
        self.stackedWidget.setStyleSheet("background-color: rgb(200,200,200)")
        self.stackedWidget.setObjectName("stackedWidget")
        
        self.IpPage = QtWidgets.QWidget()
        self.IpPage.setObjectName("IpPage")
        
        self.layoutWidget = QtWidgets.QWidget(self.IpPage)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 359, 142))
        self.layoutWidget.setObjectName("layoutWidget")
        
        self.PortIpLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.PortIpLayout.setContentsMargins(0, 0, 0, 0)
        self.PortIpLayout.setObjectName("PortIpLayout")
        
        self.EntProfileNameLayout = QtWidgets.QVBoxLayout()
        self.EntProfileNameLayout.setObjectName("EntProfileNameLayout")
        self.PortIpButtonsLayout = QtWidgets.QVBoxLayout()
        self.PortIpButtonsLayout.setObjectName("PortIpButtonsLayout")
        self.ConLabelLayout = QtWidgets.QHBoxLayout()
        self.ConLabelLayout.setObjectName("ConLabelLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.ConLabelLayout.addItem(spacerItem)
        self.ipLabel = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.ipLabel.setFont(font)
        self.ipLabel.setObjectName("ipLabel")
        self.ConLabelLayout.addWidget(self.ipLabel)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.ConLabelLayout.addItem(spacerItem1)
        self.PortIpButtonsLayout.addLayout(self.ConLabelLayout)
        self.IpLayout = QtWidgets.QHBoxLayout()
        self.IpLayout.setObjectName("IpLayout")
        self.ip_label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ip_label.setFont(font)
        self.ip_label.setObjectName("ip_label")
        self.IpLayout.addWidget(self.ip_label)

        self.ent_ip = QtWidgets.QLineEdit(self.layoutWidget)
        self.ent_ip.setStyleSheet("background-color: white")
        self.ent_ip.setObjectName("ent_ip")
        self.IpLayout.addWidget(self.ent_ip)
        self.PortIpButtonsLayout.addLayout(self.IpLayout)
        self.PortLayout = QtWidgets.QHBoxLayout()
        self.PortLayout.setObjectName("PortLayout")
        self.port_label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.port_label.setFont(font)
        self.port_label.setObjectName("port_label")
        self.PortLayout.addWidget(self.port_label)

        self.ent_port = QtWidgets.QLineEdit(self.layoutWidget)
        self.ent_port.setStyleSheet("background-color: white")
        self.ent_port.setObjectName("ent_port")
        self.PortLayout.addWidget(self.ent_port)
        self.PortIpButtonsLayout.addLayout(self.PortLayout)

        self.ip_con = QtWidgets.QPushButton(self.layoutWidget)
        self.ip_con.setStyleSheet("background-color: rgb(51, 215, 0)")
        self.ip_con.setObjectName("ip_con")
        self.PortIpButtonsLayout.addWidget(self.ip_con)

        self.ip_dcon = QtWidgets.QPushButton(self.layoutWidget)
        self.ip_dcon.setStyleSheet("background-color: rgb(255, 94, 94)")
        self.ip_dcon.setObjectName("ip_dcon")
        self.PortIpButtonsLayout.addWidget(self.ip_dcon)
        self.EntProfileNameLayout.addLayout(self.PortIpButtonsLayout)
        self.PortIpLayout.addLayout(self.EntProfileNameLayout)
        self.stackedWidget.addWidget(self.IpPage)
        self.PortPage = QtWidgets.QWidget()
        self.PortPage.setObjectName("PortPage")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.PortPage)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(0, 0, 361, 89))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.CentralPortLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.CentralPortLayout.setContentsMargins(0, 0, 0, 0)
        self.CentralPortLayout.setObjectName("CentralPortLayout")
        self.VertSubPortLayout = QtWidgets.QVBoxLayout()
        self.VertSubPortLayout.setObjectName("VertSubPortLayout")
        self.PortConLabelLayout = QtWidgets.QVBoxLayout()
        self.PortConLabelLayout.setObjectName("PortConLabelLayout")
        self.PortConLabelLayout_2 = QtWidgets.QHBoxLayout()
        self.PortConLabelLayout_2.setObjectName("PortConLabelLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.PortConLabelLayout_2.addItem(spacerItem2)
        self.PortConLabel = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.PortConLabel.setFont(font)
        self.PortConLabel.setObjectName("PortConLabel")
        self.PortConLabelLayout_2.addWidget(self.PortConLabel)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.PortConLabelLayout_2.addItem(spacerItem3)
        self.PortConLabelLayout.addLayout(self.PortConLabelLayout_2)
        self.VertSubPortLayout.addLayout(self.PortConLabelLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelPort = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.labelPort.setMinimumSize(QtCore.QSize(10, 0))
        self.labelPort.setMaximumSize(QtCore.QSize(30, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelPort.setFont(font)
        self.labelPort.setObjectName("labelPort")
        self.horizontalLayout.addWidget(self.labelPort)

        self.portChooser = QtWidgets.QComboBox(self.verticalLayoutWidget_4)
        self.portChooser.setObjectName("portChooser")
        self.horizontalLayout.addWidget(self.portChooser)

        self.portConBtn = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.portConBtn.setMinimumSize(QtCore.QSize(110, 20))
        self.portConBtn.setObjectName("portConBtn")
        self.portConBtn.setStyleSheet("background-color: rgb(51, 215, 0)")
        self.horizontalLayout.addWidget(self.portConBtn)

        self.portDConBtn = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.portDConBtn.setMinimumSize(QtCore.QSize(110, 0))
        self.portDConBtn.setObjectName("portDConBtn")
        self.portDConBtn.setStyleSheet("background-color: rgb(255, 94, 94)")
        self.horizontalLayout.addWidget(self.portDConBtn)
        self.VertSubPortLayout.addLayout(self.horizontalLayout)
        self.BaudSubLayout = QtWidgets.QVBoxLayout()
        self.BaudSubLayout.setObjectName("BaudSubLayout")
        self.BaudSubLayout_2 = QtWidgets.QHBoxLayout()
        self.BaudSubLayout_2.setObjectName("BaudSubLayout_2")

        self.labelBaud = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelBaud.setFont(font)
        self.labelBaud.setObjectName("labelBaud")
        self.BaudSubLayout_2.addWidget(self.labelBaud)
        self.baudChooser = QtWidgets.QComboBox(self.verticalLayoutWidget_4)
        self.baudChooser.setObjectName("baudChooser")
        self.BaudSubLayout_2.addWidget(self.baudChooser)

        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.BaudSubLayout_2.addItem(spacerItem4)
        self.BaudSubLayout.addLayout(self.BaudSubLayout_2)
        self.VertSubPortLayout.addLayout(self.BaudSubLayout)
        self.CentralPortLayout.addLayout(self.VertSubPortLayout)
        self.stackedWidget.addWidget(self.PortPage)

        self.verticalLayoutWidget_6 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(10, 150, 360, 113))
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")

        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.ipProfileField = QtWidgets.QLineEdit(self.verticalLayoutWidget_6)
        self.ipProfileField.setStyleSheet("background-color: white")
        self.ipProfileField.setObjectName("ipProfileField")
        self.verticalLayout_3.addWidget(self.ipProfileField)
        self.ProfileAreaLayout = QtWidgets.QHBoxLayout()
        self.ProfileAreaLayout.setObjectName("ProfileAreaLayout")

        self.listWidget = QtWidgets.QListWidget(self.verticalLayoutWidget_6)
        self.listWidget.setStyleSheet("background-color: white")
        self.listWidget.setLineWidth(4)
        self.listWidget.setObjectName("listWidget")
        self.ProfileAreaLayout.addWidget(self.listWidget)

        self.ProfButtonsLayout = QtWidgets.QVBoxLayout()
        self.ProfButtonsLayout.setObjectName("ProfButtonsLayout")

        self.ipPoffileSave = QtWidgets.QPushButton(self.verticalLayoutWidget_6)
        self.ipPoffileSave.setStyleSheet("background-color: rgb(51, 215, 0)")
        self.ipPoffileSave.setObjectName("ipPoffileSave")
        self.ProfButtonsLayout.addWidget(self.ipPoffileSave)

        self.ipProfileLoad = QtWidgets.QPushButton(self.verticalLayoutWidget_6)
        self.ipProfileLoad.setStyleSheet("background-color: blue")
        self.ipProfileLoad.setObjectName("ipProfileLoad")
        self.ProfButtonsLayout.addWidget(self.ipProfileLoad)

        self.ipProfileDel = QtWidgets.QPushButton(self.verticalLayoutWidget_6)
        self.ipProfileDel.setStyleSheet("background-color: rgb(255, 94, 94)")
        self.ipProfileDel.setObjectName("ipProfileDel")
        self.ProfButtonsLayout.addWidget(self.ipProfileDel)
        self.ProfileAreaLayout.addLayout(self.ProfButtonsLayout)
        self.verticalLayout_3.addLayout(self.ProfileAreaLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #LOGIC-------------------------------------------------------------------------------------------------------------------------------------------

        ser_list = serial.tools.list_ports.comports()
        for port, desc, hwid in ser_list:
            self.portChooser.addItem("{}".format(port))

        self.portConBtn.clicked.connect(self.portConnect)
        self.portDConBtn.clicked.connect(self.portDConnect)

        self.ip_con.clicked.connect(self.clientCon)
        self.ip_dcon.clicked.connect(self.clientDcon)

        Baud_S = ["300", "1200", "2400", "4800", "9600", "19200", "38400", "57600", "74880", "115200", "230400", "250000", "500000", "1000000", "2000000"]
        for baud in Baud_S:
            self.baudChooser.addItem(baud)
        self.baudChooser.setCurrentIndex(4)

        self.sendTextBtn.clicked.connect(self.message_send)
        self.clearTextBtn.clicked.connect(self.clearFunc)

        self.entMessageField.returnPressed.connect(self.sendTextBtn.click)

        self.changer_mode.valueChanged.connect(self.chooserMode)

        #pr = Profile()

        self.profRead()
        self.ipPoffileSave.clicked.connect(self.profSave)
        self.ipProfileLoad.clicked.connect(self.profLoad)
        self.ipProfileDel.clicked.connect(self.profDelete)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "UART-Socket Bridge Client"))
        self.entMessageField.setPlaceholderText(_translate("MainWindow", "Enter your message..."))
        self.clearTextBtn.setText(_translate("MainWindow", "Clear"))
        self.sendTextBtn.setText(_translate("MainWindow", "Send"))
        self.progTitle.setText(_translate("MainWindow", "UART - SOCKET BRIDGE"))
        self.authorsTitle.setText(_translate("MainWindow", "by D*Max & Abkerimov T.V."))
        self.picField.setPlaceholderText(_translate("MainWindow", "Image way..."))
        self.picBrowseBtn.setText(_translate("MainWindow", "Browse"))
        self.picTransBtn.setText(_translate("MainWindow", "Transmit image"))
        self.ipLabel.setText(_translate("MainWindow", "CONNECTION EDITS"))
        self.ip_label.setText(_translate("MainWindow", "IP:"))
        self.ent_ip.setPlaceholderText(_translate("MainWindow", "Enter your IP-adress..."))
        self.port_label.setText(_translate("MainWindow", "PORT:"))
        self.ent_port.setPlaceholderText(_translate("MainWindow", "Enter your port..."))
        self.ip_con.setText(_translate("MainWindow", "Connect"))
        self.ip_dcon.setText(_translate("MainWindow", "Disconnect"))
        self.PortConLabel.setText(_translate("MainWindow", "PORT CONNECTION EDITS"))
        self.labelPort.setText(_translate("MainWindow", "Port:"))
        self.portConBtn.setText(_translate("MainWindow", "Connect"))
        self.portDConBtn.setText(_translate("MainWindow", "Disconnect"))
        self.labelBaud.setText(_translate("MainWindow", "Baudrate:"))
        self.ipProfileField.setPlaceholderText(_translate("MainWindow", "Enter your profile name..."))
        self.ipPoffileSave.setText(_translate("MainWindow", "Save"))
        self.ipProfileLoad.setText(_translate("MainWindow", "Load"))
        self.ipProfileDel.setText(_translate("MainWindow", "Delete"))

#Logic-----------------------------------------------------------------------------------------
    def chooserMode(self, s_pos):
        self.stackedWidget.setCurrentIndex(s_pos)
        if s_pos == 0:
            self.portDConBtn.clicked.connect(self.portDConnect)
        else:
            self.ip_dcon.clicked.connect(self.clientDcon)

    def clearFunc(self):
        self.messageArea.clear()

    def clientCon(self):
        ip = self.ent_ip.text()
        try:
            self.consoleArea.appendPlainText("Client connected with "+ip)
        except:
            self.consoleArea.appendPlainText("Client already disconnected or troubled") 

    def clientDcon(self):
        try:
            self.consoleArea.appendPlainText("Client disconnected")
        except:
            self.consoleArea.appendPlainText("Client already disconnected or troubled") 

    def portConnect(self):
        try:
            PORT = self.portChooser.currentText()
            BAUD = self.baudChooser.currentText()

            self.uart = Uart(PORT,BAUD)

            self.consoleArea.appendPlainText("Connected to " + PORT)
        except:
            self.consoleArea.appendPlainText(PORT)
            self.consoleArea.appendPlainText(BAUD)
            self.consoleArea.appendPlainText("Trouble with connection to COM!")

    def portDConnect(self):
        try:
            self.uart.ser.close()
            self.consoleArea.appendPlainText("Port disconnected")
        except:
            self.consoleArea.appendPlainText("Port already discconected or not found!")

    def message_send(self):
        tm = localtime()
        text = self.entMessageField.text()
        string = str(tm.tm_hour)+":"+str(tm.tm_min)+":"+str(tm.tm_sec) + " << " + text
        self.messageArea.appendPlainText(string)
        self.entMessageField.clear()
        try:
            self.uart.tx(text)
        except:
            self.consoleArea.appendPlainText("Trouble")

    def profSave(self):
        conDat = [self.ent_ip.text(), self.ent_port.text()]
        f = open(self.ipProfileField.text()+".conf", 'w')
        for i in range(len(conDat)):
            f.writelines(conDat[i]+"\n")
        f.close()
        self.profRead()
    
    def profLoad(self):
        path = "D:/Test_clientApp/"
        data = str(self.listWidget.currentItem().text())
        if os.path.isfile(path+data):
            f = open(path+data, 'r')
            self.ent_ip.setText(f.readline())  
            self.ent_port.setText(f.__next__())
            f.close()
        else:
            self.consoleArea.appendPlainText("Profile not found!")

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

# ---------------------------------------------------------------------------
