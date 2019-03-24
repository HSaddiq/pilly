import socket
import serial

# Code for the Dragonboard to interface between the arduino and the main server interacting with the alexa

HOST = '192.168.43.231'  # The server's hostname or IP address
PORT = 65432  # The port used by the server

# open serial connection

ser = serial.Serial()

ser.baudrate = 9600
ser.port = "/dev/ttyACM0"
ser.open()
print("opened serial port with arduino")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("waiting to connect to server")
    s.connect((HOST, PORT))
    # wait to receive a payload from the server when required
    while True:
        data = s.recv(1024)
        print("Received '" + data.decode("utf-8") + "'")

        # send the payload from the server to the arduino via serial
        ser.write(((data.decode("utf-8")) + "/n").encode("UTF-8"))
        print("sent serial payload")

        arduino_string = ser.readline()
        print(arduino_string)

# print("Received '" + data.decode("utf-8") + "'")
