# Plan de cierre de la iteración 3c (vuelta 2) · 26 de noviembre de 2026

**Autor:** asesor de tesis (agente). **Rama:** `iteracion-3c`, HEAD `7c58906`, igual a
`origin/iteracion-3c`. **Base de comparación:** `origin/main` (HEAD `1bb4dcb`); *merge-base* `b893b23`.
**Motivo:** hallazgo m-05 de `auditorias/2026-11-23_iteracion-3c.md`. No hubo un plan de la 3c en
`asesoria/`, así que este documento reconstruye su alcance después del hecho y propone cómo cerrarla.

> **Advertencia.** La sección 1 es una **reconstrucción retroactiva**. Se basa solo en los 35 commits
> de `git log origin/main..HEAD` y en los archivos de la rama. No es un plan que Roberto haya aprobado
> antes de ejecutarlo. **El alcance y los criterios de la sección 1 solo valen como alcance de la 3c
> si Roberto da su conforme** (decisión R-1). Mientras tanto, m-05 sigue **parcial**.
>
> En `origin/main` hay un `asesoria/2026-11-08_revision-informe-preliminar.md` que no está en la
> rama. Por instrucción, no se usó como fuente de esta reconstrucción. Roberto puede revisar si
> definía algo de la 3c.

---

## 0. Diagnóstico (resumen de una página)

La 3c produjo lo que se esperaba de una iteración de redacción: la tesis maestra tiene 7 capítulos
y un estado del arte con fichas. Las cifras entran por macros (184 en `herramientas/cifras_mapa.csv`,
que regeneran `cifras.tex` y `_cifras.yml` byte a byte, según la auditoría). La paridad Python–R es
de 56/56 (`data/results/final/R_paridad_resumen.csv`). La auditoría la **APROBÓ** sin hallazgos
bloqueantes. Lo que impide cerrarla no es técnico. Hay cuatro problemas de sustancia:

1. **El capítulo 5 no usa evidencia que ya existe (M-01).** `05_resultados.tex:420, 489, 510` sigue
   marcando como `\pendiente` la tabla de compatibilidad y dos figuras que ya están en la rama.
   Además, la lectura de HT3 (`05_resultados.tex:505-508, 527, 569-573`) dice que la datación «no
   separa» los episodios intermedios. Pero `09a_compatibilidad_cortes.csv` da el corte 2014-04 a 2
   meses antes del colapso de las materias primas (compatible con h = 3) y el corte 2020-06 a 2 meses
   después de la COVID-19. **Advertencia del asesor:** antes de reescribir HT3 a favor, el jurado
   preguntará qué fracción de los meses cae, por azar, a h meses o menos de algún episodio. Los
   episodios de `tab:episodios` son seis, varios son períodos largos y sus ventanas se solapan.
   Mientras esa cobertura no se calcule, la compatibilidad de 3 de 5 cortes no puede leerse como
   evidencia fuerte (tarea F0-3).
2. **El registro de decisiones tiene dos versiones incompatibles de D19 (M-02).** En la rama,
   `decisiones.qmd:24-37` dice «Roberto decidió corregir el código». En `origin/main` (commit
   `23c0f8e`), D19 dice «se mantiene como convención […] la corrección entra en la fase 0 de la
   iteración 4». Las dos llevan la fecha del 7 de noviembre. `CLAUDE.md:25-26` también difiere entre
   las ramas. Hasta que Roberto diga cuál rige, la rama no puede integrarse.
3. **La contribución OC1 y el vacío 2 chocan con una fuente del propio asesor.** Según la ficha
   `papers/camiz_spada_2024.qmd` (lectura parcial de Roberto), Camiz y Spada proponen una HFC
   evolutiva. La tesis afirma en `02_estado_arte.tex:491` que «no existe en la literatura revisada»
   un algoritmo EHFC, en `:523` que no hay «especificación previa», y en `01_introduccion.tex:134` lo
   contrapone a la «aplicación secuencial» de la literatura. **Es la primera objeción que hará el
   Dr. Camiz**, porque se trata de su propio trabajo. La tesis no puede llegar a la sustentación
   con esa frase.
