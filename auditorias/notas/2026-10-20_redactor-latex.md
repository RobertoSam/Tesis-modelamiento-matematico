# Nota del redactor LaTeX · Iteración 3a · 20 de octubre de 2026

**Agente:** redactor LaTeX (`.claude/agents/redactor-latex.md`). **Rama:** `iteracion-3a` (sin
commit ni push). **Encargo:** sección 7 de `asesoria/2026-10-20_plan-iteracion-3.md`, apartado
«Redactor LaTeX», con la decisión B aprobada por Roberto (clase `book`, márgenes y espaciado de
`tesis/plantilla_uni.docx`).

## 1. Fuentes leídas

- `CLAUDE.md`, `decisiones.qmd` (D1–D6), `asesoria/2026-10-20_plan-iteracion-3.md`.
- `tesis/_capitulos/01_introduccion.qmd` y `02_marco_teorico.qmd` (aprobados).
- `tesis/referencias.bib` y `tesis/registro_verificacion.md` (estado al inicio de la sesión).
- `R/camiz_port.R` completo (fuente de verdad de la EPCA ponderada, `aede_r`, `fisher_r`,
  `clahfacsub_r`, `agrega_r`, `.bstatw_ac`, `.ustatw_ac`).
- `R/tesis_ciclo_financiero.Rmd`, chunk `funciones` (l. 312–491: `pca_basico`, `horn`, `coef_rv`,
  `procrustes`, `particion_fisher`, `datar`, `ch_variantes`, `tucker`, `bartlett_esfericidad`,
  `kmo`, `vara_quebrada`).
- `auditorias/2026-10-18_iteracion-1.md` (hallazgo M1 y su cierre).
- `tesis/plantilla_uni.docx` (márgenes: izquierdo 1701 twips = 3 cm; derecho, superior e inferior
  1417 twips = 2,5 cm; interlineado `w:line="360"` = 1,5 líneas; Arial 12).

## 2. Estructura creada (`tesis_latex/`)

| Archivo | Estado |
|---|---|
| `tesis.tex` | Clase `book` (12 pt, A4, `oneside`); carga `cifras.tex` si existe y después `cifras_stub.tex` (`\providecommand`: solo rellena lo que falte) |
| `preambulo.tex` | Márgenes 3 / 2,5 / 2,5 / 2,5 cm, `\onehalfspacing`, número de página centrado, `amsthm` por capítulo, `cleveref`, biblatex-apa con `../tesis/referencias.bib`, `\graphicspath{../reports/figures/}`, `\pendiente{}` y `\verificar{}` |
| `notacion.tex` | Macros y lista de símbolos (todos los símbolos de los capítulos 1 y 2, incluidos los locales de las demostraciones) |
| `cifras_stub.tex` | Las seis macros del contrato más `\anioInicioDatos` y `\anioFinDatos` (pedidas al desarrollador; ya están en su `cifras.tex`) |
| `capitulos/00_portada.tex` | Portada provisional |
| `capitulos/01_introduccion.tex` | Capítulo 1 |
| `capitulos/02_marco_teorico.tex` | Capítulo 2 |
| `capitulos/03–05_*.tex` | Solo título y `\pendiente` (regla 7 para el 4) |
| `apendices/apendices.tex`, `README.md`, `latexmkrc`, `.gitignore` | Infraestructura; el PDF y los auxiliares no se versionan |

**Fuente (propuesta para Roberto):** Nimbus Sans (paquete `helvet`), clon de Helvetica, cuyas
métricas reproduce Arial; matemáticas en Computer Modern. Mi primera opción era TeX Gyre Heros con
`fontspec`, pero **en este entorno falta `luaotfload`** (paquete Debian `texlive-luatex`, no
instalado) y `fontspec` no funciona con LuaLaTeX. La solución Type 1 + T1 compila en cualquier
TeX Live. Efecto secundario: el log trae la línea `Error in luaotfload: reverting to OT1`, que no
es un error de TeX ni detiene la compilación; conviene que el auditor lo sepa. Los signos « » ¿ ¡
— – “ ” · se declaran con `newunicodechar`.

