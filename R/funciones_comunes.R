# =============================================================================
# funciones_comunes.R · Datos, metadatos y utilidades compartidas por los bloques
# del documento R/tesis_ciclo_financiero.Rmd
# =============================================================================

suppressMessages({
  library(ggplot2)
  library(scales)
})

# ---- Datos ------------------------------------------------------------------

# Series en niveles (19 series, 2007-01 a 2025-12) y dataset transformado (17 series)
cargar_niveles <- function() {
  d <- read.csv("data/processed/dataset_niveles_mensual.csv", check.names = FALSE)
  d$fecha <- as.Date(d$fecha)
  d
}
cargar_transformado <- function() {
  d <- read.csv("data/processed/dataset_transformado_mensual.csv", check.names = FALSE)
  d$fecha <- as.Date(d$fecha)
  d
}

# Control común: calendario mensual completo y sin valores faltantes
verificar_calendario <- function(d) {
  stopifnot(!anyNA(d))
  cal <- seq(min(d$fecha), max(d$fecha), by = "month")
  if (length(cal) != nrow(d) || any(cal != d$fecha)) {
    stop("El calendario mensual tiene huecos: revisar 04b antes de continuar")
  }
  invisible(TRUE)
}

# Episodios de referencia (solo para validación ex post; mismas fechas que modelos_dl.py)
episodios <- data.frame(
  nombre = c("Crisis financiera global", "Taper tantrum", "COVID-19"),
  inicio = as.Date(c("2008-09-01", "2013-05-01", "2020-03-01")),
  fin    = as.Date(c("2009-06-01", "2013-12-01", "2020-12-01"))
)

# ---- Metadatos de las series ------------------------------------------------
# Nombres y unidades verificados contra la API del BCRP (consulta del 08/10/2026).
# tipo: "nivel" (stocks e índices: se analizan en variación porcentual) o
#       "tasa" (tasas de interés en % y spread en pbs: se analizan en cambios absolutos)
metadatos_series <- function() {
  m <- data.frame(
    columna = c("Crédito SF sector privado", "Crédito empresarial", "Crédito consumo",
                "Crédito hipotecario", "Liquidez M1", "Liquidez M2", "Liquidez M3",
                "Tasa referencia BCRP", "Tasa interbancaria", "Tasa activa TAMN",
                "Tasa pasiva TIPMN", "IPC Lima", "IPC Subyacente", "Tipo de cambio",
                "Índice BVL", "embi_peru", "PBI desestacionalizado", "Demanda interna",
                "Reservas internacionales"),
    nombre_corto = c("Crédito total (SF)", "Crédito empresarial", "Crédito consumo",
                     "Crédito hipotecario", "M1 (dinero)", "M2 (liquidez en soles)",
                     "M3 (liquidez total)", "Tasa de referencia", "Tasa interbancaria",
                     "TAMN", "TIPMN", "IPC Lima", "IPC subyacente", "Tipo de cambio",
                     "Índice BVL", "EMBIG Perú", "PBI desestacionalizado", "Demanda interna",
                     "Reservas internacionales netas"),
    bloque = c(rep("Crédito", 4), rep("Liquidez", 3), rep("Tasas de interés", 4),
               rep("Precios", 2), rep("Mercados y riesgo", 3), rep("Actividad y sector externo", 3)),
    codigo = c("PN00518MM", "PN00532MM", "PN00533MM", "PN00534MM", "PN00199MM", "PN00208MM",
               "PN00214MM", "PD04722MM", "PN07819NM", "PN07807NM", "PN07816NM", "PN38705PM",
               "PN38708PM", "PN01246PM", "PN01142MM", "PD04709XD", "PN01773AM", "PN01774AM",
               "PN00027MM"),
    nombre_bcrp = c(
      "Crédito del sistema financiero al sector privado (fin de periodo) - Crédito Total",
      "Crédito al sector privado de las sociedades creadoras de depósito - Saldos - A Empresas",
      "Crédito al sector privado de las sociedades creadoras de depósito - Saldos - Consumo",
      "Crédito al sector privado de las sociedades creadoras de depósito - Saldos - Hipotecario",
      "Liquidez del sistema financiero (fin de periodo) - Dinero",
      "Liquidez del sistema financiero (fin de periodo) - Liquidez en Soles",
      "Liquidez del sistema financiero (fin de periodo) - Liquidez Total",
      "Tasa de Referencia de la Política Monetaria",
      "Tasa Interbancaria Promedio (MN)",
      "Tasa activa promedio de las empresas bancarias en MN (TAMN)",
      "Tasa pasiva promedio de las empresas bancarias en MN (TIPMN)",
      "Índice de Precios al Consumidor, Lima Metropolitana",
      "IPC Subyacente, Lima Metropolitana",
      "Tipo de Cambio Nominal Promedio",
      "Índice General BVL",
      "Spread EMBIG Perú",
      "PBI desestacionalizado - mensual",
      "Indicador de Demanda Interna",
      "Reservas Internacionales Netas"),
    unidad = c(rep("millones S/", 4), rep("millones S/", 3), rep("% anual", 4),
               "índice dic.2021 = 100", "índice dic.2021 = 100", "S/ por US$",
               "índice 31/12/1991 = 100", "puntos básicos", "índice 2007 = 100",
               "índice 2007 = 100", "millones US$"),
    frecuencia_origen = c(rep("mensual, fin de periodo", 7), rep("mensual", 4), "mensual",
                          "mensual", "mensual, promedio del periodo", "mensual",
                          "diaria → promedio mensual", "mensual", "mensual", "mensual"),
    tipo = c(rep("nivel", 7), rep("tasa", 4), rep("nivel", 4), "tasa", rep("nivel", 3)),
    transformacion = c("—", rep("log-diferencia", 6), rep("diferencia simple", 4),
                       "log-diferencia", "—", "log-diferencia", "log-diferencia",
                       "diferencia simple", rep("log-diferencia", 3)),
    entra = c("No", rep("Sí", 11), "No", rep("Sí", 6)),
    stringsAsFactors = FALSE
  )
  m$bloque <- factor(m$bloque, levels = unique(m$bloque))
  m
}

