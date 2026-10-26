# Nulo de estructura constante para la parte dinámica (iteración 3b, tareas D7 y D10; primera pieza
# de OE11 y de HT1). Guion R aparte del Rmd por su costo de cómputo (unas 960 corridas de aede con
# maxcl = 20, del orden de 10 a 15 minutos), como prevé el plan
# (asesoria/2026-10-21_plan-iteracion-3b.md, riesgo 9). El Rmd lee sus CSV para la tabla de
# paridad (sección 4 del Rmd final) y no repite el cálculo.
#
# Ejecución, desde la raíz del repositorio (versión vigente: niveles, 16 series, data/results/final):
#   Rscript R/07b_nulo_estructura.R
#
# Parámetros (adenda 3b, §3), por variables de entorno, como los notebooks:
#   TESIS_VIA        "niveles" (vigente, D15) o "ambas" (antecedente en dos vías, D2)
#   TESIS_EXCLUIDAS  lista JSON de columnas que se excluyen al leer; por defecto ["Liquidez M2"] (D16)
#   TESIS_CARPETA    salidas de la vía en niveles; la transformada va en TESIS_CARPETA/anexo
#   TESIS_RV         "d17" (por defecto: cargas sin centrar y correlación completa, D17.2) o
#                    "antecedente" (cargas centradas, lectura de la fase 0 descartada en la adenda)
#
# Construcción del nulo (remuestreo por bloques CONJUNTO: los mismos inicios de bloque para las
# series, de modo que se conserva la correlación contemporánea y la dinámica corta, pero se
# dispersa en el tiempo cualquier cambio de estructura):
#   - vía transformada: se remuestrean las filas (227 meses);
#   - vía sin transformar: se remuestrean las filas de los incrementos mensuales (227) y se
#     acumulan desde 0, como la versión «con deriva» de nulo_tendencias (bloque b2s-nulo).
# Inicios de bloque: 200 réplicas por longitud L ∈ {12, 24, 36}, sorteadas con la semilla del
# documento (2026) fijada antes de cada longitud, con la misma función que generar_inicios del Rmd.
# Se escriben en la carpeta de cada vía, R_nulo_estructura_indices_L{12,24,36}.csv (iguales en las
# dos carpetas, porque las dos vías remuestrean 227 filas), para que Python use las mismas réplicas.
#
# Para cada réplica, vía, ancho nw ∈ {24, 36, 48, 60} y pesos (uniformes, gaussianos nsd = 3):
#   1. k* de cada criterio de aede con maxcl = 20 (codo por caída máxima, CH con k y con k - 1);
#   2. perfil del coeficiente RV entre ventanas adyacentes no solapadas (la ventana que empieza en la
#      fila i y la que empieza en i + nw), con los objetos de D17.2: las cargas de aede
#      (correlationlsq, p × 3) SIN centrar (principal) y las matrices de correlación completas p × p
#      con los pesos de aede (.bstatw_ac, sensibilidad). La frontera de cada par es la fila i + nw.
#   3. criterio de OE4 (D17.2) con las réplicas calculadas en R: p5 por posición y proporción de
#      pares observados bajo su p5, frente a la distribución nula de esa proporción (p5 de cada
#      réplica calculado dejándola fuera). Con 20 réplicas es la versión de paridad; la oficial
#      (200 réplicas de L = 24) la calcula Python (07b).
# La paridad completa con Python se exige en las 20 primeras réplicas de cada L (D7 del plan); las
# réplicas 21 a 200 de L = 24 se calculan solo en Python, y así se declara en la tabla de paridad.
# La réplica 0 es la serie observada.

suppressWarnings(Sys.setlocale("LC_CTYPE", "C.UTF-8"))
source("R/camiz_port.R")

library(jsonlite)
SEMILLA <- 2026
B_INDICES <- 200          # réplicas sorteadas por longitud de bloque
B_PARIDAD <- 20           # réplicas que se calculan en R (paridad completa)
LARGOS <- c(12, 24, 36)
NW_GRILLA <- c(24, 36, 48, 60)
PESOS <- c(uniformes = 0, gaussianos_nsd3 = 3)
MAXCL <- 20
args <- commandArgs(trailingOnly = TRUE)
if (length(args)) B_PARIDAD <- as.integer(args[1])     # solo para pruebas rápidas

