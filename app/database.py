import sqlite3

# Connect to SQLite database (create it if not exists)
conn = sqlite3.connect('comparison.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS comparisons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        comparison_id INTEGER,
        name TEXT NOT NULL,
        score REAL DEFAULT 1000,
        FOREIGN KEY (comparison_id) REFERENCES comparisons(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        comparison_id INTEGER,
        item_id INTEGER,
        rank INTEGER,
        FOREIGN KEY (comparison_id) REFERENCES comparisons(id),
        FOREIGN KEY (item_id) REFERENCES items(id)
    )
''')

# Commit changes and close connection
conn.commit()
conn.close()
