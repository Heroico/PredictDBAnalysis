__author__ = 'Alvaro Barbeira'

class GeneData:
    """A list of values for a Gene"""
    def __init__(self,name=None,column=None):
        self.data = []
        self.name = name
        self.column = column

from person import Person
from person import People
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

    def geneDataWithName(self,name):
        gene_data = None
        if name in self.genes_by_name:
            gene_data = self.genes_by_name[name]
        else:
            gene_data = GeneData()
            gene_data.name = name
            self.genes.append(gene_data)
            self.genes_by_name[name] = gene_data
        return gene_data

    def value(self, gene_name, person):
        value = "NA"
        if not gene_name in self.genes_by_name:
            return value

        gene_data = self.genes_by_name[gene_name]
        person_id = person.id

        if person_id in self.person_id_to_index:
            index = self.person_id_to_index[person_id]
            if index >= len(gene_data.data):
                print str(index) + " " + str(len(gene_data.data)) + " " + gene_data.name
            value = gene_data.data[index]

        return value

    def dumpCSVWithName(self,file_name):
        with open(file_name, "w+") as file:
            gene_names = []
            for gene_data in self.genes:
                gene_names.append(gene_data.name)
            header = ",".join(gene_names)+"\n"
            file.write(header)

            for i,person in enumerate(self.people.people):
                row = []
                for gene_data in self.genes:
                    row.append(gene_data.data[i])
                line = ",".join(row)+"\n"
                file.write(line)

    @classmethod
    def matchingSets(cls,set1,set2):
        matching1 = GeneDataSets()
        matching1.name = "matching_"+set1.name
        matching2 = GeneDataSets()
        matching2.name = "matching_"+set2.name
        people_intersection = People.peopleIntersection(set1.people, set2.people)
        matching1.setUpPeople(people_intersection)
        matching2.setUpPeople(people_intersection)
        for gene1 in set1.genes:
            name = gene1.name
            if name in set2.genes_by_name:
                mg1 = matching1.geneDataWithName(name)
                mg2 = matching2.geneDataWithName(name)
                for person in people_intersection.people:
                    v1 = set1.value(name,person)
                    mg1.data.append(v1)

                    v2 = set2.value(name,person)
                    mg2.data.append(v2)
        return matching1, matching2






