from infrastructure.network.client_socket import ClientSocket

def run_client():
    client = ClientSocket()
    try:
        client.connect()
        while True:
            message = input("client: ")
            client.send(message)

            if message.lower() == "close":
                print("Closing connection...")
                break

            response = client.receive()
            print(f"Server: {response}")

    except ConnectionRefusedError:
        print("Server is unavailable. Please try again later.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()
