import socket

class ClientSocket:
    def __init__(self, host='127.0.0.1', port=1485):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to server at {self.host}:{self.port}")

    def send(self, message: str):
        self.client_socket.sendall(message.encode('utf-8'))

    def receive(self):
        return self.client_socket.recv(1024).decode('utf-8')

    def close(self):
        self.client_socket.close()
