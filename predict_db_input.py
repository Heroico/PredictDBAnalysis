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
            people.addPerson(person)
    return people
setattr(People, 'loadPeopleFromPDBSampleFile', classmethod(loadPeopleFromPDBSampleFile))

#
from gene import GeneData
def appendFromPDBRow(self,row):
    self.data.append(row[self.column])
GeneData.appendFromPDBRow = appendFromPDBRow

#
from gene import GeneDataSets
def appendDataFromPDBRow(self, row, use_ens):
    if use_ens:
        for gene, gene_item in self.genes_by_ensemble_id_version.iteritems():
            gene_item.appendFromPDBRow(row)
    else:
        for gene, gene_item in self.genes_by_name.iteritems():
            gene_item.appendFromPDBRow(row)

GeneDataSets.appendDataFromPDBRow = appendDataFromPDBRow

def LoadGeneSetsFromPDBFile(cls, people, data_file_name, set_name=None):
    gene_sets = GeneDataSets()
    gene_sets.name = set_name
    gene_sets.setUpPeople(people)
    with open(data_file_name, 'rb') as file:
        reader = csv.reader(file, delimiter="\t", quotechar='"')
        for row in reader:
            if reader.line_num == 1:
                h = [g for g in row if "ENS" in g and "." in g]
                use_ens = len(h) > 10 # dumb heuristic
                if use_ens:
                    print "Found genes by ensemble_id_version for "+data_file_name
                else:
                    print "Found genes by name for " + data_file_name

                for col,gene in enumerate(row):
                    g = gene if not use_ens else None
                    e = gene if use_ens else None
                    gene_item = GeneData(g, e, col)
                    gene_sets.genes.append(gene_item)
                    if use_ens:
                        gene_sets.genes_by_ensemble_id_version[gene] = gene_item
                    else:
                        gene_sets.genes_by_name[gene] = gene_item
            else:
                gene_sets.appendDataFromPDBRow(row, use_ens)

    return gene_sets
setattr(GeneDataSets, 'LoadGeneSetsFromPDBFile', classmethod(LoadGeneSetsFromPDBFile))
