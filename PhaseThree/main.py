from interface.cli.server_cli import run_server
from interface.cli.client_cli import run_client

def main():
    choice = input("Run as (s)erver or (c)lient? ").strip().lower()
    if choice == 's':
        run_server()
    elif choice == 'c':
        run_client()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
