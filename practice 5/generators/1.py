def yer():
  yield 1
  yield 2
  yield 3

for i in yer():
  print(i)