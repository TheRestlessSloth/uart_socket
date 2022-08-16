# classes and methods
from tkinter.tix import Select


class DDCMP:

    states = {"HALTED":,"ISTART","ASTART","RUNNING",""}

    def __init__(self, d_select, d_interval, baudrate):
        self.dSELECT = d_select
        self.dINTERVAL = d_interval
        self.TO_INTERVAL = d_interval * 3 / 4
        self.BAUDRATE = baudrate
        self.N_DELAY = 100
        self.H_BAUD = baudrate
        self.L_BAUD = baudrate
        self.AUTOSTART = True
        self.RING_SIZE = 255
        self.SELECT = self.dSELECT
        self.PTYPE = 0
        self.state = 

    def STR(self):
        self.SELECT = True
        self.PTYPE = 40

    def STR(self):
        self.SELECT = True
        self.PTYPE = 36
    
    def ACK(self, NL=0, RL=0):
        self.SELECT = True
        self.PTYPE = 33

    def REP(self, NL, RL):
        self.SELECT = True
        self.PTYPE = 34

    def DTA(self, NL, RL, data):
        self.SELECT = False
        self.PTYPE = 17
        uart.tx(data)
    
    def DTE(self, NL, RL, data):
        self.SELECT = True
        self.PTYPE = 49
        uart.tx(data)



while True:
