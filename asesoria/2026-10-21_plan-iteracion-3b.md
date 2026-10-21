# Asesoría · Plan de la iteración 3b · 21 de octubre de 2026

**Agente:** Asesor de tesis (`.claude/agents/asesor-tesis.md`). No edita ni ejecuta el material
de la tesis: recomienda. Roberto decide y da el conforme.

**Base:** `main` en `e67f0ac` (iteración 3a integrada y publicada). **Fuentes leídas:** `CLAUDE.md`,
`decisiones.qmd` (D1–D6), `asesoria/2026-10-20_plan-iteracion-3.md` (secciones 3, 6 y 7),
`auditorias/2026-10-20_iteracion-3a.md`, `auditorias/2026-10-21_iteracion-3a_vuelta2.md`,
`auditorias/notas/2026-10-20_{desarrollador,desarrollador_port,bibliotecario}.md`,
`data/results/{,niveles/}` (05, 09, `R_aede_cortes`, `R_regimenes_criterios`, `R_hfc_jerarquia`),
`src/{camiz_port,particion,remuestreo}.py`, `tesis_latex/capitulos/01–03`,
`tesis/registro_verificacion.md` y los bloques `funciones`, `b4-replica` y `b8-estabilidad-cortes`
del Rmd.

**Qué no repite este documento:** la descripción de los apuntes 6 a 12 y sus criterios básicos
están en la sección 3 del plan anterior. Aquí solo se ajustan a lo que dejó 3a y a D6.

---

## 1. Diagnóstico tras 3a (una página)

1. **El PCA estático está cerrado y es reproducible en las dos lenguas** (49 de 49 filas de paridad;
   114 CSV idénticos byte a byte tras volver a ejecutar). Ya no es el cuello de botella.

2. **La regla D5 dio el escenario 2 del plan anterior, pero con un matiz que el plan no previó.**
   - Clasificación (`niveles/05_clasificacion_d5_resumen.csv`): componentes en niveles 0 TS / 4 DS;
     series en niveles 1 TS (EMBIG) / 13 DS / 3 indeterminadas.
   - Con eso, el nulo pertinente **no** es el que tiene deriva para todas las series. Pero tampoco es
     el que no la tiene: D5 distingue TS de DS, **no** si una serie DS tiene deriva. Un cálculo
     exploratorio del asesor (scratchpad, no versionado, **no citable**: media de los incrementos con
     error HAC de Newey-West, 12 rezagos) separa dos grupos. Los créditos, M1–M3, el IPC y las reservas
     tienen deriva clara (|t| entre 2,9 y 14). Las tasas, el tipo de cambio, el EMBIG y el índice BVL
     no la tienen (|t| < 1,4).
   - **Consecuencia:** ni el nulo con deriva (PC2: 0,015) ni el nulo sin deriva (PC2: 0,592)
     (`niveles/05_nulo_tendencias.csv`) es el nulo de estos datos. Hace falta un **nulo mixto por
     serie**, con una regla fijada antes de calcularlo (decisión O). Mientras no exista, la frase
     «el PC2 supera el nulo» no puede sostenerse ni descartarse.

3. **La evidencia de estructura común en niveles depende de tratar los meses como independientes.**
   - La mediana de $n_{\text{ef}}$ es 10,4 de 228.
   - Con $n_{\text{ef}}$, el χ² de Bartlett baja a 162,5 (p = 0,060) (`niveles/05_adecuacion.csv`).
   - Sin la recta de cada serie, el KMO cae de 0,862 a 0,701 y el PC1, de 67,2 % a 40,0 %
     (`niveles/05_pca_contraste_tendencia.csv`).
   - Esto no invalida la vía en niveles (D1), pero obliga a que **toda** la parte dinámica de 3b
     tenga un nulo de referencia, no solo umbrales nominales.

4. **El número de dimensiones (OE6) sigue sin criterio, y ya no se puede fijar «a ciegas».** En
   niveles, λ3 > 1 en el 89 % de las réplicas con L = 24 y λ4 en ninguna; Horn da 2 en niveles y 4 en
   las transformadas (`05_bootstrap_valores_propios.csv`, nota del desarrollador §4.4). Cualquier umbral
   que se elija hoy se elige conociendo estas cifras (decisión P).

5. **La parte dinámica está intacta desde la iteración 2.**
   - `aede` solo corre con $n_w = 60$ y maxcl = 10 (Rmd `:2447` y `:3868`; port, ídem).
   - El CH elige el tope (k = 10) en 7 de las 8 filas de CH de `R_aede_cortes.csv` (dos vías). La
     excepción es niveles, pesos uniformes, CH con $k-1$: k = 2, igual que el codo.
   - La estabilidad de cortes (`b8-estabilidad-cortes`, 200 réplicas) se sigue calculando inline y no
     se escribe en `data/results/` (regla 3).
   - El port de Python solo se probó con $n_w = 24$ en datos simulados (`tests/test_camiz_port.py:95`).
   - `src/particion.py` no admite longitud mínima de segmento, que la datación del 09 sí usa
     (`tam_min = 12`).

6. **Escala de la ventana: con 24 meses el problema es casi de rango completo.**
   - Con pesos gaussianos (`nsd = 3`), el $n$ efectivo de Kish, $1/\sum\omega^2$, es 18,2 con
     $n_w = 24$, 27,6 con 36, 37,0 con 48 y 46,4 con 60. Es una propiedad de los pesos de
     `pesos_aede`, no de los datos.
   - Con $p = 17$ y $n = 24$, el p95 de Horn para λ1, λ2 y λ3 es de unos 3,3, 2,7 y 2,3 (simulación
     del asesor). La expectativa razonable es que solo λ1 sea interpretable en ventanas cortas. El
     apunte 7 deja de ser cosmético: es la prueba de cuántas dimensiones existen dentro de cada ventana.

7. **Los episodios siguen siendo el bloqueo de la validación (HT3, OE10).**
   - Hay fuentes fichadas para 5 de los 6 episodios, pero conviven dos juegos de fechas (Rmd y
     `modelos_dl.py`: 2008-09, 2013-05, 2020-03; `06a` y `06b`: 2008-07, 2013-04, 2020-01).
   - Las fechas de fin del COVID-19 y de las materias primas no tienen fuente. Las fuentes de
     «impacto en el Perú» (BCRP) no fueron accesibles (nota del bibliotecario, §3).
   - `09_discriminacion_episodios.csv` usa las fechas sin fuente, y `torch` no está instalado: 08 y 09
     no pueden volver a ejecutarse aquí. **Sí puede** recalcularse la discriminación a partir de
     `09_walkforward_errores.csv`, que trae el error mensual de LSTM, AE y PCA en las dos vías.

8. **Contradicción a evitar:** el plan anterior marcaba los apuntes 6, 7 y 12 como «solo R
   (decisión E)». D6 la reemplazó: **todo lo de 3b va en paridad Python–R**, con el port como motor
   de Python.

9. **Documentos:**
   - el capítulo 3 de LaTeX y el del informe están vacíos (`03_metodologia.tex`, 7 líneas);
   - el capítulo 2 tiene 5 `\pendiente` de episodios en `sec:validacion` y fuentes sin ficha que 3b
     necesita (Camiz y Diblasi, 2013; Rencher; vara quebrada; Denimal; Lavit);
   - siguen abiertos N-12 (fechado unificado) y N-14 (marcas «sin ficha» en 13 líneas del Rmd y en 5
     de `src/`).

**Juicio de conjunto:** 3b debe hacer por la parte dinámica lo que 3a hizo por la estática:
ponerla en paridad y en una grilla declarada, **pero contrastada siempre contra un nulo de
estructura constante**. Sin ese nulo, la grilla (4 anchos × 2 pesos × 3 maxcl × 3 criterios × 2
vías) es exactamente el «jardín de senderos» que el jurado señalará.

---

## 2. Objetivo de 3b

