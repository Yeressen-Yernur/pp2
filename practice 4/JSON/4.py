import json

x = {
  "name": "Yernur",
  "age": 17,
  "married": False,
  "divorced": False,
  "pets": None,
  "cars": [
    {"model": "BMW 230", "mpg": 27.5},
    {"model": "Ford Edge", "mpg": 24.1}
  ]
}

print(json.dumps(x))