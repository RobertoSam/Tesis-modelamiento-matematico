# =============================================================================
# camiz_port.R · Versión en R puro de las funciones de AedeClahfac 1.2
# Autor de los métodos y del código original: Dr. Sergio Camiz (licencia GPL >= 3).
# Port a R: tesis de Roberto Samaniego Salcedo (UNI, MER611).
#
# Por qué existe: AedeClahfac 1.2 trae su núcleo de cálculo (clahfacsub y
# fishersub) compilado en Fortran solo para Linux, de modo que no corre en macOS
# ni en Windows. Este archivo reemplaza esas dos rutinas por su traducción a R y
# reutiliza sin cambios el código R del paquete (clahfac, clahpart, aede,
# dendhier y auxiliares). No depende de ningún binario.
#
# Validación (R/validacion_port_camiz.R): las 22 salidas de clahfacsub y la
# partición de fishersub coinciden con el binario original hasta el error de
# redondeo (error relativo < 1e-12) en el dataset de la tesis y en cientos de
# casos simulados, incluidos empates y casos límite.
#
# Comportamientos del binario que se reproducen tal cual (y se documentan):
#   1. El argumento 'poid' de clahfac no tiene efecto: el binario usa pesos 1/n.
#   2. La columna 'Eigentab' (y por tanto 'Ratio') de la jerarquía proviene de una
#      NIPALS que se detiene en la segunda iteración (su criterio de parada compara
#      el vector consigo mismo), por lo que no es el primer valor propio convergido
#      de la clase. El valor convergido se entrega aparte en 'eigentab_convergido'.
#   3. La salida cruda 'covout' usa los datos estandarizados; clahfac la recalcula
#      con los datos originales cuando corrige signos.
#   4. El último elemento diagonal de 'correp' queda en 0 en la salida cruda.
#   5. 'rho' (umbral del grafo de vecinos reducibles) no se reinicia entre fases.
# Nota sobre signos: en nodos con empate exacto (p. ej. dos variables con el mismo
# peso), la regla de signo de clahfac compara dos sumas iguales y el resultado lo
# decide el redondeo de punto flotante, en el original y en el port. En esos nodos
# el signo del factor puede diferir entre ambos; su valor absoluto es idéntico.
# Única diferencia deliberada: aede_r usa drop = FALSE al extraer los vectores
# propios, para que funcione con ndim = 1 (el original falla); con ndim >= 2 los
# resultados son idénticos.
#
# Funciones principales: clahfac_r(), clahpart_r(), dendhier_r(), aede_r().
# =============================================================================

# ---- 1. Partición óptima de Fisher (reemplaza a fishersub) ----
# Partición óptima de Fisher (1958) en R puro, con la misma interfaz de salida
# que la rutina Fortran fishersub del paquete AedeClahfac.
# y: serie ordenada; maxcl: número máximo de clases.
# Devuelve criter (suma de cuadrados intra-clase para k = 1..maxcl; criter[1]
# replica la convención de fishersub, que repite el valor de k = 2) y mod1out
# (fila k = límites superiores 1-based de las k clases).
fisher_r <- function(y, maxcl) {
  n <- length(y)
  s1 <- c(0, cumsum(y)); s2 <- c(0, cumsum(y^2))
  sce <- function(i, j) {               # filas i..j (1-based, inclusive)
    m <- j - i + 1; s <- s1[j + 1] - s1[i]
    s2[j + 1] - s2[i] - s * s / m
  }
  D <- matrix(Inf, maxcl, n); B <- matrix(0L, maxcl, n)
  for (j in 1:n) D[1, j] <- sce(1, j)
  for (k in 2:maxcl) {
    if (k > n) break
    for (j in k:n) {
      i <- (k - 1):(j - 1)                 # última fila de la clase k - 1
      c <- D[k - 1, i] + vapply(i, function(ii) sce(ii + 1, j), numeric(1))
      D[k, j] <- min(c); B[k, j] <- i[which.min(c)]
    }
  }
  criter <- D[, n]
  mod1out <- matrix(0, maxcl + 1, maxcl + 1)
  for (k in 2:maxcl) {
    lim <- n; j <- n
    for (kk in k:2) { j <- B[kk, j]; lim <- c(j, lim) }
    mod1out[k, 1:k] <- lim
  }
  criter[1] <- criter[2]                   # convención de fishersub
  list(criter = criter, mod1out = mod1out)
}

