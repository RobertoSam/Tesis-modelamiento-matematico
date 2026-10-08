# =============================================================================
# Validación de R/camiz_port.R contra el paquete original AedeClahfac 1.2
# Requiere Linux x86_64 con AedeClahfac instalado (su núcleo Fortran solo existe
# para esa plataforma). Uso, desde la raíz del repositorio:
#   Rscript R/validacion_port_camiz.R
# Salida: R/validacion_port_camiz.csv
# =============================================================================
suppressMessages(library(AedeClahfac))
source("R/camiz_port.R")

# Llamada directa a la rutina Fortran original (mismos argumentos que usa clahfac)
fortran_clahfacsub <- function(don, poid = NULL) {
  don <- as.matrix(don); storage.mode(don) <- "double"
  nind <- nrow(don); nvar <- ncol(don); nvarm1 <- nvar - 1; nvar2 <- 2 * nvar - 1; nvar21 <- 2 * nvarm1
  if (is.null(poid)) poid <- rep(1 / nind, nind)
  .Fortran("clahfacsub", units = as.integer(nind), variables = as.integer(nvar),
    nvar2 = as.integer(nvar2), nvar21 = as.integer(nvar21), don = don, poid = as.double(poid),
    datstd = matrix(0, nind, nvar), xmoy = double(nvar), xvar = double(nvar),
    cov = matrix(0, nvar, nvar), cor = matrix(0, nvar, nvar),
    nab = matrix(integer(nvarm1 * 3), nvarm1, 3), ddo = matrix(0, nvarm1, 9),
    albet = matrix(0, nvarm1, 2), poids = matrix(0, nvar2, 2), vt = double(3),
    nclstr = integer(nvar), nsg = integer(nvar), nclass = matrix(integer(nvar2 * nvar), nvar2, nvar),
    ncla = matrix(integer(nvar * nvar), nvar, nvar), narb = matrix(integer(nvar * nvar), nvar, nvar),
    npart = matrix(integer(nvar * nvar), nvar, nvar), noeuind = matrix(integer(nvar * nvar2), nvar, nvar2),
    datout = matrix(0, nind, nvar21), covout = matrix(0, nvar, nvar21), corout = matrix(0, nvar, nvar21),
    covrep = matrix(0, nvar21, nvar21), correp = matrix(0, nvar21, nvar21),
    depsilon = 1e-16, ifois = 1000L, error = 0L, PACKAGE = "AedeClahfac")
}
campos <- c("datstd", "xmoy", "xvar", "cov", "cor", "nab", "ddo", "albet", "poids", "vt", "nclstr",
            "nsg", "nclass", "ncla", "narb", "npart", "noeuind", "datout", "covout", "corout",
            "covrep", "correp")
dif_rel <- function(a, b) {
  a <- as.numeric(unlist(a)); b <- as.numeric(unlist(b))
  if (length(a) != length(b)) return(Inf)
  max(c(0, abs(a - b) / pmax(1, abs(a))), na.rm = TRUE)
}
# Comparación invariante al signo: en los nodos con empate exacto (p. ej. dos variables
# con el mismo peso) la regla de signo de clahfac compara dos sumas iguales y el resultado
# lo decide el redondeo de punto flotante, tanto en el original como en el port. El signo
# de esos factores no tiene interpretación; por eso se comparan valores absolutos.
dif_rel_abs <- function(a, b) dif_rel(abs(as.numeric(unlist(a))), abs(as.numeric(unlist(b))))

dif_lista <- function(a, b, comparar = dif_rel) {
  comunes <- intersect(names(a), names(b))
  comunes <- comunes[!vapply(comunes, function(k) is.language(a[[k]]) || is.function(a[[k]]), logical(1))]
  max(vapply(comunes, function(k) {
    x <- a[[k]]; y <- b[[k]]
    if (is.list(x) && !is.data.frame(x)) return(dif_lista(x, y, comparar))
    if (is.data.frame(x) || is.character(x)) return(if (identical(as.character(unlist(x)), as.character(unlist(y)))) 0 else Inf)
    comparar(x, y)
  }, numeric(1)), 0)
}

