def yernur(n):
    cnt = 1
    while cnt <= n:
        yield cnt
        cnt += 1
for i in yernur(5):
    print(i)