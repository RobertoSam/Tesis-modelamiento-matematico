# Nota del redactor LaTeX · Iteración 3b, fase 2 · 27 de octubre de 2026

**Agente:** redactor LaTeX (`.claude/agents/redactor-latex.md`). **Rama:** `iteracion-3b`, desde
`cf48d02`. **Encargo:** tareas L1 a L4 del plan de la iteración 3b
(`asesoria/2026-10-21_plan-iteracion-3b.md`, § «Redactor LaTeX»), con los cambios de la adenda
(`asesoria/2026-10-26_adenda-plan-iteracion-3b.md`, §4) y D15–D17. Sesión automática de
seguimiento diario: no hubo consultas; lo operativo se decidió y las ambigüedades se declaran aquí.

| Tarea | Commit | Estado |
|---|---|---|
| L1 · `sec:validacion`, macros de episodios y generador | `f904b5c` | hecha |
| L2 · piezas formales del capítulo 2 | `50db7a6` | hecha |
| L3 · capítulo 3 (métodos sin resultados) y coherencia del capítulo 1 | `f01e744` | hecha |
| L4 · lista de símbolos, README y esta nota | commit siguiente | hecha |

**Regla 7.** No se tocaron `tesis_latex/capitulos/04_resultados.tex` ni los capítulos de `tesis/`.
El único archivo de `tesis/` que cambió es `tesis/_cifras.yml`, que **genera**
`herramientas/generar_cifras.py` junto con `tesis_latex/cifras.tex` (ver «Desviaciones», 3).
Ninguna cifra de resultados entra en la tesis: las macros nuevas son de datos (dimensiones,
fechas de episodios) y de métodos (tamaño efectivo de los pesos, filas de Horn, longitudes de
bloque y réplicas del nulo).

## 1. Fuentes leídas

`CLAUDE.md`; `decisiones.qmd` (D1–D17); el plan de la iteración 3b (§§1–7) y su adenda (§§1–7);
`auditorias/notas/2026-10-26_desarrollador_adenda.md` y `2026-10-26_desarrollador_dinamica.md`;
`auditorias/2026-10-21_iteracion-3a_vuelta2.md`; `auditorias/notas/2026-10-24_bibliotecario.md`;
`tesis/registro_verificacion.md`; `tesis_latex/` completo; `herramientas/generar_cifras.py` y
`cifras_mapa.csv`; el código que se formaliza: `src/nulo_estructura.py`, `src/dinamica.py`,
`src/episodios.py`, `src/particion.py`, `src/remuestreo.py`, `src/series_tiempo.py`
(`t_hac_media`, `tratamiento_mixto`), `src/multivariado.py` (`coef_rv`, `n_kish`, `umbral_horn`),
`src/camiz_port.py` (`resumen_aede`, `ch_variantes`), `src/deteccion.py`,
`notebooks/06_epca.ipynb` (regla del 06) y el bloque de Kish y Horn de
`R/ciclo_financiero_final.Rmd`; los encabezados de los CSV de `data/results/final/` y
`data/referencia/episodios_referencia.csv`; las fichas y entradas del `.bib` de las claves citadas.

## 2. Lo redactado y sus fuentes

Numeración del PDF compilado (75 páginas).

### L1 · Validación externa (`sec:validacion`, cap. 2)

- Def. 2.5 (episodio de referencia y convención de fechado: evento o anuncio externo; sin fin con
  fuente → puntual, fin efectivo = inicio), Def. 2.6 (compatibilidad con tolerancia $h$; $h=3$
  principal, $h=6$ sensibilidad) y Obs. 2.7. Fuente: D7.
- Tabla 2.1 con los seis episodios; cada fecha entra por macro desde
  `data/referencia/episodios_referencia.csv`, y cada extremo cita su clave: `lehman_brothers_2008`,
  `nber_2010`, `bernanke_2013`, `reserva_federal_2013`, `stocker_et_al_2015`, `fmi_2016`,
  `congreso_2018`, `ustr_2018`, `ustr_2020`, `oms_2020b`, `nber_2021`; además `fmi_2015b` (metales
  «desde 2011», sin mes). Llevan `\verificar` `bernanke_2013` (pasaje no leído) y `congreso_2018`
  (texto de la resolución no leído), según sus fichas.
