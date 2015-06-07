rm -rf temp
mkdir temp

python predict_gene_expression.py --dosages data/dosagefiles/ --weights data/dbs/Adipose-Subcutaneous_0.5.db --id_col raid --out temp/wb_results