# ---- Parámetros -------------------------------------------------------------------
VIA <- Sys.getenv("TESIS_VIA", "niveles")
EXCLUIDAS <- if (nzchar(Sys.getenv("TESIS_EXCLUIDAS"))) as.character(fromJSON(Sys.getenv("TESIS_EXCLUIDAS"))) else "Liquidez M2"
CARPETA <- Sys.getenv("TESIS_CARPETA", "data/results/final")
MODO_RV <- Sys.getenv("TESIS_RV", "d17")
stopifnot(VIA %in% c("niveles", "ambas"), MODO_RV %in% c("d17", "antecedente"))
OBJETOS <- if (MODO_RV == "d17") c("cargas_sin_centrar", "correlacion") else "cargas_centradas"
# El antecedente (17 series, dos vías) no se sobrescribe nunca (criterio 17 de la adenda)
stopifnot(!normalizePath(CARPETA, mustWork = FALSE) %in% normalizePath(c("data/results", "data/results/niveles"), mustWork = FALSE))

# ---- Datos: las series del análisis, en el orden de meta_an del Rmd, sin las excluidas -----
columnas <- c("Crédito empresarial", "Crédito consumo", "Crédito hipotecario", "Liquidez M1", "Liquidez M2",
              "Liquidez M3", "Tasa referencia BCRP", "Tasa interbancaria", "Tasa activa TAMN", "Tasa pasiva TIPMN",
              "IPC Lima", "Tipo de cambio", "Índice BVL", "embi_peru", "PBI desestacionalizado", "Demanda interna",
              "Reservas internacionales")
niv <- read.csv("data/processed/dataset_niveles_mensual.csv", check.names = FALSE)
tr <- read.csv("data/processed/dataset_transformado_mensual.csv", check.names = FALSE)
md5 <- unname(tools::md5sum(c("data/processed/dataset_niveles_mensual.csv", "data/processed/dataset_transformado_mensual.csv")))
stopifnot(identical(md5, c("8088c28cf277419388d9562722faa1ad", "8c49f3e55608f2651be3c1dee4236194")))   # D4
stopifnot(all(EXCLUIDAS %in% columnas))
columnas <- setdiff(columnas, EXCLUIDAS)
X <- as.matrix(niv[, columnas])
cols_tr <- setdiff(names(tr), "fecha"); base_tr <- sub("_log_diff$|_diff$", "", cols_tr)
Xt <- as.matrix(tr[, cols_tr[match(columnas, base_tr)]])
for (d in list(niv, tr)) {
  f <- as.Date(d$fecha); cal <- seq(min(f), max(f), by = "month")
  stopifnot(!anyNA(d), length(cal) == nrow(d), all(cal == f))
}
stopifnot(nrow(X) == 228, nrow(Xt) == 227, ncol(X) == 17 - length(EXCLUIDAS), ncol(Xt) == ncol(X), !anyNA(X), !anyNA(Xt))
rownames(X) <- format(as.Date(niv$fecha), "%Y-%m-%d"); rownames(Xt) <- format(as.Date(tr$fecha), "%Y-%m-%d")
p <- ncol(X)
DIRS <- c(niveles = CARPETA, transformadas = file.path(CARPETA, "anexo"))
if (VIA == "niveles") DIRS <- DIRS["niveles"]
for (d in DIRS) dir.create(d, showWarnings = FALSE, recursive = TRUE)

# ---- Funciones (copias literales de las del Rmd: inicios_bloques, indices_desde_inicios,
# ch_variantes, resumir_aede y coef_rv) -------------------------------------------
inicios_bloques <- function(n, largo) sample(seq_len(n - largo + 1), ceiling(n / largo), replace = TRUE)
indices_desde_inicios <- function(inicios, largo, n) head(unlist(lapply(inicios, function(i) i:(i + largo - 1))), n)
generar_inicios <- function(B, n, largo, semilla = SEMILLA) {
  set.seed(semilla)
  t(vapply(seq_len(B), function(b) inicios_bloques(n, largo), integer(ceiling(n / largo))))
}
ch_variantes <- function(sce, n) {
  k <- seq_along(sce); tss <- sce[1]
  ch_k  <- ((tss - sce) / k) / (sce / (n - k))
  ch_k1 <- ((tss - sce) / (k - 1)) / (sce / (n - k))
  ch_k[1] <- NA; ch_k1[1] <- NA
  list(k = unname(ch_k), k1 = unname(ch_k1))
}
resumir_aede <- function(a) {
  part <- a$cutpoints$part
  wss <- part[, 2]; red <- c(-diff(wss) / head(wss, -1), NA)
  caida <- red[1:(length(red) - 2)] - red[2:(length(red) - 1)]
  ch <- ch_variantes(wss, nrow(a$eigenvalues))
  stopifnot(isTRUE(all.equal(ch$k[-1], unname(part[-1, 3]))))
  c(k_codo = which.max(caida) + 1, k_ch = which.max(part[, 3]), k_ch1 = which.max(ch$k1))
}
# centrar = TRUE (por defecto) es el comportamiento de siempre; centrar = FALSE compara las cargas
# sin restar la carga media de cada eje (adenda del 26-oct-2026, §1.2), lectura principal de D17.2
coef_rv <- function(X, Y, centrar = TRUE) {
  X <- as.matrix(X); Y <- as.matrix(Y)
  if (centrar) { X <- scale(X, scale = FALSE); Y <- scale(Y, scale = FALSE) }
  Sx <- tcrossprod(X); Sy <- tcrossprod(Y)
  sum(Sx * Sy) / sqrt(sum(Sx * Sx) * sum(Sy * Sy))
}
CRITERIOS <- c(k_codo = "codo (caída máxima)", k_ch = "Calinski-Harabász k gl (aede)", k_ch1 = "Calinski-Harabász k-1 gl (habitual)")

