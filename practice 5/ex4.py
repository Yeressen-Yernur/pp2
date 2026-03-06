import re
a = "Yeressen Yernur yeressen yernur"
b = r"[A-Z][a-z]+"
print(re.findall(b , a))