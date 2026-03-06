import re
yernur = "abc , defg. hijk"
result = re.sub(r"[ ,\.]", ":", yernur)
print(result)