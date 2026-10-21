# Auditoría · Iteración 3a, vuelta 2 (verificación final) · 21 de octubre de 2026

**Rama:** `iteracion-3a-wip` (HEAD `75dee3f`) · **Base del dictamen previo:** `264eed1` ·
**Dictamen previo:** `auditorias/2026-10-20_iteracion-3a.md` · **Auditor:** agente auditor (independiente)

## Dictamen: **APROBADO**

Los dos hallazgos mayores del dictamen previo (M-01 y M-02) están resueltos. De los doce menores,
diez están resueltos, N-12 sigue diferido a 3b (como preveía el dictamen) y N-02 está resuelto en los
documentos, aunque su fila del registro quedó desactualizada (se recoge en N-13). Hay **2 hallazgos
nuevos, ambos menores**: marcas de verificación que ya no reflejan el estado de las fichas. Ninguno
impide el conforme. La reproducibilidad completa (pytest, 05, cifras, Rmd, LaTeX y Quarto) se
verificó en copias y los CSV de `data/results/` quedaron idénticos byte a byte.

| Severidad | Previos abiertos | Nuevos |
|---|---|---|
| Bloqueante | 0 | 0 |
| Mayor | 0 (M-01 y M-02 resueltos) | 0 |
| Menor | 1 diferido (N-12) | 2 (N-13, N-14) |

## Alcance y método

Se comparó el árbol actual con la base mediante `git diff 264eed1 HEAD` y con la vuelta 1 mediante
`git diff 5002c36 HEAD`. La vuelta 2 (`75dee3f`) cambia el Rmd, `notebooks/05_pca.ipynb`,
`src/particion.py`, `tests/test_particion.py`, `tesis/registro_verificacion.md`, `tesis_latex/README.md` y
`tesis_latex/tesis.tex`. Se revisaron, además, los archivos de la vuelta 1 afectados por los hallazgos
(capítulos 1 y 2 de la tesis y del informe, `notacion.tex`, `decisiones.qmd`, `.bib` y fichas).

No se leyó `auditorias/notas/`. Todas las ejecuciones se hicieron en dos **copias** del repositorio en
el scratchpad del auditor (`scratchpad/v2/repo` para 05, las cifras y el Rmd; `scratchpad/v2/repo_tex`, una
copia limpia, para LaTeX y Quarto). El repositorio original no se modificó, salvo este dictamen. Los
guiones propios están en `scratchpad/v2/scripts/` (`ganancia_v2.py` y `particion_indep.py`).

## Estado de los hallazgos previos

