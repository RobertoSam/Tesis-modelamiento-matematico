# Asesoría · Diagnóstico y plan de la iteración 3 · 20 de octubre de 2026

**Agente:** Asesor de tesis (`.claude/agents/asesor-tesis.md`). No edita ni ejecuta el material
de la tesis: recomienda. Roberto decide y da el conforme.

**Fuentes leídas:** `CLAUDE.md`, `decisiones.qmd` (D1–D3), `linea_temporal.qmd`,
`auditorias/2026-10-18_iteracion-1.md`, `auditorias/2026-10-19_iteracion-2.md` (con sus tres
re-auditorías), `tesis/_capitulos/01–05`, `tesis/registro_verificacion.md`,
`R/tesis_ciclo_financiero.Rmd` (secciones 2, A.2, A.3, A.4 y A.6), `R/camiz_port.R` (`aede_r`),
`notebooks/05_pca.ipynb`, `notebooks/06b_*`, `notebooks/modelos_dl.py`, `data/results/R_*.csv`
(dos vías) y las definiciones de los seis agentes. Las cifras que cito y que no están en un CSV
vienen del HTML renderizado del Rmd (`R/tesis_ciclo_financiero.html`, no versionado); lo indico
en cada caso, porque esa ausencia es en sí un hallazgo (sección 1, punto 4).

---

## 1. Diagnóstico

1. **La cadena exploratoria está completa y auditada en R, pero no en Python ni en un documento
   formal.** La iteración 2 cerró APROBADA: el Rmd corre las dos vías, con 15 de 15 comprobaciones
   de paridad. El PCA estático de Python (`05_pca.ipynb`) sigue siendo trimestral (D3 lo deja
   pendiente). Además, `aede` y la HFC existen **solo en R**: las 15 comprobaciones de
   `R_paridad_python.csv` no las incluyen.
2. **La tesis todavía no tiene documento maestro.** No existen `tesis_latex/` ni `herramientas/`.
   El informe tiene los capítulos 1 y 2 aprobados. El 3 es un esqueleto y todavía dice
   «227 meses × 17 series», cifra superada para la vía en niveles (228).
3. **La pregunta central sigue abierta: qué vía mide el ciclo (Parte C de D2).** La evidencia
   disponible es fuerte, pero condicional. En niveles, el PC1 (67,2 %) no supera el nulo de tendencias
   independientes con deriva (proporción 0,90). El PC2 (18,3 %) sí lo supera (0,01). **Contra el nulo
   sin deriva, el resultado se invierte:** PC1 0,00 y PC2 0,59 (HTML del Rmd, sección 2). Elegir el nulo
   pertinente exige saber si las tendencias son determinísticas o estocásticas. Eso es justo lo que
   miden los apuntes 10 y 11.
4. **Trazabilidad incompleta de las cifras clave.** El nulo de tendencias, el KMO, Bartlett, el
   bootstrap de cargas y la estabilidad de cortes se calculan inline en el Rmd y no se escriben en
   `data/results/`. Hoy `generar_cifras.py` no podría emitirlas, y las cifras de `decisiones.qmd`
   (67,2 %, p ≈ 0,90, etc.) no tienen archivo de origen.
5. **Los criterios de selección (número de clases y ancho de ventana) son el punto débil
   metodológico.** El CH elige el tope de la grilla en casi todos los casos: k = 10 en 7 de las
   8 filas del CH de `R_aede_cortes.csv` (dos vías, las dos fórmulas y los dos esquemas de pesos). La ventana de 60 meses es un compromiso declarado, no
   un criterio (OE4, compromiso firme, sin ejecutar). El contexto simulado (OE11) no ha empezado.
   Sin él, ningún criterio de selección puede calibrarse.
6. **Bibliografía:** 28 marcas `[VERIFICAR]` en el Rmd, 22 en los capítulos 1 y 2 y 16 notas
   `VERIFICAR` en el `.bib`. Cuatro obras sostienen el texto y no tienen ficha: Atoche Murrieta (2022),
   Benzécri (1973), Calinski y Harabász (1974) y Horn (1965). Ningún episodio tiene una fuente fichada.
7. **Restricciones del entorno que condicionan el plan:**
   - `modelos_dl.py` importa `torch` en la cabecera, de modo que sus funciones de Fisher, Horn, RV y
     Procrustes no se pueden usar aquí;
   - `statsmodels` figura en `requirements.txt`, pero no está instalado, y hace falta para ADF, KPSS
     y la ACF en Python (en R, `tseries`, `urca` y `psych` sí están);
   - TeX Live, biblatex-apa, biber y latexmk están disponibles; la clase `memoir` también.

**Juicio de conjunto:** el proyecto tiene más resultados que tesis. El riesgo ya no es la falta
de análisis, sino la proliferación de especificaciones (2 vías × 2 esquemas de pesos × 3 anchos
de ventana × 2 fórmulas del CH × 2 topes de clases) sin un criterio fijado de antemano. La
iteración 3 debe consolidar: el PCA estático en las dos lenguas, un documento formal y la
trazabilidad de las cifras. Las preguntas dinámicas (ventana y número de clases) conviene
abordarlas cuando estén resueltas las decisiones de las que dependen.

---

## 2. ¿Una iteración o dos? Recomendación: **dividir en 3a y 3b**

| Criterio | Todo en una iteración | 3a + 3b |
|---|---|---|
| **Tamaño** | 05 reescrito en dos vías; unos 15 chunks nuevos o modificados del Rmd, en A.2, B.2, A.3, B.3, A.4, B.4, A.6 y B.6; dos módulos en `src/`; un notebook nuevo de datación; infraestructura LaTeX completa; dos capítulos formalizados; derivación del informe; más de 10 fichas. La auditoría de la iteración 2, que solo cubría el Rmd, ocupó 67 KB: dictamen inicial, dos vueltas y una verificación de cierre. | 3a: PCA estático, LaTeX y bibliografía. 3b: dinámica (EPCA, `aede`, HFC y datación). Cada una es comparable en tamaño a la iteración 2. |
| **Dependencias** | Los apuntes 6, 9 y 12 y la parte dinámica del 5 se interpretan con los episodios de referencia (R-1), cuya fuente y convención aún no existen. El 8 informa la decisión D-1, pero su lectura depende de un nulo (sección 3). El 2 está sin definir. | 3a no depende de ninguna decisión pendiente. 3b arranca con las fuentes de episodios que entrega el bibliotecario en 3a y con la convención que fije Roberto. |
| **Verificabilidad** | Con dos vueltas como máximo, un dictamen sobre tantos frentes se escalaría casi con seguridad (ya ocurrió en la iteración 2). | Todo lo de 3a y 3b se puede verificar en este entorno (R, Jupyter sin `torch` y TeX). Ningún apunte requiere `torch` ni el BCRP. |
| **Regla 7** | Mezcla resultados no consolidados de la parte dinámica con la puesta en marcha del documento maestro. | 3a no lleva resultados a la tesis: solo métodos formales (capítulos 1 y 2). |

