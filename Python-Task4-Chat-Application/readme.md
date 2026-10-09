
# Python Chat Application

## Features
- User registration and login
- Tkinter graphical interface
- Multiple chat rooms
- Real-time messaging using sockets and threads
- SQLite message history
- Timestamps
- Emoji shortcodes
- Basic sound alerts
- Graceful chat disconnection

## Requirements
- Python 3
- Tkinter
- SQLite3 (included with standard Python installations)

## Setup
1. Run: `python database.py`
2. Run: `python server.py`
3. Open another terminal.
4. Run: `python login_gui.py`
5. Register an account and log in.
6. Create or select a room and join.

Run the server before opening the chat.

## Database
- `users`: usernames and password hashes
- `rooms`: room names
- `messages`: room, username, message and timestamp

Messages are stored in `chat.db` and are loaded when joining a room.

## Security Limitations
- Messages are not encrypted in transit.
- Passwords use SHA-256, which is not recommended for production password storage.
- This is an educational localhost project, not a production-ready secure messenger.
- Authentication is performed by the login interface; the socket server does not independently authenticate clients.