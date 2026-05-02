import json
import os

FILE = "leaderboard.json"


def load_scores():

    if not os.path.exists(FILE):
        return []

    try:
        with open(FILE, "r") as f:
            data = json.load(f)

        # 🧹 чистим мусор (оставляем только числа)
        clean = []
        for x in data:
            if isinstance(x, int):
                clean.append(x)
            elif isinstance(x, dict) and "score" in x:
                clean.append(x["score"])

        return clean

    except:
        return []


def save_score(score):

    data = load_scores()

    data.append(int(score))   

    data = sorted(data, reverse=True)[:5]

    with open(FILE, "w") as f:
        json.dump(data, f)