**Asignación:** 3a = apuntes 1, 3, 4, 5 (parte estática), 10 y 11; el 05 mensual; la tesis LaTeX;
y el bibliotecario, en prioridades 1 y 2. 3b = apuntes 5 (parte dinámica), 6, 7, 8, 9, 12 y el 2, una
vez aclarado. El plan de 3b se revisa al cierre de 3a; la sección 7 es solo un esbozo.

---

## 3. Los 12 apuntes, punto por punto

Convenciones:

- **NIV** es la vía en niveles (228 × 17) y **TRA** la transformada (227 × 17).
- «Paridad» significa: mismo resultado en Python y en el Rmd, con una fila nueva en
  `R_paridad_python.csv` y tolerancia de 1e-10 salvo que se indique otra.
- Para los métodos del asesor que solo existen en R (`aede` y `clahfac`) propongo declarar una
  excepción de paridad (decisión E).
- Clase: **N** = necesario, **R** = recomendable, **O** = opcional.

### Apunte 1 · cos² en los ejes 1, 2 y 3 del PCA, con comentario — 3a · N

- **Qué se calcula:** $\cos^2_{jk} = r_{jk}^2$ (correlación de la serie $j$ con el componente $k$,
  al cuadrado) para $k = 1, 2, 3$, su suma sobre los tres ejes y la calidad en los planos 1–2 y 1–3.
  Hoy el Rmd solo informa la suma acumulada en 3 y 4 dimensiones (chunk `b3-cargas-tabla`), no
  eje por eje.
- **Dónde:** `notebooks/05_pca.ipynb` → `data/results/niveles/05_pca_cos2.csv` y
  `data/results/05_pca_cos2.csv`; Rmd, A.2 y B.2.
- **Vía:** ambas.
- **Criterio de aceptación:**
  - 17 filas por vía, con las columnas cos²₁, cos²₂, cos²₃ y su suma;
  - para cada serie, $\sum_{k=1}^{17}\cos^2_{jk} = 1$ (tolerancia 1e-12);
  - paridad Python–R;
  - en la nota del desarrollador, una línea de comentario por eje que nombre las series con
    cos² ≥ 0,5 y las que tienen calidad baja en el plano 1–2 (cos² < 0,5), y su cruce con el KMO
    individual.
- **Pregunta que responde:** OE3 (qué representa cada eje y con qué fidelidad) y HT2 (solo las
  series bien representadas sostienen la lectura de los grupos). Es estándar en la escuela
  francesa: el Dr. Camiz lo espera.

### Apunte 2 · «Medir la…» — sin acción

Está incompleto. No se infiere su contenido. Queda reservado para 3b, pendiente de que Roberto lo
aclare (decisión G).

### Apunte 3 · Autocorrelaciones y correlaciones que sustenten los PCA — 3a · N

- **Qué se calcula:**
  - ACF de cada serie en los rezagos 1, 3, 6, 12 y 24;
  - matriz de correlaciones, con mapa de calor;
  - **tamaño muestral efectivo por par** ($n_{\text{ef}}$, la corrección de la varianza de una
    correlación entre series autocorrelacionadas; fuente: propuesta para el bibliotecario, por
    verificar) y la proporción de pares cuya correlación sigue siendo distinta de cero con
    $n_{\text{ef}}$;
  - en NIV, además, las correlaciones entre las series sin su tendencia lineal (diagnóstico que
    alimenta el apunte 10).
- **Dónde:** 05 → `05_acf.csv`, `05_correlaciones.csv` y `05_n_efectivo.csv` (por vía); Rmd, A.2 y
  B.2, en la subsección «¿Tiene sentido un PCA con estos datos?».
- **Vía:** ambas.
- **Criterio de aceptación:**
  - estimador de la ACF declarado e idéntico en las dos lenguas (paridad);
  - $n_{\text{ef}} \le n$ en todos los pares;
  - la fórmula de $n_{\text{ef}}$ figura con su fuente fichada o con `[VERIFICAR]` y una fila en el
    registro.
- **Pregunta que responde:** si las correlaciones que resume el PCA son informativas, que es la
  objeción de correlación espuria del sustento de D2 (OE3). En NIV la ACF del rezago 1 será cercana a 1, así que
  $n_{\text{ef}}$ será pequeño. Es la cifra que conviene tener antes de que el jurado la pida.

### Apunte 4 · Desarrollo del KMO y de la prueba de esfericidad de Bartlett — 3a · N

- **Qué se calcula o redacta:**
  - (a) **desarrollo formal** en la tesis LaTeX: definición del KMO global y del individual a partir
    de la matriz anti-imagen ($\mathbf R^{-1}$), el estadístico de Bartlett, sus grados de libertad
    y sus supuestos (observaciones independientes y normalidad multivariada);
  - (b) cálculo en Python 05, en paridad con las funciones del Rmd `bartlett_esfericidad` y `kmo`;
  - (c) sensibilidad: Bartlett con $n_{\text{ef}}$ (apunte 3) en lugar de $n$, el número de
    condición de $\mathbf R$ y $\ln|\mathbf R|$ (en NIV hay pares casi colineales, como M2–M3 y tasa
    de referencia–interbancaria).
- **Dónde:** 05 → `05_adecuacion.csv` (global y por serie, por vía); `tesis_latex/capitulos/02_*.tex`,
  subsección «Adecuación muestral» del PCA; Rmd, A.2 y B.2.
