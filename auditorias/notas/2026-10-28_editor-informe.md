# Nota del editor del informe · Iteración 3b, fase 2 · 28 de octubre de 2026

**Agente:** editor del informe (`.claude/agents/editor-informe.md`). **Rama:** `iteracion-3b`, desde
`c9424c2`. **Encargo:** tareas E1 a E3 del plan de la iteración 3b
(`asesoria/2026-10-21_plan-iteracion-3b.md`, §4, «Editor del informe»), con la adenda del 26-oct
(E1–E3 derivan de L1–L4, sin cambios de procedimiento) y D1–D17. Sesión automática de seguimiento
diario, sin Roberto presente: lo operativo se decidió y las dudas se dejan aquí.

| Tarea | Commit | Estado |
|---|---|---|
| E1 · cap. 2 del informe desde L1 y L2 (más el cap. 1, ver «Desviaciones», 1) | `2bced25` | hecha |
| E2 · cap. 3 del informe desde L3, sin resultados | `e149f18` | hecha |
| E3 · correspondencia en `tesis/README.md`, estado en `tesis/index.qmd`, renders y esta nota | commit siguiente | hecha |

**Regla 7.** No se tocaron `tesis/_capitulos/04_resultados.qmd`, `05_conclusiones.qmd` ni ningún
contenido de resultados. El capítulo 3 no lleva cifras de resultados ni conclusiones sobre la
Parte C: sus únicas cifras son de datos y de métodos, leídas de `tesis/_cifras.yml`. No se
tocaron `tesis_latex/`, `tesis/referencias.bib`, `tesis/registro_verificacion.md`, `apa.csl` ni
`_cifras.yml`.

## 1. Fuentes leídas

`CLAUDE.md`; `decisiones.qmd` (D1–D17); el plan de la iteración 3b (§4–§6) y su adenda;
`auditorias/notas/2026-10-27_redactor-latex.md` (completa); `git diff origin/main..HEAD --
tesis_latex/` (caps. 1, 2 y 3); `tesis_latex/capitulos/03_metodologia.tex` completo;
`tesis_latex/notacion.tex` (macros nuevas); `tesis_latex/README.md` (lista de excepciones a la
regla de cifras); `tesis/_cifras.yml`; `tesis/registro_verificacion.md`; la existencia de ficha en
`papers/` y de entrada en el `.bib` de las 28 claves que el informe cita por primera vez o
vuelve a citar (todas presentes).

## 2. Lo redactado y sus fuentes

### E1 · Capítulo 2 (`tesis/_capitulos/02_marco_teorico.qmd`)

Derivación condensada de los commits `f904b5c` (L1) y `50db7a6` (L2) de la tesis, en el mismo
orden. Sin demostraciones, como en 3a; cuando la tesis demuestra algo con una técnica que importa
para leerlo, se nombra («con la desigualdad de Cauchy-Schwarz», «con un contraejemplo»).

