import socket
import threading
import queue
#Fill in the below with your IP and Port
ip = "0.0.0.0" #Putting 0.0.0.0 means any IP address to the server will work
port = 5000 #Must be an integer (no quotation marks)

message_queue = queue.Queue()

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            message_queue.put(message)

            response = "Message received!"
            client_socket.send(response.encode())

        except Exception as e:
            print(f"Error handling client: {e}")
            break

    client_socket.close()

def start_server():
    global ip
    global port
    host = ip
    port = port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()