- **Vía:** ambas.
- **Criterio de aceptación:**
  - χ², grados de libertad, KMO global y KMO por serie en paridad (1e-8);
  - el CSV reproduce las cifras del Rmd (en el HTML: χ² 12 210 en NIV y 1 831 en TRA; KMO 0,86 y 0,70);
  - las definiciones en LaTeX usan la notación de `notacion.tex` y la fuente fichada, o
    `\pendiente{}` con su fila en el registro.
- **Pregunta que responde:** la adecuación del PCA (OE3). El KMO de NIV (0,86) es mayor que el de TRA (0,70): la
  tendencia infla la adecuación. Esa es la evidencia directa del apunte 10.

### Apunte 5 · Bootstrap por bloques — parte estática en 3a, parte dinámica en 3b · N

- **Estado:**
  - el Rmd ya remuestrea las cargas (bloques de 24 meses y 500 réplicas). En NIV, la congruencia
    del PC2 tiene un p5 de 0,793 y la del PC4, de 0,608 (HTML);
  - también remuestrea los cortes de la datación con k fijo. En NIV, el corte de 2014-04 solo se
    reproduce en el 35 % de las réplicas.
  - Falta: Python; la sensibilidad a la longitud del bloque; y la declaración del supuesto.
- **3a:**
  - bootstrap de cargas y valores propios en Python 05;
  - longitudes de bloque L ∈ {12, 24, 36};
  - intervalos de los valores propios para decidir entre 2, 3 y 4 dimensiones (OE6). Horn da 2 en
    NIV y 4 en TRA, y la cadena usa 3.
- **3b:** bootstrap de la HFC (OE5, compromiso firme, sin ejecutar) y de los cortes de `aede`.
- **Dónde:** `src/remuestreo.py` (nuevo, sin `torch`); 05 → `05_bootstrap_congruencia.csv` y
  `05_bootstrap_valores_propios.csv`; Rmd, A.2 y B.2.
- **Criterio de aceptación:**
  - **paridad exacta mediante una matriz de índices compartida.** El Rmd escribe los índices de las
    réplicas en `data/results/R_bootstrap_indices_L{12,24,36}.csv` y Python los lee. Así, la
    congruencia y los intervalos coinciden al 1e-10, sin depender de generadores aleatorios
    distintos;
  - semilla declarada;
  - tabla por L.
  - El texto declara que en NIV el bootstrap por bloques supone una dependencia débil que no
    cumplen las series con tendencia, de modo que ahí mide estabilidad descriptiva y no
    incertidumbre muestral.
- **Pregunta que responde:** la robustez de los ejes (OE12) y el número de dimensiones (OE6). En 3b,
  la robustez de los grupos (OE5 y HT2).

### Apunte 6 · Ventana de 24 meses y cómo corta `aede` — 3b · N

- **Qué se calcula:**
  - (a) **descripción exacta del algoritmo**, verificada en `R/camiz_port.R:538–640`:
    - la ventana $i$ se fecha en la fila $i + n_w/2$ (con 60 meses, el mes 31 de la ventana);
    - Fisher se aplica solo a la serie de $\lambda_1$, sin longitud mínima de segmento;
    - el CH usa $k$ y $n-k$ grados de libertad;
    - los pesos gaussianos tienen $s = (n_w-1)/\sqrt2$ y se escalan por `nsd`.
  - (b) `aede` con $n_w = 24$ en las dos vías y con los dos esquemas de pesos: $\lambda_1, \lambda_2,
    \lambda_3$ por ventana y los cortes de Fisher para $k = 2, \dots, \text{maxcl}$.
- **Dónde:**
  - Rmd, A.3 y B.3; `R_aede_cortes.csv` con una columna `nw`;
  - la definición del algoritmo, con su convención de fechado, en el capítulo 2 de LaTeX (EPCA),
    que es metodología y no resultado.
- **Vía:** ambas. Es solo R (excepción de paridad, decisión E).
- **Criterio de aceptación:**
  - las filas con `nw = 60` son idénticas a las actuales;
  - el auditor comprueba numéricamente la convención de fechado;
  - con 24 meses y 17 series ($n/p = 1{,}4$), cada ventana informa el umbral de Horn para
    $n = 24$ (apunte 7).
- **Pregunta que responde:** OE4 (criterio de ventana), OE9 (Fisher sobre $\lambda_1$) y HT1.
- **Advertencia de fondo:** una ventana de 24 meses no contiene ningún ciclo financiero en la
  acepción de Drehmann et al. (2012), de 8 a 30 años. Mide cambios de estructura de corto plazo. El
  ancho de ventana fija la **escala temporal** de lo que se llama «régimen». Conviene presentarlo
  así, como análisis multiescala, y no como una búsqueda de la ventana «correcta».

### Apunte 7 · Valores propios en valor absoluto por ventana — 3b · R

- **Lectura literal:** la PCA es de correlaciones, así que la traza vale 17 en cada ventana y la
  inercia ya es $100\lambda/17$. Mostrar $\lambda$ en lugar del porcentaje **no agrega información**:
  es un cambio de escala. Tampoco hay valores propios negativos.
- **Versión que sí aporta (propuesta):** $\lambda_1, \lambda_2, \lambda_3$ absolutos por ventana,
  comparados con dos umbrales de la ventana:
  - Kaiser (1);
  - Horn p95, con $n = n_w$. Con pesos gaussianos, con el $n$ efectivo de Kish, $1/\sum\omega^2$
    (fuente: propuesta para el bibliotecario, por verificar).
  Además, el registro de los cruces $\lambda_2 \leftrightarrow \lambda_3$, que explican la
  congruencia mínima de 0,519 con 36 meses (HTML, A.3).
- **Dónde:** Rmd, A.3 y B.3 → `R_aede_valores_propios.csv` (columnas: fecha del centro, `nw`, pesos,
  λ1 a λ3 y umbral de Horn para cada uno).
- **Criterio de aceptación:**
  - $\lambda_1+\lambda_2+\lambda_3 \le 17$ en cada fila;
  - número de ventanas con $\lambda_k$ bajo el umbral, por eje y por `nw`;
  - con pesos uniformes y `nw = 60`, el CSV reproduce las columnas de `aede_u$a$eigenvalues`.
