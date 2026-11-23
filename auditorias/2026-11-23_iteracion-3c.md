# Auditoría · Iteración 3c · 23 de noviembre de 2026

**Rama:** `iteracion-3c` (HEAD `982ba89`, igual a `origin/iteracion-3c`; *clone* superficial).
**Base:** `origin/main...HEAD`, merge-base `20429f3` (integración de la 3b). 31 commits, 126 archivos.
**Alcance:** tesis LaTeX (reorganización en 7 capítulos, estado del arte, cap. 5 de avance, cap. 6,
cap. 7, anexos), `tesis/referencias.bib`, `tesis/registro_verificacion.md`, 50 fichas nuevas o
modificadas en `papers/`, código y resultados (D19 en el nulo mixto, columna `orden`, compatibilidad
corte × episodio, resúmenes 05c/07b/07c, figuras), `herramientas/generar_cifras.py`,
`herramientas/cifras_mapa.csv`, `cifras.tex` y `_cifras.yml`. El informe MMC102 (`tesis/_capitulos`,
`tesis/informe_mmc102`) no se modificó en la rama y no se audita, salvo los efectos de la integración
en `main`.

**Auditor:** agente auditor (independiente). Las notas de los agentes (`auditorias/notas/2026-11-*.md`)
y los mensajes de commit no se tomaron como evidencia. Tamaños aplicados: 228 × 16 (niveles) y
227 × 16 (transformadas), según D16.

**Plan de la iteración:** no existe un plan de la 3c en `asesoria/` (ni en la rama ni en `main`, que
solo trae `2026-11-08_revision-informe-preliminar.md`). La auditoría se hizo contra la lista de
verificación del auditor y las decisiones D1–D19 de la rama, sin criterios de aceptación propios de
la iteración (hallazgo m-05).

## Dictamen: **APROBADO** (con hallazgos mayores que deben volver a los responsables)

No hay hallazgos bloqueantes. Todas las cifras rastreadas coinciden con `data/results/`, la
regeneración de `cifras.tex` y `_cifras.yml` es idéntica byte a byte, los cinco notebooks
modificados se ejecutan sin errores y reproducen sus CSV, el Rmd final se renderiza y reproduce los
42 CSV `R_*` byte a byte con paridad 56/56, las 58 pruebas pasan y la tesis compila sin citas ni
referencias indefinidas. Cada `\textcite`/`\parencite` tiene entrada en el `.bib` y ficha en `papers/`.

Los cuatro hallazgos mayores, según el ciclo de CLAUDE.md, vuelven a sus responsables antes de
integrar. M-02 y M-03 afectan a la integración en `main` y requieren una decisión de Roberto.

| Severidad | N.º | IDs |
|---|---|---|
| Bloqueante | 0 | — |
| Mayor | 4 | M-01, M-02, M-03, M-04 |
| Menor | 5 | m-01 a m-05 |

## Hallazgos

