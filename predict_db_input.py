__author__ = 'Alvaro Barbeira'

import csv
from person import Person

class SFCF:
    """samples.txt file csv format"""
    ID = 0

def loadFromPDBRow(self,row):
    self.id = row[SFCF.ID]
Person.loadFromPDBRow = loadFromPDBRow

#
from person import People
def loadPeopleFromPDBSampleFile(cls,sample_file_name):
    people = People()
    with open(sample_file_name, 'rb') as samples:
        reader = csv.reader(samples, delimiter='\t', quotechar='"')
        for row in reader:
            person = Person()
            person.loadFromPDBRow(row)
            people.addPerson(person,reader.line_num)
    return people
setattr(People, 'loadPeopleFromPDBSampleFile', classmethod(loadPeopleFromPDBSampleFile))

#
from gene import GeneData
def appendFromPDBRow(self,row):
    self.data.append(row[self.column])
GeneData.appendFromPDBRow = appendFromPDBRow

#
from gene import GeneSets
def loadDataFromPDBRow(self, row):
    for gene, gene_item in self.genes_by_name.iteritems():
        gene_item.appendFromPDBRow(row)
GeneSets.loadDataFromPDBRow = loadDataFromPDBRow

def LoadGeneSetsFromPDBFile(cls, people, data_file_name):
    gene_sets = GeneSets()
    with open(data_file_name, 'rb') as file:
        reader = csv.reader(file, delimiter="\t", quotechar='"')
        for row in reader:
            if reader.line_num == 1:
                for col,gene in enumerate(row):
                    gene_item = GeneData(gene,col)
                    gene_sets.genes.append(gene_item)
                    gene_sets.genes_by_name[gene] = gene_item
            else:
                person_row_number = reader.line_num-1
                gene_sets.loadDataFromPDBRow(row)
    return gene_sets
setattr(GeneSets, 'LoadGeneSetsFromPDBFile', classmethod(LoadGeneSetsFromPDBFile))