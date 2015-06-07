__author__ = 'Alvaro Barbeira'

class Person:
    """A person."""
    def __init__(self):
        pass

#
class People:
    """"A group of person """
    def __init__(self):
        self.people = []
        self.people_by_row = {}

    def addPerson(self,person,line_num):
        self.people.append(person)
        self.people_by_row[line_num] = person