**Compilación:** `latexmk -lualatex -cd tesis_latex/tesis.tex` → exit 0, PDF de **45 páginas** (44 antes de la pasada de citas)
(`tesis_latex/tesis.pdf`), sin errores de TeX, sin citas ni referencias indefinidas, sin cajas
desbordadas (0 avisos `Overfull`), biber sin avisos, sin fuentes Type 3. Con `-cd`, latexmk no lee
`tesis_latex/latexmkrc`; por eso `tesis.tex` empieza con `\nonstopmode`.

## 3. Lo redactado y sus fuentes

**Capítulo 1** (`tesis/_capitulos/01_introduccion.qmd`, aprobado). Traslado literal, sin
afirmaciones nuevas. Cambios de forma: las cifras de los datos salen de `cifras.tex`
(`\nSeries`, `\nMesesNiveles`, `\nMesesTransformadas`, `\fechaInicioNiveles`,
`\fechaInicioTransformadas`, `\fechaFinDatos`, `\anioInicioDatos`, `\anioFinDatos`); «pierde enero
de 2007» pasa a «pierde el primer mes», y se añaden las fechas de la vía transformada desde
macros; los objetivos son listas con etiqueta (OE1–OE12, OC1–OC4) citables con `\cref`; se remite
a la proposición del autoencoder lineal.

**Capítulo 2** (`02_marco_teorico.qmd`, aprobado, más `R/camiz_port.R` y el chunk `funciones` del
Rmd). Se reordenó por método: antecedentes (2.1); ciclo y definiciones de régimen, transición,
detección y fase (2.2); posición epistemológica (2.3); datos (2.4); PCA, cos² y contribuciones,
número de componentes, KMO y Bartlett (2.5); HFC (2.6); EPCA ponderada y `aede` (2.7); Fisher y
CH (2.8); RV, Procrustes y Tucker (2.9); autoencoder, LSTM y LSTM-autoencoder (2.10); criterios
(2.11); vacíos y aporte (2.12). Todo el texto narrativo del informe se conserva.

| Sección | Fuente |
|---|---|
| 2.1, 2.2, 2.3 (texto), 2.11, 2.12 | Capítulo 2 del informe, con sus citas |
| 2.4, 2.5 (PCA, signo, cos², retención) | Informe; `pca_basico`, `vara_quebrada`, `horn` del Rmd |
| 2.5.4 KMO y Bartlett | `kmo` y `bartlett_esfericidad` del Rmd; fuentes `\pendiente` |
| 2.6 HFC | Informe; `distancia_hfc`, `agrega_r`, `clahfacsub_r`, `clahfac_r` |
| 2.7 EPCA y `aede` | `aede_r`, `.bstatw_ac`, `.ustatw_ac` (fuente de verdad); auditoría 1, M1 |
| 2.8 Fisher y CH | `fisher_r`; `particion_fisher`, `datar`, `ch_variantes` del Rmd |
| 2.9 | Informe; `coef_rv`, `procrustes`, `tucker` del Rmd |
| 2.10 | Informe, con sus citas |

## 4. Proposiciones (numeración del PDF)

**Demostraciones propias (las cuatro del plan):**

- (i) **Prop. 2.30**: la correlación ponderada de la EPCA es una matriz de correlaciones si la
  estandarización es ponderada (más traza = p e invariancia afín); la **Obs. 2.31** da el
  contraejemplo de la estandarización sin ponderar (diagonal 3/4).
- (ii) **Prop. 2.23**: la fusión de dos variables estandarizadas tiene μ₁ = 1 + |r| y
  μ₂ = 1 − |r| (con el **Lema 2.22** del PCA de dos factores).
- (iii) **Prop. 2.5**: la ganancia de la primera diferencia es 2 sin(π/P); además, atenúa toda
  oscilación con P > 6.
- (iv) **Prop. 2.36**: subestructura óptima de la partición de Fisher (recurrencia exacta,
  O(K_max N² q)), con el **Lema 2.35** del costo por sumas acumuladas.

