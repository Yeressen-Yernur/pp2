numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x**2, numbers))
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print("Squares:", squares)
print("Even numbers:", even_numbers)