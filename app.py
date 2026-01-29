from flask import Flask, render_template, request, jsonify
from calculations import add_practice, add_match, get_effectiveness
#fixed
app = Flask(__name__)

@app.route("/")
def index():
    return render_template(
        "index.html",
        effectiveness=get_effectiveness()
    )

@app.route("/log_practice", methods=["POST"])
def log_practice():
    data = request.get_json()
    add_practice(
        int(data["minutes"]),
        int(data["intensity"])
    )
    return jsonify({"effectiveness": get_effectiveness()})

@app.route("/log_match", methods=["POST"])
def log_match():
    data = request.get_json()
    add_match(
        int(data["opponent"]),
        data["result"]
    )
    return jsonify({"effectiveness": get_effectiveness()})

if __name__ == "__main__":
    app.run(debug=True)
