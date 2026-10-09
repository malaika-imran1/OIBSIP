import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt


# ==========================================
# DATABASE
# ==========================================

DATABASE = "bmi_history.db"


def create_database():
    try:
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                recorded_at TEXT NOT NULL
            )
        """)

        connection.commit()
        connection.close()

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not create database.\n\n{error}"
        )


# ==========================================
# BMI CATEGORY
# ==========================================

def get_category(bmi):

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    else:
        return "Obese"


# ==========================================
# COLOR
# ==========================================

def get_color(category):

    if category == "Normal":
        return "green"

    elif category == "Obese":
        return "red"

    else:
        return "orange"


# ==========================================
# GET INPUTS
# ==========================================

def get_inputs():

    username = name_entry.get().strip()

    if username == "":
        messagebox.showerror(
            "Invalid Input",
            "Please enter a user name."
        )
        return None

    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numbers for weight and height."
        )
        return None

    if weight <= 0 or height <= 0:
        messagebox.showerror(
            "Invalid Input",
            "Weight and height must be greater than zero."
        )
        return None

    return username, weight, height


# ==========================================
# CALCULATE BMI
# ==========================================

def calculate_bmi():

    data = get_inputs()

    if data is None:
        return

    username, weight, height = data

    bmi = weight / (height ** 2)

    category = get_category(bmi)

    color = get_color(category)

    result_label.config(
        text=f"BMI: {bmi:.2f}\nCategory: {category}",
        fg=color
    )


# ==========================================
# SAVE RECORD
# ==========================================

def save_record():

    data = get_inputs()

    if data is None:
        return

    username, weight, height = data

    bmi = weight / (height ** 2)

    category = get_category(bmi)

    recorded_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:

        connection = sqlite3.connect(DATABASE)

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO bmi_records
            (username, weight, height, bmi, category, recorded_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            username,
            weight,
            height,
            bmi,
            category,
            recorded_at
        ))

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Success",
            "BMI record saved successfully!"
        )

    except sqlite3.Error as error:

        messagebox.showerror(
            "Database Error",
            f"Could not save record.\n\n{error}"
        )


# ==========================================
# SHOW BMI GRAPH
# ==========================================

def show_graph():

    username = name_entry.get().strip()

    if username == "":
        messagebox.showerror(
            "Missing Name",
            "Please enter a user name first."
        )
        return

    try:

        connection = sqlite3.connect(DATABASE)

        cursor = connection.cursor()

        cursor.execute("""
            SELECT recorded_at, bmi
            FROM bmi_records
            WHERE username = ?
            ORDER BY recorded_at ASC
        """, (username,))

        records = cursor.fetchall()

        connection.close()

        if len(records) == 0:
            messagebox.showinfo(
                "No Records",
                f"No BMI records found for {username}."
            )
            return

        dates = []
        bmi_values = []

        for record in records:

            dates.append(record[0])
            bmi_values.append(record[1])

        # Create graph
        plt.figure(figsize=(8, 5))

        plt.plot(
            dates,
            bmi_values,
            marker="o"
        )

        plt.xlabel("Date")

        plt.ylabel("BMI")

        plt.title(f"BMI Trend - {username}")

        plt.xticks(rotation=45)

        plt.tight_layout()

        plt.show()

    except sqlite3.Error as error:

        messagebox.showerror(
            "Database Error",
            f"Could not read database.\n\n{error}"
        )


# ==========================================
# VIEW HISTORY
# ==========================================

def view_history():

    username = name_entry.get().strip()

    if username == "":
        messagebox.showerror(
            "Missing Name",
            "Please enter a user name first."
        )
        return

    try:

        connection = sqlite3.connect(DATABASE)

        cursor = connection.cursor()

        cursor.execute("""
            SELECT recorded_at, weight, height, bmi, category
            FROM bmi_records
            WHERE username = ?
            ORDER BY recorded_at DESC
        """, (username,))

        records = cursor.fetchall()

        connection.close()

        if len(records) == 0:
            messagebox.showinfo(
                "No Records",
                f"No records found for {username}."
            )
            return

        history_window = tk.Toplevel(window)

        history_window.title(
            f"BMI History - {username}"
        )

        history_window.geometry("650x400")

        title = tk.Label(
            history_window,
            text=f"BMI History - {username}",
            font=("Arial", 18, "bold")
        )

        title.pack(pady=15)

        for record in records:

            date = record[0]
            weight = record[1]
            height = record[2]
            bmi = record[3]
            category = record[4]

            text = (
                f"{date}   |   "
                f"Weight: {weight} kg   |   "
                f"Height: {height} m   |   "
                f"BMI: {bmi:.2f}   |   "
                f"{category}"
            )

            label = tk.Label(
                history_window,
                text=text,
                font=("Arial", 10),
                anchor="w"
            )

            label.pack(
                fill="x",
                padx=15,
                pady=5
            )

    except sqlite3.Error as error:

        messagebox.showerror(
            "Database Error",
            f"Could not read history.\n\n{error}"
        )


# ==========================================
# MAIN WINDOW
# ==========================================

window = tk.Tk()

window.title("BMI Calculator")

window.geometry("600x700")

window.resizable(False, False)


# ==========================================
# TITLE
# ==========================================

title_label = tk.Label(
    window,
    text="BMI CALCULATOR",
    font=("Arial", 24, "bold")
)

title_label.pack(pady=25)


# ==========================================
# NAME
# ==========================================

name_label = tk.Label(
    window,
    text="User Name",
    font=("Arial", 12)
)

name_label.pack()

name_entry = tk.Entry(
    window,
    width=30,
    font=("Arial", 12)
)

name_entry.pack(pady=8)


# ==========================================
# WEIGHT
# ==========================================

weight_label = tk.Label(
    window,
    text="Weight (kg)",
    font=("Arial", 12)
)

weight_label.pack()

weight_entry = tk.Entry(
    window,
    width=30,
    font=("Arial", 12)
)

weight_entry.pack(pady=8)


# ==========================================
# HEIGHT
# ==========================================

height_label = tk.Label(
    window,
    text="Height (metres)",
    font=("Arial", 12)
)

height_label.pack()

height_entry = tk.Entry(
    window,
    width=30,
    font=("Arial", 12)
)

height_entry.pack(pady=8)


# ==========================================
# BUTTONS
# ==========================================

calculate_button = tk.Button(
    window,
    text="Calculate BMI",
    command=calculate_bmi,
    font=("Arial", 11),
    width=25
)

calculate_button.pack(pady=8)


save_button = tk.Button(
    window,
    text="Save Record",
    command=save_record,
    font=("Arial", 11),
    width=25
)

save_button.pack(pady=8)


history_button = tk.Button(
    window,
    text="View BMI History",
    command=view_history,
    font=("Arial", 11),
    width=25
)

history_button.pack(pady=8)


graph_button = tk.Button(
    window,
    text="Show BMI Trend",
    command=show_graph,
    font=("Arial", 11),
    width=25
)

graph_button.pack(pady=8)


# ==========================================
# RESULT
# ==========================================

result_label = tk.Label(
    window,
    text="BMI: --\nCategory: --",
    font=("Arial", 18, "bold")
)

result_label.pack(pady=25)


# ==========================================
# CREATE DATABASE
# ==========================================

create_database()


# ==========================================
# START APPLICATION
# ==========================================

window.mainloop()