- Se agregó el sexto episodio (materias primas), que el texto anterior no nombraba.
- Las cinco marcas `\pendiente` de episodios desaparecen.

### L2 · Capítulo 2, piezas formales

| Pieza | Etiqueta (n.º) | Fuente |
|---|---|---|
| Tamaño efectivo de Kish | `def:kish` (2.37) | `src/multivariado.n_kish`; `kish_1965` con `\verificar` |
| **Prop. propia:** $1\le n_\omega\le n_w$, igualdad si y solo si uniformes (Cauchy-Schwarz); $n_\omega<n_w$ con pesos gaussianos y $n_w\ge3$; depende solo de $(n_w,\nu)$; $n_\omega/n_w\to c(\nu)<1$ | `prop:kish` (2.38) | demostración propia |
| Umbrales de Kaiser y de Horn por ventana, $n_H=\lceil n_\omega\rceil$ | `def:umbral-ventana` (2.39), `obs:umbral-ventana` (2.40) | D14; Rmd final (`kish`, `n_horn`) |
| Regla del 06 | `def:regla06` (2.41) | `notebooks/06_epca.ipynb`, celdas 4, 18–20 y 26 |
| **Corolario propio:** la regla del 06 es `aede` con pesos uniformes | `cor:regla06` (2.42), `obs:regla06` (2.43) | base formal de D17.3 |
| Ventanas que contienen un mes; borde de ventana | `lem:ventana-mes` (2.44), `def:borde` (2.45) | `src/episodios.bordes_ventana`, `borde_ventana`; D7, D13 |
| Lectura multiescala | `sec:multiescala`, `obs:multiescala` (2.46) | D10 |
| Fisher con $n_{\min}$: factibilidad y segmentos en el mínimo | `cor:fisher-factible` (2.50) | D17.1; `grilla_datacion` |
| **Prop. propia:** monotonía del costo óptimo con $n_{\min}$ y contraejemplo | `prop:fisher-monotonia` (2.51) | demostración propia |
| Trayectoria PCA-MM12 y datación | `def:datacion` (2.52) | `src/particion.datar`, `media_movil_causal` |
| Codo por caída máxima, regla K en dos pasos, «en el tope», artefacto | `def:criterios-k` (2.53), `obs:criterios-k` (2.54) | D12, D17.1; `datar`, `resumen_aede` |
| CH informativo | `obs:ch` (texto final) | D11 |
| RV sin exigir centrado; RV de cargas sin centrar y $\rho_{\mathbf R}$ | `def:rv` (ajustada), `def:rv-cargas` (2.60) | D17.2; `src/nulo_estructura.medir` |
| **Prop. propia:** el RV de cargas compara $\mathbf R_t^{[d]}$, es invariante a signos, orden y rotaciones, con $d=p$ es $\rho_{\mathbf R}$, y el centrado anula un eje de cargas iguales | `prop:rv-cargas` (2.61) | demostración propia |
| Pares adyacentes no solapados, frontera y RV adyacente | `def:pares` (2.62) | D10; `medir` |
| Índices por bloques | `def:bloques` (2.66) | `src/remuestreo.indices_desde_inicios`; Rmd `inicios_bloques` |
| Estadístico HAC; **lema propio** de no negatividad | `def:hac` (2.67), `lem:hac` (2.68) | `t_hac_media`; D8; `newey_west_1987` con `\verificar` |
| Nulo de tendencias mixto | `def:nulo-mixto` (2.69), `obs:nulo-mixto` (2.70) | D8; `nulo_tendencias(version='mixto')` |
| Nulo de estructura constante (solo incrementos acumulados) y **prop. propia** de invariancias | `def:nulo-estructura` (2.71), `prop:nulo-estructura` (2.72), `obs:nulo-estructura` (2.73) | D7 y adenda §4; `serie_nula` |
| Criterio de OE4 | `def:oe4` (2.74) | D10, D17.2; `src/dinamica.criterio_oe4` |
| **Prop. propia:** validez de la versión simétrica bajo intercambiabilidad | `sup:intercambiable` (2.75), `prop:oe4` (2.76), `obs:oe4` (2.77) | demostración propia |
| Transición fuera del nulo (operativa) y transición confirmada | `def:fuera-nulo` (2.78), `def:confirmada` (2.79) | D13, D17.3; `fuera_del_nulo`, `tabla_2017_10` |

