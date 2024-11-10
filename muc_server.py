import socket
import threading

HOST = '127.0.0.1'
PORT = 12345
clients = []
messages = []

def handle_client(client_socket):
    global messages
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"Received message: {message}")
                messages.append(message)
                if len(messages) == 2:
                    common_words = find_common_words(messages[0], messages[1])
                    for client in clients:
                        client.send(f"Common words: {common_words}".encode())
                    messages = []
            else:
                remove_client(client_socket)
                break
        except:
            continue

def find_common_words(msg1, msg2):
    words1 = set(msg1.split())
    words2 = set(msg2.split())
    common = words1 & words2
    return ' '.join(common)

def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(2)
    print("Server started. Waiting for clients to connect...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,)).start()

start_server()