| ID | Severidad | Archivo:línea | Evidencia | Acción requerida | Responsable |
|---|---|---|---|---|---|
| M-01 | Mayor | `tesis_latex/capitulos/05_resultados.tex:420-421, 489-491, 510-513, 573`; `06_conclusiones.tex:103-105, 138`; `07_pendientes.tex:133-152, 254` | La tesis declara pendientes productos que ya existen en la rama: `data/results/final/09a_compatibilidad_cortes.csv` (y `R_compatibilidad_cortes.csv`, idénticos en contenido; fila de paridad incluida), `reports/figures/final/07c_hfc_dendrograma.png` y `reports/figures/final/09a_trayectoria_pca_mm12.png` (commits `3061e06` y `e08fbe7`, del 8-nov, anteriores a la última edición de la tesis). El PDF compilado muestra tres `[PENDIENTE]` por esos productos. `07_pendientes.tex:150` afirma que «el análisis vigente no generó esas figuras», y `sec:pend-cifras` pide macros que ya están todas en `cifras.tex` (0 `\cifrafalta` en el PDF). Además, la lectura de HT3 queda sin la evidencia disponible. Con h = 3, el corte 3 (2014-04) es compatible con el colapso de las materias primas (dos meses antes de su inicio) y el corte 4 (2020-06), con la COVID-19 (dos meses después de su fin). Con h = 6 se suman el *taper tantrum* (2014-04, a 4 meses) y la guerra comercial (2020-06, a 5 meses). El texto (l. 505-507 y 525-527) dice que la datación «no separa» los episodios intermedios y no menciona que el corte de 2014-04 cae junto al colapso de las materias primas. | Integrar la tabla de compatibilidad y las dos figuras en el cap. 5. Revisar la lectura de HT3 (l. 502-528 y 569-573), C8, R4 y la `tab:estado-objetivos`. Actualizar o retirar `sec:pend-cifras` y `sec:pend-productos`. Toda distancia o marca debe entrar por macro, desde `09a_compatibilidad_cortes.csv`. | Redactor LaTeX (macros nuevas: desarrollador) |
| M-02 | Mayor | `decisiones.qmd:24-37`; `CLAUDE.md:25-26` | D19 se **reescribió en el mismo lugar** (commit `605803a`). En `20429f3` y en `origin/main`, D19 dice: «se mantiene como convención declarada en la iteración 3b […] La corrección […] entra como tarea de fase 0 de la iteración 4». La alternativa descartada era corregir el código. En la rama, la misma entrada, con la misma fecha (7-nov), dice lo contrario: «Roberto decidió corregir el código», y la alternativa descartada pasa a ser la convención. El registro pierde la versión anterior, y la única constancia del cambio es un mensaje de commit. El código de la rama (D19 aplicado en `src/remuestreo.py` y en el Rmd) es coherente con la versión nueva, de modo que, en la rama, no hay contradicción con la decisión vigente. Pero `git merge-tree HEAD origin/main` da conflictos en `decisiones.qmd` y `CLAUDE.md`, y en otros seis archivos: `herramientas/cifras_mapa.csv`, `tesis/_cifras.yml`, `tesis_latex/cifras.tex`, `tesis/registro_verificacion.md`, `tesis_latex/capitulos/03_marco_teorico.tex` y `papers/congreso_2018.qmd`. | Que Roberto confirme cuál D19 rige. Si se corrige el código en la 3c, registrarlo como una decisión nueva (p. ej., D20, «D19 se adelanta a la 3c»), con fecha, motivo y rastro, sin borrar el texto original de D19. Resolver los ocho conflictos antes de integrar y regenerar `cifras.tex` y `_cifras.yml` después de la fusión. | Orquestador (escalar a Roberto) |
| M-03 | Mayor | Integración `iteracion-3c` → `main` | (a) **Cifras:** `origin/main:tesis/_cifras.yml` y `origin/main:tesis_latex/cifras.tex` tienen el nulo mixto anterior a D19 (`nuloMixtoTsPCUno` 0,783; `nuloMixtoTsPCDos` 0,003; `nuloMixtoDsPCDos` 0,004). La rama tiene 0,775, 0,002 y 0,003. Si se integra, el informe y la tesis difieren en cifras hasta que se regenere (criterio 8c). (b) **Contenido:** el resumen del informe en `main` (`tesis/informe_mmc102/00_preliminares.md:21`) afirma que «el autoencoder no supera al análisis en componentes principales fuera de muestra», mientras que la tesis (`05_resultados.tex:531-541`, C9) declara HT4 «sin evaluar» con 16 series (D17.4). El informe afirmaría algo que la tesis no sostiene. (c) **Bibliografía:** `main` agrega `tesis/informe_mmc102/referencias.bib` y `referencias_extra.bib`, contra la regla de un único `tesis/referencias.bib`. (d) **Fichas:** `main` agrega `papers/camiz_diblasi_2013.qmd` («texto completo leído el 7-11-2026»), mientras que la rama marca la obra `\pendiente{… sin ficha}` (`02_estado_arte.tex:302`, `03_marco_teorico.tex:778`) y el registro la da por «No localizada» (`registro_verificacion.md:72, 216, 237`). `main` también cambia `fisher_1958` y `horn_1965` a «texto completo leído», pero las notas `\verificar` de la rama siguen llamándolas preliminares (`02_estado_arte.tex:212-215, 395-397`; `03_marco_teorico.tex:495`; `01_introduccion.tex:107`). | Antes de integrar: regenerar las cifras en `main` después de la fusión; alinear el informe con la tesis o la tesis con el informe (AE/LSTM); decidir si el informe vuelve al `.bib` único; incorporar las fichas de `main` al registro y a la tesis (citar Camiz y Diblasi, 2013, si su ficha lo respalda, y actualizar las notas de Fisher y Horn). | Bibliotecario (fichas, registro, `.bib`); redactor LaTeX (notas y citas); editor del informe (informe); orquestador (orden de la fusión) |
| M-04 | Mayor | `tesis_latex/capitulos/05_resultados.tex:427-433, 466-470` | D11 dice que el índice de Caliński-Harabasz «se informa en sus dos variantes» y que solo puede usarse como selector si muestra un óptimo interior con maxcl = 20 fuera del rango del nulo. En la datación (`09a_datacion_criterios.csv`), con maxcl = 20 (k_max efectivo 18), el CH elige k = 12 (variante de `aede`) y k = 11 (habitual), con `k_en_tope = False`: es un óptimo interior. La sección de datación no informa el CH ni explica por qué no se usa: no hay un nulo de estructura constante para la datación con el cual comprobar la segunda condición. Solo se discute el CH de `aede` (l. 272-275). | Informar el CH de la datación en sus dos variantes y declarar cómo se aplica D11 sin un nulo para la datación (o pedir a Roberto una decisión). | Redactor LaTeX |
| m-01 | Menor | `05_resultados.tex:377`; `data/results/final/07c_hfc_clases3.csv` (clase C3) | El «representante» de C3 (EMBIG) sale de un empate exacto: en una clase de dos series estandarizadas, ambas correlacionan con el factor con el mismo valor absoluto, √((1+\|r₁₂\|)/2). En el CSV, 0,8676372370227425 frente a −0,8676372370227423 (R: …743 frente a …742). La elección depende del redondeo en la última cifra. | Declarar el empate en la tabla (o fijar una regla de desempate en el código) y no presentar el EMBIG como representante elegido por los datos. | Desarrollador (regla) y redactor LaTeX |
| m-02 | Menor | `00_resumen.tex:22, 49`; `02_estado_arte.tex:103`; `05_resultados.tex:445-450` | Hay conteos y etiquetas escritos a mano que dependen de los datos: «tres bloques» / *three blocks* (el cuerpo usa `\clasesHfcMenor`), «menos de veinte años» y las etiquetas de fase de la `tab:res-regimenes`, copiadas de `09a_regimenes_pca.csv`. Hoy coinciden con los CSV. | Pasarlos a macros o declararlos en la lista de excepciones de `tesis_latex/README.md`. | Redactor LaTeX |
| m-03 | Menor | `02_estado_arte.tex:212-215 y 395-397`; `222-223 y 398-399` | Las notas `\verificar` de `fisher_1958` y `calinski_harabasz_1974` se repiten con el mismo texto en el mismo capítulo, lo que infla el contador `\total{nverificar}`. | Dejar una sola nota por obra y capítulo. | Redactor LaTeX |
| m-04 | Menor | `tesis_latex/tesis.log` | 15 avisos *Overfull \hbox*, de hasta 1,7 pt (tablas de los anexos y del cap. 3). Sin efecto visible apreciable. | Ajustar si se desea. | Redactor LaTeX |
| m-05 | Menor | `asesoria/` | No hay un plan de la iteración 3c con objetivos ni criterios de aceptación (paso 1 del ciclo de CLAUDE.md). Esta auditoría no pudo contrastar la iteración con criterios propios. | Registrar el plan, o el alcance acordado con Roberto, de la 3c (aunque sea retroactivo) para la trazabilidad. | Orquestador |