# ---- 2. Jerarquía de la HFC (agrega5) ----
# Traducción a R de agrega5 (Clahotm-7.2.for): jerarquía de la HFC por la técnica
# de vecinos reducibles de Bruynooghe. variante_rho:
#   "acumula" = rho no se reinicia entre fases (como está escrito en el Fortran)
#   "reinicia" = rho se reinicia a 0 en cada fase
distancia_hfc <- function(a, b, c) {
  if (c != 0) {
    delta <- (a - b)^2 + 4 * c^2
    l1 <- ((a + b) + sqrt(delta)) / 2; l2 <- ((a + b) - sqrt(delta)) / 2
    y1 <- (l1 - a) / c; nrm <- sqrt(1 + y1^2)
    return(c(dist = l2, l1 = l1, alpha = 1 / nrm, beta = y1 / nrm))
  }
  if (a >= b) c(dist = b, l1 = a, alpha = 1, beta = 0) else c(dist = a, l1 = b, alpha = 0, beta = 1)
}

agrega_r <- function(R, variante_rho = "acumula") {
  cov <- R; p <- nrow(R); xinfini <- 1e6
  nsom <- 1:p; ncarsom <- p; ii <- p + 1; rho <- 0
  nab <- matrix(0L, p - 1, 2); ind <- l1v <- numeric(p - 1); albet <- matrix(0, p - 1, 2)
  fase_a <- TRUE
  repeat {
    if (fase_a) {
      if (variante_rho == "reinicia") rho <- 0
      kk <- 0
      for (u in 1:(ncarsom - 1)) for (v in (u + 1):ncarsom) {
        rho <- rho + distancia_hfc(cov[u, u], cov[v, v], cov[u, v])["dist"]; kk <- kk + 1
      }
      rho <- rho / kk
      repeat {
        aristas <- NULL
        for (u in 1:(ncarsom - 1)) for (v in (u + 1):ncarsom) {
          d <- distancia_hfc(cov[u, u], cov[v, v], cov[u, v])
          if (d["dist"] <= rho) aristas <- rbind(aristas, c(d["dist"], u, v, d["alpha"], d["beta"]))
        }
        if (!is.null(aristas)) break
        rho <- rho^2
      }
      naret <- nrow(aristas); kmax <- naret
    }
    # Fase B: arista mínima (primera en caso de empate)
    k <- which.min(aristas[, 1])
    dd <- aristas[k, 1]; ns <- aristas[k, 2]; nsp <- aristas[k, 3]
    alphak <- aristas[k, 4]; betak <- aristas[k, 5]
    j <- ii - p
    nab[j, ] <- c(nsom[ns], nsom[nsp]); ind[j] <- dd; albet[j, ] <- c(alphak, betak)
    nsom[ns] <- ii
    # recalculcov1: el nodo agregado reemplaza a ns
    nueva <- alphak * cov[, ns] + betak * cov[, nsp]
    vns <- betak^2 * cov[nsp, nsp] + alphak^2 * cov[ns, ns] + 2 * alphak * betak * cov[ns, nsp]
    cov[ns, ] <- nueva; cov[, ns] <- nueva; cov[ns, ns] <- vns
    l1v[j] <- vns
    # vecinos de ns o nsp en el grafo
    nva <- rep(0, ncarsom)
    for (r in seq_len(naret)) {
      if (aristas[r, 1] >= xinfini) next
      a <- aristas[r, 2]; b <- aristas[r, 3]
      if (a == ns || a == nsp) nva[b] <- 1
      if (b == ns || b == nsp) nva[a] <- 1
    }
    nva[ns] <- 0; nva[nsp] <- 0
    for (r in seq_len(naret)) {
      if (aristas[r, 1] >= xinfini) next
      if (aristas[r, 2] %in% c(ns, nsp) || aristas[r, 3] %in% c(ns, nsp)) {
        aristas[r, 1] <- xinfini; kmax <- kmax - 1
      }
    }
    if (kmax != 0) for (ix in seq_len(ncarsom)) {
      if (nva[ix] == 0) next
      d <- distancia_hfc(cov[ix, ix], cov[ns, ns], cov[ix, ns])
      if (d["dist"] > rho) next
      libre <- which(aristas[, 1] >= xinfini)[1]
      aristas[libre, ] <- c(d["dist"], ix, ns, d["alpha"], d["beta"]); kmax <- kmax + 1
    }
    # recalculcov2: el último sommet pasa a la posición nsp
    if (nsp != ncarsom) {
      nsom[nsp] <- nsom[ncarsom]
      cov[nsp, ] <- cov[ncarsom, ]; cov[, nsp] <- cov[, ncarsom]
      if (kmax != 0) for (r in seq_len(naret)) {
        if (aristas[r, 1] >= xinfini) next
        if (aristas[r, 2] == ncarsom) aristas[r, 2] <- nsp
        if (aristas[r, 3] == ncarsom) aristas[r, 3] <- nsp
      }
    }
    if (ii == 2 * p - 1) break
    ii <- ii + 1; ncarsom <- ncarsom - 1
    fase_a <- (kmax == 0)
  }
  list(nab = nab, indice = ind, l1 = l1v, albet = albet)
}

