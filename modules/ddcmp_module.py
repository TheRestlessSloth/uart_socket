from time import sleep
from uart_module import *
import threading

TCNT_OVF = False

'''
class DDCMP:
    types = {}

    states = {"HALTED",
              "ISTART",
              "ASTART",
              "RUNNING",
              "INVALID"}

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
        self.state = 1

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
'''

uart = Uart("COM6",9600)

def OVF():
    TCNT_OVF = True

def timer_pr():
    a = 0
    TCNT_OVF = False
    while True:
        TCNT_OVF = False
        if a >= 5:
            a = 0
            OVF()
        a += 0.1
        sleep(0.1)

def uart_tx():
    while True:
        string = ">>> " + input()
        print(string)
        uart.tx(string.encode("ascii"))

def uart_rx():
    while True:
        print("\n<<< ",uart.rx())

def handshake(timer_p):
    print("State: START")
    uart.tx("State: START".encode("ascii"))
    timer_p.start()
    a = uart.rx()
    if TCNT_OVF:
        return False
    else:
        if  == "ok":
            return True 

def mk_connection(tx_p,rx_p,timer):
    if handshake(timer):
        uart.tx("State: RUNNING".encode("ascii"))
        print("State: RUNNING")
        tx_p.start()
        rx_p.start()

    else:
        print("try another handshake")
        
        
    
def main():
    timer_p = threading.Thread(target=timer_pr)
    tx_p = threading.Thread(target=uart_tx)
    rx_p = threading.Thread(target=uart_rx)
    mk_connection(tx_p,rx_p)
    


if __name__ == "__main__":
    main()

'''
while True:
    Timer_process()
    DC_input_process()
    DC_output_process()

    if ip_ready:
        onIncomingPacket()
    
    if((state == DDCMP.states("HALTED")) && ((ih_Cnt>0) || (isStartup && autostart))):
        if isStartup:
            isStartup = False
        state = DDCMP.states("ISTART")
        CTRLSEND(ptype_str, 0, 0, True)
    elif state == DDCMP.states("RUNNING"):
        protocol_perf()
'''