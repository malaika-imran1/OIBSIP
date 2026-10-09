import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib


DATABASE = "chat.db"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register():
    username = username_entry.get().strip()
    password = password_entry.get()

    if not username or not password:
        messagebox.showwarning(
            "Missing Information",
            "Please enter username and password."
        )
        return

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    try:
        hashed_password = hash_password(password)

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )

        connection.commit()

        messagebox.showinfo(
            "Success",
            "Registration successful! You can now login."
        )

        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Error",
            "Username already exists."
        )

    finally:
        connection.close()


def login():
    username = username_entry.get().strip()
    password = password_entry.get()

    if not username or not password:
        messagebox.showwarning(
            "Missing Information",
            "Please enter username and password."
        )
        return

    hashed_password = hash_password(password)

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, hashed_password)
    )

    user = cursor.fetchone()

    connection.close()

    if user:
        messagebox.showinfo(
            "Login Successful",
            f"Welcome, {username}!"
        )
    else:
        messagebox.showerror(
            "Login Failed",
            "Invalid username or password."
        )


# ---------------- GUI ----------------

window = tk.Tk()
window.title("Chat Application - Login")
window.geometry("400x300")

title = tk.Label(
    window,
    text="Chat Application",
    font=("Arial", 20, "bold")
)
title.pack(pady=20)


username_label = tk.Label(
    window,
    text="Username"
)
username_label.pack()

username_entry = tk.Entry(
    window,
    width=30
)
username_entry.pack(pady=5)


password_label = tk.Label(
    window,
    text="Password"
)
password_label.pack()

password_entry = tk.Entry(
    window,
    width=30,
    show="*"
)
password_entry.pack(pady=5)


register_button = tk.Button(
    window,
    text="Register",
    width=15,
    command=register
)
register_button.pack(pady=10)


login_button = tk.Button(
    window,
    text="Login",
    width=15,
    command=login
)
login_button.pack()


window.mainloop()