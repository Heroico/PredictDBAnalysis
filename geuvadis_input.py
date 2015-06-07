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
            people.addPerson(person)
    return people
setattr(People,'loadPeopleFromGEUVADISHeader',classmethod(loadPeopleFromGEUVADISHeader))

#
from gene import GeneData
def loadFromGEUVADISRow(cls,row,gencode_set):
    missing = None
    gene_data = GeneData()
    ensemble_version = row[GFTF.TARGET_ID]
    ensemble = ensemble_version.split(".")[0]
    if not ensemble in gencode_set.gencodes_by_ensemble_id:
        missing = 'Need gencode data for '+ensemble_version
    else:
        gencode = gencode_set.gencodes_by_ensemble_id[ensemble]
        gene_data.name = gencode.name
        for i,value in enumerate(row):
            if i > GFTF.COORD:
                gene_data.data.append(value)
    return gene_data, missing

setattr(GeneData, 'loadFromGEUVADISRow', classmethod(loadFromGEUVADISRow))

from gene import GeneDataSets
def LoadGEUVADISFile(gencodes, data_file_name):
    gene_sets = GeneDataSets()
    missing_gencodes =  []
    with open(data_file_name, 'rb') as file:
        reader = csv.reader(file, delimiter="\t", quotechar='"')
        for row in reader:
            if reader.line_num == 1:
                people = People.loadPeopleFromGEUVADISHeader(row)
                gene_sets.setUpPeople(people)
            else:
                gene_data, missing = GeneData.loadFromGEUVADISRow(row, gencodes)
                if missing is not None:
                    missing_gencodes.append(missing)
                    continue

                gene_sets.genes.append(gene_data)
                gene_sets.genes_by_name[gene_data.name] = gene_data
    return gene_sets, missing_gencodes