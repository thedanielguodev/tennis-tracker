from datetime import date

player_utr = None
daily_effectiveness = {}  # { 'YYYY-MM-DD': effectiveness }
practice_log = []         # list of (date, minutes, intensity)
match_log = []            # list of (date, opponent_utr, result)
baseline_effectiveness = 50

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
    today = str(date.today())
    boost = min((minutes * intensity)/40, 12)
    practice_log.append((today, minutes, intensity))
    daily_effectiveness[today] = clamp(daily_effectiveness.get(today, baseline_effectiveness) + boost, 0, 100)

def log_match(opponent_utr, result):
    global player_utr
    today = str(date.today())
    opponent_utr = float(opponent_utr)
    
    # Only count if UTR difference <=2
    if player_utr is not None and abs(opponent_utr - player_utr) <= 2:
        win = result == "win"
        actual = 1 if win else 0
        expected = 1 / (1 + 10 ** (opponent_utr - player_utr))
        form_factor = (daily_effectiveness.get(today, baseline_effectiveness) - 50) / 200
        K = 0.08
        delta = K * (actual - expected + form_factor)
        player_utr = clamp(player_utr + delta, 0, 16.5)
        daily_effectiveness[today] = clamp(daily_effectiveness.get(today, baseline_effectiveness) + (6 if win else -6), 0, 100)
    
    match_log.append((today, opponent_utr, result))

def reset_all():
    global daily_effectiveness, practice_log, match_log, player_utr
    daily_effectiveness = {}
    practice_log = []
    match_log = []
    player_utr = None

def predict_utr():
    if player_utr is None: return None
    today_eff = daily_effectiveness.get(str(date.today()), baseline_effectiveness)
    return round(clamp(player_utr + (today_eff - 50)/300, 0, 16.5), 2)

def get_state():
    today = str(date.today())
    current_eff = daily_effectiveness.get(today, baseline_effectiveness)
    return {
        "utr": round(player_utr,2) if player_utr is not None else None,
        "effectiveness": round(current_eff),
        "label": label(current_eff),
        "predicted": predict_utr(),
        "practice_log": practice_log,
        "match_log": match_log,
        "daily_effectiveness": daily_effectiveness
    }
