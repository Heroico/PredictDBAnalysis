#! /bin/bash

if [[ ! -d "data" ]] ; then
    mkdir data
fi

cd data

rm -rf pheno
mkdir pheno
cd pheno
aws s3 cp s3://imlab-open/Data/1000Genomes/Transcriptome/GEUVADIS/dosagefiles-hapmap2/GD462.GeneQuantRPKM.50FN.samplename.resk10.txt.gz .
cd ..

rm -rf dosages
mkdir dosages
cd dosages
aws s3 cp s3://imlab-open/Data/1000Genomes/Transcriptome/GEUVADIS/dosagefiles/ . --recursive
cd ..

rm -rf dbs
mkdir dbs
cd dbs
aws s3 cp s3://imlab-open/Data/PredictDB/generated_dbs/ . --recursive --exclude "*" --include "*0.5.db"