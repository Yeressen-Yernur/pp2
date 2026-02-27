import json
x = ' {"name":"Yernur" , "surname":"Yeressen"} '  
y = json.loads(x)
print(y["name"] + " " + y["surname"])