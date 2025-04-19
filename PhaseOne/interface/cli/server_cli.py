from application.use_cases.chat_use_case import ChatUseCase
from domain.entities.message import Message
from infrastructure.network.server_socket import ServerSocket

def run_server():
    server = ServerSocket()
    use_case = ChatUseCase()

    try:
        new_socket, address = server.start()
        print(f"Connected by {address}")
        while True:
            data = new_socket.recv(1024)
            if not data:
                break

            message = Message(data.decode('utf-8'))
            print(f"Client: {message.content}")

            if message.is_close_command():
                print("Client requested to close the connection.")
                break

            response = use_case.process_message(message)
            new_socket.sendall(response.encode('utf-8'))
    finally:
        new_socket.close()
        server.stop()
        print("Server closed connection.")