# ---- 3. Rutina completa clahfacsub ----
# Port a R de la rutina Fortran clahfacsub (AedeClahfac 1.2, S. Camiz).
# Devuelve una lista con los mismos componentes que .Fortran("clahfacsub", ...).
clahfacsub_r <- function(don, poid = NULL) {
  don <- as.matrix(don); storage.mode(don) <- "double"
  n <- nrow(don); p <- ncol(don); p2 <- 2 * p - 1
  if (is.null(poid)) poid <- rep(1 / n, n)
  # El binario v1.2 ignora 'poid': todos los cálculos usan pesos uniformes 1/n
  w <- rep(1 / n, n)

  # Estadísticos ponderados, matriz de covarianzas y de correlaciones
  xmoy <- colSums(don * w)
  centrado <- sweep(don, 2, xmoy)
  xvar <- colSums(centrado^2 * w)
  datstd <- sweep(centrado, 2, sqrt(xvar), "/")
  cov <- crossprod(centrado * sqrt(w))
  cor <- cov / tcrossprod(sqrt(xvar))

  # Jerarquía (agrega5): nodos p+1 ... 2p-1
  jer <- agrega_r(cor)
  nab <- cbind(jer$nab, 0L)
  hijos <- function(k) if (k <= p) integer(0) else jer$nab[k - p, ]
  hojas_dfs <- function(k) if (k <= p) k else c(hojas_dfs(hijos(k)[1]), hojas_dfs(hijos(k)[2]))
  hojas_bfs <- function(k) {           # orden de la subrutina coupure
    res <- integer(0); nivel <- k
    repeat {
      sig <- integer(0)
      for (ll in nivel) {
        if (ll <= p) { res <- c(res, ll); next }
        for (h in hijos(ll)) if (h <= p) res <- c(res, h) else sig <- c(sig, h)
      }
      if (!length(sig)) break
      nivel <- sig
    }
    res
  }
  for (j in 1:(p - 1)) nab[j, 3] <- length(hojas_dfs(p + j))

  # Padre de cada nodo y coeficiente con que entra en él
  padre <- integer(p2); coef <- numeric(p2); coef[p2] <- 1
  for (j in 1:(p - 1)) {
    padre[jer$nab[j, 1]] <- p + j; coef[jer$nab[j, 1]] <- jer$albet[j, 1]
    padre[jer$nab[j, 2]] <- p + j; coef[jer$nab[j, 2]] <- jer$albet[j, 2]
  }
  # Peso de un nodo dentro de un ancestro: producto de coeficientes a lo largo del camino
  peso_en <- function(k, ancestro) { s <- 1; while (k != ancestro) { s <- s * coef[k]; k <- padre[k] }; s }
  peso_global <- vapply(1:p2, function(k) peso_en(k, p2), numeric(1))
  signo <- ifelse(peso_global[(p + 1):p2] < 0, -1, 1)   # orientación de cada factor de nodo

  # Factores de nodo: A (primer factor, varianza lambda1) y B (segundo, varianza lambda2)
  Fv <- matrix(0, n, p2); Fv[, 1:p] <- datstd
  datout <- matrix(0, n, 2 * (p - 1))
  for (j in 1:(p - 1)) {
    a <- jer$nab[j, 1]; b <- jer$nab[j, 2]; al <- jer$albet[j, 1]; be <- jer$albet[j, 2]
    Fv[, p + j] <- al * Fv[, a] + be * Fv[, b]
    sb <- if (be < 0) 1 else -1
    datout[, 2 * j - 1] <- signo[j] * Fv[, p + j]
    datout[, 2 * j] <- sb * signo[j] * (-be * Fv[, a] + al * Fv[, b])
  }
  covp_w <- function(X, Y) crossprod(sweep(X, 2, colSums(X * w)) * sqrt(w), sweep(Y, 2, colSums(Y * w)) * sqrt(w))
  covout <- covp_w(datstd, datout)            # el binario usa los datos estandarizados
  corout <- covout / tcrossprod(rep(1, p), sqrt(diag(covp_w(datout, datout))))
  covrep <- covp_w(datout, datout)
  correp <- covrep / tcrossprod(sqrt(diag(covrep)))
  correp[nrow(correp), ncol(correp)] <- 0     # el binario deja en 0 el último elemento diagonal

  # Ponderaciones de variables y nodos en el factor raíz
  poids <- cbind(c(peso_global[1:p], abs(peso_global[(p + 1):p2])), 0)
  poids[, 2] <- poids[, 1]^2

  # Composición de clases, orden del dendrograma y particiones por etapa
  nclass <- matrix(0L, p2, p)
  for (k in 1:p) nclass[k, 1] <- k
  for (k in (p + 1):(p2 - 1)) { h <- hojas_bfs(k); nclass[k, seq_along(h)] <- h }
  nclstr <- hojas_dfs(p2); nclass[p2, ] <- nclstr
  ncla <- matrix(0L, p, p); clase <- 1:p
  ncla[, 1] <- clase
  for (s in 1:(p - 1)) {
    clase[clase %in% jer$nab[s, 1:2]] <- p + s
    ncla[, s + 1] <- clase
  }
  narb <- ncla[nclstr, ]
  npart <- matrix(0L, p, p)
  for (s in 1:p) { u <- unique(narb[, s]); npart[seq_along(u), s] <- u }
  # Nodo que une hojas consecutivas del dendrograma (ancestro común más bajo)
  ancestros <- function(k) { r <- k; while (k != p2) { k <- padre[k]; r <- c(r, k) }; r }
  nsg <- integer(p)
  for (i in 1:(p - 1)) nsg[i] <- intersect(ancestros(nclstr[i]), ancestros(nclstr[i + 1]))[1]

  # Dipolos: lado de cada variable según el signo de su peso en el factor del nodo
  noeuind <- matrix(0L, p, p2)
  for (k in 1:p) noeuind[k, k] <- 2L
  # el lado se decide por el signo de la covarianza de la variable con el factor A del nodo
  for (j in 1:(p - 1)) for (v in hojas_dfs(p + j)) {
    ps <- covout[v, 2 * j - 1]
    noeuind[v, p + j] <- if (ps >= 0) 2L else 1L
  }

  # Columna Eigentab: NIPALS del binario (se detiene en la segunda iteración)
  nipals_bin <- function(x) {
    kl <- which(colSums(x^2) != 0)[1]; th <- x[, kl]; ph <- rep(0, ncol(x))
    for (it in 1:2) {
      ph <- (ph + as.vector(crossprod(x, th))) / sum(th^2)
      ph <- ph / sqrt(sum(ph^2)); th <- as.vector(x %*% ph)
    }
    sqrt(sum(th^2))
  }
  eigentab <- vapply(1:(p - 1), function(j) {
    x <- cor; fuera <- noeuind[, p + j] == 0
    x[fuera, ] <- 0; x[, fuera] <- 0; nipals_bin(x)
  }, numeric(1))

  traza <- sum(diag(cor)); l1 <- jer$l1; l2 <- jer$indice
  ddo <- cbind(l1, l2, 100 * l1 / (l1 + l2), 100 * l2 / (l1 + l2), 100 * l1 / traza,
               100 * l2 / traza, cumsum(100 * l2 / traza), eigentab, l1 / eigentab)
  dimnames(ddo) <- NULL
  list(units = n, variables = p, don = don, poid = poid, datstd = datstd, xmoy = xmoy,
       xvar = xvar, cov = cov, cor = cor, nab = nab, ddo = ddo, albet = jer$albet,
       poids = poids, vt = c(sum(l2), l1[p - 1], traza), nclstr = nclstr, nsg = nsg,
       nclass = nclass, ncla = ncla, narb = narb, npart = npart, noeuind = noeuind,
       datout = datout, covout = covout, corout = corout, covrep = covrep, correp = correp,
       error = 0L, eigentab_convergido = vapply(1:(p - 1), function(j) {
         v <- nclass[p + j, ]; v <- v[v > 0]; max(eigen(cor[v, v], symmetric = TRUE, only.values = TRUE)$values)
       }, numeric(1)))
}

