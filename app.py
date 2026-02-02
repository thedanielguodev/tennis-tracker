from flask import Flask, render_template, request, jsonify
from calculations import set_player_utr, log_practice, log_match, get_state, reset_all

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", **get_state())

@app.route("/set_utr", methods=["POST"])
def set_utr():
    set_player_utr(request.json["utr"])
    return jsonify(get_state())

@app.route("/practice", methods=["POST"])
def practice():
    log_practice(request.json["minutes"], request.json["intensity"])
    return jsonify(get_state())

@app.route("/match", methods=["POST"])
def match():
    log_match(request.json["opponent"], request.json["result"])
    return jsonify(get_state())

@app.route("/reset", methods=["POST"])
def reset():
    reset_all()
    return jsonify(get_state())
