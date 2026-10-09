import tkinter as tk
from tkinter import messagebox
import sqlite3
import socket
import threading

DATABASE = "chat.db"

HOST = "127.0.0.1"
PORT = 5555

client = None
chat_window = None
chat_box = None
message_entry = None


# ---------------- DATABASE ----------------

def get_rooms():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM rooms ORDER BY name")
    rooms = cursor.fetchall()

    connection.close()

    return [room[0] for room in rooms]


# ---------------- ROOM FUNCTIONS ----------------

def create_room():
    room_name = room_entry.get().strip()

    if not room_name:
        messagebox.showwarning(
            "Missing Room",
            "Please enter a room name."
        )
        return

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO rooms (name) VALUES (?)",
            (room_name,)
        )

        connection.commit()

        messagebox.showinfo(
            "Success",
            f"Room '{room_name}' created successfully."
        )

        room_entry.delete(0, tk.END)

        load_rooms()

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Error",
            "This room already exists."
        )

    finally:
        connection.close()


def load_rooms():
    room_list.delete(0, tk.END)

    rooms = get_rooms()

    for room in rooms:
        room_list.insert(tk.END, room)


# ---------------- RECEIVE MESSAGES ----------------

def receive_messages():

    while True:

        try:
            message = client.recv(4096).decode()

            if not message:
                break

            # GUI ko main thread se update karna
            chat_window.after(
                0,
                display_message,
                message
            )

        except:
            break


def display_message(message):

    if chat_box:

        chat_box.config(state=tk.NORMAL)

        chat_box.insert(
            tk.END,
            message + "\n"
        )

        chat_box.see(tk.END)

        chat_box.config(state=tk.DISABLED)


# ---------------- SEND MESSAGE ----------------

def send_message():

    message = message_entry.get().strip()

    if not message:
        return

    if message.lower() == "exit":

        leave_chat()

        return

    try:

        client.send(message.encode())

        message_entry.delete(
            0,
            tk.END
        )

    except:

        messagebox.showerror(
            "Connection Error",
            "Message send nahi ho saka."
        )


# ---------------- LEAVE CHAT ----------------

def leave_chat():

    global client

    try:

        if client:
            client.send("exit".encode())
            client.close()

    except:
        pass

    client = None

    if chat_window:
        chat_window.destroy()

    window.deiconify()


# ---------------- OPEN CHAT ----------------

def open_chat(room_name):

    global client
    global chat_window
    global chat_box
    global message_entry

    username = username_entry.get().strip()

    if not username:

        messagebox.showwarning(
            "Missing Name",
            "Please pehle apna naam enter karein."
        )

        return

    # ---------------- CONNECT ----------------

    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    try:

        client.connect(
            (HOST, PORT)
        )

    except ConnectionRefusedError:

        client.close()
        client = None

        messagebox.showerror(
            "Connection Error",
            "Server running nahi hai.\n\n"
            "Pehle server.py run karein."
        )

        return

    except Exception as e:

        client.close()
        client = None

        messagebox.showerror(
            "Connection Error",
            str(e)
        )

        return

    # ---------------- SEND NAME + ROOM ----------------

    client.send(
        f"{username}|{room_name}".encode()
    )

    # Room window hide
    window.withdraw()

    # ---------------- CHAT WINDOW ----------------

    chat_window = tk.Toplevel()

    chat_window.title(
        f"Chat Application - {room_name}"
    )

    chat_window.geometry(
        "650x550"
    )

    chat_window.protocol(
        "WM_DELETE_WINDOW",
        leave_chat
    )

    # Title

    title = tk.Label(
        chat_window,
        text=f"Room: {room_name}",
        font=("Arial", 20, "bold")
    )

    title.pack(
        pady=(15, 5)
    )

    user_label = tk.Label(
        chat_window,
        text=f"Logged in as: {username}",
        font=("Arial", 10)
    )

    user_label.pack(
        pady=(0, 10)
    )

    # ---------------- CHAT BOX ----------------

    chat_box = tk.Text(
        chat_window,
        width=70,
        height=22,
        font=("Arial", 11),
        state=tk.DISABLED,
        wrap=tk.WORD
    )

    chat_box.pack(
        padx=15,
        pady=10,
        fill=tk.BOTH,
        expand=True
    )

    # ---------------- BOTTOM FRAME ----------------

    bottom_frame = tk.Frame(
        chat_window
    )

    bottom_frame.pack(
        fill=tk.X,
        padx=15,
        pady=10
    )

    message_entry = tk.Entry(
        bottom_frame,
        font=("Arial", 11)
    )

    message_entry.pack(
        side=tk.LEFT,
        fill=tk.X,
        expand=True,
        padx=(0, 10)
    )

    message_entry.focus()

    send_button = tk.Button(
        bottom_frame,
        text="Send",
        width=10,
        command=send_message
    )

    send_button.pack(
        side=tk.LEFT
    )

    leave_button = tk.Button(
        chat_window,
        text="Leave Room",
        width=15,
        command=leave_chat
    )

    leave_button.pack(
        pady=(0, 15)
    )

    # Enter key se message send
    message_entry.bind(
        "<Return>",
        lambda event: send_message()
    )

    # ---------------- RECEIVE THREAD ----------------

    receive_thread = threading.Thread(
        target=receive_messages,
        daemon=True
    )

    receive_thread.start()


# ---------------- JOIN ROOM ----------------

def join_room():

    selected = room_list.curselection()

    if not selected:

        messagebox.showwarning(
            "Select Room",
            "Please pehle ek room select karein."
        )

        return

    room_name = room_list.get(
        selected[0]
    )

    open_chat(room_name)


# ---------------- MAIN GUI ----------------

window = tk.Tk()

window.title(
    "Chat Application - Rooms"
)

window.geometry(
    "450x550"
)


# ---------------- TITLE ----------------

title = tk.Label(
    window,
    text="Chat Rooms",
    font=("Arial", 22, "bold")
)

title.pack(
    pady=(20, 15)
)


# ---------------- USERNAME ----------------

username_label = tk.Label(
    window,
    text="Your Name:",
    font=("Arial", 11)
)

username_label.pack()


username_entry = tk.Entry(
    window,
    width=35,
    font=("Arial", 11)
)

username_entry.pack(
    pady=5
)


# ---------------- CREATE ROOM ----------------

room_label = tk.Label(
    window,
    text="Create New Room:",
    font=("Arial", 11)
)

room_label.pack(
    pady=(15, 0)
)


room_entry = tk.Entry(
    window,
    width=35,
    font=("Arial", 11)
)

room_entry.pack(
    pady=5
)


create_button = tk.Button(
    window,
    text="Create Room",
    width=20,
    command=create_room
)

create_button.pack(
    pady=8
)


# ---------------- ROOM LIST ----------------

list_label = tk.Label(
    window,
    text="Available Rooms:",
    font=("Arial", 11, "bold")
)

list_label.pack(
    pady=(5, 5)
)


room_list = tk.Listbox(
    window,
    width=40,
    height=12,
    font=("Arial", 11)
)

room_list.pack(
    pady=5
)


# ---------------- BUTTONS ----------------

join_button = tk.Button(
    window,
    text="Join Selected Room",
    width=20,
    command=join_room
)

join_button.pack(
    pady=8
)


refresh_button = tk.Button(
    window,
    text="Refresh Rooms",
    width=20,
    command=load_rooms
)

refresh_button.pack()


# ---------------- LOAD ROOMS ----------------

load_rooms()

window.mainloop()