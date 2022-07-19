import socket
import serial
from time import sleep

#=-----------------config----------------
#socket
host = "192.168.0.104"
port = 65432

#uart
ttyn = "/dev/ttyS0"
baudrt = 9600

d_del = 0.1
ser = serial.Serial(ttyn, baudrt)

def uart_rx():
	#data collection from uart
    r_data = ser.read()
    sleep(0.03)
    d_left = ser.inWaiting()
    r_data += ser.read(d_left)
    return str(r_data)

def rx_md(conn):
	while True:
    	data = uart_rx()
		if not data:
			break
		conn.sendall(data.encode())

def tx_md(conn):
	while True:
    	data = conn.recv(1024).decode()
		if data == -666:
			break
		ser.write(data)

def main_p(conn):
	

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