- **Pregunta que responde:** HT1 y cuántas dimensiones son interpretables dentro de cada ventana (OE6).
  Si Roberto quiso decir otra cosa (por ejemplo, el valor absoluto de las cargas), debe precisarlo
  (decisión G).

### Apunte 8 · maxcl = 10 → 20, y el CH que elige el tope — 3b · N

- **Diagnóstico previo:**
  - la serie de $\lambda_1$ de ventanas solapadas (59 de 60 meses comunes) es casi suave, de modo
    que la suma de cuadrados intra cae con cada clase adicional;
  - el CH (las dos fórmulas) supone observaciones independientes;
  - **es previsible** que con maxcl = 20 elija otra vez el tope.
  Esto no es un resultado sino una hipótesis que la iteración debe contrastar. Si se confirma, el
  CH no sirve como selector en esta serie.
- **Qué se calcula:**
  - k* según el codo, el CH con $k$ y el CH con $k-1$, con maxcl ∈ {10, 15, 20}, para `aede` (dos
    vías, dos esquemas de pesos) y para la datación PCA-MM12;
  - un indicador de si k* = maxcl;
  - **un nulo:** la distribución de k* bajo estructura constante, con series simuladas con la
    matriz de correlaciones global y la dinámica de cada serie (remuestreo por bloques de sus
    residuos). Es la primera pieza del contexto simulado (OE11).
- **Dónde:**
  - Rmd, A.3, B.3, A.6 y B.6;
  - para Python, un notebook nuevo, `notebooks/09a_datacion_pca.ipynb`, sin `torch`, con
    `src/particion.py` (Fisher). Debe reproducir `09_regimenes_pca.csv` en las dos vías con
    maxcl = 10 antes de extenderse.
- **Criterio de aceptación:**
  - las filas con maxcl = 10 reproducen `R_aede_cortes.csv` y `R_regimenes_criterios.csv`;
  - 09a reproduce el 09 (las fechas y el k);
  - tabla k* × maxcl × criterio × vía × pesos;
  - p-valor de k* frente al nulo.
- **Pregunta que responde:** OE9 y, sobre todo, **HT3**, cuyo criterio en contra es literalmente
  «cortes […] que dependan de la regla que fija su número». También aporta la evidencia para la
  decisión D-1.

### Apunte 9 · Ventana de 60 → 24 y 36 meses — 3b · N

- **Qué se calcula:**
  - EPCA con la regla del 06 (Python 06 y Rmd) y `aede` con 24, 36 y 60 meses (este último, de
    referencia) en las dos vías;
  - las transiciones, con la marca de borde de ventana según la definición única de episodios (R-1);
  - **el criterio formal de OE4** (RV o Procrustes entre ventanas consecutivas), definido y
    registrado en `decisiones.qmd` **antes** de correrlo.
- **Dónde:** el notebook 06, con la ventana como parámetro (hoy 06b es solo TRA, con paso 3 y
  StandardScaler); Rmd, A.3 y B.3; los CSV `06_epca_transiciones_*` en formato largo, con una columna
  `ventana`.
- **Criterio de aceptación:**
  - con 60 meses, los archivos actuales se reproducen sin cambios;
  - paridad de las transiciones de la regla del 06 para cada ventana;
  - tabla de transiciones por ventana, con la marca de borde;
  - la estabilidad de 2017-10 en 24, 36 y 60 meses con los dos esquemas de pesos (R-3).
- **Pregunta que responde:** OE4 (compromiso firme, sin ejecutar), HT1 y la presentación de 2017-10.

### Apunte 10 · «El trend ha ayudado a la PCA» — 3a · N (ver sección 4)

- **Qué se calcula:** el contraste entre el PCA de NIV y el PCA de **NIV sin tendencia lineal**
  (residuos de cada serie sobre $t$). Es un diagnóstico, no una tercera vía (decisión D). Se miden:
  - la inercia de PC1 a PC4, el KMO y el χ² de Bartlett;
  - la congruencia de Tucker de las cargas de PC2 a PC4 entre NIV y NIV sin tendencia, y frente a TRA;
  - el nulo de tendencias independientes, aplicado también a las series sin tendencia.
- **Dónde:**
  - 05 → `05_pca_contraste_tendencia.csv`;
  - el nulo **ya calculado** en el Rmd (chunk `b2s-nulo`) se exporta a `R_nulo_tendencias.csv` y se
    porta a 05, con índices compartidos para la paridad exacta (como en el apunte 5);
  - Rmd, sección 2 y A.2.
- **Vía:** NIV, con TRA como referencia.
- **Criterio de aceptación:**
  - el CSV del nulo reproduce las proporciones del HTML (0,90; 0,01; 0,21; 0,93 con deriva y
    0,00; 0,59; 0,95; 0,02 sin deriva);
  - paridad;
  - congruencias informadas con umbrales de fuente fichada. Los umbrales 0,95 y 0,85 que hoy usa el
    Rmd no tienen fuente marcada (hallazgo menor, para el bibliotecario).
- **Pregunta que responde:** el sustento de D2 y la Parte C.

### Apunte 11 · Regresión de cada componente sobre el tiempo, con análisis de residuos — 3a · N (ver sección 4)

- **Qué se calcula:** para PC1 a PC4 de las dos vías:
  - MCO de $\text{PC}_k = a + b\,t + e$: pendiente, $R^2$ y gráfico de residuos con los episodios;
  - sobre los residuos: ACF (rezagos 1 y 12), Ljung-Box, ADF y KPSS, con especificación y rezagos
    **fijos y declarados**;
  - lo mismo para cada una de las 17 series de NIV, para saber a cuáles corresponde el nulo con
    deriva y a cuáles el nulo sin deriva.
- **Dónde:** 05 → `05_pca_tendencia_componentes.csv` y `05_tendencia_series.csv`; Rmd, A.2 («El
  primer componente y el tiempo») y B.2 («Las componentes y el tiempo»).