4. **El informe en `main` afirma algo que la tesis no sostiene (M-03 b).**
   `origin/main:tesis/informe_mmc102/00_preliminares.md:21` dice que «el autoencoder no supera al
   análisis en componentes principales fuera de muestra». Por D17.4, la tesis deja AE y LSTM como
   pendientes con 16 series. Ese informe ya se firmó y se compartió (commit `bb850ed` en `main`).

Hay además un hallazgo técnico menor con lectura metodológica (m-01). En una clase de dos series
estandarizadas, las dos tienen la misma |r| con el factor de la clase, así que el criterio «mayor |r|»
no define un representante. `07c_hfc_clases3.csv:16-17` y `R_hfc_clases3.csv:16-17` eligen el EMBIG
por la última cifra decimal. Con un empate exacto, `np.argmax` y `which.max` habrían elegido la
primera serie, el Índice BVL. La paridad de esa fila coincide por azar numérico.

**Lo que el Dr. Camiz preguntará, en este orden:** (i) por qué se dice que no existe una EHFC si él
la publicó con Spada; (ii) qué representante tiene una clase de dos series; (iii) si el $k$ del CH de
`aede` es deliberado (pregunta abierta desde D11); (iv) si la ponencia con Diblasi tuvo actas. Las
cuatro se resuelven con una consulta consolidada (tarea R-8), sin renunciar a las contribuciones.

---

## 1. Alcance retroactivo de la iteración 3c (reconstrucción; requiere el conforme de Roberto)

### 1.1 Objetivo inferido

Según los mensajes de commit y la nota `auditorias/notas/2026-11-07_redactor-latex.md` (commit
`1de46f9`), el encargo fue **presentar el borrador de la tesis maestra en LaTeX para MMC102**. Ese
borrador incluye la estructura de siete capítulos, el estado del arte, un avance de resultados (con la
indicación «autorizado por Roberto […]; no se publica en el sitio»), las conclusiones preliminares y el
capítulo de pendientes. También debía aplicar D18 y D19 y producir los insumos de la validación
externa. La «autorización» del avance de resultados solo consta en esa nota de agente, que no es
evidencia del conforme de Roberto. Por eso se incluye en R-1.

### 1.2 Bloques de trabajo (según los commits)

| Bloque | Commits | Producto |
|---|---|---|
| A. Decisiones | `605803a` | D18 y D19 (versión «corregir el código») en `decisiones.qmd` y `CLAUDE.md` |
| B. Código y resultados | `c6e2a27`, `d316551`, `3061e06`, `e08fbe7`, `960c867`, `396d7c0`, `c564c35` | D19 en `src/remuestreo.py` y en el Rmd; columna `orden`; `09a_compatibilidad_cortes.csv` (h = 3 y 6) y su réplica en R; figuras `07c_hfc_dendrograma.png` y `09a_trayectoria_pca_mm12.png`; resúmenes 05c, 07b y 07c; pruebas; macros (de 71 a 184) |
| C. Tesis LaTeX (borrador MMC102) | `34ae44a`, `35ddd49`, `4b21d64`, `f2ac854`, `54fa7dd`, `de6e544`, `1de46f9`, `6e5aea2` | Portada, resumen y *abstract*, caps. 2 (estado del arte), 5 (avance), 6 (conclusiones C1–C9, R1–R4) y 7 (pendientes), anexos |
| D. Bibliografía del estado del arte | `08c4015`, `4811970`/`780450d`, `bf6691f`/`c0fa997`, `675e2e5`/`9aa3b33`, `6518536`/`d4841e9`, `32c7886`/`67a9979`, `b0a34c4`/`b864902`, `539289e`/`982ba89` | Fichas y citas (Bry-Boschan, Harding-Pagan, Christiano-Fitzgerald, KPSS, Said-Dickey, Frontier, Guttman, Escofier-Pagès, Lavit et al., Lahiri, Aue et al., Audibert et al., Su et al., Pang et al., Kingma-Ba, Tölö, Beutel et al.) |
| E. Auditoría | `594e826` | `auditorias/2026-11-23_iteracion-3c.md`: APROBADO; M-01..M-04, m-01..m-05 |
| F. Vuelta 1 (fuera del cap. 5) | `f7712cc`, `34a7181`, `7c58906` | Fichas reconciliadas con `main` (M-03 d); cap. 7 al día (M-01, parcial); m-02 (parcial), m-03 y m-04; Camiz y Diblasi (2013) citada como `@presentation` |

