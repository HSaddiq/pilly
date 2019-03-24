import socket
import serial

# Code for the Dragonboard to interface between the arduino and the main server interacting with the alexa

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

#open serial connection

ser = serial.Serial()

ser.baudrate = 9600
ser.port = "/dev/tty96B0"
ser.open()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    while True:
        s.connect((HOST, PORT))
        #wait to receive a payload from the server when required
        data = s.recv(1024)

        #send the payload from the server to the arduino via serial
        ser.write(str(str(data.decode("utf-8")) + "/n").encode("UTF-8"))

print("Received '" + data.decode("utf-8") + "'")