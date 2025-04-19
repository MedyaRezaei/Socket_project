import socket 
import threading
from application.use_cases.chat_use_case import ChatUseCase
from domain.entities.message import Message 

class ServerSocket:
    def __init__(self, host='0.0.0.0', port=1485):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def start(self):
        """
        Starts the server, accepts incoming client connections, and spawns a new thread for each client.
        """
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server is listening on {self.host}:{self.port}...")

        try:
            while True:
                # Accept client connections
                client_socket, client_address = self.server_socket.accept()
                thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                thread.start()
                print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

        except KeyboardInterrupt:
            print("\nServer shutting down...")
        finally:
            self.server_socket.close()

    def handle_client(self, client_socket, client_address):
        """
        Handles communication with a single client.
        """
        print(f"[+] New connection from {client_address}")
        use_case = ChatUseCase()

        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break

                client_message = data.decode('utf-8').strip()
                print(f"[{client_address}] Client: {client_message}")

                message = Message(client_message)
                if message.is_close_command():
                    print(f"[{client_address}] Connection closed by client.")
                    break

                response = use_case.process_message(message)
                if response:
                    client_socket.sendall(response.encode('utf-8'))

        except Exception as e:
            print(f"[{client_address}] Error: {e}")
        finally:
            client_socket.close()
            print(f"[{client_address}] Connection closed.")
