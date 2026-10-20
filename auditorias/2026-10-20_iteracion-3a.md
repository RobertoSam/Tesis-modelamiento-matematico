# Auditoría · Iteración 3a · 20 de octubre de 2026

**Rama:** `iteracion-3a` · **Base:** `264eed1` · **Auditor:** agente auditor (independiente)

## Dictamen: **APROBADO**, con observaciones

No hay hallazgos bloqueantes. Los 11 criterios de aceptación de la sección 7 del plan se cumplen,
salvo el criterio 8, que se cumple de forma parcial: una marca `\pendiente` no tiene fila en el
registro (M-01). Quedan **2 hallazgos mayores** y **12 menores**. Los mayores deben corregirse
antes de integrar en `main` (una vuelta: bibliotecario y redactor LaTeX).

| Severidad | N.º |
|---|---|
| Bloqueante | 0 |
| Mayor | 2 |
| Menor | 12 |

## Alcance y método

Se auditaron los cambios que muestran `git status` y `git diff HEAD` (base `264eed1`): 05 mensual,
`src/multivariado.py`, `src/remuestreo.py`, `src/series_tiempo.py`, el Rmd, `herramientas/`,
`tesis_latex/`, `tesis/` (capítulos 1 a 3, README, metadatos), el port de Camiz (D6: `src/camiz_port.py`,
`notebooks/999_port_camiz.ipynb`, `tests/` y `data/results/999_port_*`), las 31 fichas nuevas, las
2 fichas modificadas, el `.bib` (47 entradas) y el registro. La referencia fue la sección 7 del plan
`asesoria/2026-10-20_plan-iteracion-3.md` y las decisiones D1 a D6 de `decisiones.qmd`.

No se leyó `auditorias/notas/`. Todas las ejecuciones se hicieron en **copias** del repositorio en el
scratchpad del auditor, de modo que el material auditado no se modificó. Los guiones de verificación
están en `scratchpad/auditor_3a/scripts/` (`d5_indep.py`, `proposiciones.py`, `port_indep.py`,
`boot_nulo_indep.py`).

## Hallazgos