# ---- Indicadores ------------------------------------------------------------

# Variación interanual: % para series en nivel, cambio absoluto para tasas y spreads
variacion_12m <- function(x, tipo) {
  previo <- c(rep(NA, 12), head(x, -12))
  if (tipo == "nivel") 100 * (x / previo - 1) else x - previo
}

indicadores_basicos <- function(d, meta) {
  do.call(rbind, lapply(seq_len(nrow(meta)), function(i) {
    v <- meta$columna[i]; x <- d[[v]]; f <- d$fecha; n <- length(x)
    var12 <- variacion_12m(x, meta$tipo[i])
    anios <- as.numeric(f[n] - f[1]) / 365.25
    data.frame(
      serie = meta$nombre_corto[i], bloque = meta$bloque[i], tipo = meta$tipo[i],
      unidad = meta$unidad[i],
      inicio = x[1], fin = x[n], media = mean(x), desv_est = sd(x),
      cv = if (meta$tipo[i] == "nivel") sd(x) / mean(x) else NA,
      minimo = min(x), fecha_min = format(f[which.min(x)], "%Y-%m"),
      maximo = max(x), fecha_max = format(f[which.max(x)], "%Y-%m"),
      cambio_total = if (meta$tipo[i] == "nivel") 100 * (x[n] / x[1] - 1) else x[n] - x[1],
      crec_anual = if (meta$tipo[i] == "nivel") 100 * ((x[n] / x[1])^(1 / anios) - 1) else NA,
      var12_mediana = median(var12, na.rm = TRUE),
      var12_min = min(var12, na.rm = TRUE),
      fecha_var12_min = format(f[which.min(var12)], "%Y-%m"),
      var12_max = max(var12, na.rm = TRUE),
      fecha_var12_max = format(f[which.max(var12)], "%Y-%m"),
      stringsAsFactors = FALSE
    )
  }))
}

# ---- Formato ----------------------------------------------------------------

# Números en formato peruano (coma decimal, espacio de miles) para el texto
num <- function(x, dec = 1) {
  dec <- ifelse(abs(x) >= 1000, 0, dec)          # saldos en millones: sin decimales
  vapply(seq_along(x), function(i) formatC(x[i], format = "f", digits = dec[i], big.mark = "\u00a0",
                                           decimal.mark = ","), character(1))
}
pct <- function(x, dec = 1) paste0(num(x, dec), " %")

# Paleta: un tono por serie (gráficos de una serie) y hasta tres categorías
color_serie <- "#2a78d6"
colores_cat <- c("#2a78d6", "#eb6834", "#1baf7a")
gris_episodio <- "#e4e2dc"

tema_tesis <- function() {
  theme_minimal(base_size = 10) +
    theme(panel.grid.minor = element_blank(),
          panel.grid.major = element_line(color = "#ecebe6", linewidth = 0.3),
          strip.text = element_text(face = "bold", hjust = 0, size = 9),
          plot.title = element_text(face = "bold", size = 11),
          plot.subtitle = element_text(color = "#52514e", size = 9),
          plot.caption = element_text(color = "#52514e", size = 8, hjust = 0),
          axis.title = element_text(color = "#52514e", size = 9),
          legend.position = "top")
}

# Bandas grises con los episodios de referencia
capa_episodios <- function() {
  geom_rect(data = episodios, inherit.aes = FALSE,
            aes(xmin = inicio, xmax = fin, ymin = -Inf, ymax = Inf),
            fill = gris_episodio, alpha = 0.8)
}
nota_episodios <- "Bandas grises: crisis financiera global (2008-09 a 2009-06), taper tantrum (2013-05 a 2013-12) y COVID-19 (2020-03 a 2020-12)."