### 1.3 Fuera del alcance (según lo que la rama **no** toca)

- El informe MMC102 (`tesis/_capitulos`, `tesis/informe_mmc102`): sin cambios en la rama.
- AE y LSTM con 16 series (D17.4, iteración 4). Los notebooks `06_epca`, `06c_aede_grilla` y
  `09b_walkforward_pca` no se modificaron.
- La publicación del cap. 5 en el sitio (regla 7).

### 1.4 Criterios de aceptación retroactivos que se proponen (para el conforme)

1. Tesis compilable, sin citas ni referencias indefinidas. *Se cumple según la auditoría (8d).*
2. Toda cifra entra por macro, y `generar_cifras.py --comprobar` termina con código 0. *Se cumple
   (B.6).*
3. Paridad Python–R completa y pruebas aprobadas. *Se cumple (B.7, B.8b).*
4. Toda cita tiene ficha y entrada en el `.bib`. *Se cumple (A.1).*
5. El cap. 5 usa todos los productos vigentes de la rama y no marca como pendiente nada que exista.
   *No se cumple (M-01).*
6. El registro de decisiones no tiene versiones contradictorias de una misma decisión. *No se cumple
   (M-02).*
7. La tesis no afirma nada que contradiga una ficha de `papers/`. *No se cumple (vacío 2 frente a
   `camiz_spada_2024`).*

---

## 2. Estado de los hallazgos de la auditoría al 26-11-2026

