import os
import sys
import re
from modules.uart_module import Uart

sys.path.insert(1, "./modules")

from uart_module import *
from sock_module import *
from pic_module import *
from com_module import *
from time import sleep
import binascii
import threading as thr


# -----------------config----------------   
HOST = "192.168.0.103"
PORT = 65432
SER_PORT = "COM3"
BAUD = 9600
socket_commands = {'stop':-1,'send':2,'sendpic':3,'connect':4,'disconnect':5,'send mes':6}
uart_commands = {'stop':-1}
im_src = "./files/test.png"
list_threads = []


class MainProg:
    # main program
    def __init__(self, host, port, ser_port, baud):
        self.HOST = host
        self.PORT = port
        self.SER_PORT = ser_port
        self.BAUD = baud

    def connect(self):
        self.pm = PictureModule()
        self.com = ComModule()
        self.sock = Socket(self.HOST, self.PORT, "ascii")
        self.uart = Uart(self.SER_PORT, self.BAUD, "ascii")

    def transmit(self,src1,src2,commands):
        data = src1.rx()
        if not data: return 1

        if commands.get(data): return commands[data]

        if isinstance(src1,Uart) and data[0:5] == "$PUWV": 
            src2.tx(str(self.parse2lev(self.parse(data))))
        
        else:
            src2.tx(data)
            return 1

    def parse(self,data):
        message = data
        if message: 
            message = message.split(",")
            id = message[0][-1]
            args = message[1:-1]
            farg = message[-1].split("*")[0]
            args.append(farg)
            return id,args

    def parse2lev(self,data):
        dictionary = {"0":"oshibka","G":"peredachua"}
        id = data[0]
        args = data[1]
        mes = dictionary.get(id)
        return mes + str(args)


class MultiThread(MainProg):
    def uart_sock_thread(self):
        while True:
            ret = self.transmit(self.uart,self.sock,uart_commands)
            if ret == -1: break

            else: pass

    def sock_uart_thread(self):
        while True:
            ret = self.transmit(self.sock,self.uart,socket_commands)
            if ret == -1: break

            elif ret == 2: 
                self.lock.acquire()
                self.sock.tx("Which adress?")
                addr = self.sock.rx_until(1)
                self.sock.tx("num of retries?")
                retr = self.sock.rx_until(1)
                self.sock.tx("message?")
                mes = self.sock.rx_until(64)
                mesarr = self.com.str2hex(mes)
                comm = self.com.command("G",f"{addr},{retr},{mesarr}")
                self.uart.tx(comm)
                self.lock.release()

            elif ret == 3: self.uart.tx("sendfft")

            elif ret == 4:
                self.lock.acquire()
                self.sock.tx("Which adress?")
                addr = self.sock.rx_until(1)
                comm = self.com.command("F",f"1,1,{addr}")
                self.uart.tx(comm)
                self.lock.release()

            elif ret == 5: pass

            elif ret == 6:
                self.lock.acquire()
                self.sock.tx("Which adress?")
                addr = self.sock.rx_until(1)
                self.sock.tx("num of retries?")
                retr = self.sock.rx_until(1)
                self.sock.tx("message?")
                mes = self.sock.rx_until(64)
                mesarr = self.com.str2hex(mes)
                comm = self.com.command("G",f"{addr},{retr},{mesarr}")
                self.uart.tx(comm)
                self.lock.release()

            else: pass      

    def threads(self):
        global list_threads
        self.lock = thr.Lock()
        list_threads.append(thr.Thread(target = self.uart_sock_thread))
        list_threads.append(thr.Thread(target = self.sock_uart_thread))
        for t in list_threads: t.start()
        for t in list_threads: t.join()
                          
    def main_lp(self):
        self.threads()


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
