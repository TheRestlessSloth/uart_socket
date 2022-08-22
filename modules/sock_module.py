import socket

class Socket:
    # SOCKET CLASS
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        # connect
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.HOST, self.PORT))
        self.s.listen()

        self.conn, self.addr = self.s.accept()

    def rx(self):
        return self.conn.recv(1024).decode("ascii", "replace").strip()

    def tx(self, data):
        self.conn.sendall(data)
        self.conn.sendall("\r\n".encode("ascii"))
