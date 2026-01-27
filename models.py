import sqlite3

def create_tables():
    conn = sqlite3.connect('tennis.db')
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS practices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            duration INTEGER
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            opponent_level INTEGER,
            result TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
