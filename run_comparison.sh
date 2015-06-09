if [[ ! -d "temp" ]] ; then
    mkdir temp

  echo "Running prediction of gene expression"
  for filename in ./data/dbs/*.db; do
    inname=${filename:2}
    name=${inname:9:-3}
    outname="temp/${name}.txt"
    echo "Predicting ${name}"
    python predict_gene_expression.py --dosages data/dosagefiles-hapmap2/ \
                                      --weights "${inname}" \
                                      --id_col raid --out "${outname}"
done
fi
