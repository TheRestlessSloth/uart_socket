import os
import sys

sys.path.insert(1, "./modules")

from uart_module import *
from sock_module import *
from pic_module import *
from time import sleep
from multiprocessing import Process


# -----------------config----------------
HOST = "192.168.0.103"  # "192.169.3.98"
PORT = 65432
SER_PORT = "COM1"
BAUD = 9600
commands = {'stop':-1,'send':2,'sendfft':3}
im_src = "./files/test.png"


class MainProg:
    # main program
    def __init__(self, host, port, ser_port, baud):
        self.HOST = host
        self.PORT = port
        self.SER_PORT = ser_port
        self.BAUD = baud
        self.pm = PictureModule()

    def connect(self):
        self.sock = Socket(self.HOST, self.PORT)
        self.uart = Uart(self.SER_PORT, self.BAUD)

    def transmit(self,src1,src2):
        data = src1.rx()
        if not data:
            return 1
        if commands.get(data) != None:
            return commands[data]
        else:
            src2.tx(data.encode("ascii"))
            return 1


class MultiThread(MainProg):
    def uart_sock_thread(self):
        while True:
            ret = self.transmit(self.uart,self.sock)
            if ret == -1:
                break
            elif ret == 2:
                self.uart.tx("preambl".encode("ascii"))
                sleep(2)
                self.pm.send_pic(im_src,self.uart)
            elif ret == 3:
                self.pm.send_pic_fft(im_src,self.uart)
            else:
                pass

    def sock_uart_thread(self):
        while True:
            ret = self.transmit(self.sock,self.uart)
            if ret == -1:
                break
            elif ret == 2:
                self.uart.tx("send".encode("ascii"))
            elif ret == 3:
                self.uart.tx("sendfft".encode("ascii"))
            else:
                pass
                          
    def main_lp(self):
        self.ust_p = Process(target = self.uart_sock_thread)
        self.sut_p = Process(target = self.sock_uart_thread)
        self.ust_p.start()
        self.sut_p.start()
        self.ust_p.join()
        self.sut_p.join()


def main():
    mp = MultiThread(HOST, PORT, SER_PORT, BAUD)
    mp.connect()
    with mp.sock.conn:
        print(f"Connected by {mp.sock.addr}")
        mp.main_lp()
    mp.sock.conn.close()
    print("Disconnected")

# program
if __name__ == "__main__":
    main()
