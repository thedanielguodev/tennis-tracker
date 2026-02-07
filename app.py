from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Player
from calculations import log_practice, log_match, predict_utr, reset_effectiveness, label_effectiveness

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tennis.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey123'

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

# ----------------- AUTH -----------------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form.get('role','player')
        if User.query.filter_by(username=username).first():
            return "Username taken!"
        user = User(username=username, password_hash=password, role=role)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ----------------- DASHBOARD -----------------
@app.route('/')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    players = Player.query.filter_by(user_id=user.id).all()
    return render_template('dashboard.html', user=user, players=players)

# ----------------- PLAYER ACTIONS -----------------
@app.route('/player/<int:player_id>')
def player_view(player_id):
    player = Player.query.get_or_404(player_id)
    return render_template('player.html', player=player,
                           label=label_effectiveness(player.effectiveness),
                           predicted=predict_utr(player))

@app.route('/practice', methods=['POST'])
def practice():
    data = request.json
    player = Player.query.get(data['player_id'])
    log_practice(player, data['minutes'], data['intensity'])
    db.session.commit()
    return jsonify({
        'effectiveness': round(player.effectiveness),
        'label': label_effectiveness(player.effectiveness),
        'predicted': predict_utr(player)
    })

@app.route('/match', methods=['POST'])
def match():
    data = request.json
    player = Player.query.get(data['player_id'])
    log_match(player, data['opponent_utr'], data['result'])
    db.session.commit()
    return jsonify({
        'utr': round(player.current_utr,2),
        'effectiveness': round(player.effectiveness),
        'label': label_effectiveness(player.effectiveness),
        'predicted': predict_utr(player)
    })

@app.route('/reset', methods=['POST'])
def reset():
    data = request.json
    player = Player.query.get(data['player_id'])
    reset_effectiveness(player)
    db.session.commit()
    return jsonify({
        'effectiveness': round(player.effectiveness),
        'label': label_effectiveness(player.effectiveness)
    })

if __name__ == '__main__':
    app.run(debug=True)
