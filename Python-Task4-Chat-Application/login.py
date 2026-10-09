
import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
from room_gui import RoomWindow

DATABASE = "chat.db"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register():
    username = user_entry.get().strip()
    password = pass_entry.get()

    if not username or not password:
        messagebox.showwarning("Error", "Enter username and password.")
        return

    connection = sqlite3.connect(DATABASE)
    try:
        connection.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hash_password(password))
        )
        connection.commit()
        messagebox.showinfo("Success", "Registration successful!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")
    finally:
        connection.close()


def login():
    username = user_entry.get().strip()
    password = pass_entry.get()

    if not username or not password:
        messagebox.showwarning("Error", "Enter username and password.")
        return

    connection = sqlite3.connect(DATABASE)
    result = connection.execute(
        "SELECT 1 FROM users WHERE username = ? AND password = ?",
        (username, hash_password(password))
    ).fetchone()
    connection.close()

    if result:
        window.destroy()
        RoomWindow(username)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")


window = tk.Tk()
window.title("Chat Application - Login")
window.geometry("380x320")

tk.Label(
    window, text="Chat Application",
    font=("Arial", 19, "bold")
).pack(pady=20)

tk.Label(window, text="Username").pack()
user_entry = tk.Entry(window, width=30)
user_entry.pack(pady=5)

tk.Label(window, text="Password").pack()
pass_entry = tk.Entry(window, width=30, show="*")
pass_entry.pack(pady=5)

tk.Button(window, text="Register", width=18, command=register).pack(pady=8)
tk.Button(window, text="Login", width=18, command=login).pack()

window.mainloop()