Llevar la parte dinámica (`aede`, la regla del 06, la datación PCA-MM12 y la HFC) a paridad Python–R
sobre una grilla declarada de antemano, contrastada con un nulo de estructura constante (primera
pieza de OE11), con episodios unificados y fechados con fuentes externas. Además, redactar los
métodos del capítulo 3. **Sin resultados en la tesis ni en el informe** (regla 7).

---

## 3. Decisiones de Roberto y qué bloquea cada una

### 3.1 Antes del conforme (bloquean la fase 1)

| ID | Decisión | Opciones | Recomendación | Bloquea |
|---|---|---|---|---|
| **I** | Convención de fechado de los episodios y tolerancia de HT3 | (a) fecha del evento o anuncio externo; (b) impacto en el Perú | **(a)**, con tolerancia de ±3 meses como principal y ±6 como sensibilidad. Un episodio sin fecha de fin con fuente se trata como **puntual** (solo inicio), sin inventar el fin. | D9, D10, L1, E1; N-12 |
| **O** (nueva) | Nulo de tendencias por serie | (a) seguir con los dos nulos globales; (b) nulo mixto | **(b)**, fijado antes de calcular: TS → recta más residuos remuestreados; DS con deriva si el \|t\| HAC (Newey-West, 12 rezagos) de la media de los incrementos es > 2, y sin deriva en otro caso; las indeterminadas se informan con las dos variantes. | D11, L2 |
| **P** (nueva) | Número de dimensiones (OE6) | Fijar un umbral bootstrap ahora / mantener d = 3 | **Mantener d = 3** como especificación principal, porque se fijó en la iteración 1, antes de las cifras de 3a. Informar d = 2 y d = 4 como sensibilidad. No inventar un umbral cuando las cifras ya se conocen. | D12 |
| **Q** | Criterio de ventana (OE4) y grilla | Grilla {24, 36, 60} / {24, 36, 48, 60}; RV entre ventanas consecutivas / adyacentes | Grilla **{24, 36, 48, 60}**: 48 es el ancho de Camiz et al. (2026) y da comparabilidad con el antecedente (OE3). **RV entre ventanas adyacentes no solapadas** (las consecutivas con paso 1 comparten 59 de 60 meses y su RV es casi 1 por construcción), comparado con el nulo de estructura constante del mismo ancho. La grilla se lee como **multiescala**, no como búsqueda de la ventana «correcta». | D10, L2 |
| **J** | Uso del CH (D-1) | Selector / solo informar | **Informar las dos variantes y no usar el CH como selector**, salvo que muestre un óptimo interior con maxcl = 20 **y** fuera del rango del nulo. Al Dr. Camiz se le pregunta, sin corregirlo, si el $k$ de `aede` es deliberado. | D3, D4, L2 |
| **K** | Regla de respaldo de la datación en niveles (D-2) | Formalizarla ahora / después | **Formalizarla ahora**, en dos pasos: primero la regla del 09 (reducción < 10 %) y, si no elige, la caída máxima. Se registra en `decisiones.qmd` antes de correr la grilla de maxcl. | D3, L2 |
| **L** | Lectura de la transición 2017-10 (R-3) | — | «Transición no confirmada», salvo que aparezca con ≥ 2 anchos **y** con los dos esquemas de pesos, y no coincida con un borde de ventana según I. | D10 |
| **G** | Sentido de los apuntes 2 y 7 | — | Sin aclaración, el apunte 7 se ejecuta en la versión útil (λ frente a Kaiser y Horn por ventana) y el 2 queda fuera de 3b. | D5 |

Todas las aprobadas se registran como **D7 y siguientes** en `decisiones.qmd` **antes** de que el
desarrollador ejecute la tarea que bloquean. El auditor lo comprueba con la fecha del commit.

### 3.2 No bloquean 3b

