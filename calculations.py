player_utr = None
effectiveness = 50
practice_log = []
#fixed version
def clamp(v, a, b):
    return max(a, min(v, b))

def label(e):
    if e < 30: return "Cold"
    if e < 50: return "Average"
    if e < 70: return "Sharp"
    if e < 85: return "On Fire"
    return "Peak Form"

def set_player_utr(u):
    global player_utr
    player_utr = clamp(float(u), 0, 16.5)

def log_practice(minutes, intensity):
    global effectiveness
    practice_log.append((minutes, intensity))
    boost = min((minutes * intensity) / 40, 12)
    effectiveness = clamp(effectiveness + boost, 0, 100)

def log_match(opponent_utr, result):
    global player_utr, effectiveness

    opponent_utr = float(opponent_utr)

    if abs(opponent_utr - player_utr) > 2:
        return

    win = result == "win"
    actual = 1 if win else 0
    expected = 1 / (1 + 10 ** (opponent_utr - player_utr))

    form_factor = (effectiveness - 50) / 200
    K = 0.08

    delta = K * (actual - expected + form_factor)
    player_utr = clamp(player_utr + delta, 0, 16.5)

    effectiveness = clamp(effectiveness + (6 if win else -6), 0, 100)

def predict_utr():
    return round(clamp(player_utr + (effectiveness - 50) / 300, 0, 16.5), 2)

def get_state():
    return {
        "utr": round(player_utr, 2) if player_utr is not None else None,
        "effectiveness": round(effectiveness),
        "label": label(effectiveness),
        "predicted": predict_utr() if player_utr is not None else None
    }
