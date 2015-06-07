__author__ = 'heroico'

import csv

class SFCF:
    "samples.txt file csv format"
    ID = 0

#
class Person:
    def __init__(self):
        pass

    def loadFromRow(self,row):
        self.id = row[0]
#
class People:
    def __init__(self):
        self.people = []
        self.people_by_row = {}

    def addPerson(self,person,line_num):
        self.people.append(person)
        self.people_by_row[line_num] = person

    @classmethod
    def loadPeopleFromFile(cls,sample_file_name):
        people = People()
        with open(sample_file_name, 'rb') as samples:
            reader = csv.reader(samples, delimiter='\t', quotechar='"')
            for row in reader:
                person = Person()
                person.loadFromRow(row)
                people.addPerson(person,reader.line_num)
        return people

#
class GeneData:
    def __init__(self,name,column):
        self.data = []
        self.name = name
        self.column = column

    def appendFromRow(self,row):
        self.data.append(row[self.column])
#
class GeneSets:
    def __init__(self):
        self.genes = []
        self.genes_by_name = {}

    def loadDataFromRow(self, row):
        for gene, gene_item in self.genes_by_name.iteritems():
            gene_item.appendFromRow(row)

    @classmethod
    def LoadGeneSets(cls, people, data_file_name):
        gene_sets = GeneSets()
        with open(data_file_name, 'rb') as file:
            reader = csv.reader(file, delimiter="\t", quotechar='"')
            for row in reader:
                if reader.line_num == 1:
                    #print sorted(row)
                    for col,gene in enumerate(row):
                        gene_item = GeneData(gene,col)
                        gene_sets.genes.append(gene_item)
                        gene_sets.genes_by_name[gene] = gene_item
                else:
                    person_row_number = reader.line_num-1
                    gene_sets.loadDataFromRow(row)

        return gene_sets

