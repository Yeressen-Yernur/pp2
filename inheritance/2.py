class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "I make a sound"

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed

    def speak(self):
        return f"{self.name} says Woof!"

dog = Dog("Buddy", "Labrador")
print(dog.name) 
print(dog.breed)  
print(dog.speak())  