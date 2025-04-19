import socket
import threading
from application.use_cases.chat_use_case import ChatUseCase
from domain.entities.message import Message

class ServerSocket:
    def __init__(self, host='0.0.0.0', port=1485):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.client_info = {}

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server is listening on {self.host}:{self.port}...")

        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()

        except KeyboardInterrupt:
            print("\n[SERVER SHUTDOWN] Closing all connections...")
        finally:
            for client in self.clients:
                client.close()
            self.server_socket.close()

    def handle_client(self, client_socket, client_address):
        ip, port = client_address
        print(f"[CONNECTED] Client ({ip}, {port}) connected.")
        self.clients.append(client_socket)
        self.client_info[client_socket] = (ip, port)

        self.broadcast("has joined the chat.", client_socket)

        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message or message.lower() == "/exit":
                    break

                print(f"[{ip}:{port}] {message}")  # ✅ Print to server terminal

                msg = Message(message)
                response = ChatUseCase().process_message(msg)
                self.broadcast(response, client_socket)  # Don't send back to sender

            except Exception as e:
                print(f"[ERROR] ({ip}:{port}): {e}")
                break

        print(f"[DISCONNECTED] Client ({ip}, {port}) disconnected.")
        self.broadcast("has left the chat.", client_socket)

        if client_socket in self.clients:
            self.clients.remove(client_socket)
        self.client_info.pop(client_socket, None)
        client_socket.close()

    def broadcast(self, message, sender_socket=None):
        sender_info = self.client_info.get(sender_socket, ("Server", ""))
        sender_ip, sender_port = sender_info
        formatted_message = f"[{sender_ip}:{sender_port}] {message}" if sender_socket else f"[Server] {message}"

        for client in self.clients[:]:
            try:
                if client != sender_socket:  # Don't send the message back to the sender
                    client.sendall(formatted_message.encode('utf-8'))
            except:
                self.clients.remove(client)
                self.client_info.pop(client, None)
                client.close()
