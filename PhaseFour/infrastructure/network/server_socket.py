import socket
import threading
from application.use_cases.chat_use_case import ChatUseCase
from domain.entities.message import Message
import datetime

class ServerSocket:
    def __init__(self, host='0.0.0.0', port=1485):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.client_info = {}  # {client_socket: (username, ip)}

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"[SERVER] Listening on {self.host}:{self.port}...")

        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket, client_address), daemon=True).start()
        except KeyboardInterrupt:
            print("\n[SERVER SHUTDOWN]")
        finally:
            for client in self.clients:
                client.close()
            self.server_socket.close()

    def handle_client(self, client_socket, client_address):
        ip, port = client_address
        try:
            username = client_socket.recv(1024).decode('utf-8')
            self.clients.append(client_socket)
            self.client_info[client_socket] = (username, ip)
            print(f"[CONNECTED] {username} ({ip}) connected.")

            self.send_user_list()
            self.broadcast(f"{username} has joined the chat.", client_socket)

            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if not message or message.lower() == "/exit":
                    break

                print(f"[{username}] {message}")

                if message.startswith("pm "):
                    self.handle_private_message(username, client_socket, message)
                else:
                    msg = Message(message)
                    response = ChatUseCase().process_message(msg)
                    self.broadcast(response, client_socket)

        except Exception as e:
            print(f"[ERROR] {ip}: {e}")
        finally:
            self.disconnect_client(client_socket)

    def handle_private_message(self, sender_username, client_socket, message):
        parts = message.split(' ', 2)
        if len(parts) < 3:
            client_socket.send("[SERVER] Invalid private message format.".encode('utf-8'))
            return

        target_username = parts[1]
        private_msg = parts[2]

        target_socket = None
        for sock, (uname, _) in self.client_info.items():
            if uname == target_username:
                target_socket = sock
                break

        timestamp = datetime.datetime.now().strftime('%H:%M:%S')

        if target_socket:
            sender_msg = f"[{timestamp}] [To {target_username}] {private_msg}"
            receiver_msg = f"[{timestamp}] [Private from {sender_username}] {private_msg}"

            try:
                if target_socket != client_socket:
                    target_socket.send(receiver_msg.encode('utf-8'))
                client_socket.send(sender_msg.encode('utf-8'))
            except Exception as e:
                print(f"[PM ERROR] {e}")
                try:
                    client_socket.send(f"[SERVER] Failed to send message to {target_username}".encode('utf-8'))
                except:
                    pass
        else:
            try:
                client_socket.send(f"[SERVER] User '{target_username}' not found.".encode('utf-8'))
            except:
                pass

    def disconnect_client(self, client_socket):
        username, ip = self.client_info.get(client_socket, ("Unknown", ""))
        print(f"[DISCONNECTED] {username} ({ip}) left.")
        if client_socket in self.clients:
            self.clients.remove(client_socket)
        self.client_info.pop(client_socket, None)
        self.broadcast(f"{username} has left the chat.")
        self.send_user_list()
        try:
            client_socket.close()
        except:
            pass

    def broadcast(self, message, sender_socket=None):
        sender = self.client_info.get(sender_socket, ("Server", ""))
        formatted = f"[{sender[0]}] {message}" if sender_socket else f"[Server] {message}"
        for client in self.clients[:]:
            try:
                client.sendall(formatted.encode('utf-8'))
            except:
                self.disconnect_client(client)

    def send_user_list(self):
        # Still sends both username and IP (used by client dropdown)
        user_list = [f"{username}@{ip}" for _, (username, ip) in self.client_info.items()]
        message = "USERS:" + ",".join(user_list)
        for client in self.clients[:]:
            try:
                client.sendall(message.encode('utf-8'))
            except:
                self.disconnect_client(client)