Además: la posición epistemológica ya no dice «dos vías» sino D15 (con remisión al cap. 3); los
criterios de comparación y el aporte (4) recogen D10 y D15.

### L3 · Capítulo 3 (sin resultados)

| Sección | Contenido | Fuente |
|---|---|---|
| 3.1 Diseño | Exploratorio; niveles y anexo de robustez como **propuesta sujeta a la reunión N**; «Qué vía mide qué» en `\pendiente` | D1, D2, D15; adenda §6.1 |
| 3.2 Datos | $n$, $p$, período por macro; 16 series por grupos; exclusiones; vintage y md5 | D1, D3, D4, D16; `src/datos.py` |
| 3.3 Procedimiento | Tabla de etapas; regla D5 (Def. 3.1); diagnóstico; PCA ($d=3$); parte dinámica (Tabla 3.2 de $n_\omega$ y $n_H$ por macro; nulo con $L_b$ y $B$ por macro); HFC; datación; validación y razón de error *walk-forward* (Def. 3.2); AE/LSTM en `\pendiente` | D5, D7–D17; notas del desarrollador; `src/deteccion.py` |
| 3.4 Criterios fijados de antemano | Tabla 3.3 (D1–D17 con fecha de registro) y seis lecturas propias del código que las decisiones no fijan | `decisiones.qmd`, `git log` |
| 3.5 Implementación, paridad y reproducibilidad | Notebooks, Rmd final, port, paridad con índices compartidos y excepciones, no regresión, cifras | D6, D15; notas del desarrollador |

Capítulo 1: el párrafo de datos se alinea con D15 y D16 (16 series por macro) y remite al cap. 3;
Atoche Murrieta (2022) y Camiz y Pillar (2018) se citan con su ficha.

### L4 · Notación

- `notacion.tex`: macros `\nomega`, `\nhorn`, `\Kest` ($K^\ast$, el $k^\ast$ del código), `\Kef`,
  `\Lb` (no es la $L$ del LSTM), `\mb`, `\RVad`, `\RVadr`, `\umbralRV`, `\umbralRVr`, `\fr`,
  `\red`, `\pval`, `\paso`, `\pib` (no es la constante $\pi$), `\ind`, `\epi`, `\Epis`, `\tini`,
  `\tfin`. Las macros se añadieron con L1 y L2 porque sin ellas no compilaba.
- Lista de símbolos: grupo nuevo «Episodios de referencia y nulos» y entradas nuevas en «Datos»,
  «Análisis evolutivo», «Partición de Fisher» y «Comparación». $p$ remite a `\nSeries`.
- Choques evitados: $u$ (posición en la ventana) no se usa para los incrementos centrados
  ($\dot x_t$); $\gamma$ (ganancia) no se usa para las autocovarianzas ($\hat\Gamma_k$); $P$
  (período) y $T$ (suma total) no se usan en la Prop. 2.76 ($\mathcal P_j$, $\tilde\varpi_j$); $f$
  no se usa como mes candidato ($\tau$, $\tau^\circ$); $L$ del LSTM frente a $L_b$; $\pi$ frente a
  $\pi^{\mathrm b}$; $\Delta\mathbf x_t=\mathbf x_t-\mathbf x_{t-1}$ también en los nulos (índice
  $\pi^{\mathrm b}(t)+1$).

### Macros nuevas y generador

