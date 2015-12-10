__author__ = 'Alvaro Barbeira'

class GeneData:
    """A list of values for a Gene"""
    def __init__(self,name=None, ensemble_id_version=None, column=None):
        self.data = []
        self.name = name
        self.ensemble_id_version = ensemble_id_version
        self.column = column

from person import Person
from person import People
#
class GeneDataSets:
    """Sets of -gene data-"""
    def __init__(self):
        self.genes = []
        self.genes_by_name = {}
        self.genes_by_ensemble_id_version = {}

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

    def geneDataWithEnsembleIdVersion(self, ensemble_id_version):
        gene_data = None
        if ensemble_id_version in self.genes_by_ensemble_id_version:
            gene_data = self.genes_by_ensemble_id_version[ensemble_id_version]
        else:
            gene_data = GeneData()
            gene_data.ensemble_id_version = ensemble_id_version
            self.genes.append(gene_data)
            self.genes_by_ensemble_id_version[ensemble_id_version] = gene_data
        return gene_data

    def value(self, name, ensemble_id_version, person):
        value = "NA"
        if name:
            if not name in self.genes_by_name:
                return value
            gene_data = self.genes_by_name[name]
        elif ensemble_id_version:
            if not ensemble_id_version in self.genes_by_ensemble_id_version:
                return value
            gene_data = self.genes_by_ensemble_id_version[ensemble_id_version]
        else:
            raise RuntimeError("Couldnt come up with value for gene")
        person_id = person.id

        if person_id in self.person_id_to_index:
            index = self.person_id_to_index[person_id]
            if index >= len(gene_data.data):
                # tag = gene_data.name if gene_data.name else gene_data.ensemble_id_version
                # print "Got people beyond " + str(index) + " " + str(len(gene_data.data)) + " " + tag
                value = "NA"
            else:
                value = gene_data.data[index]

        return value

    def dumpCSVWithName(self,file_name):
        with open(file_name, "w+") as file:
            tags = [x.name if x.name else x.ensemble_id_version for x in self.genes]
            header = ",".join(tags)+"\n"
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
            ensemble_id_version = gene1.ensemble_id_version
            if name and name in set2.genes_by_name:
                mg1 = matching1.geneDataWithName(name)
                mg2 = matching2.geneDataWithName(name)
                for person in people_intersection.people:
                    v1 = set1.value(name, None, person)
                    mg1.data.append(v1)

                    v2 = set2.value(name, None, person)
                    mg2.data.append(v2)
            elif ensemble_id_version and ensemble_id_version in set2.genes_by_ensemble_id_version:
                mg1 = matching1.geneDataWithEnsembleIdVersion(ensemble_id_version)
                mg2 = matching2.geneDataWithEnsembleIdVersion(ensemble_id_version)
                for person in people_intersection.people:
                    v1 = set1.value(None, ensemble_id_version, person)
                    mg1.data.append(v1)

                    v2 = set2.value(None, ensemble_id_version, person)
                    mg2.data.append(v2)

        return matching1, matching2






