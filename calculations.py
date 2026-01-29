weekly_practice_score = 0
weekly_match_score = 0

def add_practice(minutes, intensity):
    global weekly_practice_score
    weekly_practice_score += minutes * intensity

def add_match(opponent_level, result):
    global weekly_match_score

    if result == "win":
        weekly_match_score += opponent_level * 1.5
    else:
        weekly_match_score += opponent_level * 0.7

def get_effectiveness():
    return round(
        (weekly_practice_score * 0.6) +
        (weekly_match_score * 0.4),
        1
    )