- `herramientas/generar_cifras.py` admite ahora `data/referencia/` además de `data/results/`
  (docstring y `herramientas/README.md` actualizados).
- Las ocho macros de dimensiones (`\nMesesNiveles`, `\nMesesTransformadas`, `\nSeries`,
  `\fechaInicio*`, `\fechaFinDatos`, `\anio*`) leen ahora `data/results/final/05_dimensiones.csv`;
  solo cambia `\nSeries` (17 → 16).
- Nuevas: 11 fechas de episodios (`\episodio*`), `\nOmegaGauss*` y `\nHornGauss*` (4 anchos),
  `\largoBloqueNulo`, `\largoBloqueNuloCorto`, `\largoBloqueNuloLargo`, `\replicasNuloEstructura`,
  `\replicasNuloSensibilidad`, todas con su `\providecommand` en `cifras_stub.tex`.
- `generar_cifras.py --comprobar`: exit 0.

## 3. Verificación numérica de las proposiciones nuevas

Comprobadas por mí en el scratchpad (guion no versionado); se dejan las recetas para el auditor:

| Proposición | Receta | Resultado propio |
|---|---|---|
| 2.38 (Kish) | Pesos de `eq:pesos` con `nsd` 0 y 3; `1/sum(w**2)` frente a $n_w$; $n_w=2$ da pesos iguales; límite: $c(\nu)=\sqrt{2\pi}\,\mathrm{erf}(\nu/2)^2/(\nu\,\mathrm{erf}(\nu/\sqrt2))$, que es la fórmula del enunciado con $a=\nu/\sqrt2$ | $n_\omega$ coincide con `n_kish(aede(...)['weights'])` en 24, 36, 48 y 60 (diferencia ≤ 1,4e-17 en los pesos); $n_\omega/n_w$ crece hacia $c(3)$ y lo alcanza a 1e-5 con $n_w=10^5$ |
| 2.42 (regla del 06 = `aede` uniforme) | Correlación de una ventana estandarizada con `StandardScaler` frente a `camiz_port.bstatw(..., pesos 1/n_w)['correlations']`; valores propios y vectores salvo signo | (no corrido aquí; la paridad del Rmd ya compara la regla del 06 con 60 meses) |
| 2.44 (centros que contienen un mes) | Contra `bordes_ventana` de `src/episodios.py` con los cuatro anchos | coincide por construcción (misma fórmula) |
| 2.50 y 2.51 (Fisher) | `fisher_multivariado` con $y$ = 13 ceros, 13 cincos, 14 dieces, `n_min=10`, `k_max=4` | $Q_3=0$, $Q_4=112{,}5$: la monotonía falla, como dice (c) |
| 2.61 (RV de cargas) | `coef_rv(Fa, Fb, centrar=False)` frente a la fórmula con $\mathbf R^{[d]}$; rotaciones, permutaciones y signos aleatorios; con $d=p$ frente a `rv_correlacion` | diferencias ≤ 3,3e-16; la columna centrada de un eje constante es 0 |
| 2.68 (HAC no negativo) | Comparar `t_hac_media` con la fórmula de sumas móviles del lema en series aleatorias | (identidad algebraica; no corrida) |
| 2.72 (invariancias del nulo) | `serie_nula` con $X$ y con $X\,\mathrm{diag}(b)+\mathbf 1a^\top$ y los mismos inicios; `medir` da los mismos $k^\ast$ y perfiles | (no corrida) |
| 2.76 (validez simétrica) | Simulación: $B=39$, $m=30$, perfiles intercambiables (paseos aleatorios), 4 000 repeticiones | $\Pr(\tilde p\le\alpha)$ = 0,044; 0,088; 0,174 para α = 0,05; 0,10; 0,20. La versión implementada da 0,035; 0,082; 0,173 (también conservadora en este caso) |

## 4. `\pendiente` que quedan (15) y por qué

