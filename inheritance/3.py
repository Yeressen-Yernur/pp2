class Animal:
    def speak(self):
        return "I make a sound"

class Dog(Animal):
    def speak(self):
        return "Woof!"  

animal = Animal()
dog = Dog()

print(animal.speak())  
print(dog.speak())    