## Verificaciones realizadas

**A. Citas y referencias**

1. **Claves:** 106 claves citadas en `tesis_latex/` (sin comentarios). Todas están en
   `tesis/referencias.bib` (113 entradas, sin duplicados), y las 113 tienen ficha
   `papers/<clave>.qmd`. Hay siete entradas sin cita en la tesis (`baffes_streifel_2016`, `congreso_2016`,
   `doj_2016`, `fmi_2015`, `kingma_ba_2015`, `oms_2020a`, `oms_2023`). No es un hallazgo.
2. **Metadatos:** en las 50 fichas nuevas o modificadas se cotejaron automáticamente con la ficha el
   año, el DOI, el volumen, las páginas, el número, el primer autor y el inicio del título de cada
   entrada del `.bib`. No hubo discrepancias.
3. **Atribuciones:** se cotejaron con su ficha las afirmaciones con contenido de los caps. 2 y 3.
   Están respaldadas: Schüler et al. (2015: 7,2 años, rechazo del PCA), Strohsal et al. (unos 15 años),
   Galati et al. (EE. UU. y 5 países europeos), Rünstler y Vlekke (salvo Alemania), Tölö (17 países,
   1870-2016, LSTM/GRU), Beutel et al. (logit fuera de muestra; sin redes neuronales), Gómez-González et
   al., Brandão-Marques y Pérez Ruiz (6 países), Hollo et al. (5 subíndices), Illing y Liu (encuesta),
   Bai y Perron (2003, programación dinámica), Camiz y Pillar (diez reglas, Rencher), Escofier y Pagès
   (cos², contribución), Lavit et al. (1994, STATIS dual), Audibert et al. (secs. 3.2, 3.3 y 5.2), Camiz y
   Roig (Fisher sobre λ₁), Camiz, Cerda y Atoche (17 series, 1999-2020, grupos 7/4/4, ventana de 48
   meses fijada por experimentación), Drehmann et al. (8-30 frente a 1-8 años) y Granger y Newbold
   (unas tres cuartas partes). Las fichas que solo localizan la obra (Pearson, Hotelling, Lebart et al.,
   Goodfellow et al., Krolzig, Kim y Nelson, Aikman et al.) se citan solo por su aporte general.
