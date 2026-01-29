from flask import Flask, render_template, request, jsonify
from calculations import add_practice, add_match, get_effectiveness

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", score=get_effectiveness())

@app.route("/practice", methods=["POST"])
def practice():
    data = request.get_json()
    add_practice(int(data["minutes"]), int(data["intensity"]))
    return jsonify({"score": get_effectiveness()})

@app.route("/match", methods=["POST"])
def match():
    data = request.get_json()
    add_match(int(data["opponent"]), data["result"])
    return jsonify({"score": get_effectiveness()})

if __name__ == "__main__":
    app.run()
