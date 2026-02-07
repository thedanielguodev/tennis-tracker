from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(200))
    role = db.Column(db.String(20), default='player')  # player, coach
    players = db.relationship('Player', backref='owner')

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(80))
    current_utr = db.Column(db.Float, default=1.0)
    predicted_utr = db.Column(db.Float, default=1.0)
    effectiveness = db.Column(db.Float, default=50)
    practice_logs = db.relationship('PracticeLog', backref='player')
    match_logs = db.relationship('MatchLog', backref='player')

class PracticeLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    minutes = db.Column(db.Float)
    intensity = db.Column(db.Float)
    date = db.Column(db.DateTime)

class MatchLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    opponent_utr = db.Column(db.Float)
    result = db.Column(db.String(10))
    date = db.Column(db.DateTime)