| ID | Severidad | Archivo:línea | Evidencia | Acción requerida | Responsable |
|---|---|---|---|---|---|
| M-01 | Mayor | `tesis_latex/capitulos/02_marco_teorico.tex:994`; `tesis/_capitulos/02_marco_teorico.qmd:360`; `tesis/registro_verificacion.md` | `\pendiente{fuente primaria del coeficiente, Tucker (1951); sin ficha}` y `[CITA PENDIENTE: … Tucker (1951)…]` no tienen fila en el registro (`grep -i tucker` sobre el registro: 0 coincidencias). Incumple el criterio 8 y la regla 2. | Añadir la fila de Tucker (1951) en el registro, con la ubicación en los dos documentos. | Bibliotecario |
| M-02 | Mayor | `tesis_latex/capitulos/02_marco_teorico.tex:183-186` y `:200-201` (Prop. 2.5 (a)); `tesis/_capitulos/02_marco_teorico.qmd:66` | La demostración afirma que «el promedio de cos² sobre un período es 1/2». Con $t\in\mathbb Z$ es falso para $P=2$: el promedio vale $\cos^2\psi_0$ (comprobado: 0,848 con $\psi_0=0{,}4$). Para $P$ no entero, «promediada sobre un período» no está definido en tiempo discreto. La **conclusión** (a) es correcta: la razón de varianzas vale $\gamma(P)^2$ para todo $P$ entero $\ge2$ y, para cualquier $P$, como promedio de largo plazo. Así lo verificó el guion `proposiciones.py`. El resto de la proposición y de su demostración es correcto. | Reformular (a): para $P$ entero $\ge3$, el promedio sobre $P$ meses consecutivos; o, en general, el promedio de largo plazo $\lim_T \frac1T\sum_t$, excluyendo $\vartheta=\pi$, o tratando aparte $P=2$, donde la razón también es $\gamma^2=4$. El informe repite el enunciado y debe alinearse después. | Redactor LaTeX; después, editor del informe |
| N-01 | Menor | `tesis_latex/capitulos/01_introduccion.tex:52,59-61`; `02_marco_teorico.tex:42,1021-1023` | Las notas `\verificar` de la tesis no están al día respecto de las fichas y del registro. Baldi y Hornik (1989) figura como «texto completo no consultado; ambas fichas son preliminares», pero la ficha registra «texto completo leído» y el registro deja pendiente solo el DOI. En Fisher (1958), la tesis pide «número (284) y DOI», mientras que el registro los da por respaldados y deja pendientes las páginas. El informe sí está al día (`01_introduccion.qmd:60,62`), de modo que tesis e informe difieren en el estado de verificación. | Actualizar las notas `\verificar` de la tesis con el registro vigente. | Redactor LaTeX |
| N-02 | Menor | `02_marco_teorico.tex:996`; `02_marco_teorico.qmd:469`; `registro_verificacion.md:47` | `lorenzo_seva_ten_berge_2006` lleva `\verificar{se leyó el resumen… no el texto}` en los dos documentos, pero el registro lo marca «Cerrado · Ninguno». | Unificar: o el registro conserva la fila abierta para el contenido, o se retira la marca. | Bibliotecario |
| N-03 | Menor | `R/tesis_ciclo_financiero.Rmd:1324,1332,1334,1962-1964`; `notebooks/05_pca.ipynb` (celda 15) | Marcas desactualizadas: «Dickey-Fuller… [VERIFICAR: sin ficha]», «Phillips, 1986 [VERIFICAR: sin ficha]» y «umbrales de congruencia… no tienen fuente fichada». Ya existen las fichas `dickey_fuller_1979`, `phillips_1986`, `granger_newbold_1974` y `lorenzo_seva_ten_berge_2006`. | Citar las fichas con la marca de lo que sigue pendiente. KPSS se mantiene sin `.bib` (correcto) y Perron no se usa (correcto). | Desarrollador |
| N-04 | Menor | `R/tesis_ciclo_financiero.Rmd:2138,3682` (pies de tabla) | «sobre 0,95: la misma componente; bajo 0,85: distinta». La ficha de Lorenzo-Seva y ten Berge (2006) solo respalda 0,85–0,94 como «similitud aceptable» y ≥ 0,95 como «iguales». Que por debajo de 0,85 la componente sea «distinta» no está en la ficha. | Redactar según la ficha y citarla. | Desarrollador |
| N-05 | Menor | `notebooks/05_pca.ipynb` (celda 0); `decisiones.qmd:81-83`; `CLAUDE.md` (regla 4) | El notebook dice que la versión trimestral «queda en la rama `archivo/v0.3-trimestral`», que no existe: hay un **tag local** `v0.3-trimestral` (ff52c5e) sin publicar en `origin`. D3 sigue diciendo que los `05_*` trimestrales «siguen en el repositorio hasta que se rehaga 05», cuando ya se retiraron, y la regla 4 de `CLAUDE.md` mantiene «`05` por rehacer». | Corregir el rastro en el notebook y en D3 (tag `v0.3-trimestral`) y publicar el tag. La actualización de `CLAUDE.md` le corresponde al orquestador. | Desarrollador (y orquestador) |
| N-06 | Menor | `src/` | El plan (sección 7, desarrollador 1) pedía `src/particion.py`, que no se creó. La partición de Fisher está en `src/camiz_port.py` (`fisher`) y se verifica en `tests/`. | Crear el módulo o registrar el cambio de plan. | Desarrollador |
| N-07 | Menor | `tesis_latex/tesis.log` | `Error in luaotfload: reverting to OT1`, avisos de fuentes (`OT1/lmr`, `T1/lmr`) y `ignoring duplicate destination with the name 'page.I'`. El PDF es correcto: fuentes Type 1 incrustadas (Nimbus Sans, CM), sin Type 3 y con acentos, «», ¿ y ñ bien extraídos. | **Aceptable** para 3a: el preámbulo lo documenta y lo resuelve con `fontenc`/`newunicodechar`. Conviene instalar `texlive-luatex` (luaotfload) antes de fijar la tipografía final o de adoptar la plantilla UNI, porque sin él no se puede usar `fontspec` ni una fuente OpenType. El destino duplicado `page.I` se corrige con `\pagenumbering` o con `hypertexnames=false`. | Redactor LaTeX |
| N-08 | Menor | `tesis/registro_verificacion.md:70` | Remite a `02_marco_teorico.tex:146–150`; las marcas de episodios están en las líneas 147–151. | Corregir el rango (o citar la etiqueta `sec:validacion`). | Bibliotecario |
| N-09 | Menor | `tesis_latex/notacion.tex` | Faltan en la lista algunos símbolos auxiliares: $c$ (Prop. 2.41 (a)), $a_1,a_2$ (Prop. 2.41 (b)) y $\tau$ como mes de transición (Def. 2.2, distinto de $\tau_k$). Los demás símbolos de los capítulos 1 y 2 revisados por muestreo están definidos. | Añadirlos. | Redactor LaTeX |
| N-10 | Menor | `tesis_latex/capitulos/01_introduccion.tex:15,26,28`; `02_marco_teorico.tex:28-40,67-75,544` | Dígitos escritos a mano: «8 a 30 años», «1 a 8 años», «17 indicadores», «1999», «2020», «7/4/4 series», «48 meses» y «0,7». No son datos de la tesis sino hechos de la literatura, y todos están respaldados por las fichas `drehmann_borio_tsatsaronis_2012`, `camiz_cerda_atoche_2026` y `camiz_et_al_2020`. El plan, sin embargo, pide una **lista de excepciones** declarada (criterio 6), y no existe. | Declarar la lista de excepciones en `tesis_latex/README.md`: años de cita, numeración y cifras atribuidas a una fuente fichada. | Redactor LaTeX |
| N-11 | Menor | Árbol de trabajo | Toda la iteración está sin *commit* en `iteracion-3a` (`git status`: 137 entradas). El ciclo exige respaldar el trabajo en la rama. | Hacer el *commit* en `iteracion-3a` antes del conforme. | Orquestador |
| N-12 | Menor | `notebooks/05_pca.ipynb` (celda 1); Rmd (`funciones`) | Las bandas de episodios de las figuras usan fechas sin fuente, aunque marcadas `[VERIFICAR]`. No vulneran la regla 6 (no se derivan de las series), pero hay fuentes ya fichadas (`lehman_brothers_2008`, `bernanke_2013`, `oms_2020b`…) a la espera de la decisión I. | Mantenerlas marcadas hasta la decisión I y unificarlas en 3b. | Desarrollador (3b) |

