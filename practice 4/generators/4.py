def generator(a, b):
    for i in range(a, b+1):
        yield i * i

a, b = map(int, input().split())

print(" ".join(str(num) for num in generator(a,b)))