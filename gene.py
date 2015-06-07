__author__ = 'Alvaro Barbeira'

class GeneData:
    """A list of values for a Gene"""
    def __init__(self,name=None,column=None):
        self.data = []
        self.name = name
        self.column = column

import person
#
class GeneDataSets:
    """Sets of -gene data-"""
    def __init__(self):
        self.genes = []
        self.genes_by_name = {}

    def setUpPeople(self, people):
        self.people = people
        self.person_id_to_index = {}
        for i,chum in enumerate(people.people):
            self.person_id_to_index[chum.id] = i

