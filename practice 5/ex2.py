import re
yernur = r"ab{2,3}"
yeressen = ["a", "ab", "abb", "abbb" , "abbbb"]
for i in yeressen:
    if re.fullmatch(yernur, i):
        print(i)