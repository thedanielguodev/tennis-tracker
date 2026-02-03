from datetime import datetime

player_utr = 0.0
effectiveness = 50
practice_log = []
match_log = []

def clamp(v, a, b):
    return max(a, min(v, b))

def label(e):
    if e < 30: return "Cold"
    if e < 50: return "Average"
    if e < 70: return "Sharp"
    if e < 85: return "On Fire"
    return "Peak Form"

def set_player_utr(utr):
    global player_utr
    player_utr = clamp(float(utr), 0, 16.5)

def log_practice(minutes, intensity):
    global effectiveness
    date = datetime.now().strftime("%Y-%m-%d")
    practice_log.append({"minutes": minutes, "intensity": intensity, "date": date})
    boost = min((minutes * intensity) / 40, 12)
    effectiveness = clamp(effectiveness + boost, 0, 100)

def log_match(opponent_utr, result):
    global player_utr, effectiveness
    opponent_utr = float(opponent_utr)
    date = datetime.now().strftime("%Y-%m-%d")
    
    # Only count matches within 2 UTR difference
    if abs(opponent_utr - player_utr) <= 2:
        win = result.lower() == "win"
        actual = 1 if win else 0
        expected = 1 / (1 + 10 ** (opponent_utr - player_utr))
        form_factor = (effectiveness - 50) / 200
        K = 0.08
        delta = K * (actual - expected + form_factor)
        player_utr = clamp(player_utr + delta, 0, 16.5)

    effectiveness = clamp(effectiveness + (6 if result.lower() == "win" else -6), 0, 100)
    match_log.append({"opponent": opponent_utr, "result": result, "date": date})

def reset_all():
    global player_utr, effectiveness, practice_log, match_log
    player_utr = 0
    effectiveness = 50
    practice_log = []
    match_log = []

def predict_utr():
    return round(clamp(player_utr + (effectiveness - 50) / 300, 0, 16.5), 2)

def get_state():
    return {
        "utr": round(player_utr, 2),
        "effectiveness": round(effectiveness),
        "label": label(effectiveness),
        "predicted": predict_utr(),
        "practice_log": practice_log,
        "match_log": match_log
    }
