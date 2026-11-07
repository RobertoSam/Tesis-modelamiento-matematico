# Auditoría · Iteración 3b (fase 3, cierre) · 29 de octubre de 2026

**Rama:** `iteracion-3b` (HEAD `38af0cd`, igual a `origin/iteracion-3b`) · **Base:** `origin/main` ·
**Alcance:** `git log origin/main..HEAD` (38 commits: D0–D12, DF, DX y DR del desarrollador; B1–B4
del bibliotecario; L1–L4 de la tesis; E1–E3 del informe) · **Auditor:** agente auditor
(independiente), sesión automática de seguimiento diario, sin Roberto presente.

## Dictamen: **APROBADO**, con observaciones

No hay hallazgos bloqueantes. Todas las ejecuciones (pytest, los ocho notebooks vigentes, el guion R
del nulo, el Rmd final en sus dos versiones, LaTeX y Quarto) terminan sin errores, y los 289 CSV de
`data/results/` quedan idénticos byte a byte. La paridad Python–R se confirma con una comparación
propia. Las proposiciones nuevas de L2 superan 25 368 comprobaciones numéricas sin ningún fallo.
Las reglas 6 y 7 se cumplen.

Hay **2 hallazgos mayores** que deben corregirse antes de integrar en `main`, en una vuelta del
bibliotecario y del desarrollador:

- **M-01:** el registro de verificación no se actualizó después de L1–L4 y E1–E3 (criterio 13).
- **M-02:** el mapa de cifras sigue leyendo 46 macros del antecedente de 17 series.

Hay además **4 hallazgos menores**. Con esto, criterio por criterio, se cumplen los 15 del plan y los
3 nuevos de la adenda, salvo el 13, que se cumple solo en parte.

| Severidad | N.º |
|---|---|
| Bloqueante | 0 |
| Mayor | 2 |
| Menor | 4 |

## Alcance y método

- **Material comparado.** Se compararon `origin/main` y `HEAD`: 287 archivos, entre ellos el Rmd
  final, `R/07b_nulo_estructura.R`, los notebooks 05, 05c, 06, 06c, 07b, 07c, 09a y 09b, los nuevos
  módulos de `src/`, `herramientas/`, 19 fichas nuevas y 12 modificadas, el `.bib` (48 → 67
  entradas), el registro, `decisiones.qmd` (D7–D17), los capítulos 1 a 3 de la tesis y del informe,
  `notacion.tex`, `cifras.tex` y `_cifras.yml`.
- **Referencias normativas.** El plan del 21 de octubre (§6) y la adenda del 26 de octubre (§3 y §4).
- **Notas de los agentes.** `auditorias/notas/` no se usó como evidencia. Una búsqueda de texto en
  todo el repositorio mostró de forma incidental dos líneas de las notas del desarrollador sobre el
  tag (N-01), que no sustentan ningún juicio de este dictamen.
- **Copias.** Todas las ejecuciones se hicieron en tres copias del repositorio dentro del scratchpad
  del auditor:
  - `a3b/repo`: notebooks;
  - `a3b/repo_R`: guion R y Rmd;
  - `a3b/repo_tex`: LaTeX, Quarto, pytest y pruebas de no regresión.

  El repositorio original no se modificó, salvo este dictamen: `git status` está limpio en `38af0cd`.
- **Guiones del auditor.** Están en el scratchpad, como en las auditorías previas:
  `/tmp/claude-0/-home-claude-tesis-modelamiento-matematico/9b7273bf-7f57-50b6-8ff4-4cb11a3cdb58/scratchpad/a3b/scripts/`.
  - `proposiciones_3b.py`: criterio 12;
  - `paridad_indep.py`: paridad propia;
  - `criterios_5_6.py`: criterios 5 y 6;
  - `criterio8_indep.py`: criterio 8;
  - `correr_nb.sh` y `correr_R.sh`: ejecuciones.
- **Entorno.** El entorno de la sesión no traía R, Quarto, Jupyter ni varios paquetes de TeX. Se
  instalaron así:
  - R 4.3.3 y los paquetes `rmarkdown`, `knitr`, `ggplot2`, `scales`, `tseries`, `dendextend` y
    `jsonlite` (paquetes de Ubuntu), con pandoc 3.1.3;
  - Quarto 1.10.19 (paquete `quarto-cli` de PyPI);
  - `nbconvert` 7.17.2 y `statsmodels` (en un entorno virtual del scratchpad);
  - `texlive-lang-spanish`, `biber`, `texlive-luatex` y `lmodern`.

  Aun con versiones distintas de las del desarrollador, los CSV salen idénticos byte a byte.

