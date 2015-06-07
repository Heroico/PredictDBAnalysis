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

    @classmethod
    def peopleIntersection(cls,people1,people2):
        intersection = People()
        for id1, person1 in people1.people_by_id.iteritems():
            if id1 in people2.people_by_id:
                intersection.addPerson(person1)
        return intersection