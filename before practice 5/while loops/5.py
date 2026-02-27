a = True
b = False
c = 0
while a or b:
    c += 1
    if c == 4:
        a = False
print(a)