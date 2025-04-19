from infrastructure.network.client_socket import ClientSocket

def run_client():
    client = ClientSocket()
    try:
        client.connect()
        print("Connected to the server. Type /exit to leave the chat.")

        while True:
            message = input("you: ")
            if not message.strip():
                continue

            client.send(message)

            if message.lower() == "/exit":
                break

    except ConnectionRefusedError:
        print("Server is unavailable. Please try again later.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()
        print("Disconnected from server.")
