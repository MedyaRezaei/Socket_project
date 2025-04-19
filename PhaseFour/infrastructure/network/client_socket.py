import socket
import threading
from domain.entities.message import Message

class ClientSocket:
    def __init__(self, host='192.168.1.104', port=1485, username="Guest"):
        self.host = host
        self.port = port
        self.username = username
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stop_event = threading.Event()
        self.on_message = None
        self.on_user_list = None

    def connect(self):
        try:
           self.sock.connect((self.host, self.port))
           self.sock.sendall(self.username.encode('utf-8'))  # Send username first
           threading.Thread(target=self.receive_messages, daemon=True).start()
           return True
        except Exception as e:
            print(f"[ERROR] Could not connect to server: {e}")
            self.close()
            return False


    def send(self, message):
        try:
            msg = Message(message)
            self.sock.sendall(msg.content.encode('utf-8'))
        except Exception as e:
            print(f"[ERROR] Send failed: {e}")
            self.close()

    def receive_messages(self):
        while not self.stop_event.is_set():
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')

                if message.startswith("USERS:"):
                    users = message[len("USERS:"):].split(',')
                    if self.on_user_list:
                        self.on_user_list(users)
                else:
                    if self.on_message:
                        self.on_message(message)
                    else:
                        print(message)
            except Exception:
                break
        self.stop_event.set()

    def close(self):
        if not self.stop_event.is_set():
            self.stop_event.set()
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except:
                pass
            self.sock.close()
            print("[DISCONNECTED] Client socket closed.")