# Serie nula de una réplica: filas remuestreadas (transformadas) o incrementos remuestreados y
# acumulados desde 0 (niveles)
serie_nula <- function(via, ini, largo) {
  if (via == "transformadas") {
    M <- Xt[indices_desde_inicios(ini, largo, nrow(Xt)), ]; rownames(M) <- rownames(Xt)
  } else {
    D <- diff(X)
    Dn <- D[indices_desde_inicios(ini, largo, nrow(D)), ]
    M <- rbind(0, apply(Dn, 2, cumsum)); rownames(M) <- rownames(X)
  }
  M
}

# RV entre dos matrices de correlación (simétricas): tr(Ra Rb) / sqrt(tr(Ra²) tr(Rb²)) (src/dinamica.py)
rv_correlacion <- function(Ra, Rb) sum(Ra * Rb) / sqrt(sum(Ra * Ra) * sum(Rb * Rb))

# k* y perfil RV de una serie para toda la grilla
medir <- function(M) {
  kst <- list(); rv <- list(); rvr <- list()
  for (nw in NW_GRILLA) for (pz in names(PESOS)) {
    a <- aede_r(serie = M, ndim = 3, nw = nw, nsd = PESOS[[pz]], maxcl = MAXCL)
    k <- resumir_aede(a)
    kst[[length(kst) + 1]] <- data.frame(nw = nw, pesos = pz, criterio = unname(CRITERIOS[names(k)]), k = unname(k),
                                         k_en_tope = unname(k) == MAXCL)
    C <- a$correlationlsq; wn <- dim(C)[1]
    i <- seq_len(wn - nw)
    fv <- format(as.Date(rownames(a$eigenvalues)), "%Y-%m")
    frontera <- format(as.Date(rownames(M)[i + nw]), "%Y-%m")
    if ("correlacion" %in% OBJETOS)
      Rw <- lapply(seq_len(wn), function(j) .bstatw_ac(as.matrix(M[j:(j + nw - 1), ]), a$weights)$correlations)
    for (obj in OBJETOS) {
      r <- switch(obj,
                  cargas_centradas = vapply(i, function(j) coef_rv(C[j, , ], C[j + nw, , ]), numeric(1)),
                  cargas_sin_centrar = vapply(i, function(j) coef_rv(C[j, , ], C[j + nw, , ], centrar = FALSE), numeric(1)),
                  correlacion = vapply(i, function(j) rv_correlacion(Rw[[j]], Rw[[j + nw]]), numeric(1)))
      rv[[length(rv) + 1]] <- data.frame(objeto = obj, nw = nw, pesos = pz, fecha_a = fv[i], fecha_b = fv[i + nw],
                                         frontera = frontera, rv = r)
      rvr[[length(rvr) + 1]] <- data.frame(objeto = obj, nw = nw, pesos = pz, n_pares = length(r), rv_min = min(r),
                                           rv_p05 = unname(quantile(r, 0.05)), rv_p50 = unname(quantile(r, 0.5)), rv_media = mean(r))
    }
  }
  list(kstar = do.call(rbind, kst), rv = do.call(rbind, rv), rv_resumen = do.call(rbind, rvr))
}

# Criterio de OE4 (D17.2): p5 por posición entre réplicas; proporción de pares observados bajo su
# p5; distribución nula de la proporción con el p5 de cada réplica calculado sin ella; p-valor =
# proporción de réplicas con proporción mayor o igual que la observada (src/dinamica.criterio_oe4)
criterio_oe4 <- function(rv_obs, R, alfa = 0.05) {
  p5 <- apply(R, 2, quantile, probs = alfa, names = FALSE)
  bajo <- rv_obs < p5
  props <- vapply(seq_len(nrow(R)), function(b)
    mean(R[b, ] < apply(R[-b, , drop = FALSE], 2, quantile, probs = alfa, names = FALSE)), numeric(1))
  list(p5 = p5, bajo = bajo, prop_obs = mean(bajo), props_nulo = props, p_valor = mean(props >= mean(bajo)))
}

