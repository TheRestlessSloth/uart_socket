import socket
import serial
from time import sleep

#=-----------------config----------------
#socket
host = "192.169.3.99"
port = 65432

d_del = 0.1

ser = serial.Serial("/dev/serial0", 9600)

def uart_rx():
	data = ser.read()
	return data

def rx_md(conn):
	while True:
		if conn.recv(1024) == "exit":
			break
		data = uart_rx()
		sleep(d_del) 
		conn.sendall(data)

def tx_md(conn):
	while True:
		data = conn.recv(1024)
		if data == "exit":
			break
		ser.write(str(data).encode("ascii"))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((host,port))
	s.listen()
	conn, addr = s.accept()
	
	with conn:
		print(f"Connected by {addr}")
		
		#main_program
		while True:
			conn.sendall("Receive/Transmit/exit? (1, 2, 3) ".encode())
			md = conn.recv(1024).decode('ascii', 'ignore').strip()
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