| Ubicación | Marca | Motivo |
|---|---|---|
| Portada | Denominación del grado | Pautas de la UNI |
| Resumen (`tesis.tex`) | Resumen y *abstract* | Capítulos 1–5 sin aprobar |
| Cap. 1, OE6 | Frontier (1976) | Sin ficha (solo citado por Camiz y Pillar, 2018) |
| Cap. 2, `sec:cos2` | Terminología de cos² y contribuciones | Sin ficha |
| Cap. 2, `def:retencion` | Frontier (1976) | Sin ficha |
| Cap. 2, `sec:adecuacion` | Inversa de $\mathbf R$ y correlaciones parciales | Sin ficha |
| Cap. 2, `sec:hfc` (nota) | Denimal (2001) | Presentación sin actas; sin ficha |
| Cap. 2, `def:pesos` | Camiz y Diblasi (2013) | No localizada; pedirla al Dr. Camiz |
| Cap. 2, `obs:nulo-estructura` | **Nueva:** fuente del bootstrap por bloques conjunto | Lahiri (2003) no verificado para ese caso (registro) |
| Cap. 3, `sec:met-vias` | **Nueva:** «Qué vía mide qué» | Espera la reunión N con el Dr. Camiz |
| Cap. 3, `sec:met-diagnostico` | **Nueva:** Said y Dickey (1984) | Sin ficha (registro, fila `dickey_fuller_1979`) |
| Cap. 3, `sec:met-diagnostico` | **Nueva:** Kwiatkowski et al. (1992) | Ficha sin entrada en el `.bib` |
| Cap. 3, `sec:met-validacion` | **Nueva:** AE y LSTM con 16 series | D17.4: iteración 4, sin `torch` |
| Cap. 4 | Capítulo de resultados | Regla 7 |
| Cap. 5 | Conclusiones | Depende del cap. 4 |

Antes de esta iteración había 23 marcas (16 en el cap. 2, 2 en el cap. 1, 1 en el 3, más portada,
cap. 4, cap. 5 y resumen); quedan 15: se cerraron 13 y se abrieron 5. **Para el bibliotecario (B4):** se cerraron en la tesis las
marcas de los cinco episodios, Atoche Murrieta (caps. 1 y 2), Jolliffe, vara quebrada y Rencher
(ahora `camiz_pillar_2018` y `rencher_christensen_2012` con `\verificar`), Denimal (2007),
Bruynooghe, Tukey y Lavit, y el `\pendiente` de capítulo vacío del cap. 3. Hay cinco marcas
nuevas (las señaladas como «Nueva» en la tabla). Frontier (1976) sustituye, en los caps. 1 y 2, a
las marcas que pedían una fuente de la vara quebrada, y Denimal (2001) a la conjunta de Denimal. Claves citadas por primera vez en la tesis, todas con
ficha y entrada: `atoche_murrieta_2022`, `camiz_pillar_2018`, `rencher_christensen_2012`,
`jolliffe_2002`, `denimal_2007`, `bruynooghe_1978`, `tukey_1977`, `lavit_1988`, `kish_1965`,
`newey_west_1987`, `kunsch_1989`, `lahiri_2003`, `hubert_arabie_1985`, `hennig_2007`,
`dickey_fuller_1979` y las once de episodios más `fmi_2015b`. No se añadió `josse_pages_husson_2008`
(no hizo falta). Ninguna referencia se citó sin ficha.

## 5. Inconsistencias entre el código y la teoría (para el desarrollador; no resueltas en el texto)

1. **Monotonía del costo de Fisher con $n_{\min}$** (Prop. 2.51). Con $n_{\min}=12$, $Q^\ast_{K+1}\le
   Q^\ast_K$ solo está garantizado si $N>K(2n_{\min}-1)$. Diagnóstico propio (no es un resultado de la
   tesis): `datar` sobre `final/05_pca_scores.csv` con $d\in\{2,3,4\}$ y `k_max=20` da $N=217$,
   $K_{\mathrm{ef}}=18$ y **reducción negativa en $k=17$** en los tres casos. No cambia la regla K
   de la nota del 26-oct (el paso 1 elige antes), pero sí puede afectar la caída máxima y los CH
   cerca del tope con maxcl = 15 y 20. Sugerencia: una columna que marque las reducciones
   negativas en `09a_datacion_criterios.csv`.