**Otras demostraciones propias:** Prop. 2.9 (reconstrucción óptima del PCA, sin usar
Eckart-Young); Prop. 2.13 (cos² y contribuciones); Lema 2.19 (0 ≤ det R ≤ 1, signo de χ²_B);
Prop. 2.24 (descomposición de la inercia de la HFC y cota del factor por λ₁ de la submatriz);
Prop. 2.38 (la variante de `aede` del CH equivale a ((K−1)/K)·CH habitual y **nunca elige menos
segmentos** que la habitual); Prop. 2.41 (propiedades del RV); Prop. 2.43 (solución de
Procrustes); **Prop. 2.46** (autoencoder lineal y PCA: cota, minimizador único B·A = V_d V_dᵀ
con R regular y λ_d > λ_{d+1}; con pesos atados, A = O V_dᵀ). Esta última se demuestra a partir
de la Prop. 2.9, de modo que la equivalencia ya no depende de una ficha preliminar.

**Citadas, no demostradas:** Teorema 2.10 (Eckart y Young; `\pendiente`, no se usa en ninguna
prueba) y la ausencia de mínimos locales espurios del autoencoder lineal (Baldi y Hornik, 1989,
ficha preliminar con `\verificar`).

## 5. Citas resueltas y pendientes finales (`\pendiente{}`)

**Pasada final (tras la entrega del bibliotecario: 47 entradas, todas con ficha).** Se
reemplazaron por citas los pendientes cuya clave tiene entrada en el `.bib` y ficha en `papers/`.
Como casi todas las fichas son preliminares, cada cita lleva un `\verificar{}` que limita el uso
al aporte general y no atribuye fórmulas que no se han leído en la fuente.

| Pendiente anterior | Ahora | Alcance |
|---|---|---|
| Horn (1965) — cap. 1, OE6; cap. 2, Def. 2.14(b) | `horn_1965` | Aporte general; el percentil es elección de la tesis, no se atribuye |
| Calinski y Harabász (1974) — cap. 2, 2.1 y Def. 2.37 | `calinski_harabasz_1974` | Aporte general; los grados de libertad de la forma original no se atribuyen |
| Eckart y Young (1936) — Teo. 2.10 | `eckart_young_1936` | Lectura parcial; condición de unicidad por confirmar |
| Benzécri (1973) — 2.3 | `benzecri_1973` | Solo la tradición del análisis de datos; **no** se presenta «dejar hablar a los datos» como cita textual («suele resumirse como») |
| Kaiser — 2.5.3 | `kaiser_1960` | Atribución del criterio λ > 1 por confirmar |
| Bartlett y KMO — 2.5.4 | `bartlett_1950`, `bartlett_1951`, `kaiser_1970`, `kaiser_rice_1974` | Aporte general; las fórmulas son las del código y no se atribuyen a una obra concreta |
| *n* efectivo — Obs. 2.20 | `pyper_peterman_1998` | Aporte general; no se comprobó que la fórmula del código sea la del artículo |
| Umbrales de Tucker — Def. 2.44 | `lorenzo_seva_ten_berge_2006` | Uso como índice de similitud y umbrales (resumen leído); no se citan los valores |

No se usan en la tesis, porque el texto de los capítulos 1 y 2 no los requiere:
`dickey_fuller_1979`, `perron_1989` (ADF; no se cita para KPSS), `granger_newbold_1974`,
`phillips_1986`, `kish_1965`, `kunsch_1989`, `hubert_arabie_1985` ni las fuentes de los episodios.
Cambio de forma: el texto escribía «Calinski y Harabász»; se unificó con la grafía de la ficha y
del `.bib`, «Caliński y Harabasz» (`ń` se declara en el preámbulo).

**Pendientes finales (24 marcas):**

