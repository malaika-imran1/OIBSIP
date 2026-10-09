
import tkinter as tk
from tkinter import messagebox
import sqlite3
from chat_gui import ChatWindow

DATABASE = "chat.db"


class RoomWindow:
    def __init__(self, username):
        self.username = username
        self.window = tk.Tk()
        self.window.title("Select Chat Room")
        self.window.geometry("420x480")

        tk.Label(
            self.window, text=f"Welcome, {username}!",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        self.entry = tk.Entry(self.window, width=30)
        self.entry.pack(pady=5)

        tk.Button(
            self.window, text="Create Room",
            command=self.create_room
        ).pack(pady=5)

        self.rooms = tk.Listbox(self.window, width=35, height=12)
        self.rooms.pack(pady=15)

        tk.Button(
            self.window, text="Join Selected Room",
            command=self.join_room
        ).pack(pady=5)

        self.load_rooms()
        self.window.mainloop()

    def load_rooms(self):
        self.rooms.delete(0, tk.END)
        connection = sqlite3.connect(DATABASE)
        names = connection.execute(
            "SELECT name FROM rooms ORDER BY name"
        ).fetchall()
        connection.close()

        for name in names:
            self.rooms.insert(tk.END, name[0])

    def create_room(self):
        name = self.entry.get().strip()

        if not name:
            messagebox.showwarning("Error", "Enter a room name.")
            return

        connection = sqlite3.connect(DATABASE)
        try:
            connection.execute(
                "INSERT INTO rooms (name) VALUES (?)", (name,)
            )
            connection.commit()
            self.entry.delete(0, tk.END)
            self.load_rooms()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Room already exists.")
        finally:
            connection.close()

    def join_room(self):
        selection = self.rooms.curselection()
        if not selection:
            messagebox.showwarning("Error", "Select a room first.")
            return

        room_name = self.rooms.get(selection[0])
        self.window.destroy()
        ChatWindow(self.username, room_name)


if __name__ == "__main__":
    username = input("Enter username: ").strip()
    if username:
        RoomWindow(username)