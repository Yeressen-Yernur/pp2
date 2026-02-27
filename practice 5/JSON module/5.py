import json

i = {"fruit": "apple", "price": 100}
j = json.dumps(i, indent=4)
print(j)