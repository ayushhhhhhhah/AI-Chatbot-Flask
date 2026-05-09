import sqlite3

# Connect Database
conn = sqlite3.connect("users.db")

# Create Cursor
cursor = conn.cursor()

# Create Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    email TEXT
)
""")

# Save Changes
conn.commit()

# Close Connection
conn.close()

print("Database Created Successfully ✅")