- **Requisito:** instalar `statsmodels`, que ya está en `requirements.txt`.
- **Criterio de aceptación:**
  - $r(\text{PC1}, t)$ reproduce el 0,993 del HTML;
  - estadísticos ADF y KPSS en paridad con `tseries`/`urca` (1e-6), con los mismos rezagos y
    términos determinísticos. Los p-valores pueden diferir porque las tablas de interpolación son
    distintas, así que se comparan los estadísticos;
  - clasificación de cada componente con una **regla fijada antes de correr** (decisión C):
    - ADF rechaza al 5 % y KPSS no → estacionaria en tendencia (TS);
    - ADF no rechaza y KPSS sí → integrada (DS);
    - otro caso → indeterminada.
  - Se informa que, ante la evidencia de una regresión espuria, los estadísticos t de la pendiente
    no son válidos si los residuos son integrados (Granger y Newbold, 1974; Phillips, 1986, ambos
    sin ficha).
- **Pregunta que responde:** D1 y D2, la elección del nulo y la Parte C.

### Apunte 12 · Correlación entre las variables representativas de las 3 clases de la HFC (nodo 31) — 3b · R

- **Precisión necesaria, comprobada en `R_hfc_jerarquia.csv`:** el «nodo 31» es una de las tres
  clases que quedan al cortar la raíz (33) y el nodo 32; no es el corte mismo. **La numeración no
  es comparable entre vías:**

  | Vía | Las tres clases |
  |---|---|
  | NIV | nodo 30 (12 series), nodo 31 = EMBIG + Índice BVL (2) y nodo 27 (3) |
  | TRA | nodo 31 (9), nodo 23 (2) y nodo 29 (6) |

  Las clases se comparan por su composición, nunca por el número.
- **Qué se calcula:**
  - por clase: su factor (el primer componente de la clase, la representación nativa de la HFC) y
    su serie más correlacionada con ese factor;
  - matrices de correlación 3 × 3 entre factores y entre representantes, con intervalos bootstrap
    por bloques;
  - en NIV, también sin tendencia, porque las clases con tendencia inflan su correlación (apunte 10).
- **Dónde:** Rmd, A.4 y B.4 → `R_hfc_clases3.csv`. Es solo R (decisión E).
- **Criterio de aceptación:**
  - composición de cada clase con nombre y código BCRP;
  - el desarrollador documenta la relación entre la correlación de los factores hijos y el
    `Eigenv` de la fusión, y el auditor la verifica contra `R_hfc_jerarquia.csv` (en la iteración
    2 ya verificó $\lambda = 1+|r|$ para fusiones de dos hojas).
- **Pregunta que responde:** HT2 (correspondencia con los tres bloques de Camiz et al., 2026) y OE5.
  Atención: en NIV, el grupo de riesgo queda reducido a dos series, cuando la ficha de 2026 le
  asigna cuatro.

### Puntos que no aportan a ningún objetivo

El 7, en su lectura literal: es un cambio de escala. Con los umbrales por ventana pasa a ser
recomendable. El 2 no se puede evaluar. Los demás responden a un objetivo firme o a una hipótesis de
trabajo.

---

## 4. Apuntes 10 y 11 frente a D1, D2 y la evidencia ya obtenida

**Qué se sabe hoy** (HTML del Rmd; sin CSV, ver diagnóstico 4):

- El PC1 de NIV explica 67,2 %, con $r(\text{PC1}, t) = 0{,}993$. Las correlaciones con el tiempo de
  PC2, PC3 y PC4 son de 0,080, 0,036 y 0,015.
- La proporción del nulo **con deriva** es de 0,90 para PC1 y 0,01 para PC2. La del nulo **sin
  deriva** es de 0,00 para PC1 y 0,59 para PC2.
- El KMO es de 0,86 en NIV y 0,70 en TRA.

«El trend ha ayudado a la PCA» es cierto en sentido **mecánico**: la tendencia sube la inercia del
PC1, el KMO y el χ² de Bartlett. El nulo con deriva muestra que esa ayuda no prueba co-movimiento:
17 series independientes con sus derivas darían un PC1 mayor (74,6 % de mediana). La lectura
contraria, que es legítima desde «datos primero», sostiene que la tendencia **es** información:
la profundización financiera es un hecho estructural, y que el PCA la capte es un acierto. La tesis
no debe elegir entre ambas lecturas por argumento. El apunte 11 es el que las discrimina.

**El punto clave:** la conclusión de D2 sobre el PC2 depende del nulo que se elija. Con deriva, el PC2
es co-movimiento real (0,01); sin deriva, no lo es (0,59). Para saber qué nulo corresponde a cada
serie hay que saber si su tendencia es determinística (TS) o estocástica (DS). Eso es lo que
responde el análisis de residuos del apunte 11.

| Resultado del apunte 11 | Qué cambia en la tesis |
|---|---|
| **Residuos del PC1 de NIV estacionarios (TS)** y, en las series, predominio de TS | El nulo pertinente es el que tiene deriva: se sostienen el «PC1 = profundización» y el «PC2 = co-movimiento real». Además, el residuo del PC1 sin tendencia es un **candidato a ciclo** que hoy se descarta. Habría que analizarlo, con la datación, como variante y con el nulo aplicado a las series sin tendencia (apunte 10). Se refuerza D1: se mide en niveles y la tendencia se quita del **factor**, no de las series. Es una alternativa a la Parte C que respeta «datos primero» y que conviene llevar al Dr. Camiz. |
| **Residuos del PC1 integrados (DS)** y predominio de DS en las series | La regresión sobre $t$ es espuria y el PC1 no admite una lectura cíclica. El nulo pertinente para las series DS es el sin deriva, de modo que **el argumento «PC2 supera el nulo» se debilita** (0,59). Se refuerza la Parte C tal como está propuesta: la estructura se mide en niveles y la detección se hace sobre las series transformadas. La tesis debe reescribir el hallazgo de D2 condicionado al tipo de tendencia. |
| **Mixto o indeterminado** (series con distinto tipo de tendencia, o pruebas en conflicto, como es probable con n = 228 y quiebres como el de 2020) | Ningún nulo único es adecuado. Hay que construir un nulo **por serie**, con o sin deriva según su clasificación, y volver a calcularlo. Se declara la baja potencia de ADF y KPSS ante quiebres estructurales (fuente: propuesta para el bibliotecario, por verificar). La Parte C se presenta como condicional y no se redactan los resultados hasta discutirla con el asesor. |

