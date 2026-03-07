with open("sample.txt", "a") as f:
    f.write("\nAppended line")

with open("sample.txt", "r") as f:
    print(f.read())