# ---- Índices compartidos ----------------------------------------------------------
inicios <- lapply(setNames(LARGOS, paste0("L", LARGOS)), function(L) generar_inicios(B_INDICES, 227, L))
for (L in LARGOS) {
  ini <- inicios[[paste0("L", L)]]
  d <- data.frame(replica = seq_len(nrow(ini)), ini); names(d)[-1] <- paste0("inicio_", seq_len(ncol(ini)))
  for (dir in DIRS) write.csv(d, file.path(dir, sprintf("R_nulo_estructura_indices_L%d.csv", L)), row.names = FALSE)
}

# ---- Cálculo ----------------------------------------------------------------------
t0 <- Sys.time()
for (via in names(DIRS)) {
  obs <- medir(if (via == "niveles") X else Xt)
  kst <- list(data.frame(L = 0, replica = 0, obs$kstar)); rv <- list(data.frame(replica = 0, obs$rv))
  rvr <- list(data.frame(L = 0, replica = 0, obs$rv_resumen))
  perfiles <- list()                        # L -> réplicas × pares de cada (objeto, nw, pesos)
  for (L in LARGOS) for (b in seq_len(B_PARIDAD)) {
    m <- medir(serie_nula(via, inicios[[paste0("L", L)]][b, ], L))
    kst[[length(kst) + 1]] <- data.frame(L = L, replica = b, m$kstar)
    rvr[[length(rvr) + 1]] <- data.frame(L = L, replica = b, m$rv_resumen)
    if (L == 24) rv[[length(rv) + 1]] <- data.frame(replica = b, m$rv)
    perfiles[[paste0("L", L)]][[b]] <- m$rv
    cat(via, "L", L, "réplica", b, format(round(difftime(Sys.time(), t0, units = "mins"), 1)), "\n")
  }
  write.csv(do.call(rbind, kst), file.path(DIRS[[via]], "R_nulo_estructura_kstar.csv"), row.names = FALSE)
  write.csv(do.call(rbind, rv), file.path(DIRS[[via]], "R_nulo_estructura_rv.csv"), row.names = FALSE)
  write.csv(do.call(rbind, rvr), file.path(DIRS[[via]], "R_nulo_estructura_rv_resumen.csv"), row.names = FALSE)
  # Criterio de OE4 con las réplicas calculadas en R (paridad con 07b, mismas réplicas); requiere al
  # menos 2 réplicas (el p5 de cada réplica se calcula sin ella)
  if (B_PARIDAD < 2) next
  oe4 <- list(); posicion <- list()
  for (L in LARGOS) for (obj in OBJETOS) for (nw in NW_GRILLA) for (pz in names(PESOS)) {
    sel <- function(t) t[t$objeto == obj & t$nw == nw & t$pesos == pz, ]
    o <- sel(obs$rv)
    R <- do.call(rbind, lapply(perfiles[[paste0("L", L)]], function(t) sel(t)$rv))
    cr <- criterio_oe4(o$rv, R)
    oe4[[length(oe4) + 1]] <- data.frame(L = L, replicas = nrow(R), objeto = obj, nw = nw, pesos = pz,
                                         n_pares = length(o$rv), pares_bajo_p5 = sum(cr$bajo), prop_obs = cr$prop_obs,
                                         prop_nulo_p50 = unname(quantile(cr$props_nulo, 0.5)),
                                         prop_nulo_p95 = unname(quantile(cr$props_nulo, 0.95)), p_valor = cr$p_valor)
    posicion[[length(posicion) + 1]] <- data.frame(L = L, replicas = nrow(R), objeto = obj, nw = nw, pesos = pz,
                                                   fecha_a = o$fecha_a, fecha_b = o$fecha_b, frontera = o$frontera,
                                                   rv_obs = o$rv, p5 = cr$p5, bajo_p5 = cr$bajo)
  }
  write.csv(do.call(rbind, oe4), file.path(DIRS[[via]], "R_nulo_estructura_oe4.csv"), row.names = FALSE)
  write.csv(do.call(rbind, posicion), file.path(DIRS[[via]], "R_nulo_estructura_rv_posicion.csv"), row.names = FALSE)
}
cat("Terminado en", format(round(difftime(Sys.time(), t0, units = "mins"), 1)), "\n")