En los tres casos, el PC2 de NIV necesita su propia regresión. Si tiene pendiente nula y residuos
estacionarios, es el portador del ciclo en niveles, lo que refuerza D1 para la datación con PC2 y PC3
(variante que ya existe en A.6). En TRA se espera una pendiente nula. Los residuos servirán, además,
para documentar la estacionalidad residual ya detectada (demanda interna, con una ACF de 0,58 en el
rezago 12).

**Consecuencia para el plan:** los apuntes 10 y 11 son la evidencia que falta para discutir la Parte C
con el Dr. Camiz. Deben cerrarse en 3a, y la reunión con él debe ir después de 3a y antes de 3b
(decisión N).

---

## 5. Recomendaciones priorizadas (además de los 12 apuntes)

| Prioridad | Recomendación | Evidencia |
|---|---|---|
| N | Exportar a `data/results/` las cifras que hoy solo están inline en el Rmd: nulo de tendencias, KMO y Bartlett, bootstrap de cargas y estabilidad de cortes. | Diagnóstico 4; regla 3; sin esto, `generar_cifras.py` no puede emitirlas. |
| N | Crear `src/multivariado.py` (PCA con la regla de Rcamiz, Horn, RV, Procrustes, Tucker, KMO y Bartlett), `src/remuestreo.py` y `src/particion.py`, sin `torch`. **No modificar `modelos_dl.py`**: 08 y 09 no pueden re-ejecutarse aquí para verificar el cambio. La unificación queda para cuando haya `torch`. | `modelos_dl.py:35` importa `torch`. |
| N | 05 escribe `05_dimensiones.csv` (n, p, fecha inicial y fecha final por vía, con `assert`) como fuente de 228, 227 y 17 para `cifras.tex`. | Regla 3: las cifras salen solo de `data/results/`. |
| N | Renombrar las salidas de 05 según la regla del desarrollador: NIV en `data/results/niveles/05_*`. Las `05_*` trimestrales se reemplazan; su estado queda en git, y conviene el tag `v0.3-trimestral` antes de reemplazarlas. | D3 («siguen hasta que se rehaga 05»); `desarrollador.md`, regla 3. |
| N | Registrar la excepción de paridad para `aede` y `clahfac` (solo R, validados contra el binario). | Evita un hallazgo mayor automático por 8b (decisión E). |
| R | Parámetro del Rmd `version_asesor` (FALSE por defecto) que oculte los recuadros «Para Roberto». | D-4 abierta; el repositorio es público. |
| R | Cerrar C-01 (comentario «verificados contra la API…», Rmd:166) y C-02 (fila del registro), y corregir «227 meses × 17» en `03_metodologia.qmd`. | Auditoría 2, C.2; `03_metodologia.qmd:4`. |
| R | Primera pieza del contexto simulado (OE11), ligada al nulo del apunte 8. | OE11 es firme y no ha empezado; sin él, D-1 y el ancho de ventana no se pueden calibrar. |
| O | Llevar a `notebooks/` las copias en niveles de 08 y 09 (D-3). | Requiere `torch`: queda diferido. |

---

## 6. Decisiones que solo Roberto (o el Dr. Camiz) puede tomar

**Antes del conforme de 3a**

| ID | Decisión | Opciones | Recomendación |
|---|---|---|---|
| A | Dividir la iteración | Una sola / 3a + 3b | **3a + 3b** (sección 2). |
| B | Clase LaTeX provisional | `book` + geometry / `memoir` | **`book`**: es la más estándar, la más fácil de adaptar a una pauta futura y funciona con biblatex-apa. `memoir` aporta poco mientras no haya pautas de la UNI. Márgenes y espaciado iguales a los de `plantilla_uni.docx`. |
| C | Regla de clasificación TS/DS del apunte 11 | La de la sección 3 / otra | **Aprobarla ahora**, antes de ver los resultados, y registrarla en `decisiones.qmd`. |
| D | Estatus de «NIV sin tendencia» | Tercera vía / diagnóstico | **Diagnóstico.** No contradice D2, porque no se elige vía. Conviene anotarlo como aclaración de D2. |
| E | Paridad de `aede` y `clahfac` | Portar a Python / excepción declarada | **Excepción declarada**: son métodos del asesor, el port en R está validado contra su binario y portarlos a Python duplica el riesgo sin añadir verificación. |
| F | Fecha de corte de los datos | Congelar 2007-01 a 2025-12 / actualizar | **Congelar el vintage actual** como D4, con el md5 de `data/processed/*` y la fecha de descarga. Declarar el riesgo de revisión del ajuste estacional. Además, aquí no hay acceso al BCRP. |

**Antes de 3b**

| ID | Decisión | Recomendación |
|---|---|---|
| G | Aclarar el apunte 2 («Medir la…») y confirmar el sentido del 7 | Sin esto, 3b los deja fuera. |
| H | ¿Los apuntes vienen del Dr. Camiz? | Si vienen de él, se le responde con una tabla «apunte → evidencia → archivo», al cierre de 3b y con la interpretación consolidada (regla 7). |
| I | Convención de fechado de los episodios (R-1) | **La fecha del evento o anuncio externo** y una tolerancia declarada de antemano (HT3) para absorber el rezago de transmisión. Por ejemplo, ±3 meses como principal y ±6 como sensibilidad. El «impacto en el Perú» tiende a fecharse con indicadores locales, lo que roza la regla 6. Decide Roberto. |
| J | Fórmula del CH (D-1) | Informar las dos. **No usar el CH como selector** salvo que muestre un óptimo interior con maxcl = 20 y frente al nulo (apunte 8). Preguntar al Dr. Camiz si el $k$ de `aede` es deliberado, planteado como pregunta y no como corrección. |
| K | Regla de respaldo en niveles (D-2) | Formalizarla en el capítulo de métodos de LaTeX como una regla en dos pasos, **antes** de los resultados de 3b, y evaluarla en el contexto simulado. Nunca ajustarla mirando las fechas. |
| L | Transición 2017-10 (R-3) | Presentarla como «transición no confirmada». Solo se reclasifica si aparece con al menos dos anchos de ventana y con los dos esquemas de pesos, y si no coincide con un borde de ventana. |
| M | ¿Mostrar el Rmd al asesor? (D-4) | **No presentarlo formalmente** hasta cerrar 3b. Con el parámetro `version_asesor`, la versión que vea no tendrá los recuadros internos. Tener presente que el repositorio es público y él lo revisa. |
| N | Parte C con el Dr. Camiz | **Reunión después de 3a**, con la sección 2 del Rmd y los apuntes 10 y 11 como paquete de evidencia. Es la ruta crítica para los capítulos 3 a 5. |

