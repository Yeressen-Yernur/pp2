import json
import os

LEADERBOARD_FILE = "leaderboard.json"
SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "red",
    "difficulty": "normal"
}


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
                # merge with defaults in case new keys were added
                return {**DEFAULT_SETTINGS, **data}
        except Exception:
            pass
    return DEFAULT_SETTINGS.copy()


def save_settings(settings: dict):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)


def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return []


def save_score(name: str, score: int, distance: int, coins: int):
    lb = load_leaderboard()
    lb.append({"name": name, "score": score, "distance": distance, "coins": coins})
    lb.sort(key=lambda x: x["score"], reverse=True)
    lb = lb[:10]
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(lb, f, indent=2)
    return lb