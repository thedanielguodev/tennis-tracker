from datetime import datetime

player_utr = None
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

def set_player_utr(u):
    global player_utr, effectiveness
    player_utr = clamp(float(u), 1, 16.5)  # minimum UTR is now 1
    effectiveness = 50

def log_practice(minutes, intensity):
    global effectiveness
    minutes = float(minutes)
    intensity = float(intensity)
    practice_log.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "minutes": minutes,
        "intensity": intensity
    })
    boost = min((minutes * intensity) / 40, 12)
    effectiveness = clamp(effectiveness + boost, 0, 100)

def log_match(opponent_utr, result):
    global player_utr, effectiveness
    if player_utr is None: return
    opponent_utr = float(opponent_utr)
    if abs(opponent_utr - player_utr) > 2: return

    win = result == "win"
    actual = 1 if win else 0
    expected = 1 / (1 + 10 ** (opponent_utr - player_utr))

    form_factor = (effectiveness - 50) / 200
    K = 0.08

    delta = K * (actual - expected + form_factor)
    player_utr = clamp(player_utr + delta, 1, 16.5)  # min 1
    effectiveness = clamp(effectiveness + (6 if win else -6), 0, 100)

    match_log.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "opponent": opponent_utr,
        "result": result
    })

def predict_utr():
    if player_utr is None: return None
    return round(clamp(player_utr + (effectiveness - 50) / 300, 1, 16.5), 2)

def reset_state():
    global player_utr, effectiveness, practice_log, match_log
    player_utr = None
    effectiveness = 50
    practice_log = []
    match_log = []

def get_state():
    return {
        "utr": round(player_utr, 2) if player_utr is not None else None,
        "effectiveness": round(effectiveness),
        "label": label(effectiveness),
        "predicted": predict_utr(),
        "practice_log": practice_log,
        "match_log": match_log
    }