| Sección del informe | Contenido nuevo | Fuente en la tesis |
|---|---|---|
| Validación externa | `def-episodio`, `def-tolerancia`, observación, `tbl-episodios` (fechas por `meta cifras.episodio*`), párrafo de fechado con las 12 claves, dos advertencias | `def:episodio`, `def:tolerancia`, `obs:tolerancia`, `tab:episodios` |
| Posición epistemológica | Párrafo de D1/D2/D15 («propuesta, no hecho consumado») | `sec:epistemologia` |
| PCA, retención | Jolliffe (2002); vara quebrada vía Camiz y Pillar (2018) con `[CITA PENDIENTE: Frontier (1976)]`; párrafo de Rencher con `rencher_christensen_2012` | `teo:eckart-young` (texto siguiente), `def:retencion` |
| HFC | Denimal (2007) con nota; Bruynooghe (1978) | `sec:hfc`, `obs:hfc-codigo` |
| EPCA | Atoche Murrieta (2022) sobre los pesos; Tukey (1977); subsecciones de Kish (`def-kish`, `prp-kish`, `def-umbral-ventana`, observación), regla del 06 (`def-regla06`, `cor-regla06`, observación), bordes (`lem-ventana-mes`, `def-borde`) y multiescala (observación) | `sec:kish`, `sec:regla06`, `sec:bordes`, `sec:multiescala` |
| Fisher | `cor-fisher-factible`, `prp-fisher-monotonia`, `def-datacion`, `def-criterios-k`, observación de lectura; observación del CH con D11 | `sec:nmin`, `sec:datacion`, `obs:ch` |
| Comparación | RV sin exigir centrado; Lavit (1988); `def-rv-cargas`, `prp-rv-cargas`, `def-pares` | `def:rv`, `def:rv-cargas`, `prop:rv-cargas`, `def:pares` |
| Nulos (sección nueva) | Kunsch (1989), Lahiri (2003); `def-bloques`; nulo mixto (`def-hac`, `lem-hac`, `def-nulo-mixto`, observación); nulo de estructura (`def-nulo-estructura`, `prp-nulo-estructura`, observación con `[CITA PENDIENTE]`); OE4 (`def-oe4`, supuesto, `prp-oe4`, observación, `def-fuera-nulo`, `def-confirmada`) | `sec:nulos` y subsecciones |
| Criterios y aporte | Robustez (multiescala, anexo D15); aporte (4) con RV de cargas y nulo | `sec:criterios`, `sec:vacios` |

Notas al pie nuevas (`[^v2-…]`): reproducen literalmente el `\verificar{}` de la tesis para
`atoche_murrieta_2022` (dos), `bernanke_2013`, `congreso_2018`, `jolliffe_2002`,
`rencher_christensen_2012`, `bruynooghe_1978`, `tukey_1977`, `kish_1965`, `lavit_1988`,
`kunsch_1989`, `lahiri_2003` y `newey_west_1987`; la de `denimal_2007` reproduce la nota al pie
de la tesis.

### E1 · Capítulo 1 (`tesis/_capitulos/01_introduccion.qmd`)

Traslado del diff del commit `f01e744` en `01_introduccion.tex`: Atoche Murrieta (2022) con su
nota; párrafo de datos con D1 y D15 y las transformadas como anexo de robustez (remite al cap. 3);
OE6 con Camiz y Pillar (2018) y `[CITA PENDIENTE: Frontier (1976)]`; comentario de fuente apuntado
a `data/results/final/05_dimensiones.csv`. Objetivos e hipótesis sin cambios, igual que la tesis.

### E2 · Capítulo 3 (`tesis/_capitulos/03_metodologia.qmd`)

Derivación completa de `03_metodologia.tex` (L3), sin resultados. Los dos encabezados de la
estructura MMC102 se conservan: «Metodología» reúne 3.1 (diseño, con «Análisis en niveles y anexo
de robustez» y «Qué vía mide qué») y 3.2 (datos); «Desarrollo del modelo matemático y
computacional» reúne 3.3 (procedimiento), 3.4 (criterios fijados de antemano) y 3.5
(implementación, paridad y reproducibilidad), en el orden de la tesis.

- Tablas: `tbl-etapas`, `tbl-kish` y `tbl-decisiones`, con título en cursiva sobre la tabla y nota
  «*Nota.* Elaboración propia …» debajo.
- Definiciones: `def-regla-d5` y `def-walkforward`.
- Cifras, todas por `{{< meta cifras.… >}}`: `nSeries`, `nMesesNiveles`, `fechaInicioNiveles`,
  `fechaFinDatos`, `nMesesTransformadas`, `fechaInicioTransformadas`, `nOmegaGauss*` y
  `nHornGauss*` (cuatro anchos), `largoBloqueNulo`, `largoBloqueNuloCorto`,
  `largoBloqueNuloLargo`, `replicasNuloEstructura`, `replicasNuloSensibilidad`. Cada bloque lleva
  su comentario `<!-- fuente: … -->`.
- Números escritos a mano: los mismos que la tesis deja escritos, todos de las clases de la lista
  de excepciones de `tesis_latex/README.md` (parámetros fijados de antemano de D5, D7–D12 y D17;
  fechas de registro de las decisiones y de D4; parámetros de diseño del plan, clase provisional:
  ν = 3, paso 3, eje 2, media móvil de 12 meses, 3 y 4 clases, percentil 95). El comentario inicial
  del archivo lo declara.
