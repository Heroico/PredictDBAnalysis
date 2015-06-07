

PrediXcan notes
---------------

predict_gene_expression.py was downloaded from [here](https://github.com/hakyimlab/PrediXcan/tree/master/Software)
It had to be modified because the used databases had a differnet name for columns.
Where the original script expected a column "rsid", used databases had "raid" columns

Input:
------

- Data folder
called ./data by default.
``` bash
/data/dosagefiles-hapmap2   #dosage files for predixcan
/data/pheno                 #GEUVADIS observed data
/data/dbs                   #sqlite databases with predixcan weights
/data/gencode
```