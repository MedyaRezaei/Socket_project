import socket

class ServerSocket:
    def __init__(self, host='127.0.0.1', port=1485):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"Server is listening on {self.host}:{self.port}")
        return self.server_socket.accept()

    def stop(self):
        self.server_socket.close()
