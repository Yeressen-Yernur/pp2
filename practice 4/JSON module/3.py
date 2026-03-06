import json

e = {"city": "Shymkent", "country": "Kazakhstan"}

with open("a.json", "w") as f:
    json.dump(e, f)