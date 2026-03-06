def generator(n):
    while n != 0:
        yield n
        n -= 1

n = int(input())

print(" ".join(str(num) for num in generator(n)))