#!/bin/bash
# Guion del auditor: ejecuta los notebooks vigentes con nbconvert en la copia, en orden del pipeline
set -u
cd "$1"
export PATH="$2/bin:$PATH"
for nb in 05_pca 05c_anexo_no_diferenciar 06_epca 06c_aede_grilla 07c_hfc_clases 09a_datacion_pca 09b_walkforward_pca 07b_nulo_estructura; do
  inicio=$(date +%s)
  jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 --ExecutePreprocessor.timeout=-1 notebooks/${nb}.ipynb > ../log_nb_${nb}.txt 2>&1
  echo "$nb exit $? $(( $(date +%s)-inicio ))s" >> ../log_nb_estado.txt
done
