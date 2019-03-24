import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", PORT))
        s.listen(0)
        print("waiting to connect to client")
        conn, addr = s.accept()
        print("got connection with client")
        with conn:
            print('Connected by', addr)
            while True:
                # data = conn.recv(1024)
                # if data:
                #     print(repr(data))
                # else:
                #     break

                conn.sendall(b"101010000010011011")
