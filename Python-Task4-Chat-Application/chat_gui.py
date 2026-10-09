
import tkinter as tk
from tkinter import messagebox
import socket
import threading
import queue

HOST = "127.0.0.1"
PORT = 5555


class ChatWindow:
    def __init__(self, username, room_name="General"):
        self.username = username
        self.room_name = room_name
        self.messages_queue = queue.Queue()
        self.closing = False

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client.connect((HOST, PORT))

            # Tell server the username and room
            self.client.send(
                f"{username}|{room_name}".encode()
            )

        except (ConnectionRefusedError, OSError) as error:
            messagebox.showerror(
                "Connection Error",
                f"Could not connect to server.\n{error}"
            )
            self.client.close()
            return

        self.window = tk.Tk()
        self.window.title(f"{room_name} - Chat Application")
        self.window.geometry("650x550")

        tk.Label(
            self.window,
            text=f"Room: {room_name}",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        self.chat_area = tk.Text(
            self.window,
            state="disabled",
            wrap="word",
            font=("Arial", 11)
        )
        self.chat_area.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=10
        )

        bottom = tk.Frame(self.window)
        bottom.pack(fill=tk.X, padx=10, pady=10)

        self.message_entry = tk.Entry(bottom, font=("Arial", 11))
        self.message_entry.pack(
            side=tk.LEFT, fill=tk.X, expand=True, ipady=7
        )
        self.message_entry.bind("<Return>", self.enter_pressed)

        tk.Button(
            bottom,
            text="Send",
            command=self.send_message
        ).pack(side=tk.RIGHT, padx=8)

        self.window.protocol("WM_DELETE_WINDOW", self.close_chat)

        threading.Thread(
            target=self.receive_messages,
            daemon=True
        ).start()

        self.window.after(100, self.check_messages)
        self.message_entry.focus_set()
        self.window.mainloop()

    def receive_messages(self):
        while not self.closing:
            try:
                data = self.client.recv(4096)

                if not data:
                    break

                self.messages_queue.put(data.decode())

            except OSError:
                break

    def check_messages(self):
        if self.closing:
            return

        while not self.messages_queue.empty():
            message = self.messages_queue.get()

            self.chat_area.config(state="normal")
            self.chat_area.insert(tk.END, message + "\n")
            self.chat_area.config(state="disabled")
            self.chat_area.see(tk.END)

        self.window.after(100, self.check_messages)

    def send_message(self):
        message = self.message_entry.get().strip()

        if not message:
            return

        try:
            self.client.send(message.encode())
            self.message_entry.delete(0, tk.END)
        except OSError:
            messagebox.showerror("Error", "Message could not be sent.")

    def enter_pressed(self, event):
        self.send_message()

    def close_chat(self):
        self.closing = True

        try:
            self.client.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

        self.client.close()
        self.window.destroy()


if __name__ == "__main__":
    username = input("Enter username: ").strip()
    room_name = input("Enter room name: ").strip() or "General"

    if username:
        ChatWindow(username, room_name)