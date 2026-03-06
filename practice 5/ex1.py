import re
yernur = r"ab*"
yeressen = ["a", "ab", "abb", "aqqq" , "abbbbb"]
for i in yeressen:
    if re.fullmatch(yernur, i):
        print(i)