import socket
import threading
import queue
import json
#Fill in the below with your IP and Port
ip = "0.0.0.0" #Putting 0.0.0.0 means any IP address to the server will work
port = 5000 #Must be an integer (no quotation marks)

message_queue = queue.Queue()
clients_data = {}
clients_lock = threading.Lock()

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            if message.strip().lower() == "reciever":
                with clients_lock:
                    response = json.dumps(clients_data)
                client_socket.send(response.encode())

            else:
                parts = message.split(" ")
                if len(parts) >= 3:
                    hostname = parts[0]
                    cpu = parts[1]
                    ram = parts[2]

                    with clients_lock:
                        clients_data[hostname] = {"cpu": cpu, "ram": ram}

                message_queue.put(message)
                client_socket.send("Message received!".encode())

        except Exception as e:
            #print(f"Error handling client: {e}")
            break

    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen()

    #print(f"Server listening on {ip}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        #print(f"Connection from {client_address}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()