# ---- 4. Código R original de AedeClahfac 1.2 (sin llamadas a Fortran) ----
clahfac_r <- function (don, out = FALSE, poid = NULL) 
{
    nind = dim(don)[1]
    nvar = dim(don)[2]
    nvarm1 = nvar - 1
    nvar2 = 2 * nvar - 1
    nvar21 = 2 * (nvar - 1)
    kideni = rownames(don)
    kidenj = colnames(don)
    if (is.null(poid)) {
        poid = c(rep(1/nind, nind))
    }
    depsilon = 1e-16
    ifois = 1000
    error = 0
    kidenout = character(length = 2 * nvarm1)
    kidsrt = character(length = nvar)
    outclah = clahfacsub_r(don, poid)
    res = list(call = match.call())
    res$data = don
    res$mevar = rbind(outclah$xmoy, outclah$xvar)
    rownames(res$mevar) = c("Means", "Variances")
    colnames(res$mevar) = kidenj
    res$cov = outclah$cov
    res$cor = outclah$cor
    rownames(res$cov) = kidenj
    colnames(res$cov) = kidenj
    rownames(res$cor) = kidenj
    colnames(res$cor) = kidenj
    res$weight = t(outclah$poids[1:nvar, ])
    rownames(res$weight) = c("Weight", "Weight2")
    colnames(res$weight) = kidenj
    res$hierar = cbind(c((nvar - 1):1), outclah$nab, outclah$poids[(nvar + 1):nvar2, 1:2], outclah$ddo, 
        outclah$albet)
    rownames(res$hierar) = c((nvar + 1):nvar2)
    colnames(res$hierar) = c("ngr", "N1", "N2", "Num", "Weight", "Weight2", "Eigenv", "Index", "Loc_%1", 
        "Loc_%2", "Glob_%1", "Glob_%2", "Cum_%2", "Eigentab", "Ratio", "Weight_N1", "Weight_N2")
    res$inertia = rbind(outclah$vt, outclah$vt/outclah$vt[3] * 100)
    rownames(res$inertia) = c("Inertia", "Percent")
    colnames(res$inertia) = c("Hierarchy", "Repr_Var", "Total")
    kidsrt = kidenj[outclah$narb[1:nvar, 1]]
    res$nclass = outclah$nclass[(nvar + 1):nvar2, ]
    rownames(res$nclass) = c((nvar + 1):nvar2)
    colnames(res$nclass) = c(rep("", nvar))
    res$ncla = t(outclah$ncla)[nvar:1, ]
    rownames(res$ncla) = c(nvar2:(nvar + 1), nvar)
    colnames(res$ncla) = kidenj
    res$noeuind = t(outclah$noeuind[, nvar2:(nvar + 1)])
    rownames(res$noeuind) = c(nvar2:(nvar + 1))
    colnames(res$noeuind) = kidenj
    res$narb = t(outclah$narb)[nvar:1, ]
    rownames(res$narb) = c(nvar2:(nvar + 1), "")
    colnames(res$narb) = kidsrt
    res$npart = t(outclah$npart)[nvar:1, ]
    rownames(res$npart) = c("", nvar2:(nvar + 1))
    colnames(res$npart) = c(rep("", nvar))
    for (j in 1:(nvar - 1)) {
        j1 = 2 * j - 1
        j2 = 2 * j
        kidenout[j1] = paste("*", as.character(j + nvar), "A*", sep = "")
        kidenout[j2] = paste("*", as.character(j + nvar), "B*", sep = "")
    }
    res$repvar = outclah$datout
    rownames(res$repvar) = kideni
    colnames(res$repvar) = kidenout
    res$covout = outclah$covout
    rownames(res$covout) = kidenj
    colnames(res$covout) = kidenout
    res$corout = outclah$corout
    rownames(res$corout) = kidenj
    colnames(res$corout) = kidenout
    res$covrep = outclah$covrep
    rownames(res$covrep) = kidenout
    colnames(res$covrep) = kidenout
    res$correp = outclah$correp
    rownames(res$correp) = kidenout
    colnames(res$correp) = kidenout
    flag <- FALSE
    for (i in 1:(nvar - 1)) {
        nclassa <- res$nclass[i, which(res$nclass[i, ] != 0)]
        nrepa <- c(2 * i - 1, 2 * i)
        cora <- cor(res$data[nclassa], res$repvar[, nrepa])
        for (j in 1:2) {
            if (sum(cora[which(cora[, j] < 0), j]^2) > sum(cora[which(cora[, j] > 0), j]^2)) {
                cat(paste("\n changed sign at node", i, "var", j, "\n", sep = " "))
                res$repvar[, nrepa[j]] = -res$repvar[, nrepa[j]]
                flag = TRUE
            }
        }
    }
    if (flag) {
        res$covout <- .covp_ac(res$data, res$repvar)
        res$corout <- cor(res$data, res$repvar)
        res$covrep <- .covp_ac(res$repvar)
        res$correp <- cor(res$repvar)
    }
    hier = list()
    hier$merge = outclah$nab[, 1:2]
    for (i in 1:nvarm1) {
        if (hier$merge[i, 1] <= nvar) 
            hier$merge[i, 1] = -hier$merge[i, 1]
        else hier$merge[i, 1] = hier$merge[i, 1] - nvar
        if (hier$merge[i, 2] <= nvar) 
            hier$merge[i, 2] = -hier$merge[i, 2]
        else hier$merge[i, 2] = hier$merge[i, 2] - nvar
    }
    hier$height = outclah$ddo[, 2]
    hier$order = outclah$narb[, 1]
    hier$labels = kidenj
    hier$method = "clahfac"
    hier$dist.method = "correlation"
    class(hier) = "hclust"
    res$hier = hier
    class(res) = "clahfac"
    if (out) {
        res
    }
    else {
        plot(hier, hang = -1, main = "Clahfac Dendrogram", sub = "", xlab = "Hierarchical Factor Classification of Characters", 
            ylab = "Index", cex = 0.5)
        print(res$hierar[, c(1:4, 7, 8, 11, 13)])
    }
}