- Pendientes, como en la tesis: «Qué vía mide qué» (reunión con el Dr. Camiz) y AE/LSTM con 16
  series (D17.4, iteración 4), ambos en recuadro «Pendiente».
- Citas: `dickey_fuller_1979`, `hubert_arabie_1985` y `hennig_2007`, con nota VERIFICAR copiada de
  la tesis; Said y Dickey (1984) y Kwiatkowski et al. (1992) como `[CITA PENDIENTE]`.

### `nSeries` (17 → 16)

El informe lo usa en el cap. 1 (párrafo de datos) y en el cap. 3 (datos, AE/LSTM, D17). En los
dos casos «16» es coherente con D16 y con la tesis. Los «17» escritos a mano que quedan (cap. 1,
«17 indicadores»; cap. 2, antecedentes) son del antecedente de Camiz et al. (2026), cifras
atribuidas a una fuente fichada, y la tesis los conserva igual. No quedan en el informe frases que
den 17 series como conjunto de esta tesis.

### E3

- `tesis/README.md`: la sección «Correspondencia con la tesis LaTeX» se rehízo con la numeración
  del PDF de la iteración 3b. Para obtenerla compilé una **copia** de `tesis_latex/` en mi
  scratchpad (exit 0) y leí sus `.aux`; el repositorio no se tocó. Tiene ahora tres tablas:
  secciones (incluidas las nuevas del cap. 2 y todas las del cap. 3), elementos formales del cap. 2
  (de 48 a 83 filas de la tesis) y elementos formales del cap. 3.
- `tesis/index.qmd`: estado de los caps. 1 a 4.
- Renders (Quarto 1.10.19): `quarto render tesis/` → exit 0, 0 avisos; `quarto render tesis/ --to
  docx` → exit 0, 0 avisos. En los nueve HTML no queda ningún `?@` (referencia cruzada sin
  resolver) ni ningún *shortcode* sin expandir; el `.docx` del borrador completo contiene las
  fechas de episodios y la tabla de Kish. `python3 herramientas/generar_cifras.py --comprobar` →
  exit 0.

## 3. Citas pendientes del informe (9 marcas `[CITA PENDIENTE]`)

| Capítulo | Marca | ¿Fila en el registro? |
|---|---|---|
| 1 (OE6) y 2 (`def-retencion`) | Frontier (1976), vara quebrada | **No.** Pedido al bibliotecario: agregar la fila |
| 2 | Terminología de cos² y contribuciones | Sí |
| 2 | Inversa de $\mathbf R$ y correlaciones parciales | Sí |
| 2 (nota de la HFC) | Denimal (2001) | Sí (fila de `denimal_2007`) |
| 2 | Camiz y Diblasi (2013) | Sí |
| 2 (`obs` del nulo de estructura) | Bootstrap por bloques conjunto | Sí (fila de `lahiri_2003`) |
| 3 | Said y Dickey (1984) | Sí (fila de `dickey_fuller_1979`) |
| 3 | Kwiatkowski et al. (1992), sin entrada en el `.bib` | Sí |

Conteo con `grep` sobre `origin/main` y sobre el estado actual: antes había 18 marcas (2 en el
cap. 1 y 16 en el cap. 2; la nota del 20-oct daba 15 porque agrupaba algunas); ahora hay 9 (1, 6
y 2). Se cerraron 12 (Atoche Murrieta en los dos capítulos, los cinco episodios, Jolliffe,
Rencher, Bruynooghe, Tukey y Lavit); dos cambiaron de objeto (la vara quebrada pasa a Frontier,
1976, en los dos capítulos, y Denimal 2001–2007 pasa a Denimal 2001) y se abrieron 3 (bootstrap
conjunto, Said y Dickey, Kwiatkowski et al.), igual que en la tesis. Ninguna referencia se citó
sin ficha y entrada.

## 4. Desviaciones respecto del encargo

