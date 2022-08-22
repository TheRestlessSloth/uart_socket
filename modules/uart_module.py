import encodings
import serial

# classes and methods
class Uart:
    # UART CLASS
    def __init__(self, ser_port, baud, encoding = "ascii"):
        self.SER_PORT = ser_port
        self.BAUD = baud
        self.ser = serial.Serial(self.SER_PORT, self.BAUD)
        self.encoding = encoding

    def rx(self):
        if self.ser.inWaiting():
            return self.ser.readline().decode(self.encoding, "replace").strip()

    def tx(self, data):
        self.ser.write(data.encode(self.encoding))
        self.ser.write("\r\n".encode(self.encoding))
