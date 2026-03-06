def large_sequence(n):
  for i in range(n):
    yield i

gen = large_sequence(1000000)
print(next(gen))
print(next(gen))
print(next(gen))