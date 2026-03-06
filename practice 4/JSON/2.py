import json

x = {
  "name": "Yernur",
  "age": 17,
  "city": "Shymkent"
}

y = json.dumps(x)

print(y)