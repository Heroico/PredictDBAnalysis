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

            self.gencode_path = input["gencode"]
            self.pheno_path = input["pheno"]

            data = input["data"]

            dbs = data["dbs"]
            self.dbs_path = dbs["path"]
            self.dbs_ignore = dbs["ignore"]
            self.keep_all_dbs = dbs["keep_all"]

            dosages = data["dosages"]
            self.dosages_path = dosages["path"]

            run = json_data["run"]
            self.working_folder = run["working_folder"]

    def run(self):
        """High level driver"""
        self.loadObservedData()
        self.processPredicted()

    def loadObservedData(self):
        print "Loading gencode"
        self.gencodes = gencode_input.GenCodeSet.LoadGTF(self.gencode_path)
        print "Loading observed data"
        self.observed_data = None
        self.missing_gencodes = None
        self.observed_data,  self.missing_gencodes = geuvadis_input.LoadGEUVADISFile(self.gencodes, self.pheno_path, "observed_geuvadis_genquant")

    def processPredicted(self):
        if self.keep_all_dbs:
            self.predictDBSIfNecessary()
        self.predict_db_people = People.loadPeopleFromPDBSampleFile(self.dosages_path+"/samples.txt")
        self.comparePredictedToObserved()

    def predictDBSIfNecessary(self):
        contents = self.filteredContents(self.dbs_path, self.dbs_ignore)
        file_names = [x.split(".db")[0] for x in contents]
        for file_name in file_names:
            self.predictDBForFileIfNecessary(file_name)

    def predictDBForFileIfNecessary(self,file_name):
        output_file_name = self.buildPredictDBOutputFileName(file_name)
        if os.path.isfile(output_file_name):
            #print "predict db output already exists " + output_file_name
            return
        self.predictDBForFile(file_name)

    def predictDBForFile(self, file_name):
        command = self.buildPredictDBCommand(file_name)
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

    def comparePredictedToObserved(self):
        contents = self.filteredContents(self.dbs_path, self.dbs_ignore)
        file_names = [x.split(".db")[0] for x in contents]

        output = []
        for file_name in file_names:
            output_file_name = self.buildQQR2Comparison(file_name)
            output.append(output_file_name)

        file_list_name = self.working_folder + "/" + "comparison_file_list.txt"
        with open(file_list_name, "w+") as file:
            for output_file_name in output:
                line = output_file_name+"\n"
                file.write(line)

    def buildQQR2Comparison(self,file_name):
        out = self.buildQQR2ComparisonOutputFileName(file_name)
        print "Starting "+out
        if os.path.isfile(out):
            print "qqr2 already done for "+file_name
            return out
        matching_predict_db_name, matching_observed_name = self.buildComparisonFiles(file_name)
        self.qqR2Compare(file_name, matching_predict_db_name, matching_observed_name)
        return out

    def qqR2Compare(self,file_name, matching_predict_db_name, matching_observed_name):
        print "Calculating qqR2"
        out = self.buildQQR2ComparisonOutputFileName(file_name)
        command = "Rscript comparison_qqR2.R "
        command += "--file1 " + matching_predict_db_name + " "
        command += "--file2 " + matching_observed_name + " "
        command += "--name "+file_name+" "
        command += "--out "+ out
        call([command], shell=True)
        os.remove(matching_predict_db_name)
        os.remove(matching_observed_name)

    def buildComparisonFiles(self,file_name):
        print "Comparing files for"+file_name
        predict_db_file = self.buildPredictDBOutputFileName(file_name)
        predict_db_data = GeneDataSets.LoadGeneSetsFromPDBFile(self.predict_db_people, predict_db_file, "predict_db_"+file_name)
        matching_predict_db, matching_observed = GeneDataSets.matchingSets(predict_db_data, self.observed_data)

        matching_predict_db_name = self.buildComparisonOutputFileName(matching_predict_db.name)
        matching_predict_db.dumpCSVWithName(matching_predict_db_name)

        matching_observed_name = self.buildComparisonOutputFileName(matching_observed.name)
        matching_observed.dumpCSVWithName(matching_observed_name)
        return matching_predict_db_name, matching_observed_name

    def buildComparisonOutputFileName(self,file_name):
        name = self.working_folder + "/" + file_name + ".csv"
        return name

    def buildQQR2ComparisonOutputFileName(self,file_name):
        out = self.buildComparisonOutputFileName(file_name+"_correlation")
        return out
#

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