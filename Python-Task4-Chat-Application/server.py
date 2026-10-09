
import socket
import threading
import sqlite3
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5555
DATABASE = "chat.db"

clients = {}
clients_lock = threading.Lock()


def get_time():
    return datetime.now().strftime("%H:%M")


def save_message(room, username, message, timestamp):
    connection = sqlite3.connect(DATABASE)
    try:
        connection.execute(
            """INSERT INTO messages
               (room, username, message, timestamp)
               VALUES (?, ?, ?, ?)""",
            (room, username, message, timestamp)
        )
        connection.commit()
    finally:
        connection.close()


def get_history(room):
    connection = sqlite3.connect(DATABASE)
    try:
        cursor = connection.execute(
            """SELECT username, message, timestamp
               FROM messages
               WHERE room = ?
               ORDER BY id DESC LIMIT 50""",
            (room,)
        )
        rows = cursor.fetchall()
        return list(reversed(rows))
    finally:
        connection.close()


def send_to_client(client, message):
    try:
        client.sendall((message + "\n").encode())
        return True
    except OSError:
        return False


def broadcast(room, message):
    with clients_lock:
        recipients = [
            client for client, info in clients.items()
            if info["room"] == room
        ]

    for client in recipients:
        send_to_client(client, message)


def handle_client(client, address):
    username = None
    room = None

    try:
        # Receive username|room
        initial_data = client.recv(1024).decode().strip()

        if "|" not in initial_data:
            send_to_client(
                client,
                "ERROR: Invalid login information."
            )
            return

        username, room = initial_data.split("|", 1)
        username = username.strip()
        room = room.strip()

        if not username or not room:
            send_to_client(client, "ERROR: Username and room are required.")
            return

        # Confirm that the room exists in the database.
        connection = sqlite3.connect(DATABASE)
        try:
            result = connection.execute(
                "SELECT name FROM rooms WHERE name = ?",
                (room,)
            ).fetchone()
        finally:
            connection.close()

        if not result:
            send_to_client(
                client,
                f"ERROR: Room '{room}' does not exist. Create it first."
            )
            return

        with clients_lock:
            clients[client] = {
                "username": username,
                "room": room
            }

        print(f"{username} joined room '{room}' from {address}")

        # Send previous messages to this user only.
        for old_username, old_message, old_time in get_history(room):
            send_to_client(
                client,
                f"[{old_time}] {old_username}: {old_message}"
            )

        join_message = f"[{get_time()}] {username} joined {room}."
        broadcast(room, join_message)

        while True:
            message = client.recv(4096).decode().strip()

            if not message or message.lower() == "exit":
                break

            timestamp = get_time()
            formatted = f"[{timestamp}] {username}: {message}"

            save_message(room, username, message, timestamp)
            print(f"[{room}] {formatted}")
            broadcast(room, formatted)

    except (ConnectionResetError, BrokenPipeError):
        print(f"{address} disconnected.")
    except Exception as error:
        print("Server error:", error)
    finally:
        with clients_lock:
            was_connected = client in clients
            if was_connected:
                del clients[client]

        try:
            client.close()
        except OSError:
            pass

        if was_connected and username and room:
            leave_message = f"[{get_time()}] {username} left {room}."
            broadcast(room, leave_message)
            print(leave_message)


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((HOST, PORT))
        server.listen()

        print(f"Chat server running at {HOST}:{PORT}")
        print("Waiting for clients...")

        while True:
            client, address = server.accept()

            thread = threading.Thread(
                target=handle_client,
                args=(client, address),
                daemon=True
            )
            thread.start()

    except OSError as error:
        print("Could not start server:", error)
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.close()


if __name__ == "__main__":
    main()