clahpart_r <- function (res, noeud = 0, exch = NULL) 
{
    nind = dim(res$data)[1]
    nvar = dim(res$data)[2]
    nvarm1 = nvar - 1
    kidenj = rownames(res$cov)
    if (!is.null(exch)) {
        for (i in 1:length(exch)) {
            nv = abs(exch[i]) - nvar
            if (exch[i] > 0) {
                iv = 2 * nv - 1
            }
            else {
                iv = 2 * nv
            }
            res$repvar[, iv] = -res$repvar[, iv]
        }
        res$covout = (nind - 1)/nind * cov(res$data, res$repvar)
        res$corout = cor(res$data, res$repvar)
        res$covrep = (nind - 1)/nind * cov(res$repvar)
        res$correp = cor(res$repvar)
    }
    if (noeud > 0) {
        classes = sort(res$npart[noeud + 1, 1:(noeud + 1)])
        cla = classes - nvar
        cla2 = cla[(cla > 0)]
        clou = c(cla2, c((nvar - noeud):(nvar - 1)))
        clout = c()
        for (i in 1:length(clou)) {
            clout = c(clout, (2 * clou[i] - 1), (2 * clou[i]))
        }
        itemclas = data.frame()
        cs = cla[cla <= 0] + dim(res$data)[2]
        if (length(cs) > 0) {
            for (i in 1:length(cs)) {
                itemclas = rbind(itemclas, cbind(as.character(cs[i]), kidenj[cs[i]]))
            }
        }
        cc = res$nclass[cla2, , drop = FALSE]
        iclas = rowSums(cc != 0)
        res$classes = rbind(classes, c(rep(1, length(cs)), iclas))
        for (i in (1:dim(cc)[1])) {
            itemclas = rbind(itemclas, cbind(rep(rownames(cc)[i], iclas[i]), kidenj[cc[i, 1:iclas[i]]]))
        }
        colnames(itemclas) = c("class", "label")
        res$itemclas = itemclas
        coord = list()
        for (n in 1:noeud) {
            coor = list()
            node = nvarm1 - n + 1
            nodeb = 2 * node
            nodea = nodeb - 1
            datcl = cbind(res$data[, res$nclass[node, ]], res$repvar[, nodea:nodeb])
            coor$var = res$corout[res$nclass[node, ], nodea:nodeb]
            coor$faccov = sqrt(res$hierar[node, 7:8])
            naj = res$hierar[node, 2]
            nbj = res$hierar[node, 3]
            if (min(naj, nbj) > nvar) {
                naj = naj - nvar
                nbj = nbj - nvar
                najb = 2 * naj
                naja = najb - 1
                nbjb = 2 * nbj
                nbja = nbjb - 1
                coor$sup = res$correp[c(naja, najb, nbja, nbjb), nodea:nodeb]
                coor$supcov = coor$sup * sqrt(as.vector(t(res$hierar[c(naj, nbj), 7.8])))
                datcl = cbind(datcl, res$repvar[, c(naja, najb, nbja, nbjb)])
            }
            else if (max(naj, nbj) < nvar) {
                coor$sup = NULL
                coor$supcov = NULL
            }
            else if (naj > nvar) {
                naj = naj - nvar
                najb = 2 * naj
                naja = najb - 1
                coor$sup = res$correp[naja:najb, nodea:nodeb]
                coor$supcov = coor$sup * sqrt(as.vector(t(res$hierar[naj, 7:8])))
                datcl = cbind(datcl, res$repvar[, c(naja, najb)])
            }
            else if (nbj > nvar) {
                nbj = nbj - nvar
                nbjb = 2 * nbj
                nbja = nbjb - 1
                coor$sup = res$correp[nbja:nbjb, nodea:nodeb]
                coor$supcov = coor$sup * sqrt(as.vector(t(res$hierar[nbj, 7:8])))
                datcl = cbind(datcl, res$repvar[, c(nbja, nbjb)])
            }
            coor$dat = datcl
            coor$ind = res$repvar[, nodea:nodeb]
            coord[[n]] = coor
        }
        res$coord = coord
    }
    res
}