| # | Ubicación | Qué falta |
|---|---|---|
| 1 | Portada | Denominación exacta del grado (pautas de la UNI) |
| 2 | Resumen | Resumen y abstract |
| 3 | Cap. 1, 1.1 | Atoche Murrieta (2022), tesis PUCP; sin ficha |
| 4 | Cap. 1, OE6 | Fuentes de la vara quebrada y del criterio de Rencher |
| 5 | Cap. 2, 2.1 | Atoche Murrieta (2022) |
| 6–10 | Cap. 2, 2.2.3 | Fuentes externas de los cinco episodios. **Se mantienen a propósito:** las fichas existen (`lehman_brothers_2008`, `nber_2010`, `bernanke_2013`, `reserva_federal_2013`, `oms_2020a`, `oms_2020b`, `congreso_2018`, `ustr_2018`, etc.), pero la convención de fechado la decide Roberto (decisión I) |
| 11 | Teo. 2.10 | Obra de referencia del PCA (Jolliffe, 2002) |
| 12 | 2.5.2 | Terminología de cos² y contribuciones de la escuela francesa |
| 13 | Def. 2.14(a) | Fuente del modelo de vara quebrada |
| 14 | 2.5.3 | Fuente del criterio de Rencher (no se formaliza sin ella) |
| 15 | 2.5.4 | Relación entre R⁻¹ y las correlaciones parciales |
| 16 | 2.6 | Denimal (2001, 2007), fuente primaria de la HFC |
| 17 | Obs. 2.25 | Técnica de vecinos reducibles (Bruynooghe) |
| 18 | 2.7.1 | Camiz y Diblasi (2013), pesos gaussianos |
| 19 | 2.7.3 | Tukey (1977) |
| 20 | 2.9 | Lavit (1988), STATIS |
| 21 | Def. 2.44 | Tucker (1951), fuente primaria del coeficiente de congruencia |
| 22–24 | Cap. 3, 4 y 5 | Capítulos por redactar (el 4, regla 7) |

(Las filas 6–10 son cinco marcas y las 22–24, tres: 23 `\pendiente` en `capitulos/`, portada
incluida, y 1 en el resumen de `tesis.tex`.)

Las marcas `\verificar{}` de las claves antiguas reproducen las notas VERIFICAR del informe; las
de las claves nuevas resumen el campo `verificar` del `.bib` y el estado de lectura de la ficha.
Compilación final: exit 0, 45 páginas, sin errores, sin citas ni referencias indefinidas, sin
cajas desbordadas, sin caracteres faltantes y biber sin avisos.

## 6. Inconsistencias entre código y teoría (para el desarrollador; no resueltas en el texto)

1. **`aede_r`, l. 613:** `diff[i] <- sum((autvet[, k] - autveto[, k])^2)` está fuera del bucle en
   `k`, de modo que `least_squares_differences` mide solo el último eje (`k = ndim`) y no la suma
   sobre los ejes. ¿Es deliberado? Plantearlo al Dr. Camiz como pregunta.
2. **`.bstatw_ac`, l. 669:** `corr[is.nan(corr)] <- 0` pone en cero también el elemento diagonal
   de una serie constante en la ventana: entonces R_t no es una matriz de correlaciones y su traza
   es menor que p. La tesis lo excluye con el Supuesto 2.29; conviene que el código avise.
3. **Dos reglas de signo:** `aede` (paso 3) usa la regla lineal y el PCA global (`pca_basico`,
   `Rcamiz`) la cuadrática (Obs. 2.11 y 2.33). Ya está documentado en el Rmd (`signo_difiere`);
   las cargas evolutivas y las globales pueden quedar con signos opuestos en el mismo eje.
4. **CH de `aede`:** la Prop. 2.38 demuestra que la variante con K grados de libertad nunca elige
   menos segmentos que la habitual. Es coherente con el diagnóstico del plan (k = maxcl) y aporta
   un argumento formal para la decisión D-1/J; no cambia el código.
5. **Dos particiones de Fisher:** `fisher_r` (univariada, n_min = 1) y `particion_fisher`
   (multivariada, `tam_min`). Ambas implementan la misma recurrencia (Prop. 2.36) y eligen el
   primer mínimo en los empates; la tesis las trata como la misma definición con distinto n_min.
   Para D6 (port a Python), las dos deben conservar esa regla de empate.
6. **HFC, vecinos reducibles:** `agrega_r` no recorre todos los pares en cada paso, como dice la
   ecuación (2.15). Su equivalencia depende de la reducibilidad del índice, no demostrada. Como
   diagnóstico (no es un resultado de la tesis), comparé en mi scratchpad `agrega_r` con un
   algoritmo voraz sobre todos los pares: misma secuencia de fusiones en las dos vías y en 300
   casos simulados. Conviene que el auditor o el desarrollador lo verifiquen formalmente.
7. **Fechado de ventanas pares:** con n_w par, `aede` fecha en el posterior de los dos meses
   centrales (posición n_w/2 + 1). Está declarado en la Def. 2.26; el LSTM-autoencoder fecha al
   final de su ventana (Def. 2.48). Cualquier comparación de fechas entre ambos debe alinear esas
   convenciones.