---

## 7. Plan de la iteración 3a (para el conforme)

**Objetivo:** PCA estático mensual en dos vías, en Python y R, que responda a los apuntes 1, 3, 4, 5
(parte estática), 10 y 11; puesta en marcha de la tesis LaTeX con los capítulos 1 y 2 formalizados;
informe derivado de ella; y bibliografía en las prioridades 1 y 2. **Sin resultados en la tesis**
(regla 7): los resultados quedan en el notebook, el Rmd y la nota del desarrollador.

**Rama:** `iteracion-3a`.

**Orden:**

1. El desarrollador y el bibliotecario trabajan en paralelo.
2. El redactor LaTeX arranca la estructura y la notación desde el inicio, y cita cuando el
   bibliotecario entrega.
3. El editor del informe trabaja después del redactor.
4. Al final, el auditor.

### Desarrollador

1. `src/multivariado.py`, `src/remuestreo.py` y `src/particion.py` (sin `torch`), con pruebas mínimas
   contra el Rmd. Instalar `statsmodels`.
2. Reescribir `notebooks/05_pca.ipynb` en frecuencia mensual con las 17 series y las dos vías, y con
   `assert` de 228 × 17 y 227 × 17, calendario continuo y ausencia de faltantes. Secciones:
   dimensiones; ACF y correlaciones (apunte 3); KMO y Bartlett (apunte 4); PCA, criterios de
   retención y cos² (apunte 1); bootstrap con L ∈ {12, 24, 36} (apunte 5); tendencia y residuos
   (apunte 11); contraste sin tendencia y nulo (apunte 10).
3. Rmd: los mismos cálculos en A.2, B.2 y la sección 2; exportar el nulo, la adecuación, el bootstrap
   y los índices compartidos; añadir las filas nuevas de paridad. Añadir el parámetro `version_asesor`.
   Cerrar C-01.
4. `herramientas/generar_cifras.py`:
   - lee un mapa versionado, `herramientas/cifras_mapa.csv` (macro, archivo, fila, columna, formato
     con coma decimal);
   - escribe `tesis_latex/cifras.tex` y un archivo de valores para Quarto;
   - es idempotente.
5. Nota `auditorias/notas/AAAA-MM-DD_desarrollador.md`, con una línea de interpretación y las dudas
   abiertas de cada resultado. En particular, la clasificación TS, DS o indeterminada de cada
   componente según la regla C, **sin** sacar conclusiones sobre la Parte C.

### Bibliotecario

- **Prioridad 1** (bloquea el texto):
  - Atoche Murrieta (2022), Benzécri (1973), Calinski y Harabász (1974), Horn (1965) y Eckart y
    Young (1936);
  - las fuentes de la prueba de esfericidad de Bartlett y del KMO;
  - Granger y Newbold (1974) y Phillips (1986);
  - completar las fichas preliminares de Fisher (1958) y Baldi y Hornik (1989), que sostienen
    proposiciones del capítulo 2.
- **Prioridad 2:** fuentes externas citables (BCRP, FMI, BIS, Reserva Federal, OMS, Congreso de la
  República) para los seis episodios del registro. Para cada uno: la fecha que respalda la fuente y si
  corresponde al anuncio o al impacto. La convención la decide Roberto (decisión I).
- **Prioridad 3 · propuestas del asesor, todas por verificar:**
  - fuente del bootstrap por bloques móviles (se suele atribuir a Künsch, 1989);
  - fuente del tamaño muestral efectivo para correlaciones entre series autocorrelacionadas y del
    $n$ efectivo de Kish;
  - fuentes de ADF y KPSS (Dickey y Fuller; Kwiatkowski et al.);
  - pruebas de raíz unitaria con quiebre (se suele citar a Perron, 1989);
  - coeficiente de congruencia de Tucker y sus umbrales de 0,85 y 0,95;
  - criterio de Rencher (OE6) e índice de Rand ajustado.
- **Entregable:** fichas con la Ficha Estándar, entradas del `.bib`, registro actualizado y una nota
  con el conteo de marcas abiertas antes y después.

### Redactor LaTeX

1. Estructura de `tesis_latex/`:
   - `tesis.tex`, `preambulo.tex`, `notacion.tex` (macros y lista de símbolos), `cifras.tex`
     (generado), `capitulos/`, `apendices/`, `README.md` y `latexmkrc`;
   - clase según la decisión B; biblatex-apa con `tesis/referencias.bib`;
   - `\graphicspath` hacia `reports/figures/`;
   - macro `\pendiente{}`.
2. Capítulo 1 llevado desde el informe aprobado, sin afirmaciones nuevas y con las cifras de
   `cifras.tex`.
3. Capítulo 2 con el rigor de la tesis. Hay que formalizar con definiciones las piezas que el
   informe ya expone: PCA, cos² y contribuciones, KMO y Bartlett (apunte 4), HFC, EPCA ponderada
   (con la corrección de M1 de la iteración 1), el algoritmo `aede` con su convención de fechado,
   Fisher, el CH en sus dos variantes, RV, autoencoder y LSTM. Proposiciones:
   - **con demostración propia** (no requieren cita):
     - (i) la correlación ponderada de la EPCA es una matriz de correlaciones si la
       estandarización también es ponderada;
     - (ii) en la HFC, la fusión de dos variables estandarizadas tiene $\lambda_1 = 1+|r|$;
     - (iii) la ganancia de la primera diferencia es $2\sin(\pi/P)$;
     - (iv) la subestructura óptima de la partición de Fisher;
   - **con cita a una ficha** (o `\pendiente`): Eckart-Young y la equivalencia entre el
     autoencoder lineal y el PCA.
