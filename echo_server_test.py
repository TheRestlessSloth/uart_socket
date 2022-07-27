import socket
import serial
from time import sleep

#=-----------------config----------------
#socket
host = "192.169.3.99"
port = 65432

d_del = 0.01

ser = serial.Serial("/dev/serial0", 9600)

def uart_rx():
    #data = ser.inWaiting()
    data = ser.read()
    return data

def rx_md(conn):
    rx_data = uart_rx()
    dd = rx_data.decode('ascii')
    if dd == "s":
        return False
    else:
        sleep(d_del)
    conn.sendall(rx_data)

def tx_md(conn):
    data = conn.recv(1024).decode()
    #if data == "stop":
        #return False
    ser.write(str(data).encode("ascii"))

def main_lp(conn):
    while True:
        tx_md(conn)
        rx_md(conn)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    try:
        s.bind((host,port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")

            #main_program
            main_lp(conn)
            '''
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
            '''
    except:
        print("Error were executed")
    finally:
        s.close()
        print("Disconnected")