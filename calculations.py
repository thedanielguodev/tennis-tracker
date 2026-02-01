score = 0

def add_practice(minutes, intensity):
    global score
    score += minutes * intensity * 0.1

def add_match(opponent_level, result):
    global score
    if result == "win":
        score += opponent_level * 5
    else:
        score -= opponent_level * 2
        if score < 0:
            score = 0

def get_score():
    return round(score, 1)
