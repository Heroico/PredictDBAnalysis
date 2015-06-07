

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
/data/dosagefiles-hapmap2           #dosage files for predixcan
/data/pheno                         #GEUVADIS observed data
/data/dbs                           #sqlite databases with predixcan weights
/data/gencode.v22.annotation.gtf    #gencode file with gene info
```

the script
```
build_data.sh
```
will attempt to pull data from Haky Im's public repository.

So far, only

```
/data/gencode.v22.annotation.gtf
```

needs to be downloaded.