| ID | Decisión | Recomendación |
|---|---|---|
| **N** | Reunión con el Dr. Camiz sobre la Parte C | **Hacerla ya**, con el paquete de 3a: sección 2 del Rmd en `version_asesor = TRUE`, D5 y la clasificación, el contraste sin tendencia y la pregunta del nulo mixto (O). Bloquea solo la sección «Qué vía mide qué» del capítulo 3 (L3) y, por regla 7, cualquier resultado. |
| **H** | ¿Los apuntes son del Dr. Camiz? | Si lo son, se le responde al cierre de 3b con una tabla «apunte → evidencia → archivo». |
| **M** | ¿Mostrarle el Rmd? (D-4) | Solo la sección 2, para la reunión N. El documento completo, al cierre de 3b. |

### 3.3 Qué avanza ya y qué espera

| Fase | Tareas | Depende de |
|---|---|---|
| **0 (desde el conforme)** | D1–D8, B1–B4 | Ninguna decisión. J y K solo afectan a la **lectura** de D3 y D4, no al cálculo, que informa todos los criterios. |
| **1** | D9–D12 | I, O, P, Q y L registradas; D2–D7 terminadas |
| **2** | L1–L4, E1–E3 | Fase 1; para L3, además, la reunión N (si no se ha hecho, esa sección queda en `\pendiente`) |
| **3** | Auditoría | Todo lo anterior |

Si las decisiones de 3.1 no llegan antes de que termine la fase 0, conviene auditar la fase 0 como
**3b-0** y no esperar con el trabajo sin respaldo.

---

## 4. Plan por agente

Convenciones: NIV = `data/results/niveles/`; TRA = `data/results/`. «Paridad» significa una fila
en `R_paridad_python.csv` de la vía, con tolerancia de 1e-10 salvo que se indique otra. Las réplicas
aleatorias usan **índices compartidos** escritos por el Rmd, como en 3a.

### Desarrollador (12 tareas)

**Fase 0**

- **D1 · N-14.** Sustituir «[VERIFICAR: sin ficha…]» y «propuesta para el bibliotecario» por la cita a
  la ficha con su pendiente vigente, en las 13 líneas del Rmd y las 5 de `src/` que enumera N-14.
  Se mantienen sin ficha la vara quebrada, Adam y Markov.
- **D2 · `src/particion.py` con longitud mínima.** Añadir `n_min` (por defecto 1, que reproduce el
  comportamiento actual), con pruebas contra la fuerza bruta en `tests/test_particion.py`. La
  necesitan el 09a y la regla de `datar` (`tam_min = 12`).
- **D3 · `notebooks/09a_datacion_pca.ipynb`** (sin `torch`):
  1. reproducir `09_regimenes_pca.csv` en las dos vías (fechas y k) con maxcl = 10;
  2. portar `b8-estabilidad-cortes`: el Rmd exporta `R_estabilidad_cortes.csv` (las dos vías) y el
     09a lo reproduce con los mismos índices;
  3. grilla maxcl ∈ {10, 15, 20} × criterio {codo, CH con $k$, CH con $k-1$, regla K}, con la columna
     `k_en_tope`.

  Salidas: `09a_datacion_criterios.csv` en formato largo.
- **D4 · `aede` en grilla (apuntes 6, 8 y 9, parte `aede`).** $n_w$ ∈ {24, 36, 48, 60} × pesos
  {uniformes, gaussianos con `nsd = 3`} × maxcl ∈ {10, 15, 20} × vía, en el Rmd y con el port
  (`999_port_camiz` o un notebook `06c_aede_grilla.ipynb`). `R_aede_cortes.csv` pasa a formato largo
  con las columnas `nw` y `maxcl`; las filas con `nw = 60` y `maxcl = 10` deben ser idénticas a las
  actuales. El auditor verifica numéricamente la convención de fechado de `def:ventana` con
  $n_w = 24$ (centro en la fila $i + n_w/2$).
- **D5 · Valores propios por ventana (apunte 7, versión útil).** `R_aede_valores_propios.csv`
  (fecha del centro, `nw`, pesos, λ1–λ3, $n_\omega$ de Kish, umbral de Kaiser y p95 de Horn con
  $n = \lceil n_\omega \rceil$), más el número de ventanas bajo el umbral por eje y el registro de los
  cruces λ2 ↔ λ3. Para Horn rige la **excepción de generadores de 3a**: se compara el número de
  ventanas bajo el umbral, no el umbral en sí.
