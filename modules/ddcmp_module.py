from time import sleep
from uart_module import *
import threading

com = "COM4"
baud = 9600
encoding = "utf-8"

uart = Uart(com,9600,encoding)

class DDCMP:
    def __init__(self,timeout):
        self.timeout = 4
        self.states = ("HALTED",
                       "ISTART",
                       "ASTART",
                       "RUNNING",
                       "INVALID")
        self.cur_state = self.states[0]
    
    def state_mes(self):
        ret = "State: " + self.cur_state
        print(ret)
        uart.tx(ret)

    def timer_pr(self):
        self.TCNT_OVF = False
        for counter in range(0,self.timeout*10):
            sleep(0.1)
        self.TCNT_OVF = True
        return

    def uart_tx(self):
        while True:
            string = ">>> " + input()
            print(string)
            uart.tx(string)

    def uart_rx(self):
        while True:
            data = uart.rx()
            if data is not None: 
                print("<<< ",data)

    def handshake(self,timer_p):
        self.cur_state = self.states[1] 
        self.state_mes()
        
        timer_p.start()

        while not self.TCNT_OVF:
            mes = uart.rx()
            if mes == "ok":
                timer_p.counter = self.timeout
                return True 
        return False

    def mk_connection(self,tx_p,rx_p,timer_p):
        if self.cur_state is not self.states[3]:
            if self.handshake(timer_p):
                self.cur_state = self.states[3]
                self.state_mes()
                tx_p.start()
                rx_p.start()
            else:
                print("timeout. making another handshake")
                return False
        else:
            return False


def main():
    ddcmp = DDCMP(4)
    timer_p = threading.Thread(target=ddcmp.timer_pr)
    timer_p.__reduce__
    tx_p = threading.Thread(target=ddcmp.uart_tx)
    rx_p = threading.Thread(target=ddcmp.uart_rx)
    while not ddcmp.mk_connection(tx_p,rx_p,timer_p):
        pass

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
