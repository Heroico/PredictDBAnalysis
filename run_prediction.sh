

echo "Running prediction of gene expression"
for filename in ./data/dbs/*.db; do
  inname=${filename:2}
  name=${inname:9:-3}
  outname="temp/${name}.txt"
  if [[ -f ${outname} ]]; then
    echo "Skipping ${name}"
    continue
  fi
  echo "Predicting ${name}"
  python predict_gene_expression.py --dosages data/dosagefiles-hapmap2/ \
                                    --weights "${inname}" \
                                    --out "${outname}"
#                                    --id_col raid \
done
#fi
