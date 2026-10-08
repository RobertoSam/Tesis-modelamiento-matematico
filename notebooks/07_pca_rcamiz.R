# =============================================================================
# 07 · PCA con Rcamiz sobre el dataset mensual transformado
# Tesis: Medición del ciclo financiero en Perú mediante técnicas de reducción
#        dimensional y machine learning
# Autor: Roberto Samaniego Salcedo · Asesor: Dr. Sergio Camiz
#
# Calcula el PCA normado con la función pca() del paquete Rcamiz (v0.4.2) y
# guarda valores propios, cargas y scores para compararlos con scikit-learn en
# el notebook 07_verificacion_rcamiz.ipynb.
#
# Requisito: el paquete Rcamiz instalado localmente. No se distribuye en este
# repositorio porque es software del asesor.
#
# Uso (desde la raíz del repositorio):
#   Rscript notebooks/07_pca_rcamiz.R
# =============================================================================

suppressMessages(library(Rcamiz))

# Entrada: dataset mensual transformado (227 meses x 17 variables)
ruta_datos <- "data/processed/dataset_transformado_mensual.csv"
datos <- read.csv(ruta_datos, row.names = 1, check.names = FALSE)
cat("Dimensiones del dataset:", dim(datos), "\n")

# Control: no se trabaja con datos incompletos
stopifnot(!anyNA(datos))
meses <- as.Date(rownames(datos))
calendario <- seq(min(meses), max(meses), by = "month")
if (length(calendario) != nrow(datos)) {
  stop("El calendario mensual tiene huecos: revisar 04b antes de continuar.")
}

# PCA normado (st = TRUE): se piden todas las dimensiones (nd) para obtener
# coordenadas, y r = 10 para no redondear la salida a 3 decimales
res <- pca(datos, st = TRUE, nd = ncol(datos), r = 10)

# Salidas con el prefijo del notebook
dir.create("data/results", showWarnings = FALSE)
write.csv(res$eigenvalues, "data/results/07_rcamiz_valores_propios.csv")
write.csv(res$coord$var,   "data/results/07_rcamiz_cargas.csv")
write.csv(res$coord$ind,   "data/results/07_rcamiz_scores.csv")

cat("Versión de R:", R.version.string, "\n")
cat("Versión de Rcamiz:", as.character(packageVersion("Rcamiz")), "\n")
print(head(res$eigenvalues, 5))
