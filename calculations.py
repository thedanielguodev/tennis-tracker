from datetime import datetime

def clamp(v, a, b):
    return max(a, min(v, b))

def label_effectiveness(e):
    if e < 30: return "Cold"
    if e < 50: return "Average"
    if e < 70: return "Sharp"
    if e < 85: return "On Fire"
    return "Peak Form"

def log_practice(player, minutes, intensity):
    from models import PracticeLog, db
    minutes = float(minutes)
    intensity = float(intensity)
    log = PracticeLog(player_id=player.id, minutes=minutes, intensity=intensity)
    db.session.add(log)
    boost = min((minutes * intensity)/40, 12)
    player.effectiveness = clamp(player.effectiveness + boost, 0, 100)

def log_match(player, opponent_utr, result):
    from models import MatchLog, db
    opponent_utr = float(opponent_utr)
    win = result == "win"
    actual = 1 if win else 0
    expected = 1 / (1 + 10 ** (opponent_utr - player.current_utr))
    form_factor = (player.effectiveness - 50) / 200
    K = 0.08
    delta = K * (actual - expected + form_factor)
    player.current_utr = clamp(player.current_utr + delta, 1, 16.5)
    player.effectiveness = clamp(player.effectiveness + (6 if win else -6), 0, 100)
    log = MatchLog(player_id=player.id, opponent_utr=opponent_utr, result=result)
    db.session.add(log)

def predict_utr(player):
    return round(clamp(player.current_utr + (player.effectiveness - 50)/300, 1, 16.5), 2)

def reset_effectiveness(player):
    player.effectiveness = 50