2. **p-valor del criterio de OE4** (Obs. 2.77). `criterio_oe4` calcula el p5 de cada réplica con
   las otras $B-1$ réplicas (sin el perfil observado) y el p-valor como $\#\{\varpi_\zeta\ge
   \varpi_0\}/B$, sin sumar uno. La Prop. 2.76 garantiza el nivel para la versión simétrica (cada
   perfil contra los otros $B$, p-valor $(1+\#)/(B+1)$). La diferencia es de orden $1/B$ y la
   simulación del §3 no muestra exceso de rechazos, pero conviene decidir si se adopta la versión
   simétrica o se declara la actual.
3. **La regla del 06 centra las cargas** (Obs. 2.43(b)): su estabilidad es una correlación de Pearson
   entre vectores de cargas, el mismo centrado que D17.2 descartó para el RV. ¿Se mantiene por ser
   la regla del antecedente o se ofrece la congruencia sin centrar como variante?
4. **Nulo mixto, rama TS** (Obs. 2.70(c)). `nulo_tendencias(version='mixto')` indexa $n$ residuos
   con los inicios sorteados para $n-1$ incrementos; la sucesión solo cubre $n$ meses si
   $\lceil(n-1)/L\rceil L\ge n$. Con $n-1=227$ y $L=12$ se cumple ($19\cdot12=228$), pero fallaría
   si $L$ dividiera a $n-1$ (la longitud quedaría corta y la asignación a `M[:, j]` daría error o
   truncaría). Sugerencia: un `assert`.
5. **Ventanas con una serie constante** (Obs. 2.40(c); pendiente 2 de la nota del redactor de 3a).
   `bstatw` pone a cero la fila y la columna, diagonal incluida; esas ventanas (7 con $n_w=24$,
   según la nota del desarrollador) no cumplen el Supuesto 2.32: su traza es menor que $p$, y el
   RV de la correlación completa y los conteos de Horn se calculan sobre una matriz que no es de
   correlaciones. Sugerencia: excluirlas de los conteos o informarlas aparte (la columna
   `serie_constante` ya existe).
6. **Lectura de D12** (Obs. 2.54(a)): «el menor $k$ a partir del cual la reducción es menor que
   10 %» se implementa como el primer $k$ con reducción menor que 10 %, sin exigir que siga bajo el
   umbral. Coinciden si la reducción es decreciente; se declara.
7. **Mapa de cifras.** Unas 45 macros de resultados de `cifras_mapa.csv` (inercias, KMO, nulos,
   clases D5…) siguen leyendo las carpetas del antecedente (`data/results/*.csv` y
   `data/results/niveles/`), contra lo que dice `data/results/LEEME.md` («no se consumen en
   `herramientas/generar_cifras.py`»). No las usa la tesis ni el informe. No las toqué porque son
   macros de resultados: conviene retirarlas o apuntarlas a `final/`.
8. **Parámetros de diseño sin CSV.** Para leer por macro lo que hoy escribo a mano (clase
   provisional del README): $\nu=3$ (`nsd`), paso 3 y eje 2 de la regla del 06, media móvil de 12
   meses, particiones en 3 y 4 clases, percentil 95 de la razón *walk-forward*, longitud de bloque y
   réplicas del nulo de tendencias, réplicas del bootstrap de la HFC y de la estabilidad de cortes.
   Propuesta: `data/results/final/parametros_diseno.csv` (parámetro, valor, fuente).
9. **Horn por ventana.** El código usa $\lceil n_\omega-10^{-9}\rceil$; quedó documentado en la
   Obs. 2.40(d). No es una inconsistencia, solo un detalle que el texto ahora declara.

## 6. Desviaciones respecto del encargo

1. **Capítulo 1 modificado** (fuera de L1–L4 en sentido estricto): el párrafo de datos decía «dos
   vías (D2)» y, con `\nSeries` = 16, debía alinearse con D15 y D16; además, las marcas de Atoche
   Murrieta y de la vara quebrada y Rencher (OE6) pasaron a citas fichadas. No se tocaron los
   objetivos ni las hipótesis (ver §7, duda 2).
2. **Más marcas cerradas que las cinco de episodios**: se aplicó lo que la nota del bibliotecario
   (§5) señala como ya citable.
3. **`tesis/_cifras.yml` regenerado.** Lo escribe el generador junto con `cifras.tex`; no se puede
   pasar `--comprobar` sin él. Cambia el valor de `nSeries` (17 → 16) y el archivo de origen de las
   dimensiones, y se añaden claves nuevas. El informe mostrará «16 series» donde usa
   `{{< meta cifras.nSeries >}}`, lo que es coherente con D16; el editor debe revisarlo en E1–E3.
4. **README de la tesis**: nuevas clases de excepciones a la regla de cifras («Identificadores y
   fechas de registro», «Metadatos bibliográficos», sugeridas por la auditoría 3a, y una clase
   **provisional** de parámetros del plan que `decisiones.qmd` no recoge). La última requiere la
   aceptación del auditor o la exportación del §5.8.
5. **Entorno**: faltaban `texlive-lang-spanish`, `texlive-bibtex-extra`, `biber` y
   `texlive-luatex`; se instalaron con `apt-get` (anotado en el README). Sin ellos no compilaba ni
   el estado de partida.
6. **Commits**: las macros de notación de L4 entraron con L1 y L2 (eran necesarias para compilar);
   el pie de la Tabla 2.1 se ajustó en el commit de L2; el arreglo de `\crefname{table}` (decía
   «cuadro») y el espaciado de listas como $\{1, 2\}$ con `icomma` (antes se leían como decimales)
   entraron con L3.
7. **Plan, criterio 11**: compilación limpia (abajo). No se ejecutó `pytest`: no cambié código de
   análisis, solo el generador de cifras, que no tiene pruebas.

## 7. Dudas para Roberto

1. **Tolerancia de D7**: ¿se mide al intervalo del episodio (lectura adoptada en la Def. 2.6, la del
   código) o solo a sus extremos? Afecta a los períodos largos (materias primas, guerra comercial).
2. **Redacción de OE3, OE4 y de la evaluación de las hipótesis** (cap. 1): OE3 dice «en las dos vías
   del diseño»; OE4, «criterio objetivo para el ancho… entre ventanas consecutivas»; y las
   hipótesis «se evalúan por la convergencia de la evidencia en las dos vías». D10 (pares
   adyacentes, lectura multiescala) y D15 (niveles con anexo) ya no coinciden con esas frases. Son
   compromisos de la ficha de inscripción: no los cambié. ¿Se reformulan?
3. **Fechas principales de los episodios** (pendiente del desarrollador): ¿se confirman las del
   archivo único frente a las alternativas fichadas (COVID-19 2020-01 o fin 2023-05; Kuczynski
   como período desde 2016-12)?
4. **Para el Dr. Camiz** (sin decidir aquí): la definición de «transición fuera del nulo»
   (Def. 2.78), el codo de `aede` como candidato de D13, la serie representante de la HFC y el
   diseño en niveles con anexo como propuesta.
5. **D17.1**: ¿se acepta el conteo de segmentos en el mínimo como sustituto de la marca literal de
   artefacto, que por el Cor. 2.50(b) solo puede activarse si $N$ es múltiplo de 12?
6. **Parámetros escritos a mano** (README, clase provisional): ¿se registran en `decisiones.qmd` o
   se encarga al desarrollador el CSV del §5.8?

## 8. Compilación

`latexmk -lualatex -cd tesis_latex/tesis.tex`: exit 0, 75 páginas, 0 citas o referencias
indefinidas, 0 `Overfull`, 0 avisos de LaTeX en el log y biber sin avisos. El PDF no se versiona.
