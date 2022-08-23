import os
import sys
import re
from unicodedata import decimal
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
socket_commands = {'stop':-1, 'send':2, 'sendpic':3, 
                   'connect':4, 'default':5, 'send mes':6,
                   'auto':7}
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
            farg = message[-1].split("*")
            args.append(farg[0])
            hr = farg[1]
            return id,args,hr

    def parse2lev(self,data):
        dictionary = {"0":"error","G":"transmit"}
        id,args,hr = data
        if id in dictionary:
            mes = dictionary.get(id) +"\twith args ="+str(args)+ "\thash = " + hr
            if id == 'G':
                mes += "\tdata =" + self.parse3lev(data[1][2][2:])
            return mes
        else:
            return "There is no such command"

    def parse3lev(self,data):
        darr = data
        barr = []
        b_chunk = ""
        for d_chunk in darr:
            b_chunk += d_chunk
            if (len(b_chunk) % 2) == 0: 
                barr.append(b_chunk)
                b_chunk = ""
        mes = ""
        for byte in barr:
            mes += chr(int("0x"+byte,16))
        return mes


class MultiThread(MainProg):
    def uart_sock_thread(self):
        while True:
            ret = self.transmit(self.uart,self.sock,uart_commands)
            if ret == -1: break

            else: pass

    def sock_uart_thread(self):
        while True:
            ret = self.transmit(self.sock,self.uart,socket_commands)
            if ret == -1: 
                self.lock.acquire()
                self.sock.tx("Stoppin sequence")
                comm = self.com.command("6","0,0,0,0,0,0")
                self.uart.tx(comm)
                self.lock.release() 

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

            elif ret == 5:
                self.lock.acquire()
                self.sock.tx("Default settings")
                comm = self.com.command("1","0,0,0.,0,0,9.8067")
                self.uart.tx(comm)
                self.lock.release() 

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

            elif ret == 7:
                self.lock.acquire()
                self.sock.tx("Auto transmit")
                comm = self.com.command("6","0,1000,1,1,1,1")
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
