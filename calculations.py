practice_score = 0
match_score = 0

def add_practice(minutes, intensity):
    global practice_score
    practice_score += minutes * intensity

def add_match(opponent_level, result):
    global match_score
    if result == "win":
        match_score += opponent_level * 1.5
    else:
        match_score += opponent_level * 0.7

def get_effectiveness():
    return round(practice_score + match_score, 1)
