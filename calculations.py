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
    minutes = float(minutes)
    intensity = float(intensity)
    player.effectiveness = clamp(player.effectiveness + min((minutes*intensity)/40, 12), 0, 100)
    player.practice_logs.append({'minutes': minutes, 'intensity': intensity, 'date': datetime.now()})

def log_match(player, opponent_utr, result):
    opponent_utr = float(opponent_utr)
    if abs(opponent_utr - player.current_utr) > 2:
        return

    win = result == 'win'
    actual = 1 if win else 0
    expected = 1 / (1 + 10 ** (opponent_utr - player.current_utr))
    form_factor = (player.effectiveness - 50) / 200
    K = 0.08

    delta = K * (actual - expected + form_factor)
    player.current_utr = clamp(player.current_utr + delta, 1, 16.5)
    player.effectiveness = clamp(player.effectiveness + (6 if win else -6), 0, 100)
    player.match_logs.append({'opponent_utr': opponent_utr, 'result': result, 'date': datetime.now()})

def predict_utr(player):
    return round(clamp(player.current_utr + (player.effectiveness - 50)/300, 1, 16.5), 2)

def reset_effectiveness(player):
    player.effectiveness = 50
