__author__ = 'Alvaro Barbeira'

class Person:
    """A person."""
    def __init__(self):
        self.id = None

#
class People:
    """"A group of person """
    def __init__(self):
        self.people = []
        self.people_by_id = {}

    def addPerson(self,person):
        self.people.append(person)
        self.people_by_id[person.id] = person

    def dumpWithName(self,file_name):
        with open(file_name, "w+") as file:
            for i,person in enumerate(self.people):
                line = person.id+","+str(i)+"\n"
                file.write(line)

    @classmethod
    def peopleIntersection(cls,people1,people2):
        intersection = People()
        for i1, person1 in enumerate(people1.people):
            if person1.id in people2.people_by_id:
                intersection.addPerson(person1)
        return intersection