| ID | Severidad previa | Estado | Evidencia |
|---|---|---|---|
| M-01 | Mayor | **Resuelto** | `registro_verificacion.md:36` tiene la fila de `tucker_1951`. La marca `\pendiente{… sin ficha}` se sustituyó por `\parencite{tucker_1951}\verificar{…}` (`02_marco_teorico.tex:1031`) y `[CITA PENDIENTE]`, por `[@tucker_1951][^v2-tk]` (`02_marco_teorico.qmd:360,477`). El Rmd lleva `[VERIFICAR: …]` (`:1326`). La entrada del `.bib` (`@techreport`, PRS Report 984, 1951) coincide con la ficha `papers/tucker_1951.qmd`, que es preliminar, y solo se atribuye la autoría habitual del coeficiente, con marca. Correspondencia entre marca y registro: ver N-13 (columna de ubicación desactualizada). |
| M-02 | Mayor | **Resuelto** | Prop. 2.5 (`prop:ganancia`, `02_marco_teorico.tex:176-240`) reformulada con media y varianza temporales sobre $T$ meses consecutivos: (a) es exacta sobre $P$ meses cuando $P$ es entero (incluido $P=2$) y vale como límite en $T$ para cualquier $P\ge2$ real. Se trata aparte $P=2$ (varianza $\varrho^2\cos^2\psi_0$, $\Delta x=2x$) y se excluye el caso degenerado $\cos\psi_0=0$. La demostración por sumas geométricas es correcta (cota uniforme $2/\lvert e^{ik\vartheta}-1\rvert$ si $e^{ik\vartheta}\ne1$, y suma nula sobre el período entero). El informe (`02_marco_teorico.qmd:66`) replica el enunciado literalmente. Comprobación numérica (`ganancia_v2.py`): **1 328 de 1 328 comprobaciones**. Se probó la identidad, (a) sobre el período y en el límite ($T=2\cdot10^5$), el valor $\varrho^2/2$ o $\varrho^2\cos^2\psi_0$, y (b) y (c), con $P\in\{2,3,4,5,6,7,12,24,96,240\}$, con $P$ no entero $\{2{,}5;\ 3{,}3;\ 13{,}7;\ 40{,}01;\ 100{,}5\}$, con 20 pares aleatorios $(\varrho,\psi_0,t_0)$ para cada $P$, y con $P=2$ para todo $T\in\{1,2,3,7,10\}$. Ya no queda la afirmación errónea «el promedio de cos² es 1/2» como hecho general: la línea 230 dice lo contrario para $P=2$, que es lo correcto. |
| N-01 | Menor | **Resuelto** | Las notas de la tesis coinciden con el registro y con el informe: Baldi y Hornik, «solo el DOI; el texto completo ya se leyó» (`01_introduccion.tex:59-61`, `02_marco_teorico.tex:1064`); Fisher, «páginas… solo en fuentes secundarias; número y DOI ya verificados» (`01_introduccion.tex:52`, `02_marco_teorico.tex:42`). |
| N-02 | Menor | **Resuelto en los documentos** | Ni la tesis (`:1035`) ni el informe (`:360`) llevan marca para `lorenzo_seva_ten_berge_2006`, coherentes con el registro («Cerrado (metadatos); contenido: solo resumen»), y lo que se le atribuye está en el resumen fichado. La columna de marcas del registro sigue citando una nota `v2-lst` del informe que no existe: N-13. |
| N-03 | Menor | **Resuelto** (en las líneas señaladas) | Rmd `:1183-1184`, `:1326`, `:1333`, `:1335` y `:1963-1966`, y NB05 celda 15: citan `granger_newbold_1974`, `phillips_1986`, `dickey_fuller_1979`, `kwiatkowski_et_al_1992`, `lorenzo_seva_ten_berge_2006` y `tucker_1951`, cada una con su marca vigente (KPSS: «sin entrada en el `.bib`», correcto). El mismo defecto subsiste en otros lugares que el dictamen previo no enumeró: N-14. |
| N-04 | Menor | **Resuelto** | Pies de tabla del Rmd (`:2140`, `:3684` y `:4386`): «más de 0,95, componentes iguales; entre 0,85 y 0,94, similitud aceptable (Lorenzo-Seva y ten Berge, 2006)». Coincide con la ficha (`papers/lorenzo_seva_ten_berge_2006.qmd:43-44,55`) y ya no afirma que «bajo 0,85» la componente sea «distinta». |
| N-05 | Menor | **Resuelto** | El rastro remite a la rama `archivo/v0.3-trimestral` (NB05 celda 0; `decisiones.qmd:82`), que ahora **existe en `origin`** (`git ls-remote`: `refs/heads/archivo/v0.3-trimestral` → `ff52c5e`). Se optó por la rama en vez del tag (el tag local ya no existe), y el texto es exacto. `CLAUDE.md` (regla 4) dice «`05` rehecho en mensual en la iteración 3a». |
| N-06 | Menor | **Resuelto** | `src/particion.py` existe: envuelve `camiz_port.fisher` y devuelve etiquetas, límites, cortes fechados y SCE. Revisión en la sección «Revisión de `src/particion.py`». |
| N-07 | Menor | **Resuelto** | `\pagenumbering{Alph}` en la portada (`tesis.tex:28-32`). Compilación limpia: 0 avisos de destino duplicado, 0 `Error in luaotfload` (luaotfload 3.26 se carga) y 0 `Font Warning`. |
| N-08 | Menor | **Resuelto** | El registro ya no usa números de línea, sino sección y etiqueta (`sec:validacion`), según la convención declarada en su encabezado. |
| N-09 | Menor | **Resuelto** | `notacion.tex:173` ($\tau$, distinto de $\tau_k$), `:179` ($c$), `:180` ($a_1,a_2$) y `:120` ($\prom{y}_{t_0,T}$ y $\vart_{t_0,T}$, nuevos en M-02). |
| N-10 | Menor | **Resuelto** | `tesis_latex/README.md:64-80` declara seis clases de excepciones. Se extrajeron todos los dígitos de `capitulos/*.tex` fuera del modo matemático y de las macros (ver «Contraste de la lista de excepciones»). Todos encajan en alguna clase. |
| N-11 | Menor | **Resuelto** | La iteración está confirmada en dos *commits* (`5002c36` y `75dee3f`) y la rama `iteracion-3a-wip` está en `origin` en `75dee3f`; el árbol está limpio. **Nota para el orquestador:** `origin/iteracion-3a` sigue en `264eed1`, de modo que, al integrar, debe tomarse `iteracion-3a-wip`. |
| N-12 | Menor | **Diferido a 3b** | Sin cambios, como preveía el dictamen previo (pendiente de la decisión I). |

## Hallazgos nuevos

