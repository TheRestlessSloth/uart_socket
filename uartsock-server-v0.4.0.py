import os
from uart_module import *
from sock_module import *
from pic_module import *

from time import sleep
from multiprocessing import Process


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
        if commands.get(rx_data) != None:
            return commands[rx_data]
        else:
            self.sock.tx(rx_data.encode("ascii"))
            return 1

    def tx_md(self):
        tx_data = self.sock.rx()
        if not tx_data:
            return 1
        if commands.get(tx_data) != None:
            return commands[tx_data]
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
                self.pm.send_pic("./files/12.jpg",self.uart.tx)
            else:
                pass

    def mt_tx(self):
        while True:
            ret = self.tx_md()
            if ret == -1:
                break
            elif ret == 2:
                self.uart.tx("send".encode("ascii"))
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
HOST = "10.32.31.17"  # "192.169.3.98"
PORT = 65432
SER_PORT = "/dev/ttyUSB1"
BAUD = 9600
commands = {'stop':-1,'send':2}

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
