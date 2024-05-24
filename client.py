import socket
import threading
import tkinter as tk
from tkinter import messagebox
import json
import base64
import pymongo
import pytz
from datetime import datetime
from cryptography.fernet import Fernet
import requests
import io
from PIL import Image, ImageTk

class ChatApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Application")
        self.root.geometry("400x600")

        # Create UI components
        self.username_label = tk.Label(root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(root, width=30)
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, width=30, show="*")
        self.password_entry.pack()

        self.register_button = tk.Button(root, text="Register", command=self.register)
        self.register_button.pack()

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack()

        self.chat_log = tk.Text(root, width=40, height=20)
        self.chat_log.pack()

        self.message_entry = tk.Entry(root, width=30)
        self.message_entry.pack()

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack()

        self.client_socket = None
        self.fernet = Fernet(Fernet.generate_key())

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("127.0.0.1", 9090))

        self.client_socket.sendall(username.encode('utf-8'))
        self.client_socket.sendall(password.encode('utf-8'))

        response = self.client_socket.recv(1024).decode('utf-8')
        if response == "Registered":
            messagebox.showinfo("Success", "Registration successful")
        else:
            messagebox.showerror("Error", "Registration failed")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("127.0.0.1", 9090))

        self.client_socket.sendall(username.encode('utf-8'))
        self.client_socket.sendall(password.encode('utf-8'))

        response = self.client_socket.recv(1024).decode('utf-8')
        if response == "Login successful":
            messagebox.showinfo("Success", "Login successful")
            self.start_listening()
        else:
            messagebox.showerror("Error", "Login failed")

    def start_listening(self):
        listen_thread = threading.Thread(target=self.listen_for_messages)
        listen_thread.start()

    def listen_for_messages(self):
        while True:
            message = self.client_socket.recv(1024)
            if not message:
                break
            message = self.fernet.decrypt(message).decode('utf-8')
            self.chat_log.insert(tk.END, message + "\n")

    def send_message(self):
        message = self.message_entry.get()
        if not message:
            return

        self.client_socket.sendall(self.fernet.encrypt(message.encode('utf-8')))
        self.message_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApplication(root)
    root.mainloop()


 