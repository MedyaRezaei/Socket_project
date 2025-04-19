import sys
import os

# Ensure imports work even when running directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from infrastructure.network.server_socket import ServerSocket

def run_server():
    try:
        server = ServerSocket()
        server.start()
    except KeyboardInterrupt:
        print("\n[SERVER SHUTDOWN] Server manually stopped.")
    except Exception as e:
        print(f"[SERVER ERROR] {e}")

if __name__ == '__main__':
    run_server()