## Verificación por criterio de aceptación (plan, sección 7)

| # | Criterio | Resultado | Evidencia |
|---|---|---|---|
| 1 | 05 se ejecuta con nbconvert; `assert` y CSV | **Cumple** | Exit 0 en 16 s. `assert` 228 × 17 y 227 × 17, calendario continuo y sin faltantes. Escribe `05_pca_contraste_tendencia`, `05_pca_tendencia_componentes`, `05_tendencia_series`, `05_nulo_*` y `05_dimensiones`. **Todos los CSV de `data/results/` (118) quedaron idénticos byte a byte** tras volver a ejecutar 05, 999 y el Rmd. |
| 2 | Rmd con exit 0, sin Warning ni Error; paridad | **Cumple** | Render en 2 min 44 s, exit 0, sin avisos en el log ni en el HTML. `R_paridad_python.csv`: 21 + 28 = **49 filas, todas «sí»**, con una diferencia máxima de 4,7e-11. Port: **32 de 32** filas de aceptación coinciden. |
| 3 | El nulo reproduce el HTML | **Cumple** | Recálculo propio con los índices compartidos: con deriva, 0,902 / 0,015 / 0,212 (r̄ 0,932); sin deriva, 0,004 / 0,592 / 0,950 (0,017). Al redondeo de R coincide con 0,90; 0,01; 0,21; 0,93 y 0,00; 0,59; 0,95; 0,02. La mediana del PC1 con deriva es 74,59. |
| 4 | `generar_cifras.py` idempotente; mapa → CSV | **Cumple** | Dos ejecuciones dan el mismo md5 (`cifras.tex` b9638de2…, `_cifras.yml` 9727ea01…), iguales a los versionados. `--comprobar`: exit 0. Son 54 macros y cada fila del mapa apunta a un CSV y a una fila únicos (el guion lo exige). |
| 5 | latexmk sin indefinidas ni cajas > 10 pt | **Cumple** | Compilación desde cero: exit 0, 45 páginas, 0 citas o referencias indefinidas, 0 `Overfull`, biber sin avisos. Ver N-07. |
| 6 | Sin números de datos a mano en `capitulos/*.tex` | **Cumple** (con N-10) | Las cifras de datos (228, 227, 17 y las fechas) entran por macro. Las macros de resultados (inercias, KMO, clases D5, nulo…) están definidas pero **no se usan** en ningún capítulo ni en el informe. |
| 7 | Símbolos en `notacion.tex` | **Cumple** (con N-09) | Lista de símbolos amplia; faltan algunos auxiliares. |
| 8 | `\pendiente` y `[VERIFICAR]` en el registro; clave ↔ ficha | **Parcial** | 28 claves citadas en la tesis y 47 en el `.bib`, todas con ficha. Sin ficha y sin `.bib`, `kwiatkowski_et_al_1992` (correcto). Los metadatos del `.bib` coinciden con las fichas (año, volumen, página inicial y DOI). Falta Tucker (1951) en el registro (M-01). |
| 9 | Proposiciones verificadas numéricamente | **Cumple** (con M-02) | `proposiciones.py`: 48 de 48 comprobaciones (ver la tabla siguiente). |
| 10 | Informe sostenido por la tesis; render sin advertencias | **Cumple** (con N-01) | `quarto render tesis/` y `--to docx`: exit 0, sin avisos de citas ni referencias. Los shortcodes `meta cifras.*` se resolvieron. Capítulos 1 y 2 del informe sin contenido nuevo; la notación es la de `notacion.tex` (LSTM: $\mathbf g^{\mathrm e},\mathbf g^{\mathrm o},\mathbf g^{\mathrm s},\mathbf s_t$; «cal», «cong»). |
| 11 | Capítulo de resultados sin cambios | **Cumple** | `tesis/_capitulos/04_resultados.qmd` no figura en el diff. `tesis_latex/capitulos/04_resultados.tex` contiene solo `\pendiente` (regla 7). |

