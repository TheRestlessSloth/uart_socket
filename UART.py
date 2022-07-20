import serial
import time

ind = input()

ser = serial.Serial("/dev/serial0", 9600)

while True:
    res=ser.write(str(ind).encode('utf-8'))
    time.sleep(0.03)
    

