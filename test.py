import re

text = "I have 2 apples and 10 bananas"
pattern = r'[0-9]+'

print(re.findall(pattern, text))