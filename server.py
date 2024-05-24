#save the both file server.py and client.py for the task 5

import socket
import threading
import json
import hashlib
import os
import base64
import pymongo
from cryptography.fernet import Fernet

# Configuration
HOST = '127.0.0.1'
PORT = 9090
BUFFER_SIZE = 1024
KEY = Fernet.generate_key()  # Generate a secret key for encryption
fernet = Fernet(KEY)

# User database (using MongoDB)
client = pymongo.MongoClient('localhost', 27017)
db = client['chat_app']
users = db['users']
messages = db['messages']

def register_user(username, password):
    if users.find_one({'username': username}):
        return False

    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    users.insert_one({'username': username, 'password': hashed_password})
    return True

def handle_client(client_socket, address):
    print(f"Connected by {address}")

    # Receive and verify username and password
    username = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    password = client_socket.recv(BUFFER_SIZE).decode('utf-8')

    if not register_user(username, password):
        client_socket.sendall(b"Registration failed")
        client_socket.close()
        return

    client_socket.sendall(b"Registered")

    # Handle incoming messages
    while True:
        message = client_socket.recv(BUFFER_SIZE)
        if not message:
            break
        message = fernet.decrypt(message).decode('utf-8')

        # Store message history
        messages.insert_one({'from': username, 'to': 'all', 'message': message})

        # Broadcast message to all connected clients
        for client in clients:
            if client != client_socket:
                client.sendall(fernet.encrypt(message.encode('utf-8')))

    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server started on {HOST}:{PORT}")

    global clients
    clients = []

    while True:
        client_socket, address = server_socket.accept()
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

if __name__ == "__main__":
    start_server()
