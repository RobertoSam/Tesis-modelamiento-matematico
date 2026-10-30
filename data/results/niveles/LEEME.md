# Antecedente · 17 series, vía sin transformar · no consumir

Los CSV de esta carpeta se calcularon con **17 series** (iteraciones 3a y 3b, fase 0). Desde las
decisiones D15 y D16 de `decisiones.qmd` (Rmd final solo en niveles y exclusión de la Liquidez M2),
son **antecedente**:

- **no se consumen** en la tesis, en el informe ni en `herramientas/generar_cifras.py`;
- **no se borran ni se sobrescriben** (criterio 17 de la adenda del 26-oct-2026: md5 iguales a los
  del commit `2be3665`);
- el estado completo queda en el commit `2be3665`. El tag `v0.4-17series-dos-vias` que debía
  marcarlo no existe todavía: queda pendiente de crear por Roberto (auditoría 3b, N-01).

Los resultados vigentes de la vía sin transformar, con 16 series, se escriben en
`data/results/final/`.
