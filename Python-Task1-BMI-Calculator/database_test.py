import sqlite3

# Connect to database
connection = sqlite3.connect("bmi_history.db")

# Create cursor
cursor = connection.cursor()

# Create table
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

# Save changes
connection.commit()

# Close database
connection.close()

print("Database created successfully!")