| ID | Estado | Evidencia |
|---|---|---|
| **M-01** | **Parcial** | **Resuelto en el cap. 7:** commit `34a7181`. `07_pendientes.tex:134-153` dice que los productos existen y que su integración queda para la vuelta del cap. 5. **Abierto en el cap. 5:** siguen los `\pendiente` de `05_resultados.tex:420, 489, 510`. La lectura de HT3 (`:497-528`, `:569-573`) no menciona 2014-04 / materias primas. En el cap. 6: `06_conclusiones.tex:103` («completar el contraste externo con una tabla de compatibilidad») y `:138` (`tab:estado-objetivos`, «falta la tabla de compatibilidad»). **No hay macros** de la compatibilidad: `herramientas/cifras_mapa.csv` tiene 0 filas de `09a_compatibilidad_cortes.csv`. |
| **M-02** | **Abierto** | En la rama, `decisiones.qmd:24-37` es la versión «corregir el código» (`605803a`). En `origin/main`, D19 es la convención (`23c0f8e`). `CLAUDE.md:25-26` difiere entre ramas. El diseño del sorteo (aparte o común) sigue sin validar (`07_pendientes.tex:84-92`, `sec:pend-d19`). `git merge-tree --write-tree HEAD origin/main` da hoy **16** archivos en conflicto: los 8 de la auditoría y 8 fichas *add/add* (`abdi_2010`, `camiz_2021_pca`, `camiz_diblasi_2013`, `camiz_spada_2024`, `fisher_1958`, `horn_1965`, `purizaca_2023`, `torres_baltazar_2023`). Las fichas surgieron en `f7712cc`, que llevó las fichas de `main` a la Ficha Estándar. Era esperable, pero hay que resolverlo. |
| **M-03** | **Parcial** | (a) **Abierto:** las cifras del nulo mixto en `main` siguen siendo anteriores a D19; se regeneran después de la fusión. (b) **Abierto:** `origin/main:tesis/informe_mmc102/00_preliminares.md:21` (afirmación sobre el AE). (c) **Abierto:** `origin/main` sigue teniendo `tesis/informe_mmc102/referencias.bib` y `referencias_extra.bib`. (d) **Resuelto en la rama:** `f7712cc` (fichas y registro); `34a7181` (`\textcite{camiz_diblasi_2013}` en `02_estado_arte.tex:305` y `03_marco_teorico.tex:781`; sin `\verificar` de Fisher y Horn); `7c58906` (`@presentation`, `tesis/referencias.bib:1232`). Queda `camiz_spada_2024` (`referencias.bib:1242`): tiene entrada pero ninguna cita, a la espera de R-4. |
| **M-04** | **Abierto** | `05_resultados.tex:268-275` discute solo el CH de `aede` frente al nulo. En la datación, `09a_datacion_criterios.csv:11-12` (maxcl = 20, k_max efectivo 18) da k = 12 (variante de `aede`) y k = 11 (habitual), con `k_en_tope = False`. **Observación nueva:** los cortes del CH habitual con k = 11 (`:12`) son idénticos a los de la regla K con maxcl = 15 y 20 (`:8`, `:13`). El cap. 5 (`:466-470`) ya reconoce que el número de regímenes depende de la regla, pero no dice que el CH y la regla K convergen en 11 con la grilla ampliada. |
| **m-01** | **Abierto** | `05_resultados.tex:377` presenta el EMBIG como representante de C3 sin aclaración. `07c_hfc_clases3.csv:16-17`: 0,8676372370227425 frente a −0,8676372370227423. `R_hfc_clases3.csv:16-17`: …743 frente a …742. El código elige con `np.argmax(np.abs(r))` (notebook 07c, celda `composicion_hfc`) y con `which.max(abs(r))` (`R/ciclo_financiero_final.Rmd:2334`). Ninguno de los dos detecta el empate. La fila de paridad «clase, nodo, código BCRP y representante» de `R_paridad_python.csv` coincide por la última cifra decimal. Las correlaciones entre representantes no generan macros (0 filas `tipo=representantes` en `cifras_mapa.csv`): el efecto se limita a la tabla `tab:res-hfc`. |
| **m-02** | **Parcial** | **Resuelto:** `00_resumen.tex` («tres bloques» pasa a `\clasesHfcMenor{}`) y «menos de veinte años» pasa a macros de años en los caps. 2 y 3 (`34a7181`). **Abierto:** las etiquetas de fase escritas a mano en `tab:res-regimenes` (`05_resultados.tex:445-450`). Ya existen como columna `fase` de `09a_regimenes_pca.csv`, y el generador admite el formato `texto`. |
| **m-03** | **Resuelto** | `34a7181`: queda una sola nota de Caliński y Harabasz en el cap. 2 (`02_estado_arte.tex:224`). Las de Fisher se retiraron (ficha completada en `f7712cc`). |
| **m-04** | **Resuelto** | `34a7181`: `\@pnumwidth` en `preambulo.tex` y anchos de `tab:sintesis-ea` y `tab:md5`. La nota del redactor (24-11) informa 0 *Overfull \hbox*. **Lo verificará el auditor en la vuelta 2.** |
| **m-05** | **Parcial** | Este documento. Pasa a resuelto con el conforme de Roberto a la sección 1 (R-1). |

---

## 3. Recomendaciones priorizadas

### Necesario (sin esto la 3c no puede integrarse ni la tesis sostenerse)

- **N1 (M-02).** Registrar la decisión real sobre D19 sin borrar ninguna versión: una entrada nueva
  (D20), con su fecha, que deje constancia de ambos textos. Evidencia: sección 2, fila M-02.
- **N2 (vacío 2).** Retirar o reformular la afirmación de que «no existe» una EHFC publicada
  (`02_estado_arte.tex:491, 523`; `01_introduccion.tex:134`). Evidencia: ficha
  `camiz_spada_2024.qmd`; nota del bibliotecario del 24-11, §3. La contribución puede defenderse
  con otra formulación (ver R-4): primera aplicación a datos macrofinancieros mensuales de
  una economía emergente, especificación formal propia (cap. 3), validación con nulos y con
  episodios fechados externamente, y la comparación con la EPCA y la datación de Fisher. Todo eso es
  verificable en la rama y no depende de que no exista otra EHFC.
