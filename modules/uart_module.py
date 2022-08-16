import serial

# classes and methods
class Uart:
    # UART CLASS
    def __init__(self, ser_port, baud):
        self.SER_PORT = ser_port
        self.BAUD = baud
        self.ser = serial.Serial(self.SER_PORT, self.BAUD)

    def rx(self):
        return self.ser.readline().decode("ascii").strip()

    def tx(self, data):
        self.ser.write(data)
        self.ser.write("\r\n".encode("ascii"))
