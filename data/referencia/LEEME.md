# Datos de referencia externos

`episodios_referencia.csv` es el **único** archivo de episodios de referencia (decisión D7,
tarea D9 del plan de la iteración 3b). Está fuera de `data/processed/` para no alterar los md5
congelados de D4.

- Cada fecha es la de un **evento o anuncio externo** (D7), tomada del texto de una fuente con
  ficha en `papers/` y entrada en `tesis/referencias.bib` (columnas `clave_inicio` y `clave_fin`).
  Ninguna fecha se deriva de las series, de los cortes de Camiz et al. (2026) ni de un indicador
  (regla 6).
- `fin` vacío: episodio **puntual** (solo inicio), porque no hay fuente para el fin; no se inventa.
- Formato de fecha: `AAAA-MM` (mes del evento).
- Origen de las fechas: propuesta del bibliotecario según D7 (`auditorias/notas/2026-10-24_bibliotecario.md`,
  §1). Las alternativas fichadas (COVID-19 de 2020-01 con `oms_2020a`, fin 2023-05 con `oms_2023`;
  Kuczynski como período desde 2016-12 con `doj_2016`) no entran en este archivo.

Lo leen `src/episodios.py` (notebook 05, `notebooks/modelos_dl.py`) y el Rmd final
(`R/ciclo_financiero_final.Rmd`).