dendhier_r <- function (hier, ncl, hiertit = "Dendrogram", plotname = NULL, off = -0.1) 
{
    p <- length(hier$labels)
    partition <- .partclas_ac(hier, ncl)
    subtit <- paste0("Partition in ", ncl, " classes")
    mnodes <- ncl - 1
    nmax <- dendextend::nnodes(hier) - p
    nmin <- nmax - mnodes + 1
    labnod <- .hc2axes_ac(hier)
    rownames(labnod) <- paste0("*", c((p + 1):(p + nmax)), "*")
    wclas <- partition$ord.class[which(partition$ord.class >= 0)]
    labclas <- labnod[wclas, ]
    maxheight <- max(hier$height)
    plot(hier, hang = -5, ylab = "Index", cex = 0.5, ylim = c(0, maxheight), main = hiertit, xlab = subtit, 
        sub = " ")
    rect.hclust(hier, ncl)
    text(labnod[nmin:nmax, ], labels = rownames(labnod)[nmin:nmax], cex = 0.5, col = "blue", pos = 3, 
        offset = 0.2)
    text(labclas[, 1], rep(labnod[nmin - 1, 2] + off, ncl), labels = rownames(labclas), cex = 0.5, col = "red", 
        pos = 3)
    if (!is.null(plotname)) {
        dev.copy(pdf, plotname, width = 8, height = 5)
        dev.off()
    }
    partition
}

