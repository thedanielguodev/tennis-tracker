from flask import Flask, render_template, request, redirect
from models import create_tables
from calculations import weekly_practice_total, match_win_rate
import sqlite3
from datetime import datetime

app = Flask(__name__)
create_tables()

@app.route("/")
def home():
    weekly_total = weekly_practice_total()
    win_rate = match_win_rate()
    return render_template("index.html", weekly_total=weekly_total, win_rate=win_rate)

@app.route("/log_practice", methods=["POST"])
def log_practice():
    date = request.form["date"]
    duration = int(request.form["duration"])
    
    conn = sqlite3.connect('tennis.db')
    c = conn.cursor()
    c.execute("INSERT INTO practices (date, duration) VALUES (?, ?)", (date, duration))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/log_match", methods=["POST"])
def log_match():
    date = request.form["date"]
    opponent_level = int(request.form["opponent_level"])
    result = request.form["result"]
    
    conn = sqlite3.connect('tennis.db')
    c = conn.cursor()
    c.execute("INSERT INTO matches (date, opponent_level, result) VALUES (?, ?, ?)", 
              (date, opponent_level, result))
    conn.commit()
    conn.close()
    return redirect("/")
