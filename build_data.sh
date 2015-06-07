rm -rf data/dosages
cd data
mkdir dosages
aws s3 cp s3://imlab-open/Data/1000Genomes/Transcriptome/GEUVADIS/dosagefiles/ . --recursive