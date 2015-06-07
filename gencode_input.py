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

class GenCode:
    """-gencode- information. Yes, without 'e' in 'gene'"""
    def __init__(self,row):
        self.ensemble_version = row[GFTF.ENS_ID]
        self.ensemble = self.ensemble_version.split('.')[0]
        self.version = self.ensemble_version.split('.')[1]
        self.name = row[GFTF.GENE_NAME]
        pass

class GenCodeSet:
    """Collection of gencode data sets"""
    def __init__(self):
        self.gencodes = []
        self.gencodes_by_ensemble_id = {}

    @classmethod
    def LoadGeneCodeInput(cls, file_name):
        gencodes = GenCodeSet()
        with open(file_name, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
            for row in reader:
                gencode = GenCode(row)
                gencodes.gencodes.append(gencode)

                if not gencode.ensemble in gencodes.gencodes_by_ensemble_id:
                    gencodes.gencodes_by_ensemble_id[gencode.ensemble] = gencode
                else:
                    raise Exception('Duplicate ensemble id, check'+gencode.ensemble)
        return gencodes