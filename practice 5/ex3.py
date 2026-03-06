import re
a = "yernur_yeressen yeressen_yernur"
b = r"[a-z]+_[a-z]+"
c = re.findall(b, a)
print(c)