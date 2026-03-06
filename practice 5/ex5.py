import re
a = r"a.*b"
b = ["ab" , "ayernurb" , "ayeressenb" , "a2008b" , "ac"]
for i in b:
    if re.fullmatch(a, i):
        print(i)