aede_r <- function (title = "Evolutionary Principal Component Analysis", serie, standard = TRUE, ndim = 3, nw, 
    nsd = 0, maxcl = 10) 
{
    prog <- "  ** AEDE **  -- 3.4 -- 24-04-2025 **  "
    res <- list()
    n <- dim(serie)[1]
    p <- dim(serie)[2]
    wn <- n - nw + 1
    res$input = rbind(c(" program = ", prog), c(" data = ", title), c(" rows number =", n), c(" columns number =", 
        p), c(" windows size = ", nw), c(" number of windows = ", wn), c(" weights in std. dev. = ", 
        nsd), c(" standardize =", standard), c(" solution dimension = ", ndim))
    autoval <- matrix(0, nrow = wn, ncol = ndim)
    facnames <- c(sprintf("Dim_%02d", c(1:ndim)))
    rownames(autoval) <- rownames(serie)[(1 + nw/2):(wn + nw/2)]
    colnames(autoval) <- facnames
    diff <- numeric(length = wn)
    diff[1] = 0
    correlsn <- array(0, dim = c(wn, p, ndim), dimnames = list(rownames(autoval), colnames(serie), facnames))
    correlsq <- array(0, dim = c(wn, p, ndim), dimnames = list(rownames(autoval), colnames(serie), facnames))
    weight <- rep(1/nw, length.out = nw)
    if (nsd != 0) {
        am <- (nw + 1)/2
        s <- (nw - 1)/sqrt(2)
        for (i in 1:nw) {
            ex <- (i - am)/s
            weight[i] <- exp(-0.5 * (ex * nsd)^2)
        }
        som <- sum(weight)
        weight <- weight/som
    }
    for (i in 1:wn) {
        dati <- as.matrix(serie[i:(i + nw - 1), 1:p])
        bstat <- .bstatw_ac(dati, weight)
        med <- bstat$univariate[, 1]
        dev <- bstat$univariate[, 3]
        if (standard) {
            dati <- sweep((dati - med), 2, dev, "/")
            covp <- bstat$correlations
        }
        else {
            dati <- dati - med
            covp <- bstat$covariances
        }
        eig <- eigen(covp)
        autoval[i, 1:ndim] <- eig$values[1:ndim]
        autvet <- eig$vectors[1:p, 1:ndim, drop = FALSE]
        for (k in 1:ndim) {
            corp <- sum(autvet[which(autvet[, k] > 0), k])
            if (is.na(corp)) {
                corp = 0
            }
            corn <- sum(autvet[which(autvet[, k] < 0), k])
            if (is.na(corn)) {
                corn = 0
            }
            if (abs(corn) > corp) {
                autvet[, k] <- -autvet[, k]
            }
        }
        correlsn[i, 1:p, 1:ndim] <- sweep(autvet, 2, sqrt(autoval[i, 1:ndim]), "*")
        correlsn[i, 1:p, 1:ndim] <- sweep(autvet, 2, sqrt(autoval[i, 1:ndim]), "*")
        if (i != 1) {
            for (k in 1:ndim) {
                corp <- sum((autvet[, k] - autveto[, k])^2)
                if (is.na(corp)) {
                  corp = 0
                }
                corn <- sum((autvet[, k] + autveto[, k])^2)
                if (is.na(corn)) {
                  corn = 0
                }
                if (abs(corn) < corp) {
                  autvet[, k] <- -autvet[, k]
                }
            }
            diff[i] <- sum((autvet[, k] - autveto[, k])^2)
        }
        autveto <- autvet
        correlsq[i, 1:p, 1:ndim] <- sweep(autvet, 2, sqrt(autoval[i, 1:ndim]), "*")
    }
    res$weights <- weight
    res$eigenvalues <- autoval
    res$least_squares_differences <- diff
    res$correlationsgn <- correlsn
    res$correlationlsq <- correlsq
    nbind <- dim(autoval)[1]
    nvar <- 2
    dat <- cbind(c(1:nbind), autoval[, 1])
    tss <- sum(scale(autoval[, 1], center = TRUE, scale = FALSE)^2)
    npos <- 2
    iv <- 1
    maxcl1 <- maxcl + 1
    valnames <- paste("v", c(1:maxcl), sep = "_")
    out = list()
    outpart <- fisher_r(autoval[, 1], maxcl)
    df1 <- c(1:(maxcl))
    df2 <- (nbind - df1)
    wss <- outpart$criter[1:maxcl]
    wss[1] <- tss
    bss <- tss - wss
    CH <- (bss/df1)/(wss/df2)
    out$title <- title
    out$act <- noquote(paste("Partitioning of variable ", iv, " minimizing the inertia of ", npos, " :", 
        sep = ""))
    classes <- outpart$mod1out[1:maxcl, 1:maxcl]
    part <- cbind(c(1:maxcl), wss, CH, classes)
    colnames(part) <- c("n", "Within ssq", "Calinski-Harabasz", valnames)
    out$part <- part
    res$cutpoints <- out
    res
}