## Hallazgos

| ID | Severidad | Archivo:línea | Evidencia | Acción requerida | Responsable |
|---|---|---|---|---|---|
| M-01 | Mayor | `tesis/registro_verificacion.md` (todo el archivo; última modificación en `d1bf179`, 24-10, antes de L1–L4 del 27-10 y de E1–E3 del 28-10) | **Criterio 13 incumplido en parte.** (1) **Dos `\pendiente` nuevos sin fila:** «Qué vía mide qué» (`03_metodologia.tex:53`, `sec:met-vias`) y AE/LSTM con 16 series (`03_metodologia.tex:304`), con sus recuadros «Pendiente» en el informe. La tabla de marcas no bibliográficas (`:108`) aún dice que el cap. 3 está «por redactar». (2) **La columna de marcas contradice los documentos** en las filas de `atoche_murrieta_2022` (`:25`), `camiz_pillar_2018`/`rencher_christensen_2012` (`:29`), `jolliffe_2002` (`:31`), `denimal_2007` (`:32`), `tukey_1977` (`:34`), `lavit_1988` (`:35`) y `bruynooghe_1978` (`:49`): dicen «Tesis (`\pendiente`) e Informe (`[CITA PENDIENTE]`)», pero hoy se citan con `\textcite`/`\parencite` y `\verificar` o nota `[^v…]`. Las de `kish_1965` (`:54`), `newey_west_1987` (`:60`), `hennig_2007` (`:62`) y `lahiri_2003` (`:63`) dicen «Ninguna marca todavía», y las cuatro llevan `\verificar` en la tesis (`02_marco_teorico.tex:937, 1517, 1534`; `03_metodologia.tex:253`) y nota en el informe. Las marcas nuevas del cap. 3 de `dickey_fuller_1979`, `kwiatkowski_et_al_1992` (con Said y Dickey, 1984) y `hubert_arabie_1985` no figuran en sus filas (`:42`, `:43`, `:50`). (3) **Episodios** (`:79-97`): siguen anunciando «cinco `\pendiente`» en `sec:validacion` y en el informe, que ya no existen, y «unificación pendiente (D9)» en cada fila, aunque D9 está hecha (`3c416c2`). La fila de Kuczynski (`:96`) pide «confirmar la definición al cerrar D9». (4) **El Rmd final no está registrado:** el encabezado define «Rmd» como `R/tesis_ciclo_financiero.Rmd` (exploración), y ninguna fila menciona `R/ciclo_financiero_final.Rmd`, que lleva unas 25 marcas `[VERIFICAR: …]`. (5) Falta el conteo de marcas abiertas antes y después que pedía B4 en el propio registro. Ninguna marca de la tesis o del informe carece de ficha: el defecto es de registro, no de citas. | Hacer de nuevo B4 sobre el estado de `38af0cd`: una fila (o la ubicación correcta) para cada `\pendiente`, `\verificar`, `[VERIFICAR]` y `[CITA PENDIENTE]` de la tesis, el informe, el Rmd final y `src/`; poner al día la sección de episodios tras D9 y L1; actualizar la tabla de marcas no bibliográficas, y registrar el conteo antes y después. | Bibliotecario |
| M-02 | Mayor | `herramientas/cifras_mapa.csv:10-55`; resultado en `tesis_latex/cifras.tex` y `tesis/_cifras.yml` | De las 78 macros del mapa, 46 siguen leyendo el **antecedente de 17 series** (`data/results/*.csv` y `data/results/niveles/`). Eso contradice `data/results/LEEME.md:8` («no se consumen en la tesis, en el informe ni en `herramientas/generar_cifras.py`») y el docstring de `generar_cifras.py`. Por eso `cifras.tex` publica valores que no son los vigentes: `\inerciaPCUnoNiveles` = 67,2 (antecedente) frente a 65,2 en `final/05_pca_valores_propios.csv`, y `\nSeriesTS`/`\nSeriesDS`/`\nSeriesIndeterminadas` = 1/13/3 (suman 17, mientras `\nSeries` = 16) frente a 1/12/3 en `final/05_clasificacion_d5_resumen.csv`. Hoy **ningún capítulo usa esas 46 macros** (conteo: 0 usos en `capitulos/*.tex` y en `_capitulos/*.qmd`), por eso el hallazgo no es bloqueante. Pero cualquier uso futuro, por ejemplo en el capítulo 4, daría cifras del antecedente sin aviso. | Eliminar esas 46 filas del mapa o reapuntarlas a `data/results/final/` (y a `final/anexo/` para las transformadas), volver a generar `cifras.tex` y `_cifras.yml` y comprobar con `--comprobar`. Opcional: que `generar_cifras.py` rechace rutas fuera de `final/` y `data/referencia/`. | Desarrollador |
| N-01 | Menor | `data/results/LEEME.md:11`; `data/results/niveles/LEEME.md:10`; `R/ciclo_financiero_final.Rmd:109, 1063`; `notebooks/modelos_dl.py:533` | Estos textos afirman que el estado del antecedente «queda en el tag `v0.4-17series-dos-vias`», pero el tag no existe ni en local (`git tag -l`: solo `v0.1-transformadas` y `v0.2-niveles`) ni en `origin` (`git ls-remote --tags`). El commit `2be3665` sí está en la rama, así que el estado es recuperable. `linea_temporal.qmd:45` deja la subida como pendiente. | Crear y subir el tag sobre `2be3665` desde un entorno con permiso o, mientras no exista, remitir al commit `2be3665` en esos cinco lugares. | Desarrollador (la subida del tag, el orquestador o Roberto) |
| N-02 | Menor | `papers/congreso_2018.qmd:38`; `tesis/registro_verificacion.md:94` (fila COVID-19); `tesis_latex/capitulos/02_marco_teorico.tex:153-156, 222-225` | D7 y la `def:episodio` fechan por el «evento o anuncio **externo**». La ficha de `congreso_2018` califica la renuncia de Kuczynski como «evento interno» y aun así fecha un episodio, mientras que el registro descarta `pcm_2020` como fecha por ser «un evento interno: contexto, no fecha». El texto de la tesis no aclara si «externo» significa externo al análisis (lectura compatible con la regla 6) o extranjero. La propia tesis reconoce que las fechas son «casi todas» de eventos estadounidenses o globales (`:234-235`). No afecta a la regla 6: la fecha sale de una fuente fichada, no de las series. | Declarar en `def:episodio` (y en el informe) qué significa «externo». Después, aplicar el mismo criterio a `congreso_2018` y a `pcm_2020` en las fichas y en el registro. | Redactor LaTeX (definición); bibliotecario (fichas y registro); editor del informe (derivación) |
| N-03 | Menor | `tesis_latex/README.md`, clase «Parámetros de diseño del plan (provisional)» | Seis parámetros de diseño escritos a mano no están en `decisiones.qmd` ni en un CSV: ν = 3, paso 3, eje 2 de la regla del 06, media móvil de 12 meses, particiones en 3 y 4 clases, y percentil 95 de la razón *walk-forward*. El README los declara como excepción **provisional**, con un pendiente para el desarrollador. Se admiten (criterio 11), pero el pendiente no figura en ningún registro con responsable y fecha. | Exportarlos a un CSV de `data/results/final/` (p. ej., `parametros_diseno.csv`) y leerlos por macro, o registrarlos como decisión. | Desarrollador |
| N-04 | Menor | `tesis_latex/capitulos/02_marco_teorico.tex:1594-1602` (`obs:nulo-mixto` (c)); `src/remuestreo.py` | La observación declara que la rama TS del nulo mixto usa, para $n$ residuos, inicios sorteados para $n-1$ incrementos. Con $n' = 227$ (primo) y $\Lb \in \{12, 24, 36\}$ siempre se cubren los 228 meses, pero el residuo del último mes nunca se sortea como inicio de bloque, porque los inicios están en $\{1,\dots,n'-\Lb+1\}$. La tesis lo declara; no es un error de la demostración. Lo que falta es decidir si se corrige el código o se mantiene como convención. | Decidir y registrar: corregir el sorteo de la rama TS (inicios en $\{1,\dots,n-\Lb+1\}$, en Python y en R, con paridad) o dejarlo declarado como convención en `decisiones.qmd`. | Desarrollador |

