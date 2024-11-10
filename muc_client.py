import tkinter as tk
import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

root = tk.Tk()
root.title("Client Chat")

chat_display = tk.Text(root, height=15, width=50, state=tk.DISABLED)
chat_display.pack(padx=10, pady=10)

message_entry = tk.Entry(root, width=40)
message_entry.pack(padx=10, pady=10)

def send_message():
    message = message_entry.get()
    if message:
        client_socket.send(message.encode())
        message_entry.delete(0, tk.END)

def receive_message():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                chat_display.config(state=tk.NORMAL)
                chat_display.insert(tk.END, f"{message}\n")
                chat_display.config(state=tk.DISABLED)
                chat_display.yview(tk.END)
        except:
            break

send_button = tk.Button(root, text="Send", width=10, command=send_message)
send_button.pack(pady=10)

threading.Thread(target=receive_message, daemon=True).start()

root.mainloop()
