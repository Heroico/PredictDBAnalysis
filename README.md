# Description

This project automates comparison of **predict db** output against **GEUVADIS** phenotypes.

It builds several text files with correlation stats, and plots of **GEUVADIS vs predictdb correlation**.

# TLDR

For the dash and brazen:

Run:

```bash
# attempt to download public data from HAky Im's S3 server
$ bash build_data.sh
```

Download **gencode.v22.annotation.gtf** into:
```
./data/gencode.v22.annotation.gtf
```

then run:

```bash
$ python geuvadis_predict_db_comparison.py
```

# Input

All Genomics data should ideally lie in subfolders within this project (see **.gitignore**).

## JSON config file

Several parameters of the comparison process can be configured at a JSON file. Its default name is:

```bash
geuvadis_predict_db_input.json
```

But you can write your own and use it as:

```bash
python geuvadis_predict_db_comparison.py --config_file my_config.json
```

Most of the settings deal with paths of folders with the data.

One exception is **"keep_all"** (let me call it *data.dbs.keep_all*).
If set to true, will cause all the **predict db** files
to be calculated and stored in case you want them for another calculation, since they take oh so long to finish.
If set to false, will calculate each file on the fly and then erase it. Friendlier to the hard drive, enemier to time and energy.

Another exception is "predict_db_col_rsid" (*data.dbs.predict_db_col_rsid*). Some *predict db's input sqlite files*
may have different column names, this allows to identify the id.


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

