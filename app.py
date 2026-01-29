from flask import Flask, render_template, request, jsonify
from calculations import add_practice_minutes, get_weekly_minutes

app = Flask(__name__)

@app.route("/")
def index():
    return render_template(
        "index.html",
        weekly_total=get_weekly_minutes()
    )

@app.route("/log_practice", methods=["POST"])
def log_practice():
    data = request.get_json()
    minutes = int(data["duration"])
    add_practice_minutes(minutes)
    return jsonify({
        "weekly_total": get_weekly_minutes()
    })

if __name__ == "__main__":
    app.run(debug=True)