1. **Capítulo 1 modificado** (el encargo nombra el cap. 2). El informe seguía diciendo «Ambas
   vías se ejecutan con el mismo código (decisión D2)» y tenía la marca de Atoche Murrieta, cosas
   que la tesis ya no sostiene tras `f01e744`. Dejarlo así contradecía la regla de derivación. Se
   trasladó solo ese diff, sin tocar objetivos ni hipótesis.
2. **`tesis/index.qmd`**: se actualizó la tabla de estado (caps. 1 a 4), que no figuraba en E3.
3. **Remisiones al cap. 2 escritas como texto** en el cap. 3 («capítulo 2, definición de …»):
   cada capítulo es una página aparte y una referencia cruzada entre páginas no se resuelve.
   Dentro del cap. 2 sí se usan referencias cruzadas de Quarto.
4. **Condensación** (sin añadir nada): sin demostraciones; enumeraciones de definiciones y
   proposiciones en línea; el contraejemplo de la Prop. 2.51(c) solo se describe; en la
   Prop. 2.72 se explicita $\mathbf G_b=\operatorname{diag}(b_1,\dots,b_p)$, que la tesis define
   en la prueba de la Prop. 2.33. El detalle está en la columna «Nota» del README.
5. **Entorno.** Quarto no estaba instalado y `github.com` responde 403 a través del proxy, así que
   no se pudo bajar el `.deb` ni el *tarball*. Se instaló el paquete oficial `quarto-cli` de PyPI
   (Quarto 1.10.19) en un entorno virtual del scratchpad. No quedó instalado en el sistema: una
   sesión futura debe repetir `python3 -m venv … && pip install quarto-cli`. Para recompilar la
   copia de la tesis instalé con `apt-get` `texlive-lang-spanish`, `texlive-bibtex-extra`, `biber`
   y `texlive-luatex`, como hizo el redactor.

## 5. Observaciones para el redactor LaTeX (no corregidas en el informe, que sigue a la tesis)

1. `sec:comparacion`, tras `prop:procrustes`: «La normalización de la distancia para el criterio
   de ventana (OE4) queda por definir». Con D10 y D17.2 el criterio de OE4 usa el RV de cargas y no
   Procrustes. ¿Sigue vigente la frase?
2. `sec:retencion`, frase inicial: «las fuentes están pendientes». Con Horn, Camiz y Pillar y
   Rencher y Christensen ya citados, solo queda pendiente Frontier (1976).
3. `sec:vacios`: el vacío 5 sigue diciendo «criterio **objetivo**», mientras que el aporte (4) dice
   ahora «un criterio» y lo lee como multiescala. Coherencia menor.
4. `01_introduccion.tex`, comentario antes del párrafo de datos: dice que las dimensiones las
   escribe `notebooks/05_pca.ipynb` en `data/results/`; la fuente vigente es
   `data/results/final/05_dimensiones.csv` (solo un comentario).
5. Siguen las dudas 1 y 2 del redactor (tolerancia al intervalo; OE3, OE4 e hipótesis en «dos
   vías»). El informe las reproduce tal como están en la tesis.

## 6. Pendientes y dudas para Roberto

1. **«&» en las citas narrativas** (de 3a, sin decidir): siguen saliendo «Camiz & Pillar (2018)» y
   «Newey & West (1987)», además de las 18 anteriores. La propuesta del filtro Lua
   `tesis/herramientas/apa_es.lua` (nota del 20-oct, §4) sigue a la espera del conforme. ¿Se
   activa?
2. **Dudas heredadas de la tesis**, que el informe no puede resolver por su cuenta: medición de la
   tolerancia (intervalo frente a extremos), reformulación de OE3, OE4 y la evaluación de las
   hipótesis en «dos vías», y confirmación de las fechas principales de los episodios.
3. **Pautas de la UNI**: el formato del informe sigue usando la guía provisional de 2018
   (`tesis/README.md`).
4. **Quarto en el entorno de las sesiones automáticas**: ¿se fija la instalación por PyPI como
   procedimiento estándar (anotarlo en `CLAUDE.md`, sección «Comandos»)? Es un cambio de
   configuración que no hice.
