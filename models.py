
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    players = db.relationship("Player", backref="owner", lazy=True)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    utr = db.Column(db.Float, default=1.0)
    effectiveness = db.Column(db.Float, default=50.0)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    practices = db.relationship("PracticeLog", backref="player", lazy=True)
    matches = db.relationship("MatchLog", backref="player", lazy=True)

class PracticeLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    minutes = db.Column(db.Float)
    intensity = db.Column(db.Float)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)

class MatchLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    opponent_utr = db.Column(db.Float)
    result = db.Column(db.String(10))  # "win" or "loss"
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)
