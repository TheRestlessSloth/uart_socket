import os
import sys
from modules.com_module import ComModule

sys.path.insert(1, "./modules")

from uart_module import *
from sock_module import *
from pic_module import *
from com_module import *
from time import sleep
import binascii
import threading as thr


# -----------------config----------------   
HOST = "192.169.10.110"
PORT = 65432
SER_PORT = "/dev/serial0"
BAUD = 9600
commands = {'stop':-1,'send':2,'sendfft':3,'connect':4,'disconnect':5,'send mes':6}
im_src = "./files/test.png"
flag = True


class MainProg:
    # main program
    def __init__(self, host, port, ser_port, baud):
        self.HOST = host
        self.PORT = port
        self.SER_PORT = ser_port
        self.BAUD = baud
        self.pm = PictureModule()
        self.com = ComModule()

    def connect(self):
        self.sock = Socket(self.HOST, self.PORT, "ascii")
        self.uart = Uart(self.SER_PORT, self.BAUD, "ascii")

    def transmit(self,src1,src2):
        data = src1.rx()
        if not data:
            return 1
        if commands.get(data):
            print(commands.get(data))
            return commands[data]
        else:
            print(data)
            src2.tx(data)
            return 1


class MultiThread(MainProg):
    def uart_sock_thread(self):
        global flag
        while flag:
            ret = self.transmit(self.uart,self.sock)
            if ret == -1:
                break
            elif ret == 2:
                self.uart.tx("preambl")
                sleep(2)
                self.pm.send_pic(im_src,self.uart)
            elif ret == 3:
                self.pm.send_pic_fft(im_src,self.uart)
            else:
                pass

    def sock_uart_thread(self):
        global flag
        while flag:
            ret = self.transmit(self.sock,self.uart)
            if ret == -1:
                break
            elif ret == 2:
                self.uart.tx("send")
            elif ret == 3:
                self.uart.tx("sendfft")
            elif ret == 4:
                flag = False
                self.sock.tx("Which adress?")
                addr = None
                while addr == None: addr = self.sock.rx(1)
                comm = self.com.command("F",f"1,1,{addr}")
                print(comm)
                self.uart.tx(comm)
                flag = True
            elif ret == 5:
                pass
            elif ret == 6:
                flag = False
                
                self.sock.tx("Which adress?")
                addr = None
                while addr == None: addr = self.sock.rx().strip()
                
                self.sock.tx("num of retries?")
                retr = None
                while retr == None: retr = self.sock.rx().strip()
                
                self.sock.tx("message?")
                mes = None
                while mes == None: mes = self.sock.rx().strip()
                bytearr = bytearray(mes.encode("ascii"))
                mesarr = list(byte for byte in bytearr)
                comm = self.com.command("G",f"{addr},{retr},{mesarr}")
                print(comm)
                self.uart.tx(comm)
                flag = True
            else:
                pass
                          
    def main_lp(self):
        self.ust_p = thr.Thread(target = self.uart_sock_thread)
        self.sut_p = thr.Thread(target = self.sock_uart_thread)
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
    print
    ("Disconnected")

# program
if __name__ == "__main__":
    main()