4. **Verificaciones pendientes:** todas las fichas modificadas figuran en `registro_verificacion.md`.
   Las `\pendiente` de fuentes (Camiz y Diblasi, Denimal 2001, BCRP/PUCP, tamaño de muestra en redes
   profundas) también figuran en el registro.
5. No hay citas textuales de 8 palabras o más entre «» o ``'' en los capítulos y anexos.

**B. Cifras y resultados**

6. **Recalculadas con Python** desde `data/processed/dataset_niveles_mensual.csv` (md5 de D4
   verificados), con las 16 series: 228 × 16; inercias 65,2 / 19,4 / 7,6 / 3,1 % (acumulada de tres
   ejes, 92,2 %); λ₃ = 1,21; Kaiser 3, vara quebrada 2; KMO 0,84, con los tres valores individuales más
   bajos 0,61 / 0,62 / 0,68 (tasa de referencia, interbancaria y EMBIG); Bartlett 10 492 con 120 gl;
   condición 10 968; \|r(PC1, t)\| = 0,993; sin tendencia, PC1 38,5 % y KMO 0,68; y los signos y
   magnitudes de las cargas descritos en `sec:res-pca`. Todo coincide con las macros. Las medianas
   del espectro (93,4 y 23,4 %) se recalcularon desde `R_anexo_espectro.csv`. Las lecturas cualitativas
   del cap. 5 se cotejaron con los CSV: nulo mixto (PC1 no supera, PC2 sí, PC3 no), OE4 (ningún
   p < 0,05, ni en las sensibilidades: mínimo 0,15), codo de `aede`, `k*` dentro del rango del nulo,
   2017-10 «no confirmada», la única candidata (2012-07, regla del 06, 36 meses), la composición y
   estabilidad de la HFC, los intervalos de las correlaciones entre factores, los regímenes, la
   estabilidad de los cortes (2014-04: 0,40) y el primer régimen de 12 meses.
   **Regeneración:** `python3 herramientas/generar_cifras.py`, en una copia de la rama: 184 macros,
   con `cifras.tex` y `_cifras.yml` idénticos byte a byte a los versionados; `--comprobar` termina
   con código 0. Se revisaron filas de `cifras_mapa.csv` (filtros y columnas) de una muestra de 30
   macros nuevas.
