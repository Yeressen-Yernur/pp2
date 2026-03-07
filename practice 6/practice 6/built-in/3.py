names = ["Yernur" , "Nurken" , "Ashna"]
ages = [17 , 17 , 19]
for i, name in enumerate(names):
    print(i, name)
for name, age in zip(names, ages):
    print(name, age)