## Verificación por criterio de aceptación (plan §6 y adenda §4)

| N.º | Criterio | Estado | Evidencia |
|---|---|---|---|
| 1 | pytest; `n_min` contra fuerza bruta; `aede` con $n_w$ ∈ {24, 36, 48} contra R | **Cumple** | `pytest tests/`: **51 passed** en 9,7 s. `test_particion.py::test_nmin_coincide_con_fuerza_bruta` y `test_camiz_port.py::test_aede_anchos_cortos_contra_R` (no se omite: 12 de 12 en `test_camiz_port.py`). Esta última compara con el antecedente de 17 series; con 16 series, la paridad de `aede` en grilla la cubren la fila 26 de `final/R_paridad_python.csv` y la comparación propia. |
| 2 | Notebooks y Rmd con exit 0, sin `Warning` ni `Error`, en las dos versiones; Rmd de exploración sin cambios | **Cumple** | 05 (16 s), 05c (6 s), 06 (9 s), 06c (11 s), 07c (35 s), 09a (13 s), 09b (6 s) y 07b (618 s, con las 200 réplicas): exit 0. `Rscript R/07b_nulo_estructura.R`: exit 0 (797 s). Rmd final con `version_asesor = FALSE` (123 s) y `TRUE` (122 s): exit 0, 0 `Warning` en los logs y 0 bloques `## Warning`/`## Error` en los HTML. La versión del asesor retira los 19 recuadros `.pregunta`. md5 de `R/tesis_ciclo_financiero.Rmd` = `c21946b6…`, igual al de `2be3665`. |
| 3 → adenda §3 | No regresión con 17 series | **Cumple** | `herramientas/no_regresion_05.py`: exit 0, 37 archivos (idénticos o ampliados con las columnas declaradas). `herramientas/no_regresion_dinamica.py`: exit 0. Los notebooks 06, 06c, 07c y 09a y los `R_*` de las secciones 4 a 6 coinciden byte a byte o difieren solo en las columnas nuevas declaradas (D17.1, D9). El nulo reproduce los $k^*$ y los perfiles RV del antecedente (Python, diferencia máxima 9,7e-17; R, 0). |
| 4 | Paridad en `final/` y `final/anexo/` | **Cumple** | `final/R_paridad_python.csv`: 55 filas; `final/anexo/R_paridad_python.csv`: 9 filas; **64 de 64 «sí»**, con las excepciones (Horn y réplicas 21–200) declaradas en las filas 3, 30 y 40. **Comparación propia** (`paridad_indep.py`, sin usar esas tablas): **31 de 31 pares** Python ↔ R coinciden. Diferencia absoluta máxima en valores pequeños: 9,1e-11. En el número de condición y en el χ², la diferencia absoluta es de 1,1e-9, que en relativo da 2,7e-13. En la estabilidad de la regla del 06, la única diferencia es el formato de fecha (AAAA-MM-DD frente a AAAA-MM). Tras volver a ejecutar R, los 47 CSV `R_*` reescritos son idénticos byte a byte a los versionados. |
| 5 (adenda: ≤ 16) | λ1 + λ2 + λ3 ≤ 16; $n_\omega = n_w$ con pesos uniformes; $n_w = 60$ reproduce `aede` | **Cumple** | `criterios_5_6.py`: máximo de λ1 + λ2 + λ3 = 15,56 en 1496 filas; $n_\omega = n_w$ en todas las filas con pesos uniformes; con $n_w = 60$ y pesos uniformes, las 169 ventanas coinciden con `camiz_port.aede` sobre 228 × 16 (tolerancia 1e-12). |
| 6 | `k_en_tope` y posición de cada $k^*$ en el nulo | **Cumple** | `final/06c_aede_cortes.csv` tiene `k_en_tope` (72 filas). `final/07b_nulo_estructura_kstar_posicion.csv` (72 filas) tiene p05/p50/p95, `prop_nulo_ge_obs`, `prop_nulo_le_obs` y `prop_nulo_en_tope`. |
| 7 (adenda) | Archivo único de episodios; claves con ficha y `.bib`; cero fechas a mano | **Cumple** | Leen `data/referencia/episodios_referencia.csv` el Rmd final (`:186`), el 05, el 09a, el 09b, el 07b (bordes) y `modelos_dl.py` (`:526-540`). El 06 no usa episodios. Las 11 claves tienen ficha y entrada en el `.bib`. La búsqueda de fechas de episodio entre comillas en `src/`, `modelos_dl.py`, el Rmd final, el guion R y los notebooks vigentes da **0**. N-12 queda cerrado. |
| 8 | Ruta sin `torch` reproduce `09_discriminacion_episodios.csv` con las fechas antiguas | **Cumple** | Recálculo propio sin `src/` (`criterio8_indep.py`): en las dos vías, todas las celdas coinciden al redondeo publicado (2 decimales). |
| 9 | Decisiones antes que sus resultados | **Cumple** | `53fdc5d` (D7–D14) es el primer commit de la rama, anterior a D3 (`a7ee103`), D9 (`3c416c2`), D11 (`14b8e13`), D10 (`0fd116c`) y D12 (`0ae1d39`). |
| 10 | N-14: sin marcas «sin ficha» para obras con ficha | **Cumple** | Las únicas marcas «sin ficha» que quedan (en el Rmd de exploración `:1336, 1384, 1395, 1838, 2892, 2949`) corresponden a obras realmente sin ficha: Said y Dickey, Engle y Granger, filtros, Frontier (vara quebrada), Adam y Markov. En el Rmd final y en `src/` no queda ninguna. |
| 11 | `latexmk` limpio; `--comprobar`; dígitos solo en macros o excepciones | **Cumple** | `latexmk -lualatex` sobre una copia limpia: exit 0, **75 páginas**, 0 `Warning` (ni de citas, ni de referencias, ni de fuentes), 0 `Overfull`, biber sin avisos. `generar_cifras.py --comprobar`: exit 0. Los dígitos fuera de modo matemático, citas y macros de los capítulos 1–3 caen todos en las clases de `tesis_latex/README.md`: años de citas, fechas de episodios, decisiones D1–D17, grilla {24, 36, 48, 60}, tolerancias de 3 y 6 meses, maxcl 10/15/20, $n_{\min}$ = 12, fechas de registro, nombres de notebooks y los parámetros provisionales de N-03. Ver también M-02. |
| 12 | Proposiciones nuevas de L2 comprobadas numéricamente | **Cumple** | `proposiciones_3b.py`: **25 368 comprobaciones, 0 fallos**. Detalle en la sección siguiente. |
| 13 | Cada `\pendiente`/`[VERIFICAR]` nuevo con fila; toda clave citada con ficha | **Parcial** | Las 56 claves citadas (las mismas en la tesis y en el informe) tienen entrada en el `.bib` y ficha; las 67 entradas del `.bib` tienen ficha. El registro, en cambio, no se actualizó: M-01. |
| 14 | Regla 7 | **Cumple** | `04_resultados.tex` y `04_resultados.qmd` no cambian (`git diff --stat` vacío). El cap. 3 (leído completo en las dos versiones) no tiene cifras de resultados ni conclusiones sobre la Parte C: «Qué vía mide qué» sigue en `\pendiente`. Las macros nuevas (episodios, $n_\omega$, $n_{\mathrm H}$, $L_{\mathrm b}$, réplicas) son de métodos y datos. Las 46 macros de resultados del antecedente no se usan en ningún capítulo (M-02). |
| 15 | Regla 6 | **Cumple** | Las 11 fechas de `episodios_referencia.csv` salen del texto de fichas de fuentes externas al análisis (Lehman, NBER 2010 y 2021, Bernanke, FOMC, Stocker et al., FMI 2016, Congreso 2018, USTR 2018 y 2020, OMS 2020b). Cada ficha registra la fecha que respalda. El fin de 2016-01 se toma de la frase del FMI («first increase in five months»), no del índice (`fmi_2016.qmd:55`). Ninguna fecha sale de las series ni de los cortes de Camiz et al. (2026). Matiz de lectura en N-02. |
| 16 (adenda) | Ningún CSV de `final/` con «Liquidez M2» | **Cumple** | `grep -r "Liquidez M2" data/results/final`: 0 archivos. D17 ratifica que no hay proyección suplementaria. |
| 17 (adenda) | Antecedentes idénticos a `2be3665` | **Cumple** | `git diff 2be3665 HEAD -- data/results ':!data/results/final'` solo agrega `LEEME.md` y `niveles/LEEME.md`; ningún CSV cambia. Los md5 de D4 coinciden con `decisiones.qmd`. |
| 18 (adenda) | D17 antes del primer resultado con 16 series | **Cumple** | `a933ace` (D17, 19:27) precede a `36458d7`, `7e70318` (primeros CSV dinámicos de `final/`, 20:22) y `0fd116c`. |

