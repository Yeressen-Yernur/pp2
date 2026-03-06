import re
text = "YeressenYernurArnuruly"
result = re.split(r"(?=[A-Z])", text)
print(result)