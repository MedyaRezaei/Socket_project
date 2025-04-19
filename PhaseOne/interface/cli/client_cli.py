from infrastructure.network.client_socket import ClientSocket

def run_client():
    client = ClientSocket()
    try:
        client.connect()
        while True:
            msg = input("client: ")
            client.send(msg)

            if msg.lower() == "close":
                print("Closing connection...")
                break

            response = client.receive()
            print(f"Server: {response}")
    except ConnectionRefusedError:
        print("Server is unavailable. Please try again later.")
    finally:
        client.close()
        print("Client closed connection.")
