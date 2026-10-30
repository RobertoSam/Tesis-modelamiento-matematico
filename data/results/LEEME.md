# Antecedente · 17 series, vía transformada · no consumir

Los CSV de esta carpeta (y de `niveles/`, que tiene su propio `LEEME.md`) se calcularon con
**17 series** y en **dos vías** (iteraciones 3a y 3b, fase 0). Desde las decisiones D15 (Rmd final
solo en niveles; las transformadas pasan a un anexo de robustez) y D16 (se excluye la Liquidez M2:
16 series) de `decisiones.qmd`, son **antecedente**:

- **no se consumen** en la tesis, en el informe ni en `herramientas/generar_cifras.py`;
- **no se borran ni se sobrescriben**: el criterio 17 de la adenda del 26-oct-2026 exige que sus
  md5 sigan siendo los del commit `2be3665`;
- el estado completo queda en el commit `2be3665` (que solo agrega D15 y D16 a `81d8a94`). El tag
  `v0.4-17series-dos-vias` que debía marcarlo no existe todavía: queda pendiente de crear por
  Roberto (auditoría de la iteración 3b, N-01).

Los resultados vigentes (16 series) se escriben en `data/results/final/` (niveles, análisis
oficial) y en `data/results/final/anexo/` (transformadas, anexo de robustez).
