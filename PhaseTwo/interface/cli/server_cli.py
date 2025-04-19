# interface/cli/server_cli.py

from application.use_cases.chat_use_case import ChatUseCase
from domain.entities.message import Message
from infrastructure.network.server_socket import ServerSocket

def run_server():
    """
    Runs the server application, accepting client connections,
    processing messages, and sending responses.
    """
    server = ServerSocket()
    use_case = ChatUseCase()

    try:
        # Start the server and accept incoming client connections
        new_socket, address = server.start()
        print(f"Connected by {address}")

        while True:
            # Receive data from the client
            data = new_socket.recv(1024)
            if not data:
                break  # No data means the client has closed the connection

            # Create a Message object from the received data
            message = Message(data.decode('utf-8'))
            print(f"Client: {message.content}")

            # If the message is a close command, break the loop
            if message.is_close_command():
                print("Client requested to close the connection.")
                break

            # Process the message and generate a response using the use case
            response = use_case.process_message(message)

            # Send the response back to the client
            new_socket.sendall(response.encode('utf-8'))

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the socket and stop the server gracefully
        new_socket.close()
        server.stop()
        print("Server closed connection.")