## Comprobación numérica de las proposiciones de L2 (criterio 12)

Guion propio: `proposiciones_3b.py`. Usa implementaciones independientes salvo donde la proposición
afirma algo sobre el código, que entonces se contrasta con el código.

- **`prop:kish`.**
  - (a) Cotas $1 \le n_\omega \le n_w$ con 3000 vectores de pesos aleatorios (algunos con ceros), y
    los casos de igualdad (uniformes; un peso igual a uno).
  - (b) Con $n_w$ = 2…120 y ν ∈ {0,1; 0,5; 1; 2; 3; 5}: igualdad si ν = 0, desigualdad estricta si
    $n_w \ge 3$ y $n_\omega = 2$ si $n_w = 2$. El peso de los extremos vale $e^{-\nu^2/4}$.
  - (d) El límite $c(\nu)$ por cuadratura coincide con $n_\omega/n_w$ para $n_w = 2\cdot10^5$
    (error < 1e-4) y está en (0, 1) para seis valores de ν; $c(3) = 0{,}782$.
  - Las macros 18,2 / 27,6 / 37,0 / 46,4 y 19 / 28 / 38 / 47 se recalculan aquí desde cero.
    `pesos_aede` y `n_kish` coinciden con la `def:pesos`.
- **`def:ventana` y `lem:ventana-mes`.**
  - Para todo $n_w \le 60$ y toda ventana de $n = 228$: conjunto de meses, centros que contienen
    cada mes y conteo $n_w$.
  - **Convención de fechado con el port** (pedida en D4 del plan): con $n_w$ ∈ {24, 36, 48, 60, 25},
    la etiqueta de la ventana 1 es la fila $1 + \lfloor n_w/2 \rfloor$ y la última, la fila
    $n - n_w + 1 + \lfloor n_w/2 \rfloor$. El λ1 de la ventana 1 es el de las filas $1..n_w$.
  - `def:borde`: `bordes_ventana` coincide con $c^{\mathrm{ent}}$ y $c^{\mathrm{sal}}$ en los
    6 episodios × 4 anchos.
