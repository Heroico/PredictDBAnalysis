#! /bin/bash

FOLDER="data"

if ! [[ -d  "$FOLDER" ]] ; then
    mkdir $FOLDER
fi

mkdir $FOLDER
cd $FOLDER
echo $FOLDER

if ! [[ -f "gencode.v22.annotation.gtf" ]]; then
    wget ftp://ftp.sanger.ac.uk/pub/gencode/Gencode_human/release_22/gencode.v22.annotation.gtf.gz
    gunzip gencode.v22.annotation.gtf.gz
else
    echo "Annotation gencode.v22.annotation.gtf already exists, delete it if you want it downloaded again"
fi

if ! [[ -d "pheno" ]]; then
    mkdir pheno
    cd pheno
    aws s3 cp s3://imlab-open/Data/1000Genomes/Transcriptome/GEUVADIS/E-GEUV-3/GD462.GeneQuantRPKM.50FN.samplename.resk10.txt.gz .
    gunzip GD462.GeneQuantRPKM.50FN.samplename.resk10.txt.gz
    cd ..
else
    echo "Phenotype folder 'pheno' already exists, delete it if you want it downloaded again"
fi

if ! [[ -d "dosagefiles-hapmap2" ]]; then
    mkdir dosagefiles-hapmap2
    cd dosagefiles-hapmap2
    aws s3 cp s3://imlab-open/Data/1000Genomes/Transcriptome/GEUVADIS/dosagefiles-hapmap2/ . --recursive
    cd ..
else
    echo "Dosage folder 'dosagefiles-hapmap2' already exists, delete it if you want it downloaded again"
fi

if ! [[ -d "dbs" ]]; then
    mkdir dbs
    cd dbs
    aws s3 cp s3://imlab-open/Data/PredictDB/generated_dbs/ . --recursive --exclude "*" --include "*0.5.db"
else
    echo "Databases folder 'dbs' already exists, delete it if you want it downloaded again"
fi