- **N3 (M-01).** Integrar los tres productos en el cap. 5 y reescribir HT3, C8, R4 y
  `tab:estado-objetivos`. La lectura nueva debe acompañarse de la cobertura de azar (F0-3). Si no, se
  pasaría de un error por omisión («no separa») a una sobrelectura.
- **N4 (M-03 b).** El informe no puede afirmar un resultado del autoencoder que la tesis declara
  pendiente (regla de documentos de `CLAUDE.md`).
- **N5 (m-01).** No presentar el EMBIG como «representante elegido por los datos». Hay que dejar
  constancia del empate en la salida (Python y R) y en la tabla.

### Recomendable (fortalece)

- **Rc1 (M-04).** Informar el CH de la datación en sus dos variantes y declarar cómo se lee D11 sin un
  nulo de datación, incluida la coincidencia del CH habitual y la regla K en k = 11.
- **Rc2.** Fusionar `origin/main` **en** `iteracion-3c` (no al revés) antes de la auditoría de la
  vuelta 2. Así el auditor examina el estado que se integrará, con las cifras regeneradas (M-03 a)
  y los conflictos ya resueltos.
- **Rc3.** Hacer una consulta consolidada al Dr. Camiz (R-8) en lugar de preguntas sueltas.

### Opcional (trabajo futuro, iteración 4)

- **O1.** Un nulo formal de compatibilidad: cortes aleatorios con n_min = 12 y el mismo número de
  cortes. Su diseño implica decisiones (distribución de los cortes, estadístico), así que no entra
  en la 3c.
- **O2.** Un nulo de estructura constante para la datación, que permitiría aplicar D11 completo.
- **O3.** Las correlaciones entre representantes con el Índice BVL como representante alternativo
  de C3, solo como sensibilidad y solo si el Dr. Camiz mantiene la definición actual.

---

## 4. Decisiones que esperan a Roberto (una línea cada una)

| N.º | Decisión | Opciones | Recomendación del asesor |
|---|---|---|---|
| R-1 | Alcance retroactivo de la 3c (m-05) y conforme a la «autorización» del avance del cap. 5 que solo consta en una nota de agente | (a) Conforme a la sección 1; (b) conforme con ajustes | (a), indicando expresamente si el avance del cap. 5 se autorizó para el borrador MMC102 |
| R-2 | Qué D19 rige (M-02) | (a) Ratificar la corrección en la 3c como **D20** («D19 se adelanta a la 3c»), conservar el texto de `main` y validar el diseño de sorteo aparte (`sec:pend-d19`); (b) volver a la convención, revertir `c6e2a27` y sus cifras y dejar la corrección para la iteración 4 | (a): el código ya está auditado, con paridad 56/56 y las 58 pruebas aprobadas, y la auditoría no encontró cambios en la lectura cualitativa del nulo mixto |
| R-3 | Conforme de la regla 7 para la vuelta del cap. 5 y de las partes del cap. 6 que dependen de resultados (M-01, m-01, m-02, M-04) | (a) Autorizar la vuelta en la rama, sin publicar; (b) postergarla a la iteración 4 | (a): sin ella, M-01 queda abierto y la tesis contradice sus propios productos |
| R-4 | Camiz y Spada (2024) y el vacío 2 / OC1 | (a) Citarla como EHFC previa y reformular el vacío 2 y OC1 como aplicación y validación (N2); (b) mantener el vacío hasta terminar la lectura; (c) consultar primero al Dr. Camiz | (a) junto con (c): la frase actual no puede quedarse; terminar la lectura completa y confirmar el alcance con el asesor |
| R-5 | Cómo se aplica D11 en la datación (M-04) | (a) Informar el CH (k = 12 y 11) sin usarlo como selector, porque no puede comprobarse la segunda condición de D11; (b) construir un nulo de datación (O2) antes de decidir; (c) usar el CH como selector | (a) para la 3c y (b) como trabajo futuro: es la lectura conservadora de D11 y no cambia la especificación principal |
| R-6 | Afirmación sobre el AE en el informe de `main` (M-03 b), que ya se firmó y se compartió | (a) Alinear el informe con la tesis (AE pendiente con 16 series; el resultado con 17 series, como antecedente explícito) en una versión nueva; (b) mantenerla | (a): el informe no puede afirmar lo que la tesis no sostiene |
| R-7 | `.bib` del informe en `main` (M-03 c) | (a) Volver al `.bib` único: el bibliotecario incorpora las entradas que tengan ficha; (b) excepción documentada para el informe preliminar UNI | (a): es la regla de `CLAUDE.md`; las entradas sin ficha (`camiz_aedeclahfac`, `camiz_claede_2025`, `samaniego_2026`) quedan como `[CITA PENDIENTE]` hasta que el Dr. Camiz diga cómo citarlas |
| R-8 | Consulta consolidada al Dr. Camiz | (a) Una sola consulta con cuatro preguntas: EHFC con Spada y su relación con la propuesta, representante en clases de dos series, $k$ del CH de `aede`, actas de la ponencia con Diblasi; (b) preguntas sueltas | (a) |