- **`cor:regla06`.** En 50 casos aleatorios, la correlación sin ponderar de la ventana coincide con
  $\mR_t$ con pesos uniformes (calculada aquí y con `bstatw`).
- **`cor:fisher-factible` y `prop:fisher-monotonia`.**
  - Fuerza bruta propia en 120 trayectorias ($N$ = 4–14, $n_{\min}$ = 1–4, $q$ = 1–2, con empates):
    factibilidad si y solo si $Kn_{\min} \le N$, segmentos todos de longitud $n_{\min}$ si y solo si
    $N = Kn_{\min}$, y monotonía bajo la condición de (a) y con $n_{\min} = 1$.
  - `particion_fisher` con `n_min` da la SCE óptima.
  - El contraejemplo de (c) da $Q_3 = 0 < Q_4$, con la fuerza bruta y con `particion_fisher`.
- **`prop:ch`.** 2000 casos: $K^{\mathrm a} \ge K^{\mathrm h}$.
- **`prop:rv` y `prop:rv-cargas`.**
  - 300 pares de matrices de correlación con $p$ = 3–16 y $d \le p$: (a) la forma con
    $\mR^{[d]}$; (b) invariancia a rotación, permutación y signo; (c) con $d = p$ coincide con
    $\rho_{\mR}$ y con `dinamica.rv_correlacion`; (d) el centrado anula un eje de cargas iguales.
  - `coef_rv(centrar=False)` coincide con la definición.