7. **Notebooks re-ejecutados** de principio a fin en una copia (`git archive HEAD`): `05_pca`,
   `05c_anexo_no_diferenciar`, `07b_nulo_estructura` (6 min), `07c_hfc_clases` y `09a_datacion_pca`.
   Ninguno falla. Los 54 CSV que escriben son idénticos byte a byte a los versionados. Solo difieren
   cuatro PNG del 05, por diferencias de rasterizado (menos del 0,06 % de píxeles distintos, sin
   cambio de contenido). `pytest tests/`: 58 pruebas aprobadas, incluidas `test_compatibilidad.py` y
   `test_nulo_mixto.py`. Rangos de D19 verificados en `R_nulo_indices_ts.csv` (inicios en
   {1, …, 217} = {1, …, n − 12 + 1}, 19 bloques) y en `R_nulo_indices.csv` ({1, …, 216}). Solo cambiaron
   las filas `mixto_*` de `05_nulo_tendencias.csv`.
8. Las cifras del cap. 5 salen de `data/results/final/`. Las corridas de 17 series solo se mencionan
   como antecedente (D17.4).
8b. **Paridad Python–R:** `R/ciclo_financiero_final.Rmd` se renderizó en una copia (R 4 con los
   paquetes de Debian, sin `Rcamiz`, port en R puro) sin errores. Los 42 CSV `R_*` (incluidos
   `R_nulo_tendencias`, `R_nulo_indices_ts`, `R_compatibilidad_cortes`, `R_estabilidad_cortes` y
   `R_regimenes_pca`) son idénticos byte a byte a los versionados, y `R_paridad_resumen.csv` da 56/56.
   `09a_compatibilidad_cortes.csv` y `R_compatibilidad_cortes.csv` coinciden en contenido. El cambio de
   D19 está en Python (`src/remuestreo.py`) y en R (chunk `b2-nulo`).

**B2. Coherencia entre documentos**

8c. El informe no cambió en la rama. Las diferencias con `main` se tratan en M-03.
8d. `latexmk -lualatex` (copia en un directorio temporal, con los paquetes de TeX instalados por apt)
   termina sin errores: 134 páginas, sin citas ni referencias indefinidas, sin avisos de biber, y el
   PDF no tiene «??». El PDF tiene 13 marcas `[PENDIENTE]`, entre ellas las tres de M-01. La notación
   del cap. 5 (`\nw`, `\Lb`, `\KMO`, `\pval`, `\mR`) está definida en `notacion.tex` y compila.

**C. Coherencia**

9. D1, D4, D7, D8, D9, D10, D12, D13, D15, D16, D17 y D18 se respetan en los caps. 4 a 7. Sobre D11,
   ver M-04; sobre D19, ver M-02.
10. No aparecen otros tamaños de muestra que 228 × 16 y 227 × 16. La EHFC se presenta como no
    publicada (`02_estado_arte.tex:484-487, 515-516`). Los episodios se fechan con fuentes externas
    (`data/referencia/episodios_referencia.csv`, D7 y D18).
11. Estilo académico, impersonal y en español. Resumen de unas 240 palabras con cuatro palabras
    clave. La estructura (introducción, estado del arte, marco teórico, metodología, resultados,
    conclusiones, pendientes, referencias y anexos) es coherente con una guía MMC102, pero la guía
    no está en el repositorio (ver abajo).

## No verificado

- **`quarto render` (D.12):** el informe no cambió en la rama y Quarto no está instalado en el entorno.
- **Notebooks `06_epca`, `06c_aede_grilla` y `09b_walkforward_pca`:** no cambiaron en la rama y no se
  re-ejecutaron. Tampoco se ejecutó `herramientas/no_regresion_dinamica.py`, que es caro.
- **Commit `2be3665`** (antecedente de 17 series, citado en `05_resultados.tex:538` y en el anexo D):
  el *clone* es superficial y el objeto no está disponible. La auditoría de la 3b dejó constancia de
  que existía.
- **Guía de estructura MMC102:** el documento «Estructura Seminario de Tesis II» no está en el
  repositorio. La estructura se juzgó por la organización declarada en `01_introduccion.tex`.
- **Contenido de las fuentes:** solo se cotejaron fichas, no las obras. Las fichas leídas «con una
  herramienta que resume» se aceptan con esa salvedad, que ya declaran sus notas `\verificar`.
- **Que D19 en su versión de la rama sea la decisión de Roberto:** en el repositorio solo hay un
  mensaje de commit (M-02).

## Notas de proceso

- Todas las comprobaciones se hicieron en copias del directorio temporal de la sesión. En el
  repositorio solo se escribió este archivo, y no se hizo commit.
