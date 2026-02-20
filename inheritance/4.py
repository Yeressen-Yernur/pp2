class Mother:
    def skills(self):
        return "Cooking"

class Father:
    def skills(self):
        return "Gardening"

class Child(Mother, Father):
    def skills(self):
        mother_skills = Mother.skills(self)
        father_skills = Father.skills(self)
        return f"{mother_skills} and {father_skills}"

child = Child()
print(child.skills())  