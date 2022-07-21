import socket
from time import sleep

#=-----------------config----------------
#socket
host = "10.32.31.13"
port = 65432

d_del = 0.1

def uart_rx():
	#Max's code
	return data

def rx_md(conn):
	while True:
		data = uart_rx()
		if not data:
			break
		sleep(d_del) 
		conn.sendall(data)

def tx_md(conn):
	while True:
		data = conn.recv(1024)
		if data == -666:
			break
		#ser.write(data)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((host,port))
	s.listen()
	conn, addr = s.accept()
	
	with conn:
		print(f"Connected by {addr}")
		
		#main_program
		while True:
			conn.sendall("Receive/Transmit/exit? (1, 2, 3) ".encode())
			md = conn.recv(1024).decode('utf-8', 'ignore').strip()
			print(md)
			#modes
			if md == "1":
				rx_md(conn)
			elif md == "2":
				tx_md(conn)
			elif md == "3":
				break
			else:
				continue
		print("Disconnected")	
