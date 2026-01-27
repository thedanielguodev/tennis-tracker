import sqlite3
from datetime import datetime, timedelta

def weekly_practice_total():
    conn = sqlite3.connect('tennis.db')
    c = conn.cursor()
    
    one_week_ago = datetime.now() - timedelta(days=7)
    c.execute('''
        SELECT SUM(duration) FROM practices
        WHERE date >= ?
    ''', (one_week_ago.strftime('%Y-%m-%d'),))
    
    total = c.fetchone()[0]
    conn.close()
    
    return total or 0

def match_win_rate():
    conn = sqlite3.connect('tennis.db')
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM matches WHERE result='win'")
    wins = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM matches")
    total = c.fetchone()[0]
    
    conn.close()
    return (wins / total * 100) if total > 0 else 0
