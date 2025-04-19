from interface.cli.server_cli import run_server
from interface.cli.client_cli import run_client

if __name__ == "__main__":
    choice = input("Run (s)erver or (c)lient? ").lower()
    if choice == 's':
        run_server()
    elif choice == 'c':
        run_client()
    else:
        print("Invalid choice.")