- **D6 · Regla del 06 por ancho de ventana (apunte 9, parte EPCA).** `notebooks/06_epca.ipynb` con la
  ventana como parámetro (paso 3, como hoy) para $n_w$ ∈ {24, 36, 48, 60} en las dos vías, y lo
  mismo en el chunk `b4-replica`. Salidas en formato largo, `06_epca_transiciones_*`, con la columna
  `ventana`. Con 60 meses se reproducen los archivos actuales.
- **D7 · Nulo de estructura constante (primera pieza de OE11; HT1).** Remuestreo por bloques
  **conjunto**: los mismos inicios de bloque para las 17 series, con L = 24.
  - En TRA, sobre las filas.
  - En NIV, sobre los incrementos, que luego se acumulan como en `nulo_tendencias`. Así se conserva la
    correlación contemporánea y la dinámica corta, pero se dispersa en el tiempo cualquier cambio de
    estructura.

  Para cada réplica y cada $n_w$ de la grilla se calculan:
  1. el $k^*$ de cada criterio con maxcl = 20;
  2. el perfil del RV entre ventanas adyacentes no solapadas.

  Son 200 réplicas por combinación. La paridad completa se exige en las 20 primeras; el resto, solo en
  Python, **declarado** en la tabla de paridad. Salidas: `R_nulo_estructura_indices.csv`,
  `07b_nulo_estructura_kstar.csv` y `07b_nulo_estructura_rv.csv` (nombres por confirmar con la
  numeración del pipeline).
- **D8 · HFC (apunte 12 y OE5).**
  1. Partición en 3 y 4 clases en las dos vías, con la composición de cada clase (nombre y código
     BCRP). Las clases se comparan **por composición, nunca por el número de nodo**.
  2. Factor de cada clase, su serie representante y las matrices 3 × 3 de correlación entre factores
     y entre representantes, con intervalos bootstrap. En NIV, también sin tendencia.
  3. Bootstrap de la HFC con `R_bootstrap_indices_L24.csv`: ARI de la partición en 3 y 4 clases
     frente a la original, frecuencia de coclasificación de cada par de series y correlación
     cofenética.

  Salidas: `R_hfc_clases3.csv`, `R_hfc_bootstrap.csv` y sus homólogos de Python.

**Fase 1** (requiere las decisiones registradas)

- **D9 · Episodios unificados (N-12; decisión I).**
  1. Crear un archivo único, `data/referencia/episodios_referencia.csv` (fuera de `data/processed/`
     para no tocar el md5 de D4), con las columnas nombre, inicio, fin (vacío si es puntual),
     `clave_inicio`, `clave_fin`, tipo y convención.
  2. Lo leen el Rmd, el 05, el 06 y `modelos_dl.py`. Este último solo cambia su diccionario por la
     lectura del CSV y no se ejecuta.
  3. `06a` y `06b` quedan como antecedentes superados (D3): se les añade una nota, pero no se
     reescriben.
  4. **Discriminación recalculada sin `torch`** desde `09_walkforward_errores.csv` (las dos vías),
     con la misma regla (umbral 1): `09a_discriminacion_episodios.csv`. El
     `09_discriminacion_episodios.csv` antiguo no se borra, se declara superado y el Rmd deja de
     leerlo.
  5. Marca de borde de ventana para cada $n_w$ con la tolerancia de I.
- **D10 · Criterio de OE4 y 2017-10 (decisiones Q y L).** Por $n_w$ y vía: la proporción de pares
  adyacentes con RV bajo el p5 del nulo de D7, y las transiciones de `aede` y de la regla del 06 con la
  marca de borde. Además, una tabla de 2017-10 por ancho × pesos × método con la clasificación de la
  regla L.
