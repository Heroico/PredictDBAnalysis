# Description

This project automates comparison of **predict db** output against **GEUVADIS** phenotypes.

It builds several text files with correlation stats, and plots of **GEUVADIS vs predictdb correlation**.

# TLDR

For the dash and brazen, if you have **AWS** cli tools: 

Run:

```bash
# attempt to download public data from HAky Im's S3 server
# requires aws
$ bash build_data.sh
```

Download **gencode.v22.annotation.gtf** into:
```
# github markdown doesn't get links to ftps:
# Download it from here ftp://ftp.sanger.ac.uk/pub/gencode/Gencode_human/release_22/gencode.v22.annotation.gtf.gz
# to this place:
./data/gencode.v22.annotation.gtf
```

then run:

```bash
$ python geuvadis_predict_db_comparison.py
```

# Input & Operation

All Genomics data should ideally lie in subfolders within this project (see **.gitignore**).

**geuvadis_predict_db_comparison.py** is the main utility in this repository. 
It takes a set of tissue model db's as described in PrediXcan and Hae Kyung Im's publications,
it then figures out predicted gene expression matrices for those models,
and finally it outputs some charts and statistics.

It has two ways of accepting input: via command line parameters, or a configuration file.
If you provide a configuration file, all other options will be ignored.

## Command line parameters

When executing the script, you have the following argument options:
* --config_file: If you provide this, options willbe parse from a JSON file. See below.
* --dosages_folder: Folder with indiviudal sample dosages in "PrediXcan format". See files from **build_data.sh** For an example. 
* --input_db: What sqlite model file to analise.
* --pheno_file: Observed expression. Defaults to **GD462.GeneQuantRPKM.50FN.samplename.resk10.txt** from GEUVADIS.
* --gencode_file: Gencode annotation data, defaults to **gencode.v22.annotation.gtf**
* --working_folder: folder where intermediate stats will be dumped.
* --results_folder: folder where result plots will be generated.
* --predict_db_rsid: Name of column with RSID name in model database.
* --keep_predictions: keep Gene Expression Predictions files after we are done with them. They are big-ish files.
* --eager_clean_up: delete **working_folder** and **results_folder** before analysis.


## JSON config file

Several parameters of the comparison process can be configured at a JSON file.
If a config file is provided, the analysis will be carried in "batch mode" and process sets of dbs.
Its default name is:

```bash
geuvadis_predict_db_input.json
```

But you can write your own and use it as:

```bash
python geuvadis_predict_db_comparison.py --config_file my_config.json
```

Most of the settings deal with paths of folders with the data, and mirror command line parameters. 
Hierarchy of objects and key is fixed.

See a sample below:

```bash
{
  "input": {
    "data": {
      #root data folder
      "root": "data",
      #db parameters
      "dbs": {
        #keep prediction files
        "keep_all": false,
        #relative path from script to dbs
        "path": "data/dbs",
        #files to ignore within the folder
        "ignore": [
          ".DS_Store",
          ".py"
        ]
      },
      #dosage files
      "dosages": {
        "path": "data/dosagefiles-hapmap2"
      }
    },
    #phenotype file
    "pheno": "data/pheno/GD462.GeneQuantRPKM.50FN.samplename.resk10.txt",
    #gencode file
    "gencode": "data/gencode.v22.annotation.gtf",
    # delete contents from working folder and results.
    "eager_clean_up": false
  },
  "run": {
    #Folder for support stats
    "working_folder": "temp"
  },
  "results": {
    "comparison": {
      # Where the images will be saved
      "output_path": "test_images"
    }
  }
}
```

## Data folder example

called ./data by default.
```bash
/data/dosagefiles-hapmap2           #dosage files for predixcan
/data/pheno                         #GEUVADIS observed data
/data/dbs                           #sqlite databases with predixcan weights
/data/gencode.v22.annotation.gtf    #gencode file with gene info
```

# PrediXcan notes

`predict_gene_expression.py` was downloaded from [here](https://github.com/hakyimlab/PrediXcan/tree/master/Software).
It had to be modified because the used databases had a different name for sqlite columns.
Where the original script expected a column "rsid", used databases had "raid" columns
It also supports nested folder paths output.