---

## 5. Plan de cierre (vuelta 2)

**Objetivo.** Cerrar los hallazgos de la auditoría del 23-11-2026 y dejar `iteracion-3c` lista para
integrarse: el cap. 5 coherente con sus productos, un registro de decisiones sin contradicciones y la
rama ya fusionada con `main` para la auditoría.

**Convención.** **[F0]** = fase 0: no depende de ninguna decisión de la sección 4, no toca
`05_resultados.tex`, ni las partes de `06_conclusiones.tex` que dependen de resultados, ni el informe,
y no escribe resultados en la tesis. **[R-n]** = espera esa decisión de Roberto.

### 5.1 Fase 0 (se lanza apenas se entregue este plan, en `iteracion-3c`)

**F0-1 · Desarrollador · m-01, señalar el empate (sin regla nueva).**
En `notebooks/07c_hfc_clases.ipynb` y en el chunk equivalente de `R/ciclo_financiero_final.Rmd`, agregar
a `07c_hfc_clases3.csv` y a `R_hfc_clases3.csv` una columna booleana (p. ej., `empate_representante`).
Vale `True` para los miembros de una clase en la que el máximo de |r| lo alcanza más de una serie, con
una tolerancia numérica declarada en el código (relativa, del orden de 1e-10). **No se cambia** la
columna `representante` ni el criterio de elección. Comentar en el código que, en una clase de dos
series estandarizadas, el empate es estructural (ambas tienen |r| = √((1+|r₁₂|)/2)). Agregar a la
paridad una fila que compare la nueva columna, y una prueba en `tests/`.
*Por qué es fase 0:* no fija ninguna regla de desempate ni cambia el representante, la partición ni
ninguna cifra. La pregunta de fondo (`sec:pend-representante`) queda abierta para el Dr. Camiz
(R-8). No toca la tesis ni el informe. Además, deja de depender de la última cifra decimal en la
paridad, lo que es una mejora de reproducibilidad, no una decisión metodológica.

**F0-2 · Desarrollador · macros para M-01 y m-02 (sin usarlas en el texto).**
Agregar a `herramientas/cifras_mapa.csv` macros desde `09a_compatibilidad_cortes.csv`: `distancia_meses`
y `lado` de cada par corte × episodio con `compatible_h6 = True` (5 pares). Agregar también macros
`texto` desde la columna `fase` de `09a_regimenes_pca.csv`, para los regímenes 1 a 6. Regenerar
`cifras.tex` y `_cifras.yml`. Si un conteo requiere agregación (p. ej., cortes compatibles por h),
escribirlo en un CSV de resumen de 09a con su réplica en R, no a mano.

**F0-3 · Desarrollador · cobertura descriptiva de los episodios (recomendable).**
En 09a y en el Rmd, calcular desde `data/referencia/episodios_referencia.csv` la fracción de los meses
de la muestra, y de las posiciones de corte admisibles con n_min = 12, que cae a h meses o menos de
algún episodio, con h = 3 y h = 6 (parámetros de D7). Escribirla en un CSV nuevo con paridad. Es un
conteo determinista con parámetros ya decididos: no fija un nulo ni un estadístico (eso sería O1).

