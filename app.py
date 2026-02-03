from flask import Flask, render_template, request, jsonify
from calculations import set_player_utr, log_practice, log_match, reset_all, get_state

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", **get_state())

@app.route("/set_utr", methods=["POST"])
def set_utr():
    data = request.json
    set_player_utr(data.get("utr", 0))
    return jsonify(get_state())

@app.route("/practice", methods=["POST"])
def practice():
    data = request.json
    minutes = data.get("minutes", 0)
    intensity = data.get("intensity", 1)
    log_practice(minutes, intensity)
    return jsonify(get_state())

@app.route("/match", methods=["POST"])
def match():
    data = request.json
    opponent = data.get("opponent", 0)
    result = data.get("result", "loss")
    log_match(opponent, result)
    return jsonify(get_state())

@app.route("/reset", methods=["POST"])
def reset():
    reset_all()
    return jsonify(get_state())

if __name__ == "__main__":
    app.run(debug=True)
