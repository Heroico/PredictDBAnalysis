__author__ = 'heroico'

import json
import os
from subprocess import call

from person import People
from gene import GeneDataSets
import predict_db_input
import geuvadis_input
import gencode_input

class Process:
    def __init__(self, json_file):
        with open(json_file) as data_file:
            json_data = json.load(data_file)

            input = json_data["input"]
            data = input["data"]

            dbs = data["dbs"]
            self.dbs_path = dbs["path"]
            self.dbs_ignore = dbs["ignore"]

            dosages = data["dosages"]
            self.dosages_path = dosages["path"]

            run = json_data["run"]
            self.working_folder = run["working_folder"]

    def run(self):
        """High level driver"""
        self.processPredicted()

    def processPredicted(self):
        contents = self.filteredContents(self.dbs_path, self.dbs_ignore)
        file_names = [x.split(".db")[0] for x in contents]
        for file_name in file_names:
            output_file_name = self.buildPredictDBOutputFileName(file_name)
            if os.path.isfile(output_file_name):
                #print "predict db output already exists " + output_file_name
                continue
            command = self.buildPredictDBCommand(file_name)
            print command
            call([command], shell=True)

    def filteredContents(self,path,patterns =[]):
        contents = os.listdir(path)
        filtered_contents = []
        for file in contents:
            is_excluded = False
            for pattern in patterns:
                if pattern in file:
                    is_excluded = True
                    break
            if not is_excluded:
                filtered_contents.append(file)
        return filtered_contents

    def buildPredictDBOutputFileName(self,file_name):
        output_file_name = self.working_folder + "/" + file_name + ".txt"
        return output_file_name

    def buildPredictDBInputFileName(self,file_name):
        input_file_name = self.dbs_path + "/" + file_name + ".db"
        return input_file_name

    def buildPredictDBCommand(self,file_name):
        command = "python predict_gene_expression.py "
        command += "--dosages " + self.dosages_path + "/ "
        command += "--weights " + self.buildPredictDBInputFileName(file_name) + " "
        command += "--id_col raid "
        command += "--out " + self.buildPredictDBOutputFileName(file_name)
        return command


#
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Compare a series of predicted values against an observeded geuvadis data file.')

    parser.add_argument("--config_file",
                        help="json input file name",
                        default="geuvadis_predict_db_input.json")


    args = parser.parse_args()

    process = Process(args.config_file)

    process.run()