- **`def:pares`.** Hay $n - 2n_w + 1$ pares disjuntos y contiguos, y el CSV publicado
  (`final/07b_nulo_estructura_rv.csv`, réplica 0) tiene exactamente ese número por ancho.
- **`lem:hac`.** En 400 series: identidad entre el estimador y la suma de cuadrados de sumas móviles,
  no negatividad y caso constante. `t_hac_media` reproduce la `def:hac`.
- **`prop:nulo-estructura`.** Con `serie_nula` y `medir` del repositorio: (a) los incrementos de la
  réplica son los observados en el orden de los bloques; (b) con una transformación afín por serie,
  la réplica es $\mX^{(\zeta)}\mathbf{G}_b$ y los $k^*$ y el RV no cambian; (c) acumular desde
  $\vx_1$ no cambia nada.
- **`prop:oe4`.**
  - Simulación de 400 conjuntos de perfiles intercambiables con dependencia entre posiciones
    ($B = 39$, $m = 15$). La versión simétrica respeta $\Pr(\widetilde{\pval} \le \alpha_0) \le
    \alpha_0$ en α0 ∈ {0,05; 0,1; 0,2; 0,5}, dentro del margen de Monte Carlo (0,0475 con α0 = 0,05).
  - La versión implementada (`criterio_oe4`) da 0,0375, coherente con la `obs:oe4`.