## Puntos de especial atención

**D5 (regla TS/DS).** La especificación es fija y está declarada en `src/series_tiempo.py:20-23` y en el
Rmd (`:598-615`, con `stopifnot` sobre los rezagos):

- ADF con constante y tendencia, 6 rezagos, sin selección automática (`autolag=None`);
- KPSS con nula de tendencia y 4 rezagos del núcleo de Bartlett;
- α = 0,05;
- p-valores interpolados en las tablas de `tseries`, que comprobé contra el código de `tseries`.

Los 6 y 4 rezagos son los valores por defecto de `tseries` para n = 227–228. **Recalculé por mi cuenta**
el PCA y las pruebas, con una regresión ADF escrita a mano además de `statsmodels`:

- valores propios en niveles 11,417 / 3,104 / 1,210 / 0,494, inercia del PC1 = 67,16 % y r(PC1, t) = 0,9926;
- estadísticos ADF y KPSS de PC1–PC4 idénticos a los del CSV en seis decimales;
- clasificación: niveles **DS, DS, DS, DS**; transformadas **TS, TS, TS, indeterminada**; series en
  niveles **1 TS, 13 DS y 3 indeterminadas** (TS: EMBIG; indeterminadas: crédito de consumo, TIPMN y PBI).

La clasificación no cambia si se usan los p-valores de MacKinnon en lugar de los de `tseries`. Casos
cerca del umbral: PC3 en niveles (KPSS p = 0,043), tasa de referencia (ADF p = 0,057) y PBI (ADF
p = 0,048).

**Paridad (8b).** El Rmd cambió, se renderiza y sus 49 filas coinciden. Comprobé por mi cuenta una muestra:

- KMO global (0,8624), χ² de Bartlett (12 210) y número de condición (67 647) en niveles;
- percentil 5 de la congruencia bootstrap con L = 24 (0,934 / 0,793 / 0,799 / 0,608), con mi propio
  código y los índices de R;
- el nulo completo (3 000 réplicas);
- en el port, comparé columna por columna `999_port_*` con `R_*` en las dos vías: aede, jerarquía HFC y
  cofenética, con una diferencia máxima de 5,7e-14 y el texto idéntico.

Además, una HFC propia por **definición** (argmin $\mu_2$, búsqueda exhaustiva) reproduce los tamaños y los
valores propios de todos los nodos de `R_hfc_jerarquia.csv` en las dos vías (diferencia ≤ 2,7e-14).
`pytest tests/`: 9 de 9 pruebas pasan.

**Parámetro `version_asesor`.** Renderizado con `version_asesor = TRUE`: exit 0. Se retiran los 32
recuadros `.pregunta` y no queda ningún `:::` suelto. La única mención restante de «Para Roberto» es
la regla CSS de la clase. Las tablas de interpolación de `src/series_tiempo.py` se contrastaron con el
código de `tseries` 0.10-55 instalado (`adf.test`, `kpss.test`, `lshort`) y coinciden.

**Proposiciones (`proposiciones.py`).**

