#!/bin/bash
# Guion del auditor: ejecuta el nulo de estructura en R y renderiza el Rmd final en las dos versiones
set -u
cd "$1"
inicio=$(date +%s)
Rscript R/07b_nulo_estructura.R > ../log_R_nulo.txt 2>&1; echo "nulo exit $? $(( $(date +%s)-inicio ))s" >> ../log_R_estado.txt
inicio=$(date +%s)
Rscript -e "rmarkdown::render('R/ciclo_financiero_final.Rmd')" > ../log_R_render.txt 2>&1; echo "render FALSE exit $? $(( $(date +%s)-inicio ))s" >> ../log_R_estado.txt
cp R/ciclo_financiero_final.html ../ciclo_final_FALSE.html
inicio=$(date +%s)
Rscript -e "rmarkdown::render('R/ciclo_financiero_final.Rmd', params = list(version_asesor = TRUE), output_file = 'ciclo_final_asesor.html')" > ../log_R_render_asesor.txt 2>&1; echo "render TRUE exit $? $(( $(date +%s)-inicio ))s" >> ../log_R_estado.txt