.bstatw_ac <- function (x, w) 
{
    n <- dim(x)[1]
    p <- dim(x)[2]
    if (length(w) != n) {
        print("length of weights different from the number of units")
        print(paste("weights =", length(w), "units =", n), sep = " ")
    }
    if (sum(w) != 0) {
        w = w/sum(w)
    }
    res <- list()
    sx <- .ustatw_ac(x, w)
    res$univariate <- sx
    u <- matrix(rep(1, n * p), nrow = n, ncol = p)
    xc <- as.matrix(x - sweep(u, 2, sx[, 1], "*"))
    cova <- t(xc) %*% diag(w) %*% xc
    res$covariances = cova
    corr <- cova/(sx[, 3] %*% t(sx[, 3]))
    corr[is.nan(corr)] <- 0
    res$correlations <- corr
    res
}

.ustatw_ac <- function (x, w) 
{
    if (length(w) != dim(x)[1]) {
        print("length of weights different from the number of units")
        print(paste("weights =", length(w), "units =", dim(x)[1]), sep = " ")
    }
    if (sum(w) != 0) {
        w = w/sum(w)
    }
    m <- t(w) %*% as.matrix(x)
    v <- t(w) %*% (sweep(as.matrix(x), 2, m, "-")^2)
    sd <- sqrt(v)
    cv <- sd/m
    res <- t(rbind(m, v, sd, cv))
    colnames(res) = c("mean", "variance", "standard_deviation", "coefficient of variation")
    res
}

.covp_ac <- function (data1, data2 = NULL) 
{
    n = dim(data1)[1]
    res <- (n - 1)/n * cov(data1, data2)
    return(res)
}

.partclas_ac <- function (hier, ncl) 
{
    p <- length(hier$labels)
    clasnod <- matrix(0, nrow = p, ncol = p)
    rownames(clasnod) <- c(0:(p - 1))
    colnames(clasnod) <- hier$labels
    clasnod[1, ] <- -(1:p)
    for (i in 2:p) {
        clasnod[i, ] <- clasnod[i - 1, ]
        ia <- hier$merge[i - 1, 1]
        ib <- hier$merge[i - 1, 2]
        clasnod[i, which(clasnod[i - 1, ] == ia)] <- i - 1
        clasnod[i, which(clasnod[i - 1, ] == ib)] <- i - 1
    }
    clasnod <- clasnod[-1, ]
    clasnodord <- clasnod[, hier$order]
    partition <- clasnod[p - ncl, ]
    classapp <- paste0("*", partition + p, "*")
    partition <- as.data.frame(cbind(partition, classapp, c(1:p)))
    colnames(partition) <- c("Position", "Class", "Number")
    partition[, 1] <- as.numeric(partition[, 1])
    class <- unique(partition[, 1:2])
    nclass <- class[, 2]
    class <- class[, 1]
    names(class) <- nclass
    class <- class[order(class)]
    partitord <- clasnodord[p - ncl, ]
    classapp <- paste0("*", partitord + p, "*")
    partitord <- as.data.frame(cbind(partitord, classapp))
    colnames(partitord) <- c("Position", "Class")
    partitord[, 1] <- as.numeric(partitord[, 1])
    classord <- unique(partitord)
    nclassord <- classord[, 2]
    classord <- classord[, 1]
    names(classord) <- nclassord
    tp <- table(partition[, 1])
    names(tp) <- names(class)
    tpord <- tp[names(classord)]
    out <- list()
    out$numofclass <- ncl
    out$partition <- partition
    out$class <- class
    out$numitem <- tp
    out$ord.partition <- partitord
    out$ord.class <- classord
    out$ord.numitem <- tpord
    out
}

.hc2axes_ac <- function (x) 
{
    A <- x$merge
    n <- nrow(A) + 1
    x.axis <- c()
    y.axis <- x$height
    x.tmp <- rep(0, 2)
    zz <- match(1:length(x$order), x$order)
    for (i in 1:(n - 1)) {
        ai <- A[i, 1]
        if (ai < 0) 
            x.tmp[1] <- zz[-ai]
        else x.tmp[1] <- x.axis[ai]
        ai <- A[i, 2]
        if (ai < 0) {
            x.tmp[2] <- zz[-ai]
        }
        else {
            x.tmp[2] <- x.axis[ai]
        }
        x.axis[i] <- mean(x.tmp)
    }
    return(data.frame(x.axis = x.axis, y.axis = y.axis))
}