**F0-4 · Desarrollador · inventario de la fusión con `main`.**
Ejecutar `git merge-tree --write-tree HEAD origin/main` y registrar en
`auditorias/notas/AAAA-MM-DD_desarrollador.md`, para cada uno de los 16 archivos en conflicto, el
tipo de conflicto y la resolución propuesta. Para `cifras_mapa.csv`, `cifras.tex` y `_cifras.yml`:
unión del mapa y regeneración. Para `03_marco_teorico.tex`: comparación de los fragmentos.
**No fusionar.** `decisiones.qmd` y `CLAUDE.md` quedan marcados como «esperan R-2».

**F0-5 · Bibliotecario · cotejo de `camiz_spada_2024`.**
Nuevo intento de verificar el año (2023 según DOAJ, 2024 según el PDF), las páginas 13–23 y el DOI en
doi.org, Crossref o la página de la revista. Actualizar la ficha y el registro solo con lo verificado.
No hay cita en la tesis hasta R-4.

**F0-6 · Bibliotecario · inventario del `.bib` del informe en `main` (M-03 c) y de las fichas en
conflicto.**
(a) Listar las claves de `origin/main:tesis/informe_mmc102/referencias.bib` y `referencias_extra.bib`,
clasificadas así: ya está en `tesis/referencias.bib` / tiene ficha pero no entrada / no tiene ficha.
(b) Para las 9 fichas en conflicto (las 8 *add/add* y `congreso_2018`), confirmar que la versión de
la rama no pierde nada de la de `main`. **No se modifica ningún `.bib`.** El resultado va al registro
y a una nota.

**F0-7 · Redactor LaTeX · propiedad del representante en clases de dos series (sin resultados).**
En `04_metodologia.tex` (`sec:met-hfc`) o en `03_marco_teorico.tex`, agregar una observación con su
demostración. En una clase de dos series estandarizadas, cuyo factor es el primer componente de la
clase, ambas series tienen la misma |r| con el factor, así que el criterio «mayor |r|» no define un
representante. Actualizar `07_pendientes.tex`, `sec:pend-representante`, para incluir ese caso en la
pregunta al asesor. **No** se nombra ninguna serie, clase ni cifra de los resultados.

### 5.2 Tareas que esperan a Roberto

| Tarea | Agente | Espera | Contenido |
|---|---|---|---|
| W-1 | Orquestador | R-2 | Registrar D20 (o la reversión) en `decisiones.qmd` sin borrar el texto de `main`; alinear `CLAUDE.md`. Si se elige la reversión, el desarrollador revierte `c6e2a27` y regenera las cifras |
| W-2 | Orquestador + desarrollador | R-2 y F0-4 | Fusionar `origin/main` en `iteracion-3c` con las resoluciones de F0-4; regenerar `cifras.tex` y `_cifras.yml` después de la fusión (M-03 a) |
| W-3 | Redactor LaTeX | R-3 (y F0-1, F0-2, F0-3) | Cap. 5: integrar la tabla de compatibilidad (por macros), `07c_hfc_dendrograma.png` y `09a_trayectoria_pca_mm12.png`; reescribir HT3 con la cobertura de F0-3; declarar el empate en `tab:res-hfc` (m-01); pasar las fases de `tab:res-regimenes` a macros (m-02). Cap. 6: C8, R4, l. 103 y `tab:estado-objetivos` |
| W-4 | Redactor LaTeX | R-3 y R-5 | Cap. 5: CH de la datación en sus dos variantes, la lectura de D11 elegida y la coincidencia con la regla K en k = 11 (M-04) |
| W-5 | Redactor LaTeX + bibliotecario | R-4 (y F0-5) | Citar `camiz_spada_2024` con `\verificar` (incluido el año); reformular el vacío 2 (`02_estado_arte.tex:491, 523`), OC1 (`01_introduccion.tex:134`) y las conclusiones del cap. 6 que mencionen la EHFC |
| W-6 | Editor del informe | R-6, R-7 y W-2 | Alinear `00_preliminares.md` y el resto del informe con la tesis (AE); pasar el informe al `.bib` único según R-7 |
| W-7 | Bibliotecario | R-7 (y F0-6) | Incorporar a `tesis/referencias.bib` las entradas con ficha; dejar las demás con `[CITA PENDIENTE]` y en el registro |
| W-8 | Auditor | Todo lo anterior | Auditoría de la vuelta 2 sobre la rama ya fusionada |