- **D11 · Nulo mixto (decisión O).** Agregar `version='mixto'` a `nulo_tendencias` (Python y Rmd), con
  la regla de O y los mismos índices de `R_nulo_indices.csv`. Salida: filas nuevas en
  `05_nulo_tendencias.csv` y una columna `deriva_hac_t` en `05_tendencia_series.csv`.
- **D12 · Sensibilidad de la dimensión (decisión P), cifras y nota.**
  1. Datación PCA-MM12 con d ∈ {2, 3, 4} en el 09a.
  2. Mapa de cifras ampliado solo con macros de **métodos y datos** (anchos, $n_\omega$, réplicas,
     tolerancias), no de resultados.
  3. Nota en `auditorias/notas/`, con una línea de interpretación y las dudas abiertas por resultado,
     **sin** conclusiones sobre la Parte C.

### Bibliotecario (4 tareas, fase 0)

- **B1 · Huecos de los episodios.**
  - Fuente del fin del COVID-19 y de las materias primas, o constancia de que no la hay (el episodio
    pasa a ser puntual según I).
  - Una fuente de precios de **metales** (el Perú exporta metales; las fichas actuales tratan el
    petróleo).
  - Fichar el D. S. 044-2020-PCM.
  - Fuente primaria de la firma de la «fase uno».
  - Lista de documentos del BCRP que Roberto debe descargar a mano (Incapsula bloquea el acceso
    automático).
- **B2 · Fuentes que 3b usa y aún no tienen ficha:**
  - Camiz y Diblasi (2013) (pesos gaussianos);
  - el capítulo y la página de la fórmula de Kish (`kish_1965`, metadatos ya verificados);
  - el modelo de vara quebrada y el criterio de Rencher (OE6);
  - Denimal (2001, 2007), fuente primaria de la HFC;
  - Bruynooghe;
  - Lavit (1988);
  - Tukey (1977);
  - Jolliffe (2002);
  - un nuevo intento con Atoche Murrieta (2022).
- **B3 · Propuestas del asesor (todas por verificar):**
  - fuente del estimador HAC de Newey-West (si se aprueba O);
  - fuente sobre la estabilidad de clasificaciones jerárquicas bajo remuestreo (OE5);
  - fuente del contraste del coeficiente RV bajo independencia o por permutación;
  - fuente del bootstrap por bloques **conjunto** para series multivariadas (D7).

  Si no se encuentra una ficha verificable, el texto lo marca `\pendiente` y no se atribuye nada.
- **B4 · Registro.** Una fila por cada marca nueva de D1–D12 y L1–L4, y el conteo de marcas abiertas
  antes y después.

### Redactor LaTeX (4 tareas, fase 2)

- **L1 · `sec:validacion`.** Sustituir los 5 `\pendiente` de episodios por las citas fichadas y
  declarar la convención y la tolerancia de I. Las fechas entran por macro, desde el CSV de D9, vía
  `generar_cifras.py`.
- **L2 · Capítulo 2, piezas formales nuevas:**
  - $n_\omega$ de Kish y umbral de Horn por ventana, con una proposición de demostración propia:
    $n_\omega = n_w$ si los pesos son uniformes y $n_\omega < n_w$ en otro caso (desigualdad de
    Cauchy-Schwarz);
  - Fisher con $n_{\min}$;
  - nulo de estructura constante (D7) y nulo mixto (O);
  - el criterio de OE4 (Q) como definición;
  - la regla de respaldo K en dos pasos;
  - la lectura multiescala de $n_w$.

  Las proposiciones nuevas se verifican numéricamente en el guion del auditor.
- **L3 · Capítulo 3, métodos sin resultados:**
  - datos y vintage (D1, D4), por macro;
  - diseño en dos vías (D2, sin elegir vía);
  - criterios fijados de antemano (D5 y D7 en adelante, con su fecha de registro);
  - implementación, paridad (D6) y reproducibilidad.

  La sección «Qué vía mide qué» (Parte C) queda en `\pendiente` hasta la reunión N.
- **L4 · `notacion.tex` y nota.** Nuevos símbolos ($n_\omega$, $n_{\min}$, $k^*$, RV adyacente) y una
  nota con las inconsistencias entre el código y la teoría para el desarrollador.

