from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="player")  # player or coach
    players = db.relationship('Player', backref='owner', lazy=True)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    current_utr = db.Column(db.Float, default=1.0)
    effectiveness = db.Column(db.Float, default=50.0)  # always percentage
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    practice_logs = db.relationship('PracticeLog', backref='player', lazy=True)
    match_logs = db.relationship('MatchLog', backref='player', lazy=True)

class PracticeLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    minutes = db.Column(db.Float, nullable=False)
    intensity = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class MatchLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    opponent_utr = db.Column(db.Float, nullable=False)
    result = db.Column(db.String(10), nullable=False)  # 'win' or 'loss'
    date = db.Column(db.DateTime, default=datetime.utcnow)
