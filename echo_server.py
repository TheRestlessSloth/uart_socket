import socket
from time import sleep

#=-----------------config----------------
#socket
host = "192.168.0.104"
port = 65432

d_del = 0.1


def rx_md(conn):
	data = 0
	while True:
    	data += 1 
		if not data:
			break
		d = str(data)
		conn.sendall(data.encode())

def tx_md(conn):
	while True:
    	data = conn.recv(1024).decode()
		if data == -666:
			break
		print(data)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((host,port))
	s.listen()
	conn, addr = s.accept()
	
	with conn:
		print(f"Connected by {addr}")
		
		#main_program
		conn.sendall("Receive/Transmit/exit? (1, 2, 3)".encode())
		md = conn.recv(1024).decode()
		#modes
		if md == 1:
			rx_md(conn)
		elif md == 2:
			tx_md(conn)
		else

		print("Disconnected")	