### Editor del informe (3 tareas, fase 2)

- **E1 ·** Derivar en el capítulo 2 del informe los cambios de L1 y L2, sin contenido nuevo.
- **E2 ·** Sustituir los recuadros «Pendiente» de `03_metodologia.qmd` por la derivación de L3, con
  las cifras desde `_cifras.yml`.
- **E3 ·** Actualizar la tabla de correspondencia de `tesis/README.md`; `quarto render tesis/` y
  `--to docx` sin avisos.

---

## 5. Orden

1. **Fase 0:** D1–D8 y B1–B4 en paralelo. D2 va antes de D3. D4 va antes de D5 y D7.
2. **Registro de las decisiones** (D7 y siguientes en `decisiones.qmd`), con commit propio, **antes**
   de la fase 1.
3. **Fase 1:** D9 → D10 (usa los episodios y el nulo de D7); D11 y D12 en paralelo.
4. **Fase 2:** L1–L4 → E1–E3.
5. **Fase 3:** auditoría. Si el dictamen observa varios frentes, el orquestador reparte las vueltas
   por agente (lección de 3a).

Rama: `iteracion-3b` (y `iteracion-3b-wip` para los respaldos intermedios). Al integrar, tomar la
rama con el HEAD auditado (en 3a el remoto `iteracion-3a` quedó atrasado).

---

## 6. Criterios de aceptación (verificables por el auditor)

1. `pytest tests/` pasa. `test_particion.py` incluye `n_min` frente a la fuerza bruta, y
   `test_camiz_port.py` incluye `aede` con $n_w$ ∈ {24, 36, 48} contra R.
2. 05, 06, 09a y el notebook de la grilla de `aede` se ejecutan con `nbconvert`, con exit 0. El Rmd
   se renderiza con exit 0, sin `Warning` ni `Error`, en las dos versiones de `version_asesor`.
3. **No regresión:** las filas con `nw = 60`, `maxcl = 10` reproducen el `R_aede_cortes.csv` actual;
   el 06 con 60 meses reproduce `06_epca_transiciones_*`; el 09a con maxcl = 10 reproduce
   `09_regimenes_pca.csv` (las dos vías). Los demás CSV de 3a quedan idénticos byte a byte.
4. **Paridad:** filas nuevas de `aede` (grilla), valores propios por ventana, regla del 06 por ventana,
   09a, estabilidad de cortes, HFC (clases, factores y bootstrap), nulo de estructura (20 réplicas) y
   nulo mixto. Todas en «sí». Las excepciones (generadores de Horn; réplicas del nulo después de la
   20) declaradas en la propia tabla.
5. En `R_aede_valores_propios.csv`: λ1 + λ2 + λ3 ≤ 17 en cada fila; $n_\omega = n_w$ con pesos
   uniformes; con pesos uniformes y `nw = 60`, las columnas reproducen `aede_u$a$eigenvalues`.
6. La tabla $k^*$ × maxcl × criterio × $n_w$ × pesos × vía tiene la columna `k_en_tope`, y cada
   $k^*$ observado se acompaña de su posición en la distribución del nulo de D7.
7. Todos los consumidores (Rmd, 05, 06, `modelos_dl.py` y 09a) leen un **único** archivo de episodios.
   Cada fecha tiene una clave con ficha y entrada en el `.bib`, o está vacía (episodio puntual). Una
   búsqueda de fechas de episodio escritas a mano en el código da cero. N-12 queda cerrado.
8. `09a_discriminacion_episodios.csv`, recalculado con las fechas antiguas, reproduce
   `09_discriminacion_episodios.csv` (prueba de la ruta sin `torch`) antes de aplicar las nuevas.
9. Las decisiones I, O, P, Q, J, K y L están en `decisiones.qmd`, con un commit **anterior** al
   primer commit que contiene sus resultados (`git log`).
