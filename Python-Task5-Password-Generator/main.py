import tkinter as tk
from tkinter import messagebox
import secrets
import string
import pyperclip


# ==========================================
# PASSWORD HISTORY
# ==========================================

password_history = []


# ==========================================
# GENERATE SECURE PASSWORD
# ==========================================

def generate_password():

    try:
        length = int(length_spinbox.get())

    except ValueError:
        messagebox.showerror(
            "Invalid Length",
            "Please enter a valid password length."
        )
        return

    # Minimum length
    if length < 8:
        messagebox.showerror(
            "Invalid Length",
            "Password length must be at least 8 characters."
        )
        return

    # ==========================================
    # CHARACTER TYPES
    # ==========================================

    selected_types = []

    if uppercase_var.get():
        selected_types.append("uppercase")

    if lowercase_var.get():
        selected_types.append("lowercase")

    if numbers_var.get():
        selected_types.append("numbers")

    if symbols_var.get():
        selected_types.append("symbols")

    # At least 2 types required
    if len(selected_types) < 2:
        messagebox.showerror(
            "Invalid Selection",
            "Please select at least 2 character types."
        )
        return

    # ==========================================
    # CHARACTER SETS
    # ==========================================

    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    numbers = string.digits
    symbols = string.punctuation

    # ==========================================
    # AMBIGUOUS CHARACTERS
    # ==========================================

    ambiguous = "0Ol1"

    if exclude_ambiguous_var.get():

        uppercase = "".join(
            char for char in uppercase
            if char not in ambiguous
        )

        lowercase = "".join(
            char for char in lowercase
            if char not in ambiguous
        )

        numbers = "".join(
            char for char in numbers
            if char not in ambiguous
        )

    # ==========================================
    # AVAILABLE CHARACTER POOL
    # ==========================================

    character_pool = ""

    if uppercase_var.get():
        character_pool += uppercase

    if lowercase_var.get():
        character_pool += lowercase

    if numbers_var.get():
        character_pool += numbers

    if symbols_var.get():
        character_pool += symbols

    # ==========================================
    # GUARANTEE ONE CHARACTER FROM EACH TYPE
    # ==========================================

    password_characters = []

    if uppercase_var.get():
        password_characters.append(
            secrets.choice(uppercase)
        )

    if lowercase_var.get():
        password_characters.append(
            secrets.choice(lowercase)
        )

    if numbers_var.get():
        password_characters.append(
            secrets.choice(numbers)
        )

    if symbols_var.get():
        password_characters.append(
            secrets.choice(symbols)
        )

    # ==========================================
    # FILL REMAINING CHARACTERS
    # ==========================================

    remaining = length - len(password_characters)

    for _ in range(remaining):

        password_characters.append(
            secrets.choice(character_pool)
        )

    # ==========================================
    # SECURE SHUFFLE
    # ==========================================

    # Fisher-Yates shuffle using secrets
    for i in range(len(password_characters) - 1, 0, -1):

        j = secrets.randbelow(i + 1)

        password_characters[i], password_characters[j] = (
            password_characters[j],
            password_characters[i]
        )

    password = "".join(password_characters)

    # ==========================================
    # DISPLAY PASSWORD
    # ==========================================

    password_entry.delete(0, tk.END)

    password_entry.insert(0, password)

    # ==========================================
    # STRENGTH
    # ==========================================

    update_strength(length, len(selected_types))

    # ==========================================
    # COPY AUTOMATICALLY
    # ==========================================

    try:
        pyperclip.copy(password)

    except Exception:
        pass

    # ==========================================
    # HISTORY
    # ==========================================

    password_history.insert(0, password)

    # Keep only last 5
    if len(password_history) > 5:
        password_history.pop()

    update_history()


# ==========================================
# PASSWORD STRENGTH
# ==========================================

def update_strength(length, type_count):

    if length < 10 or type_count < 3:

        strength = "Weak"
        color = "red"

    elif length < 14 or type_count == 3:

        strength = "Medium"
        color = "orange"

    else:

        strength = "Strong"
        color = "green"

    strength_label.config(
        text=f"Strength: {strength}",
        fg=color
    )


# ==========================================
# COPY BUTTON
# ==========================================