| Proposición | Verificación numérica | Lógica de la demostración |
|---|---|---|
| 2.5 ganancia | Identidad con error < 1e-11 para P ∈ {2, 3, 5, 6, 7, 12, 24, 96, 240, 13,7}; (b) y (c) en P = 2…399 | Correcta salvo el paso de (a) (M-02) |
| 2.9 PCA | J(V_d) = Σλ_{>d}; 2 000 bases aleatorias por encima de la cota; invariante a la base | Correcta |
| 2.13 cos² | (a)–(d) con datos reales | Correcta |
| 2.19 det R | 0 ≤ det ≤ 1; χ² de Bartlett recalculado | Correcta |
| 2.23 HFC hojas | λ₁ = 1 + \|r\| en las 5 fusiones hoja–hoja de `R_hfc_jerarquia.csv` (error 4e-15); la primera fusión es M2–M3 | Correcta |
| 2.24 inercia HFC | μ₁(raíz) + Σμ₂ = 17 en las dos vías | Correcta |
| 2.30 correlación ponderada | (a)–(d) en 3 ventanas reales con pesos gaussianos (ν = 2, $n_w$ = 24); rango ≤ $n_w$ − 1 si $n_w$ ≤ p | Correcta |
| Obs. 2.31 | El ejemplo da 3/4 | Correcta |
| 2.36 Fisher | Recurrencia = fuerza bruta en 40 trayectorias (K ≤ 4, $n_{\min}$ ∈ {1, 2}, q ∈ {1, 2}) | Correcta |
| 2.38 CH | 0 violaciones de $K^a ≥ K^h$ en 741 trayectorias; coherente con el port (transformadas: k gl = 9, k − 1 gl = 8) | Correcta |
| 2.41 RV y 2.43 Procrustes | Rango, invariancias y optimalidad frente a 3 000 rotaciones | Correctas |
| 2.46 autoencoder lineal | Cota alcanzada; 3 000 pares (A, B) aleatorios por encima; mínimos cuadrados alternados convergen a BA = V_dV_dᵀ (8e-13); pesos atados A = O V_dᵀ | Correcta |

**Citas.** Lo que el texto atribuye a cada obra está respaldado por su ficha:

- Camiz et al. (2026): 17 series, 1999–2020, grupos de 7, 4 y 4, ventana de 48 meses elegida por
  experimentación;
- Drehmann et al. (2012): 8–30 y 1–8 años, exclusión de las acciones, «recesión inconclusa»;
- Tuhin et al. (2025), Hinton y Salakhutdinov (2006), Camiz et al. (2020) (umbral 0,7 vía Jolliffe) y
  Camiz y Roig (2011) (dos anchos).

Con fichas preliminares (Fisher, Horn, Kaiser, Bartlett, Caliński-Harabasz, Robert-Escoufier, Pyper-Peterman,
Bourlard-Kamp) solo se atribuye el aporte general, con `\verificar`. Benzécri (1973) se cita solo como
tradición, sin cita textual ni atribución de la fórmula *laisser parler les données*. Perron (1989) no se
cita en ningún documento y el registro advierte que no sostiene KPSS. KPSS sigue sin `.bib` y marcado. No
hay citas textuales de 15 palabras o más.

**Coherencia (8c y 8d).** Las cifras del informe salen de `_cifras.yml` (el mismo origen que `cifras.tex`)
y coinciden con `data/results/` y con mi recálculo (228, 227 y 17; 2007-01, 2007-02 y 2025-12). Notación
coherente. La única divergencia entre los documentos está en las notas de verificación (N-01).

**Regla 7.** No hay resultados en la tesis ni en el informe (criterio 11).

## Lo que no se verificó, y por qué

- **Contenido de las fuentes.** No se consultaron los textos originales: no hay acceso a las obras, y
  el auditor contrasta contra las fichas. Las afirmaciones apoyadas en fichas preliminares quedan
  sujetas a la verificación pendiente del registro.
- **Notebooks 08 y 09** (`torch` no está instalado) y las filas de paridad heredadas de 05b, 06 y 09:
  no cambiaron en 3a. Se aceptan por la tabla de paridad regenerada.
- **Renderizado del sitio completo** (`quarto render` en la raíz) y la publicación: fuera del
  alcance; solo se renderizó `tesis/` (HTML y docx).
- **Lista de símbolos:** revisada por muestreo, no de forma exhaustiva.
- **Remoto:** no se comprobó que el remoto tenga la rama al día (N-11).

## Decisiones que quedan para Roberto

1. **Decisión I** (convención de fechado de los episodios). Las fuentes ya están fichadas, y la decisión
   bloquea la unificación de las fechas (N-12) y las `\pendiente` de la sección 2.2.3.
2. **Reunión N con el Dr. Camiz (Parte C).** Con la evidencia de 3a (componentes en niveles DS y series
   mayoritariamente DS), el escenario del plan es el segundo: el nulo pertinente para la mayoría de las
   series es el que no tiene deriva. Ese escenario debilita el argumento «el PC2 supera al nulo». Es una
   lectura del auditor sobre el plan, no una conclusión: debe consolidarse antes de presentarla (regla 7).
3. **Instalar `texlive-luatex`** antes de fijar la tipografía final (N-07). No es urgente.
4. Confirmar el **cambio de alcance** de `src/particion.py` (N-06).