8. **Informe (para el editor):** la notación cambió respecto del informe para evitar choques:
   `X` (datos) / `Z` (estandarizados); `W_d` → `V_d`; `V` (candidata del PCA) → `E`; `w` → `n_w`;
   `R_t^{(w)}` → `R_t`; `y_A` → `φ_A`; configuraciones del RV `Y, Z` → `F_1, F_2`; `G(P)` → `γ(P)`;
   `d(·,·)` → `δ`; `S(·)` → `𝒮`; compuertas `i_t, f_t, o_t, c_t` → `g^e_t, g^o_t, g^s_t, s_t`;
   código latente `z_t` → `η_t`. Las ecuaciones del informe se remiten a etiquetas `\label` del
   capítulo 2.

## 7. Notas para el auditor

- Números escritos a mano que quedan en los capítulos 1 y 2: años de cita; cifras de las fuentes
  citadas (8 a 30 y 1 a 8 años; 1999, 2020; 17, 15, 7 y 4 series; 48 meses; 0,7; S&P 500, 2000 y
  2022; 25 de abril de 2026); datos de las notas `\verificar` (284, 843–852, FKI-207-95);
  constantes matemáticas (6 en la Prop. 2.5; 1/4, 1/2, 2/3, 3/4 del contraejemplo; (2p + 5)/6;
  numeración. Ninguna cifra de los datos.
- `cifras.tex` ya trae macros de resultados (inercias, KMO, nulo, clases D5). No se usan en la
  tesis (regla 7).
- Las propiedades de demostración propia se pueden comprobar numéricamente: Prop. 2.5, 2.9, 2.13,
  2.23, 2.24, 2.30, 2.36, 2.38, 2.41, 2.43 y 2.46.

## Vuelta 1 (dictamen `auditorias/2026-10-20_iteracion-3a.md`)

### M-02 · Prop. 2.5 (a) (`capitulos/02_marco_teorico.tex`, `prop:ganancia`)

- **Enunciado nuevo.** Se definen la media y la varianza temporales en un tramo de $T$ meses
  consecutivos, $\langle y\rangle_{t_0,T}$ y $\operatorname{var}_{t_0,T}(y)$. (a) Si $P$ es entero
  ($P\ge2$), $\operatorname{var}_{t_0,P}(\Delta x)=\gamma(P)^2\operatorname{var}_{t_0,P}(x)$ para todo
  $t_0$ (período completo). Para todo $P\ge2$ real, los límites de largo plazo ($T\to\infty$)
  existen, no dependen de $t_0$ y guardan la misma razón $\gamma(P)^2$; la varianza de largo plazo
  de $x$ es $\varrho^2/2$ si $P>2$ y $\varrho^2\cos^2\psi_0$ si $P=2$. Se excluye solo el caso
  degenerado $P=2$, $\cos\psi_0=0$ ($x\equiv0$).
- **Demostración nueva.** Sumas geométricas de $e^{\mathrm{i}k\vartheta t}$, $k\in\{1,2\}$:
  - si $P>2$, se tiene $e^{\mathrm{i}k\vartheta}\ne1$; las sumas son nulas sobre un período
    entero y están acotadas en general;
  - si $P=2$, el promedio de $\cos^2$ no es 1/2, pero $\Delta x_t=2x_t=\gamma(2)x_t$ de forma
    exacta.
- **Comprobación numérica propia.** Para $P\in\{2,3,5,12\}$ (período completo) y $P=13{,}7$
  (200 000 meses), con $\psi_0\in\{0{,}4;1{,}1\}$, la razón coincide con $\gamma(P)^2$; en
  $P=13{,}7$, hasta $10^{-6}$. Guion en línea, no versionado.
- (b) y (c) no cambian.
- **Pendiente para el editor del informe:** alinear `tesis/_capitulos/02_marco_teorico.qmd:66`
  con el nuevo (a).

### N-01 y N-02 · Notas `\verificar`

- **Fisher (1958)**, `01_introduccion.tex:52` y `02_marco_teorico.tex:42`: falta verificar las
  páginas 789–798, que constan solo en fuentes secundarias. El número y el DOI ya están
  verificados. La ficha sigue preliminar porque el texto no se ha leído.
- **Baldi y Hornik (1989)**, `01_introduccion.tex:59` y `02_marco_teorico.tex` (párrafo previo
  a `prop:ae-lineal`): solo falta el DOI; el texto completo ya se leyó. La marca de Bourlard y
  Kamp (1988) se mantiene: número del fascículo, alcance del resultado y ficha preliminar.
- **Lorenzo-Seva y ten Berge (2006)**, `02_marco_teorico.tex` (`def:tucker`): se retiró la marca,
  porque el registro lo da por cerrado.
  - Matiz: la ficha dice «resumen leído; texto no consultado». La frase de la tesis («su uso […]
    y los umbrales de interpretación se discuten en») solo pide lo que da el resumen.
  - Si el bibliotecario reabre la fila (N-02 es suyo), se repone la marca.

### N-09 · `notacion.tex`

- Macros nuevas: `\prom` (media temporal) y `\vart` (operador var).
- Símbolos nuevos en la lista:
  - $t_0$, $T$, $\langle y\rangle_{t_0,T}$ y $\operatorname{var}_{t_0,T}(y)$;
  - $y$, $\varrho_y$, $\psi_y$ (en la demostración de la Prop. 2.5);
  - $\tau$ (mes de transición, distinto de $\tau_k$) y $\mathcal W_\tau^{\pm}$;
  - $c$ (Prop. 2.41 (a)) y $a_1$, $a_2$ (Prop. 2.41 (b)).
- Colisiones evitadas: $\phi$ ya denota los parámetros del decodificador, $\omega$ los pesos y
  $\mathbf V$ los vectores propios. Por eso se usan $\varrho_y$, $\psi_y$ y `var`.

### Compilación

`latexmk -lualatex -cd tesis_latex/tesis.tex`:

- exit 0, 46 páginas;
- 0 citas o referencias indefinidas, 0 `Overfull` y biber sin avisos;
- quedan los avisos de fuentes de N-07, aceptados para 3a.

### No atendido en esta vuelta

N-07 (`page.I` y luaotfload) y N-10 (lista de excepciones en `README.md`) no estaban en el
encargo de la vuelta 1, así que siguen abiertos.

### Vuelta 1 · pasada corta (Tucker y paridad de marcas con el informe)

**Tucker (1951)** (`def:tucker`)

- El `\pendiente{… sin ficha}` pasa a `\parencite{tucker_1951}` con un `\verificar`. La marca
  recoge que la ficha es preliminar, que faltan la entidad emisora y el lugar, y que el texto no
  se ha leído.
- Solo se le atribuye ser la fuente habitual del coeficiente.
- La bibliografía del PDF imprime la entrada.

**Paridad de marcas (según la nota del bibliotecario, «Vuelta 1»)**

El registro mantiene las tres obras como «Pendiente», así que la tesis adopta las marcas:

- `camiz_maulucci_roig_2010`: `\verificar` en la sección del EPCA (primer párrafo), equivalente a `v2-cmr`;
- `camiz_roig_2011`: `\verificar` en el párrafo de la elección de $n_w$, equivalente a `v2-cr`;
- `tuhin_et_al_2025`: `\verificar` en `sec:validacion`, equivalente a `v2-tu`. Se conserva la
  marca de «LSTM-autoencoder».

**Lorenzo-Seva y ten Berge (2006)**

- El registro dice ahora «Cerrado (metadatos); contenido: solo resumen» y considera admisible la
  cita sin marca, porque lo que la tesis atribuye a la obra está en el resumen.
- La tesis se mantiene sin marca. El informe debe retirar `v2-lst`.

**Compilación:** exit 0, 46 páginas, sin indefinidas, sin `Overfull` y biber sin avisos.

**Para el editor del informe**

1. Prop. 2.5 (a): nuevo enunciado y nueva demostración (M-02).
2. `@def-tucker`: citar `@tucker_1951` con su nota VERIFICAR, en lugar del `[CITA PENDIENTE]`.
3. Retirar `v2-lst`.
4. Añadir una nota VERIFICAR de Tuhin et al. (2025) en «LSTM-autoencoder».
5. Mantener `v2-cmr`, `v2-cr` y `v2-tu`, que ya tienen equivalente en la tesis.
