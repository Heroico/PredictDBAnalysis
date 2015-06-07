__author__ = 'Alvaro Barbeira'

import csv

class GFTF:
    """"Geuvadis file table format"""
    TARGET_ID=0
    GENE_SYMBOL=1
    CHR=2
    COORD=3

#
from person import Person
from person import People
def loadPeopleFromGEUVADISHeader(cls,header):
    people = People()
    for i,text in enumerate(header):
        if i > GFTF.COORD:
            person = Person()
            person.id = text
            people.people.append(person)
    return people
setattr(People,'loadPeopleFromGEUVADISHeader',classmethod(loadPeopleFromGEUVADISHeader))

#
from gene import GeneData
def loadFromGEUVADISRow(cls,row,gene_code_set):
    pass
setattr(GeneData, 'loadFromGEUVADISRow', classmethod(loadFromGEUVADISRow))

from gene import GeneDataSets
def LoadGEUVADISFile(gencodes, data_file_name):
    gene_sets = GeneDataSets()
    people = None
    with open(data_file_name, 'rb') as file:
        reader = csv.reader(file, delimiter="\t", quotechar='"')
        for row in reader:
            if reader.line_num == 1:
                people = People.loadPeopleFromGEUVADISHeader(row)
            else:
                gene_data = GeneData.loadFromGEUVADISRow(row, gencodes)
                #gene_sets.genes.append(gene_data)
                #gene_sets.genes_by_name[gene_data.name] = gene_data
    return gene_sets, people