def copy_password():

    password = password_entry.get()

    if password == "":
        messagebox.showwarning(
            "No Password",
            "Generate a password first."
        )
        return

    try:

        pyperclip.copy(password)

        messagebox.showinfo(
            "Copied",
            "Password copied to clipboard."
        )

    except Exception as error:

        messagebox.showerror(
            "Clipboard Error",
            f"Could not copy password.\n\n{error}"
        )


# ==========================================
# UPDATE HISTORY DISPLAY
# ==========================================

def update_history():

    history_listbox.delete(0, tk.END)

    for password in password_history:

        history_listbox.insert(
            tk.END,
            password
        )


# ==========================================
# MAIN WINDOW
# ==========================================

window = tk.Tk()

window.title("Random Password Generator")

window.geometry("650x700")

window.resizable(False, False)


# ==========================================
# TITLE
# ==========================================

title_label = tk.Label(
    window,
    text="RANDOM PASSWORD GENERATOR",
    font=("Arial", 22, "bold")
)

title_label.pack(pady=20)


# ==========================================
# LENGTH
# ==========================================

length_label = tk.Label(
    window,
    text="Password Length",
    font=("Arial", 12)
)

length_label.pack()

length_spinbox = tk.Spinbox(
    window,
    from_=8,
    to=100,
    width=10,
    font=("Arial", 12)
)

length_spinbox.delete(0, tk.END)
length_spinbox.insert(0, "16")

length_spinbox.pack(pady=8)


# ==========================================
# CHARACTER TYPE CHECKBOXES
# ==========================================

uppercase_var = tk.BooleanVar(value=True)

lowercase_var = tk.BooleanVar(value=True)

numbers_var = tk.BooleanVar(value=True)

symbols_var = tk.BooleanVar(value=True)

exclude_ambiguous_var = tk.BooleanVar(value=False)


uppercase_check = tk.Checkbutton(
    window,
    text="Uppercase Letters (A-Z)",
    variable=uppercase_var,
    font=("Arial", 11)
)

uppercase_check.pack(anchor="w", padx=180)


lowercase_check = tk.Checkbutton(
    window,
    text="Lowercase Letters (a-z)",
    variable=lowercase_var,
    font=("Arial", 11)
)

lowercase_check.pack(anchor="w", padx=180)


numbers_check = tk.Checkbutton(
    window,
    text="Numbers (0-9)",
    variable=numbers_var,
    font=("Arial", 11)
)

numbers_check.pack(anchor="w", padx=180)


symbols_check = tk.Checkbutton(
    window,
    text="Symbols (!@#$...)",
    variable=symbols_var,
    font=("Arial", 11)
)

symbols_check.pack(anchor="w", padx=180)


ambiguous_check = tk.Checkbutton(
    window,
    text="Exclude ambiguous characters (0, O, l, 1)",
    variable=exclude_ambiguous_var,
    font=("Arial", 11)
)

ambiguous_check.pack(anchor="w", padx=180, pady=8)


# ==========================================
# GENERATE BUTTON
# ==========================================

generate_button = tk.Button(
    window,
    text="Generate Password",
    command=generate_password,
    font=("Arial", 12, "bold"),
    width=25
)

generate_button.pack(pady=15)


# ==========================================
# PASSWORD DISPLAY
# ==========================================

password_entry = tk.Entry(
    window,
    width=45,
    font=("Arial", 14),
    justify="center"
)

password_entry.pack(pady=5)


# ==========================================
# STRENGTH
# ==========================================

strength_label = tk.Label(
    window,
    text="Strength: --",
    font=("Arial", 14, "bold")
)

strength_label.pack(pady=10)


# ==========================================
# COPY BUTTON
# ==========================================

copy_button = tk.Button(
    window,
    text="Copy to Clipboard",
    command=copy_password,
    font=("Arial", 11),
    width=25
)

copy_button.pack(pady=5)


# ==========================================
# HISTORY
# ==========================================

history_title = tk.Label(
    window,
    text="Last 5 Generated Passwords",
    font=("Arial", 14, "bold")
)

history_title.pack(pady=15)


history_listbox = tk.Listbox(
    window,
    width=50,
    height=5,
    font=("Arial", 10)
)

history_listbox.pack()


# ==========================================
# START PROGRAM
# ==========================================

window.mainloop()