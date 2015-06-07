__author__ = 'Alvaro Barbeira'

class GeneData:
    """A list of values for a Gene"""
    def __init__(self,name,column):
        self.data = []
        self.name = name
        self.column = column
#
class GeneDataSets:
    """Sets of -gene data-"""
    def __init__(self):
        self.genes = []
        self.genes_by_name = {}