4. Nota `auditorias/notas/AAAA-MM-DD_redactor-latex.md`, con las inconsistencias entre el código y
   la teoría que encuentre (se informan al desarrollador; no se resuelven en el texto).

### Editor del informe

1. Derivar los capítulos 1 y 2 del informe desde la tesis: alinear la notación con `notacion.tex` y
   leer las cifras del archivo generado. **Ningún contenido nuevo** que no esté en la tesis.
2. Una tabla de correspondencia «sección del informe → etiqueta de LaTeX» en `tesis/README.md`.
3. Corregir `03_metodologia.qmd` («227 × 17») y C-02.

### Criterios de aceptación de 3a (verificables por el auditor)

1. `05_pca.ipynb` se ejecuta de principio a fin con `nbconvert`, sin errores. Sus `assert` de
   dimensiones pasan y escribe todos los CSV listados en la sección 3.
2. El Rmd se renderiza con exit 0, sin `Warning` ni `Error`. `R_paridad_python.csv` incluye las
   filas nuevas (valores propios mensuales, cos², ACF, KMO y Bartlett, bootstrap con índices
   compartidos, ADF y KPSS de los residuos, nulo), y todas coinciden.
3. El CSV del nulo reproduce las proporciones del HTML actual (sección 3, apunte 10).
4. `generar_cifras.py`, ejecutado dos veces, da un `cifras.tex` idéntico byte a byte. Cada macro
   remite a una fila del mapa, y cada fila del mapa, a un CSV existente.
5. `latexmk -lualatex -cd tesis_latex/tesis.tex`: exit 0, sin citas ni referencias indefinidas y
   sin cajas desbordadas de más de 10 pt.
6. Ningún número de datos escrito a mano en `tesis_latex/capitulos/*.tex`: el auditor busca dígitos
   fuera de las macros, con una lista de excepciones (años de cita y numeración).
7. Cada símbolo matemático de los capítulos 1 y 2 está definido en `notacion.tex`.
8. Cada `\pendiente` y cada `[VERIFICAR]` tiene su fila en el registro. Cada clave citada tiene una
   ficha en `papers/`.
9. Las proposiciones de demostración propia se comprueban numéricamente en un script del auditor, en
   su scratchpad.
10. Toda afirmación de los capítulos 1 y 2 del informe está sostenida por la tesis (criterio 8c).
    `quarto render tesis/` termina sin advertencias.
11. El capítulo de resultados no cambia, ni en la tesis ni en el informe (regla 7).

### Esbozo de 3b (se revisa al cierre de 3a)

- **Precondiciones:** decisiones G, I, J, K y L; las fuentes de los episodios fichadas en 3a; y,
  si es posible, la reunión N.
- **Contenido:**
  - apuntes 6, 7, 8 y 9 (`aede` y la regla del 06 con 24, 36 y 60 meses; maxcl hasta 20 con su
    nulo; criterio RV o Procrustes registrado de antemano para OE4);
  - apunte 12 y bootstrap de la HFC (OE5);
  - `notebooks/09a_datacion_pca.ipynb`;
  - definición única de los episodios en el código (`modelos_dl.py` se cambia solo en su
    diccionario, o los episodios se leen de un CSV compartido);
  - apunte 2, si se ha aclarado.

---

## 8. Riesgos

**Ante el Dr. Camiz**

1. **Malinterpretar sus apuntes**, si son suyos. Por ejemplo, el 10 puede expresar que la tendencia
   es información y no un estorbo. Mitigación: responder punto por punto con la evidencia y sin
   reformular su pregunta (decisión H).
2. **Que la regresión sobre el tiempo y el contraste sin tendencia se lean como un abandono de
   «datos primero».** Mitigación: presentarlos como diagnósticos sobre los datos tal como se
   publican, con la alternativa de quitar la tendencia del factor y no de las series, que es
   coherente con su posición.
3. **Corregir su código.** El CH con $k$ y el signo lineal de `aede` se plantean siempre como
   preguntas.
4. **La Parte C, aún no discutida**, condiciona los capítulos 3 a 5. Si se redactan antes de la
   reunión, puede haber que rehacerlos.

**Ante el jurado** (perfil de modelización matemática)

1. **Supuestos violados:** Bartlett, el CH y el bootstrap por bloques suponen independencia o
   dependencia débil, y en NIV no la hay. Deben declararse, y conviene usar $n_{\text{ef}}$ (apuntes
   3, 4 y 5).
2. **Regresión espuria** en el apunte 11: los estadísticos t de la pendiente no son válidos con
   residuos integrados. Solo se interpreta la clasificación TS o DS.
3. **Multiplicidad de especificaciones** (*garden of forking paths*): elegir a posteriori la
   ventana, el maxcl o la fórmula que «mejor» calza con los episodios invalidaría HT3. Mitigación:
   registrar los criterios en `decisiones.qmd` antes de 3b y presentar la grilla como un análisis
   de sensibilidad, no como selección.
4. **Compromisos firmes sin ejecutar:** OE4 (criterio de ventana), OE5 (bootstrap de la HFC) y OE11
   (contexto simulado). El jurado los contrastará con la ficha de inscripción. OE11 es además el
   único camino para calibrar el CH y la ventana.
5. **Poder estadístico:** cinco o seis episodios y n/p = 1,4 con ventanas de 24 meses. Declararlo,
   como ya hace el capítulo 1 con las hipótesis de trabajo.
6. **Proposiciones citadas sin ficha** (Eckart-Young y Baldi-Hornik, con ficha preliminar): no
   pueden presentarse como demostradas. Conviene demostrar en casa lo que sea breve.

**Del proceso**

1. 3a sigue siendo grande. Si el auditor observa la tesis LaTeX y el 05 a la vez, conviene que
   el orquestador reparta las vueltas por agente para no agotar las dos vueltas en un solo frente.
2. No se conoce la fecha de entrega de MMC102; Roberto debe confirmarla, porque puede reordenar
   3a y 3b.
3. `statsmodels` debe instalarse para el apunte 11. Si no se puede, el desarrollador debe detenerse
   y avisar, no simular.
