import socket
import serial
import os

from time import sleep
from PIL import Image, ImageFile
from multiprocessing import Process


# classes and methods
class Uart:
    # UART CLASS
    def __init__(self, ser_port, baud):
        self.SER_PORT = ser_port
        self.BAUD = baud
        self.ser = serial.Serial(self.SER_PORT, self.BAUD)

    def rx(self):
        return self.ser.readline()

    def tx(self, data):
        self.ser.write(data)
        self.ser.write("\r\n".encode("ascii"))


class Socket:
    # SOCKET CLASS
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        # connect
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.HOST, self.PORT))
        self.s.listen()

        self.conn, self.addr = self.s.accept()

    def rx(self):
        return self.conn.recv(1024).decode("ascii", "ignore").strip()

    def tx(self, data):
        self.conn.sendall(data)
        self.conn.sendall("\r\n".encode("ascii"))


class PictureModule:
    def read_pic(self, path):
        file = Image.open(path)
        file.show()
        print(file.format)
        print(file.mode)

    def send_pic_socket(self, path, main_prog):
        file = open(path, "rb")
        p = ImageFile.Parser()
        while 1:
            s = file.read(1024)
            if not s:
                break
            p.feed(s)
            main_prog.sock.tx(s)
        p.close()

    def send_pic_uart(self, path, main_prog):
        file = open(path, "rb")
        p = ImageFile.Parser()
        while 1:
            s = file.read(1024)
            if not s:
                break
            p.feed(s)
            main_prog.uart.tx(s)
        p.close()


class MainProg:
    # main program
    def __init__(self, host, port, ser_port, baud):
        self.HOST = host
        self.PORT = port
        self.SER_PORT = ser_port
        self.BAUD = baud

    def connect(self):
        self.sock = Socket(self.HOST, self.PORT)
        self.uart = Uart(self.SER_PORT, self.BAUD)

    def rx_md(self):
        rx_data = self.uart.rx().decode("ascii").strip()
        if rx_data == "stop":
            print("Stopped from UART")
            return -1
        if rx_data == "send nudes":
            print("sending nudes fr Uart")
            return 2
        else:
            self.sock.tx(rx_data.encode("ascii"))
            return 1

    def tx_md(self):
        tx_data = self.sock.rx()
        if not tx_data:
            return 1
        if tx_data == "stop":
            print("Stopped from Socket")
            return -1
        if tx_data == "send nudes":
            print("sending nudes fr Socket")
            return 2
        else:
            self.uart.tx(tx_data.encode("ascii"))
            return 1


class MultiThread(MainProg):

    def pm_init(self):
        self.pm = PictureModule()
    
    def mt_rx(self):
        while True:
            ret = self.rx_md()
            if ret == -1:
                break
            elif ret == 2:
                self.pm.send_pic_uart("./files/12.jpg",self)
            else:
                pass

    def mt_tx(self):
        while True:
            ret = self.tx_md()
            if ret == -1:
                break
            elif ret == 2:
                self.pm.send_pic_socket("./files/12.jpg",self)
            else:
                pass
                
                          
    def main_lp(self):
        self.rx_p = Process(target = self.mt_rx)
        self.tx_p = Process(target = self.mt_tx)
        self.rx_p.start()
        self.tx_p.start()
        self.rx_p.join()
        self.tx_p.join()
  


# -----------------config----------------
HOST = "10.32.31.15"  # "192.169.3.98"
PORT = 65432
SER_PORT = "/dev/ttyUSB0"
BAUD = 9600

# program
if __name__ == "__main__":
    mp = MultiThread(HOST, PORT, SER_PORT, BAUD)
    mp.connect()
    mp.pm_init()
    with mp.sock.conn:
        print(f"Connected by {mp.sock.addr}")
        mp.main_lp()
    mp.sock.conn.close()
    print("Disconnected")
