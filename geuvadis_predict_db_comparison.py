__author__ = 'heroico'

import json
import os
from subprocess import call

from person import People
from gene import GeneDataSets
import predict_db_input
import geuvadis_input
import gencode_input
import project_utils

#
def split_list(alist, wanted_parts=1):
    """Split an array into -wanted_parts- subarrays"""
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
             for i in range(wanted_parts) ]

#
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
            self.predict_db_rsid = dbs["predict_db_col_rsid"] if "predict_db_col_rsid" in dbs else None

            dosages = data["dosages"]
            self.dosages_path = dosages["path"]

            run = json_data["run"]
            self.working_folder = run["working_folder"]

            results = json_data["results"]
            comparison = results["comparison"]
            self.comparison_plot_path = comparison["output_path"]

    def run(self):
        """High level driver"""
        self.loadObservedData()
        output_files = self.processPredicted()
        self.plotComparison()
        self.plotComparisonMosaic(output_files)

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
        file_list_name = self.comparePredictedToObserved()
        return file_list_name

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
        call(command.split(" "))

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
        if self.predict_db_rsid is not None:
            command += "--id_col "+self.predict_db_rsid + " "
        command += "--out " + self.buildPredictDBOutputFileName(file_name)
        return command

    def comparePredictedToObserved(self):
        contents = self.filteredContents(self.dbs_path, self.dbs_ignore)
        file_names = [x.split(".db")[0] for x in contents]

        output_files = []
        for file_name in file_names:
            output_file_name = self.buildQQR2Comparison(file_name)
            output_files.append(output_file_name)

        file_list_name = self.buildComparisonFileListName()
        with open(file_list_name, "w+") as file:
            for output_file_name in output_files:
                line = output_file_name+"\n"
                file.write(line)
        return output_files

    def buildQQR2Comparison(self,file_name):
        out = self.buildQQR2ComparisonOutputFileName(file_name)
        print "Starting "+out
        if os.path.isfile(out):
            print "qqr2 already done for "+file_name
            return out
        else:
            print "qqr2 needs doing for "+file_name+ " at "+out
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
        command = command.encode("ascii","ignore")
        command = command.replace("\\(", "(")
        command = command.replace("\\)", ")")
        call(command.split(" "))
        os.remove(matching_predict_db_name)
        os.remove(matching_observed_name)

    def buildComparisonFiles(self,file_name):
        print "Comparing files for"+file_name
        predict_db_file = self.buildPredictDBOutputFileName(file_name)

        if not os.path.isfile(predict_db_file):
            print "missing predict db output, calculating for "+file_name
            self.predictDBForFile(file_name)
        predict_db_data = GeneDataSets.LoadGeneSetsFromPDBFile(self.predict_db_people, predict_db_file, "predict_db_"+file_name)
        if not self.keep_all_dbs:
            os.remove(predict_db_file)

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

    def buildComparisonFileListName(self):
        file_list_name = self.working_folder + "/" + "comparison_file_list.txt"
        return file_list_name

    def plotComparison(self):
        print "Plotting..."
        project_utils.ensure_folder_path(self.comparison_plot_path)
        command = "Rscript plot_qqR2_results.R "
        command += "--result_list_file " + self.buildComparisonFileListName() + " "
        command += "--output_prefix " + self.comparison_plot_path
        call(command.split(" "))

    def plotComparisonMosaic(self, output_files):
        if len(output_files) == 0:
            return
        parts =round(len(output_files)/9.0)+1
        splitted = split_list(output_files, int(parts))
        for i,split in enumerate(splitted):
            output = self.comparison_plot_path + "/mosaic"+str(i)+".png"
            command = "Rscript plot_qqR2_mosaic.R --results_files "
            command += " ".join(split) + " "
            command += "--output "+output
            call(command.split(" "))
            print command
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