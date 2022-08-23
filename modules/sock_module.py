import socket

class Socket:
    # SOCKET CLASS
    def __init__(self, host, port, encoding = "ascii"):
        self.HOST = host
        self.PORT = port
        self.encoding = encoding
        # connect
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.HOST, self.PORT))
        self.s.listen()
        self.conn, self.addr = self.s.accept()
    
    def rx_until(self,nbytes):
        data = None
        while True: 
            data = self.rx(nbytes)
            if data:
                break
        return data

    def rx(self,nbytes=1024):
        return self.conn.recv(nbytes).decode(self.encoding, "ignore").strip()

    def tx(self, data):
        self.conn.sendall(data.encode(self.encoding))
        self.conn.sendall("\r\n".encode(self.encoding))
