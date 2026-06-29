import sqlite3

conn = sqlite3.connect("complaints.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS complaints (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    mobile TEXT,

    village TEXT,

    address TEXT,

    complaint_type TEXT,

    description TEXT,

    image TEXT,

    video TEXT

)
""")

conn.commit()
conn.close()

print("Database Created Successfully!")