- **Revisión de las demostraciones.** Se leyeron las de `prop:kish` (Cauchy-Schwarz y sumas de
  Riemann), `lem:ventana-mes`, `cor:fisher-factible`, `prop:fisher-monotonia`, `lem:hac` (conteo de
  productos, $\bar m - k$ veces), `prop:nulo-estructura` y `prop:oe4` (conjunto $\mathcal{J}$ con
  $\#\mathcal{J} \le k$). No se encontraron errores.

## Coherencia entre documentos

- **Informe ↔ tesis.**
  - El cap. 3 del informe reproduce el cap. 3 de la tesis sección por sección (tabla de
    correspondencia de `tesis/README.md:82-94`) y con las mismas definiciones (`def-regla-d5`,
    `def-walkforward`).
  - Las definiciones y proposiciones nuevas del cap. 2 del informe (`prp-kish`, `lem-ventana-mes`,
    `def-borde`, `prp-fisher-monotonia`, `lem-hac`, `def-nulo-estructura`, `def-oe4`, `prp-oe4`,
    `def-tolerancia` y `def-confirmada`) tienen el mismo enunciado que en la tesis.
  - Las mismas 56 claves se citan en los dos documentos. Toda obra con `\verificar` en la tesis
    lleva nota `VERIFICAR` en el informe, y viceversa. Hay 11 `\pendiente` en los caps. 1–3 de la
    tesis y 11 marcas `[CITA PENDIENTE]` o «Pendiente» en el informe.
- **Cifras.** El informe usa las mismas macros, vía `_cifras.yml`. Con 16 series, ninguna cifra
  difiere entre la tesis, el informe y `data/results/final/`.
- **Notación.** Los símbolos nuevos de L2 y L4 tienen su macro en `notacion.tex` y su fila en la
  lista de símbolos. La compilación no deja ninguna macro indefinida.
- **Decisiones.** El texto respeta D1–D17. D15 se presenta como propuesta reversible sujeta a la
  reunión N (`03_metodologia.tex:43-48`), y D11 se respeta: el CH no es selector. Las definiciones
  operativas que no fijan las decisiones se declaran como tales (`03_metodologia.tex:356-369`) y
  quedan como preguntas para el asesor. No hay citas textuales de fuentes de 15 palabras o más; la
  única cita larga (16 palabras, `02_marco_teorico.tex:1298`) reproduce el texto de D12 del propio
  registro de decisiones.
- **Estructura MMC102.** El cap. 3 del informe conserva «Metodología» y «Desarrollo del modelo
  matemático y computacional». El estilo es académico, impersonal y en español.

## Verificación de reproducibilidad

| Paso | Resultado |
|---|---|
| `pytest tests/` | Exit 0, **51 passed** (9,7 s) |
| Notebooks 05, 05c, 06, 06c, 07c, 09a, 09b, 07b (`nbconvert --execute --inplace`, copia) | Exit 0 en todos. 07b, con 200 réplicas: 10 min 18 s |
| CSV tras los notebooks | **289 de 289** idénticos byte a byte (md5). Solo cambian 7 PNG de `reports/figures/final/` (metadatos de matplotlib); no son cifras |
| `Rscript R/07b_nulo_estructura.R` | Exit 0 (13 min 17 s) |
| `rmarkdown::render('R/ciclo_financiero_final.Rmd')`, versiones `FALSE` y `TRUE` | Exit 0 en las dos; 0 avisos; 0 bloques de aviso o error en los HTML |
| CSV tras R | 47 CSV reescritos; **289 de 289** idénticos byte a byte |
| `no_regresion_05.py` / `no_regresion_dinamica.py` | Exit 0 / exit 0 |
| `generar_cifras.py --comprobar` | Exit 0 |
| `latexmk -lualatex -cd tesis_latex/tesis.tex` (copia limpia) | Exit 0, 75 páginas, 0 avisos, 0 `Overfull`, biber limpio |
| `quarto render tesis/` y `--to docx` | Exit 0 en los dos, sin avisos. En el HTML no quedan `?@clave`, `citeproc-not-found` ni *shortcodes* `meta` sin resolver |

## Referencias introducidas en la iteración

- **19 entradas nuevas del `.bib`.** Se contrastaron con su ficha en autores, año, título, fuente,
  volumen, número, páginas y DOI/URL: coinciden todas. Cada entrada con un pendiente lleva el campo
  `verificar` con el mismo motivo que la ficha.
- **Fichas que solo localizan la obra** (Jolliffe, Tukey, Lavit, Bruynooghe, Rencher, Lahiri y
  Hennig). El texto solo les atribuye el aporte general o la fuente del método, siempre con
  `\verificar`.
- **Camiz y Pillar (2018).** El texto les atribuye la generalización de Rencher de la prueba de
  Bartlett y la atribución de la vara quebrada a Frontier. Ambas cosas constan en la ficha
  (sección 4).
- **Sin ficha y marcadas como `\pendiente`:** Frontier (1976), Camiz y Diblasi (2013), Denimal
  (2001), Said y Dickey (1984), la fuente del bootstrap por bloques conjunto y Kwiatkowski et al.
  (ficha preliminar sin `.bib`).

**No se introdujo ninguna referencia inventada ni sin marcar.**

## Lo que no se verificó, y por qué

- **Contenido de las fuentes.** No hay acceso a los originales; se contrastó contra las fichas.
- **Notebooks 08 y 09.** Requieren `torch`, que sigue ausente; tampoco cambiaron en 3b (D17.4).
- **`modelos_dl.py`.** Solo se revisó el cambio (lectura del CSV de episodios); no se ejecutó, por
  la misma razón.
- **Rmd de exploración.** No se volvió a renderizar: su md5 es el de `2be3665`.
- **Sitio completo** (`quarto render` en la raíz) y `quarto publish`: fuera del alcance de la
  auditoría y de la tarea automática.
- **Equivalencia exacta de entornos.** R, Quarto y TeX se instalaron en la sesión con versiones que
  pueden diferir de las del desarrollador. Aun así, los CSV coinciden byte a byte. No se compararon
  los PDF ni los HTML byte a byte.
- **Tag `v0.4-17series-dos-vias`.** No se pudo comprobar su contenido porque no existe (N-01).

## Para el orquestador y para Roberto

1. **Antes de integrar en `main`**, una vuelta: el bibliotecario rehace B4 (M-01) y el desarrollador
   corrige el mapa de cifras (M-02). Los menores N-01, N-03 y N-04 pueden ir en la misma vuelta del
   desarrollador; N-02 requiere al redactor LaTeX, al bibliotecario y al editor.
2. La definición de auditor (`.claude/agents/auditor.md`, punto 10) todavía toma como tamaño de
   referencia 228 × 17 y 227 × 17. Desde D16 son 228 × 16 y 227 × 16 (`CLAUDE.md` de la rama ya está
   al día). Conviene actualizarla; este dictamen aplicó D16.
3. Siguen abiertos la reunión N con el Dr. Camiz (Parte C, sección «Qué vía mide qué»), la consulta
   sobre el representante de clase de la HFC y la definición de transición fuera del nulo
   (`def:fuera-nulo`), declaradas en la tesis como preguntas para el asesor.
4. La regla 7 sigue vigente: este dictamen no autoriza a publicar resultados.
