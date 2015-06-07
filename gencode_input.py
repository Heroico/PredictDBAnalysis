__author__ = 'heroico'


import csv

# look at gencode http://www.gencodegenes.org/data_format.html
class GFTF:
    """gencode file table format"""
    CHROMOSOME = 0
    FEATURE_TYPE = 1
    N_START_LOCATION = 2
    N_END_LOCATION = 3
    ENS_ID = 4
    GENE_NAME = 5
    GENE_TYPE = 6

KEY_ENSEMBLE_ID = "ensemble"
KEY_GENE_NAME = "name"

class GeneCode:
    """genecode information"""
    def __init__(self,row):
        self.ensemble_version = row[GFTF.ENS_ID]
        self.ensemble = self.ensemble_version.split('.')[0]
        self.version = self.ensemble_version.split('.')[1]
        self.name = row[GFTF.GENE_NAME]
        pass

class GeneCodeSet:
    """Collection of gencode data sets"""
    def __init__(self):
        self.genecodes = []
        self.genecodes_by_ensemble_id = {}

    def ReadGeneCodeInput(file_name='data/gencode.v12.V1.summary.protein'):
        genecodes = GeneCodeSet()
        with open(file_name, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
            for row in reader:
                genecode = GeneCode(row)
                genecodes.genecodes.append(genecode)

                if not genecode.ensemble in genecodes.genecodes_by_ensemble_id:
                    genecodes.genecodes_by_ensemble_id[genecode.ensemble] = genecode
                else:
                    raise Exception('Duplicate ensemble id, check'+genecode.ensemble)
        return genecodes