# interface/cli/server_cli.py

from infrastructure.network.server_socket import ServerSocket

def run_server():
    """
    Starts the chat server and handles multiple clients concurrently.
    """
    try:
        server = ServerSocket()
        server.start()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    except Exception as e:
        print(f"An error occurred: {e}")
