import socket
import serial
from time import sleep

#classes and methods
class UARTcls:
    #UART CLASS
    def __init__(self,ser_port,baud):
        self.ser_port = ser_port
        self.baud = baud
        self.ser = serial.Serial(self.ser_port, self.baud)
    def uart_rx(self):
        return self.ser.readline()
    def uart_tx(self,data):
        self.ser.write(data)
        self.ser.write("\r\n".encode("ascii"))
    
class SOCKETcls:
    #SOCKET CLASS
    def __init__(self,host,port):
        self.__host = host
        self.__port = port
        #connect
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.s.bind((self.__host,self.__port))
        self.s.listen()
        self.conn, self.addr = self.s.accept()
    def sock_rx(self):
        self.conn.recv(1024).decode("ascii","ignore").strip()
        return self.conn.recv(1024).decode("ascii","ignore").strip()
    def sock_tx(self, data):
        self.conn.sendall(data)
        self.conn.sendall("\r\n".encode("ascii"))

class main_prog:
    def __init__(self,host,port,ser_port,baud):
        self.__host = host
        self.__port = port
        self.__ser_port = ser_port
        self.__baud = baud
    
    def connect(self):
        self.server = SOCKETcls(self.__host,self.__port)
        self.uart = UARTcls(self.__ser_port,self.__baud)
    
    def rx_md(self):
        rx_data = self.uart.uart_rx().decode("ascii").strip()
        if rx_data == "stop":
            return False
        else:
            self.server.sock_tx(rx_data.encode("ascii"))
            return True
        
    def tx_md(self):
        tx_data = self.server.sock_rx()
        if not tx_data:
            return True
        if tx_data == "stop":
            return False
        else:
            self.uart.uart_tx(tx_data.encode("ascii"))
            return True
    
    def main_lp(self):
        while True:
            self.tx_md()
            self.rx_md()

    def old_lp(self):
        while True:
            self.server.conn.send("Receive/Transmit/exit? (1, 2, 3) ".encode("ascii"))
            md = self.server.sock_rx()
            if not md:
                continue
            print("Mode = "+md)
            #modes
            if md == "1":
                while self.rx_md():
                    pass                   
            elif md == "2":
                while self.tx_md():
                    pass
            elif md == "3":
                break
            else:
                continue

#=-----------------config----------------
host = "192.168.0.101"#"192.169.3.98"
port = 65432
ser_port = "/dev/serial0"
baud = 9600

#program
mp = main_prog(host,port,ser_port,baud)
mp.connect()
with mp.server.conn:
    print(f"Connected by {mp.server.addr}")
    #main_program
    #main_lp(conn)
    mp.old_lp()
mp.server.conn.close()
print("Disconnected")