### 5.3 Criterios de aceptación (verificables por el auditor)

1. **F0-1:** `07c_hfc_clases3.csv` y `R_hfc_clases3.csv` tienen la columna nueva. Vale `True` en las
   dos filas de C3 de la partición en 3 clases y `False` en todas las demás (las clases unitarias de
   la partición en 4 no cuentan como empate). Las demás columnas de ambos CSV y los otros CSV de 07c
   son idénticos byte a byte a los de `7c58906`. La paridad sigue completa (las filas nuevas
   coinciden). `pytest tests/` aprueba.
2. **F0-1 y F0-2:** `python3 herramientas/generar_cifras.py --comprobar` termina con código 0. Las
   184 macros previas no cambian de valor. Ninguna macro nueva aparece en `tesis_latex/capitulos/`
   antes de W-3.
3. **F0-3:** el CSV nuevo existe en Python y en R, con paridad. Los parámetros h = 3, h = 6 y
   n_min = 12 se leen de D7 y D17.1, no se fijan de nuevo.
4. **F0-4 y F0-6:** las notas cubren los 16 archivos en conflicto y todas las claves de los dos `.bib`
   de `main`. `git diff 7c58906 -- tesis/referencias.bib decisiones.qmd CLAUDE.md` sale vacío al
   cierre de la fase 0.
5. **F0-7:** la observación tiene su demostración, usa la notación de `notacion.tex` y no contiene
   ningún nombre de serie, clase ni cifra de `data/results/`. La tesis compila sin referencias
   indefinidas.
6. **Fase 0 en general:** `git diff 7c58906 -- tesis_latex/capitulos/05_resultados.tex tesis/` sale
   vacío. `06_conclusiones.tex` no cambia.
7. **W-1:** `decisiones.qmd` contiene **ambos** textos de D19 (el de `main` y el de la rama) y una
   entrada D20 con su fecha, su motivo y su rastro. `CLAUDE.md` es coherente con D20.
8. **W-2:** `git merge-tree HEAD origin/main` no da conflictos. Las cifras regeneradas después de la
   fusión coinciden con `data/results/`. Ninguna cifra del nulo mixto anterior a D19 aparece en
   `tesis/_cifras.yml`.
9. **W-3:** en el PDF no queda ningún `[PENDIENTE]` por los tres productos. Las distancias y las
   fases entran por macro. La lectura de HT3 menciona la cobertura de F0-3. `tab:res-hfc` declara el
   empate de C3.
10. **W-4:** el cap. 5 informa el CH de la datación (k = 12 y 11 con maxcl = 20, por macro) y la lectura
    de D11 que fijó Roberto.
11. **W-5:** ninguna frase de la tesis afirma que no existe una EHFC publicada. Si `camiz_spada_2024`
    se cita, lleva su `\verificar` con el año en duda.
12. **W-6 y W-7:** el informe no afirma nada sobre el AE que la tesis no sostenga. El informe usa un
    único `.bib` (o la excepción queda documentada según R-7).

### 5.4 Dependencias y ruta crítica

```
F0-1..F0-7 (paralelo, ya) ──┐
R-1, R-2 ── W-1 ── W-2 ─────┼── W-3, W-4, W-5 (redactor) ── W-6, W-7 ── W-8 (auditor) ── conforme 3c
R-3, R-4, R-5, R-6, R-7 ────┘
R-8 (consulta al Dr. Camiz): no bloquea el cierre si R-4 se resuelve con (a) y un \verificar
```

La ruta crítica pasa por **R-2** (sin ella no hay fusión) y por **R-3** (sin ella no se cierra M-01).
Las dos pueden resolverse en una sola respuesta de Roberto. La fase 0 no espera a ninguna.