10. N-14: cero marcas «sin ficha» para obras con ficha, en el Rmd y en `src/`.
11. `latexmk`: exit 0, sin citas ni referencias indefinidas y sin `Overfull` de más de 10 pt.
    `generar_cifras.py --comprobar`: exit 0. No hay dígitos de datos fuera de macros ni de las
    excepciones declaradas en `tesis_latex/README.md`.
12. Las proposiciones nuevas de L2 se comprueban numéricamente en un guion del auditor.
13. Cada `\pendiente` y cada `[VERIFICAR]` nuevo tiene su fila en el registro. Toda clave citada tiene
    ficha.
14. **Regla 7:** `04_resultados.tex` y `04_resultados.qmd` no cambian. El capítulo 3 no contiene
    cifras de resultados ni conclusiones sobre la Parte C. Las macros nuevas son solo de métodos y
    datos.
15. **Regla 6:** ninguna fecha de episodio se deriva de las series, de los cortes de Camiz et al. (2026)
    ni de un indicador.

---

## 7. Riesgos

**Metodológicos (ante el jurado)**

1. **Senderos que se bifurcan.** Solo `aede` tiene 144 combinaciones (4 anchos × 2 pesos × 3 maxcl ×
   3 criterios × 2 vías), sin contar el 06 ni el 09a. Mitigación: las decisiones se registran antes (criterio 9), se informa la grilla completa y
   todo $k^*$ y todo corte se lee contra el nulo, nunca contra los episodios.
2. **El nulo de D7 también es una elección.** El bloque conjunto con L = 24 conserva la correlación
   contemporánea, pero mezcla tramos de regímenes distintos. Si hay un cambio de varianza fuerte
   (2020), el nulo puede ser «demasiado fácil» de superar. Mitigación: informar también L = 12 y
   L = 36 en las 20 réplicas en paridad, como sensibilidad.
3. **Poco poder estadístico.** Hay entre 5 y 6 episodios, de los cuales algunos serán puntuales. Con
   $n_w = 24$ y pesos gaussianos, $n_\omega \approx 18 \approx p$. HT3 debe presentarse como
   correspondencia descriptiva, como ya hace el capítulo 1.
4. **El nulo mixto (O) es un umbral de |t| > 2 sobre un estimador HAC** que también supone dependencia
   débil de los incrementos. Hay que declararlo, y declarar la frontera de las series con \|t\|
   cercano a 2 (PBI y demanda interna, en la exploración del asesor).
5. **Discriminación de AE y LSTM con episodios nuevos sin volver a entrenar.** Es válido, porque los
   errores walk-forward no dependen de los episodios, pero el texto debe decir que los modelos no se
   volvieron a ejecutar.

**Ante el Dr. Camiz**

6. **Leer la grilla de ventanas como una corrección a su ancho de 48 meses.** Mitigación: presentar 48
   como el ancho de referencia del antecedente y la grilla como lectura multiescala.
7. **El CH con $k$ grados de libertad:** solo como pregunta (decisión J).
8. **Avanzar el capítulo 3 sin la reunión N.** Mitigación: la sección de la Parte C queda en
   `\pendiente`, y el resto del capítulo no elige vía.

**Del proceso**

9. **Tiempo de cómputo.** El nulo de D7 supone unas 200 × 4 × 2 × 2 corridas de `aede` en Python, más
   20 réplicas por combinación en R puro. Si el Rmd supera unos 15 minutos de render, el desarrollador
   mueve el nulo a un chunk con caché declarada o a un script R aparte que escriba el CSV, y lo
   informa. **No reduce réplicas en silencio.**
10. **Tamaño.** La fase 0 por sí sola es comparable a 3a. Si las decisiones se demoran, auditarla como
    3b-0 (sección 3.3).
11. **`torch` sigue ausente:** 08 y 09 no se vuelven a ejecutar. Cualquier cambio en `modelos_dl.py`
    que no sea leer el CSV de episodios queda fuera de 3b.
12. **Fecha de entrega de MMC102:** sigue sin confirmar. Si es cercana, conviene priorizar L3 y E2
    (métodos) sobre D7 y D10.