| ID | Severidad | Archivo:línea | Evidencia | Acción requerida | Responsable |
|---|---|---|---|---|---|
| N-13 | Menor | `tesis/registro_verificacion.md:36, 37, 55` y fila de `tuhin_et_al_2025` | La columna «Marcas en los documentos» no refleja el estado actual. (1) `tucker_1951` (`:36`): describe la marca de la tesis como «`\pendiente`, que aún dice "sin ficha"» y la del informe como «`[CITA PENDIENTE]`, ídem», cuando hoy son `\verificar` y la nota `[^v2-tk]`. (2) `lorenzo_seva_ten_berge_2006` (`:55`): cita una nota `v2-lst` del informe que no existe (no aparece en `264eed1`, `5002c36` ni `HEAD`) y una marca del Rmd «desactualizada (N-03)» que ya se corrigió. (3) `granger_newbold_1974` (`:37`): dice «NB05, celda 15 (sin marca propia)», pero ya tiene marca propia. (4) La fila de `tuhin_et_al_2025` no recoge la marca de la tesis en cap. 2, «Validación externa» (`02_marco_teorico.tex:142`). En los dos sentidos, toda marca tiene su fila y toda fila con marcas apunta a la obra correcta: el defecto está solo en la descripción de la ubicación. | Actualizar la columna de marcas de esas cuatro filas. | Bibliotecario |
| N-14 | Menor | `R/tesis_ciclo_financiero.Rmd:362, 430, 492, 556, 1197, 1380, 1717, 1721, 1755, 1835, 2471, 2529, 2756`; `src/multivariado.py:90, 164, 182`; `src/remuestreo.py:19`; `src/series_tiempo.py:53` | Marcas «[VERIFICAR: sin ficha…]» o «propuesta para el bibliotecario» para obras que **ya tienen ficha** desde la vuelta 1: Horn (1965), Caliński y Harabasz (1974), Benzécri (1973), Bartlett (1950, 1951), Kaiser (1960, 1970), Kaiser y Rice (1974), Hubert y Arabie (1985), Künsch (1989) y Pyper y Peterman (1998). Es el mismo defecto de N-03 en ubicaciones que el dictamen previo no enumeró (las líneas `:362`, `:430` y `:1380` ya estaban así en `5002c36`). El registro sí lista estas ubicaciones y las obras, de modo que nada queda sin marcar: la marca solo dice algo que ya no es cierto. Se mantienen correctamente sin ficha la vara quebrada (`:1835`, en la parte que le toca), Adam (`:2889`) y Markov (`:2946`). | Sustituir «sin ficha» por la cita a la ficha con su pendiente vigente (por ejemplo, «Horn, 1965 [VERIFICAR: solo se leyó el resumen]»), en el Rmd y en los *docstrings* de `src/`. Puede hacerse en 3b. | Desarrollador |

## Revisión de `src/particion.py` y `tests/test_particion.py`

- **Corrección.** La prueba independiente `particion_indep.py` compara contra una programación dinámica
  propia (sin `camiz_port`) en 200 series de longitud 2 a 39, una de cada cinco con empates (valores
  redondeados), con $k=1,\dots,\min(n,6)$ y `maxcl` ∈ {`None`, $k$, $k+3$}: **3 474 de 3 474 casos
  correctos**. Se comprobó que la SCE informada es la óptima y la de las etiquetas devueltas, que las
  clases son contiguas y crecientes, que el último límite es $n$ y que cada corte es la posición
  0-based del inicio de la clase siguiente. El caso $k=n$ da SCE ≈ 0. Los errores de `k ∉ [1, n]` y de
  `maxcl < k` se señalan con `ValueError`.
- **Pruebas del módulo.** Las tres pruebas cubren la fuerza bruta (30 series, $k\in\{2,3,4\}$), el
  fechado con `PeriodIndex` y el caso $k=1$. Son pertinentes. `pytest tests/`: **12 de 12** pasan.
- **Estilo.** *Docstrings* y comentarios en español; el módulo declara su relación con el plan y con
  `camiz_port.fisher` y no duplica la recurrencia. Sin observaciones.

## Contraste de la lista de excepciones (N-10)

Dígitos escritos a mano en `capitulos/*.tex` fuera del modo matemático, de `\cite`/`\ref` y de las
macros, clasificados según `tesis_latex/README.md`:

- **Cifras atribuidas a una fuente fichada:**
  - 8–30 y 1–8 años (`drehmann_borio_tsatsaronis_2012`);
  - 17 indicadores, 1999–2020, 7/4/4 series, «otras 15» y 48 meses (`camiz_cerda_atoche_2026`; la
    ficha registra el PCA reducido a 15 series);
  - 0,7 (`camiz_et_al_2020`);
  - «S&P 500 entre 2000 y 2022» (`02_marco_teorico.tex:1193`; la ficha `tuhin_et_al_2025` dice
    «375 acciones del S&P 500… 2000–2022»).
