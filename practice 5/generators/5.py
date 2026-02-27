def simple_gen():
  yield "Yeressen"
  yield "Yernur"
  yield "Arnuruly"

gen = simple_gen()
print(next(gen))
print(next(gen))
print(next(gen))