datos <- read.csv("data/processed/dataset_transformado_mensual.csv", row.names = 1, check.names = FALSE)
colnames(datos) <- sub("_log_diff$|_diff$", "", colnames(datos))
resultados <- list()
registrar <- function(prueba, casos, dif) {
  resultados[[length(resultados) + 1]] <<- data.frame(prueba = prueba, casos = casos,
    dif_relativa_maxima = signif(dif, 3), coincide = dif < 1e-10)
}

# 1. clahfac completo sobre el dataset de la tesis
invisible(capture.output({ h_orig <- clahfac(datos, out = TRUE); h_port <- clahfac_r(datos, out = TRUE) }))
registrar("clahfac: objeto completo, dataset de la tesis (salvo signo de factores)", 1,
          dif_lista(h_orig, h_port, dif_rel_abs))
# Columnas cuyo signo difiere: deben ser exactamente las de empate en la regla de signo
cols_signo <- which(colSums(h_orig$repvar * h_port$repvar) < 0)
empates <- vapply(cols_signo, function(k) {
  nodo <- (k + 1) %/% 2; v <- h_orig$nclass[nodo, ]; v <- v[v != 0]
  r <- cor(h_orig$data[v], h_orig$repvar[, k])
  abs(sum(r[r < 0]^2) - sum(r[r > 0]^2)) < 1e-10
}, logical(1))
registrar("clahfac: columnas con signo distinto que no son empates", length(cols_signo),
          if (all(empates)) 0 else Inf)

# 2. clahpart en los 8 nodos superiores
d_part <- max(sapply(1:8, function(k) {
  invisible(capture.output({ a <- clahpart(h_orig, noeud = k); b <- clahpart_r(h_port, noeud = k) }))
  dif_lista(a, b, dif_rel_abs)
}))
registrar("clahpart: noeud = 1..8, dataset de la tesis (salvo signo)", 8, d_part)

# 3. aede: ventanas de 36 a 72 meses, pesos uniformes y gaussianos
config <- expand.grid(nw = c(36, 48, 60, 72), nsd = c(0, 3))
d_aede <- max(apply(config, 1, function(cf) {
  a <- aede(serie = as.matrix(datos), ndim = 3, nw = cf[["nw"]], nsd = cf[["nsd"]], maxcl = 10)
  b <- aede_r(serie = as.matrix(datos), ndim = 3, nw = cf[["nw"]], nsd = cf[["nsd"]], maxcl = 10)
  dif_lista(a, b)
}))
registrar("aede: 4 ventanas x 2 esquemas de pesos, dataset de la tesis", nrow(config), d_aede)

# 4. clahfacsub: 22 salidas en datos simulados (incluye pesos, que el binario ignora)
set.seed(2026)
d_sim <- replicate(200, {
  n <- sample(20:200, 1); p <- sample(2:25, 1)
  X <- matrix(rnorm(n * p), n) %*% matrix(rnorm(p * p, sd = runif(1, 0.1, 1)), p)
  if (runif(1) < 0.15) X[, p] <- X[, 1]                  # columnas duplicadas: empates
  pw <- if (runif(1) < 0.3) runif(n) else NULL
  f <- fortran_clahfacsub(X, pw); r <- clahfacsub_r(X, pw)
  max(vapply(campos, function(k) dif_rel(f[[k]], r[[k]]), numeric(1)))
})
registrar("clahfacsub: 22 salidas, datos simulados", length(d_sim), max(d_sim))

# 5. fishersub: partición de Fisher en series simuladas
d_fisher <- replicate(300, {
  y <- cumsum(rnorm(sample(15:200, 1))); k <- sample(2:12, 1)
  f <- .Fortran("fishersub", dat = cbind(seq_along(y), y), nbind = length(y), nvar = 2L, npos = 2L,
                iv = 1L, maxcl = as.integer(k), criter = double(k), mod1out = matrix(0, k + 1, k + 1),
                PACKAGE = "AedeClahfac")
  r <- fisher_r(y, k)
  max(dif_rel(f$criter, r$criter), dif_rel(f$mod1out, r$mod1out))
})
registrar("fishersub: criterio y límites, series simuladas", length(d_fisher), max(d_fisher))

tabla <- do.call(rbind, resultados)
tabla$plataforma <- paste(R.version$platform, R.version.string)
write.csv(tabla, "R/validacion_port_camiz.csv", row.names = FALSE)
print(tabla[, 1:4], row.names = FALSE)