- **Años de las citas:** 2002, 2007, 2001, 2013, 1977, 1988, 2010/2011 y «el trabajo de 2010».
- **Fechas de episodios:** COVID-19.
- **Numeración:** D1–D6, HT1–HT4, «paso 3», «Tabla 1», «regla 7», (1)–(4) y `06_epca.ipynb`.
- **Constantes matemáticas:** solo dentro de `\[…\]` o de entornos de ecuaciones.

Quedan dos tipos de dígitos no enumerados de forma expresa, que no son cifras de datos:

- los metadatos bibliográficos dentro de las notas `\verificar` (páginas 789–798, 1–27 y 843–852,
  «FKI-207-95» y la fecha del manuscrito, 25 de abril de 2026);
- las medidas de maquetación de la portada (`1.5cm`, `red!75!black`).

Conviene nombrarlos en la clase «Años de las citas» (como «metadatos bibliográficos») la próxima vez
que se edite el README. No se registra como hallazgo.

## Verificación de reproducibilidad

| Paso | Resultado |
|---|---|
| `pytest tests/` | Exit 0, **12 passed** (9 previas + 3 de `test_particion.py`) en 0,75 s |
| `jupyter nbconvert … --execute --inplace … notebooks/05_pca.ipynb` | Exit 0 en 16 s. En la copia, el notebook solo cambia en las marcas de tiempo de ejecución |
| CSV tras 05 | **114 de 114** CSV de `data/results/` idénticos byte a byte (md5 antes y después) |
| `python3 herramientas/generar_cifras.py --comprobar` | Exit 0 (`cifras.tex` y `_cifras.yml` coinciden con lo regenerado) |
| `Rscript -e "rmarkdown::render('R/tesis_ciclo_financiero.Rmd')"` | Exit 0 en **3 min 29 s**. 0 `Warning message` en el log y 0 bloques `## Warning` o `## Error` en el HTML |
| CSV tras el Rmd | **114 de 114** idénticos byte a byte |
| Paridad Python–R | `R_paridad_python.csv` (21 filas) y `niveles/R_paridad_python.csv` (28 filas): **49 filas, todas «sí»**, diferencia máxima 4,7e-11 |
| `latexmk -lualatex -cd tesis_latex/tesis.tex` (copia limpia, sin auxiliares) | Exit 0, 46 páginas, **0 citas o referencias indefinidas, 0 `Overfull`, 0 destinos duplicados**, 0 avisos de fuentes, biber sin avisos |
| `quarto render tesis/` | Exit 0 en 24 s, sin avisos de citas ni de referencias. Las notas `[^v2-tk]`, `[^v2-ey]` y `[^v2-horn]` se resuelven en el HTML |
| `quarto render tesis/ --to docx` | Exit 0, sin avisos |

## Referencias introducidas en los cambios

Obras nombradas en el diff de la vuelta 2 y en las secciones de la vuelta 1 afectadas por los hallazgos:

- **Con ficha y entrada en el `.bib`:** Tucker (1951), Lorenzo-Seva y ten Berge (2006), Granger y
  Newbold (1974), Phillips (1986), Dickey y Fuller (1979), Fisher (1958) y Drehmann et al. (2012).
- **Con ficha, sin `.bib` y marcada:** Kwiatkowski et al. (1992).
- **Sin ficha y marcada como tal:** Said y Dickey (1984), dentro del `[VERIFICAR]` de Dickey y
  Fuller, y recogida en la fila `dickey_fuller_1979` del registro.

**No se introdujo ninguna referencia inventada ni sin marcar.** No hay citas textuales nuevas de 15 o
más palabras.

## Lo que no se verificó, y por qué

- **Contenido de las fuentes:** sin acceso a los originales. Se contrasta contra las fichas, como en
  la vuelta 1.
- **Notebooks 08 y 09** (requieren `torch`): no cambiaron en 3a.
- **Sitio completo** (`quarto render` en la raíz) y `quarto publish`: fuera del alcance pedido. Solo se
  renderizó `tesis/` (HTML y docx).
- **Versión `version_asesor = TRUE` del Rmd:** no se volvió a renderizar en la vuelta 2. Los cambios
  del Rmd en esta vuelta son de texto y pies de tabla, fuera de los recuadros `.pregunta`.
- **Lista de símbolos:** se verificaron los símbolos de N-09 y los nuevos de M-02, no la lista entera.

## Para el orquestador y para Roberto

1. El dictamen permite el **conforme de la iteración 3a**. Al integrar en `main`, debe tomarse
   `iteracion-3a-wip` (`75dee3f`), no `origin/iteracion-3a` (`264eed1`).
2. N-13 y N-14 son correcciones de marcas y pueden hacerse al inicio de 3b.
3. Siguen abiertas, sin cambios, la decisión I (convención de fechado, N-12) y la reunión con el
   Dr. Camiz sobre la Parte C.
