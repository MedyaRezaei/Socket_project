from interface.cli.server_cli import run_server
from interface.cli.client_cli import run_client

def main():
    # Ask the user if they want to run the server or client
    choice = input("Run as (s)erver or (c)lient? ").strip().lower()

    if choice == 's':
        # Run the server CLI
        run_server()
    elif choice == 'c':
        # Run the client CLI
        run_client()
    else:
        print("Invalid choice. Please choose 's' for server or 'c' for client.")

if __name__ == "__main__":
    main()
