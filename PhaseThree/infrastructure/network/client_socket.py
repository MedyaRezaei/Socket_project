import socket
import threading
from application.use_cases.chat_use_case import ChatUseCase
from domain.entities.message import Message

class ClientSocket:
    def __init__(self, host='192.168.1.104', port=1485):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.use_case = ChatUseCase()
        self.stop_event = threading.Event()

    def connect(self):
        try:
            self.sock.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.daemon = True
            self.receive_thread.start()
        except Exception as e:
            print(f"Connection error: {e}")
            self.close()

    def send(self, message):
        try:
            msg = Message(message)
            self.sock.sendall(msg.content.encode('utf-8'))
        except Exception as e:
            print(f"Send error: {e}")
            self.close()

    def receive_messages(self):
        while not self.stop_event.is_set():
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                print("\r" + message)
                print("you:", end=" ", flush=True)
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
