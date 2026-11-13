# Nota del bibliotecario — 13-nov-2026 (iteración 3c, seguimiento diario)

Rama `iteracion-3c`, commit de partida `c0fa997`. Encargo: cerrar, en lo verificable contra
fuentes oficiales, dos `\pendiente` bibliográficos del marco teórico (fuera del capítulo de
resultados), con un máximo de dos o tres búsquedas por tema:

1. `03_marco_teorico.tex` l. ~544 — fuente de la relación entre la inversa de la matriz de
   correlaciones y las correlaciones parciales (contexto KMO).
2. `03_marco_teorico.tex` l. ~429 y `02_estado_arte.tex` l. ~291 — fuente de la terminología de
   calidad de representación (cos²) y contribuciones de la escuela francesa.

No se tocaron `tesis_latex/`, `tesis/_capitulos/`, `data/`, `src/`, `R/` ni `notebooks/`.

## Archivos

- Nuevas fichas: `papers/guttman_1953.qmd` (FB-105) y `papers/escofier_pages_2023.qmd` (FB-106).
- `tesis/referencias.bib`: entradas `guttman_1953` (con campo `verificar`) y `escofier_pages_2023`.
  Parseo con pybtex: 105 entradas, sin claves duplicadas, todas con ficha en `papers/`.
- `papers/lebart_morineau_piron_1995.qmd`: la sección 6 remite ahora a `escofier_pages_2023` para
  la terminología cos²/contribuciones; Lebart queda como marco general.
- `tesis/registro_verificacion.md`: filas de los dos pendientes del marco teórico actualizadas
  (antes sin clave) y nueva sección «Pendientes del marco teórico (13-11-2026)».

## Lo verificado y la fuente de cada dato

### 1. Anti-imagen e inversa de la matriz de correlaciones · `guttman_1953` · ficha preliminar (resumen)

- Revisé primero si `kaiser_1970` o `kaiser_rice_1974` lo sustentan: según sus fichas y sus
  registros oficiales (Cambridge Core, SAGE/ERIC), ninguno de los dos trata la relación entre la
  inversa de la matriz de correlaciones y las correlaciones parciales; usan la anti-imagen en la
  MSA, nada más. No sirven para esta frase.
- Búsqueda 1 (web + Crossref): Dempster, «Covariance selection» (*Biometrics*, 1972), candidato
  conocido para la igualdad inversa ↔ correlación parcial. La API de Crossref quedó bloqueada
  (permiso no respondido a tiempo) y la búsqueda general no devolvió un registro oficial con
  resumen que lo sustente. No se fichó.
- Búsqueda 2 (web + Cambridge Core): Guttman, «Image theory for the structure of quantitative
  variates». Página del artículo en Cambridge Core
  (cambridge.org/core/journals/psychometrika/article/abs/image-theory-for-the-structure-of-quantitative-variates/8F167AD3F1184DFF5CA858DBA1FF74E1):
  autor Louis Guttman; *Psychometrika*, 18(4), 277–296; diciembre de 1953; DOI 10.1007/BF02289264.
  El resumen define la imagen y la anti-imagen de una variable como la predicción y el error de la
  regresión de mínimos cuadrados sobre las demás, y propone un cálculo «based upon the inverse of
  the correlation matrix». **No** menciona las «correlaciones parciales» ni da la fórmula de la
  correlación anti-imagen.
- Conclusión: Guttman (1953) es fuente primaria revisada por pares de la **anti-imagen** y de su
  cálculo desde $\mathbf{R}^{-1}$, pero el resumen **no** sostiene la igualdad literal «correlación
  anti-imagen = correlación parcial dado el resto». Esa igualdad se queda sin fuente vista.

### 2. Calidad de representación (cos²) y contribuciones · `escofier_pages_2023` · texto parcial

- `lebart_morineau_piron_1995` era la candidata. Intenté localizar su tabla de contenidos oficial:
  la ficha del catálogo de Nantes (Nantilus) está tras un bloqueo antibots; la página de Dunod de
  la 4.ª edición de Lebart, Piron y Morineau (2006, ISBN 9782100496167, *Statistique exploratoire
  multidimensionnelle. Visualisation et inférence en fouille de données*) muestra un sommaire de
  capítulos sin entrada de «aides à l'interprétation», «contributions» ni «cosinus carrés». No se
  localizó una sección verificable de cos²/contribuciones en Lebart; su fila sigue abierta.
- Siguiendo el enlace «feuilletage» del ecosistema de Dunod se llega al extracto oficial
  (dunod.com/sites/default/files/atoms/files/Feuilletage_3448.pdf), que resultó ser de **Escofier y
  Pagès, *Analyses factorielles simples et multiples*, 5e éd., Dunod, 2023, ISBN 978-2-10-085957-3**
  (portada y créditos vistos en el extracto). El extracto contiene pp. iii–viii, 1–6 y 7–28, es
  decir el capítulo 1 completo incluida la **sección 1.9 «Aides à l'interprétation» (p. 24)**:
  1.9.1 define a) «Qualité de représentation d'un élément par un axe» (identificada en el texto con
  el **coseno cuadrado** del ángulo entre el elemento y el eje), b) la calidad de una nube por un
  eje y c) la «Contribution d'un élément à l'inertie d'un axe», para individuos y variables.
- Esta obra es una fuente verificada (texto parcial) de la **terminología y los conceptos**; no se
  cotejaron las fórmulas ni las ponderaciones exactas de `def:cos2`.

## Regla para el redactor (y el editor del informe)

- **`guttman_1953`** — `03_marco_teorico.tex`, `sec:adecuacion`, l. ~544 (y en el informe,
  `[CITA PENDIENTE]` de «Adecuación muestral»). El `\pendiente` actual pide la fuente de la
  igualdad «correlación anti-imagen = correlación parcial dado el resto». Esa igualdad **no** está
  en ninguna fuente vista. Dos opciones, a elección del redactor:
  - Citar a Guttman solo por lo que su resumen sostiene —el concepto de anti-imagen y su cálculo a
    partir de la inversa de la matriz de correlaciones— y reescribir la frase para **no** afirmar la
    igualdad con la correlación parcial como atribuida a una fuente, p. ej.: «La correlación
    anti-imagen \parencite{guttman_1953} se obtiene de la inversa de la matriz de correlaciones; en
    la práctica coincide con la correlación parcial entre las series $j$ y $j'$ dada el resto.»,
    presentando la coincidencia como hecho de álgebra, no como cita. Con `\verificar{solo resumen
    consultado; el resumen de Guttman no emplea el término «correlación parcial»}`.
  - Si se quiere citar a una fuente **para la igualdad misma**, mantener el `\pendiente`: no hay
    fuente vista (Dempster, 1972, no se pudo verificar). No inventar la atribución.
  - En APA: «Guttman (1953)».
- **`escofier_pages_2023`** — `03_marco_teorico.tex`, `sec:cos2`, l. ~429, y `02_estado_arte.tex`,
  l. ~291 (y los `[CITA PENDIENTE]` correspondientes del informe). Sustituir el `\pendiente` por
  `\textcite{escofier_pages_2023}` **sin** `\verificar`. Atribuirle solo la **terminología**: que la
  escuela francesa llama «calidad de representación» (coseno cuadrado del ángulo entre el elemento y
  el eje) y «contribución» (a la inercia del eje) a las dos ayudas a la interpretación, para
  individuos y variables. **No** atribuirle las fórmulas exactas de `def:cos2` (la calidad en un
  plano como suma de dos cos², la normalización $\ctr_{t\ell}=c_{t\ell}^2/(n\lambda_\ell)$): esas
  siguen apoyándose en la definición de la tesis. En el `02_estado_arte.tex` l. ~291, el `\pendiente`
  menciona además el STATIS dual y la ponderación gaussiana (Camiz y Diblasi, 2013): esos dos siguen
  pendientes; al cerrar la parte de cos²/contribuciones, dejar el `\pendiente` reducido a esas dos
  fuentes aún sin ficha. En APA: «Escofier y Pagès (2023)».
- **`lebart_morineau_piron_1995`**: no se cita ya para cos²/contribuciones (sección no localizada).
  Puede seguir citándose como marco general de la escuela francesa donde el texto lo use así.

## Accesos fallidos y lo que no se hizo

- api.crossref.org (consulta de Dempster, 1972): permiso no respondido a tiempo; no se reintentó.
- Nantilus (catálogo de Nantes): bloqueo antibots (Anubis); no se buscó otra ruta.
- doi.org: no se probó para Guttman (metadatos ya verificados en Cambridge Core).
- No se usó curl ni python para acceder a sitios; solo la herramienta de lectura web.
- No se buscó Camiz y Diblasi (2013), Denimal (2001) ni el bootstrap por bloques conjunto (fuera
  del encargo de hoy): siguen pendientes según la nota del 11-11-2026.
- No se rehízo el conteo de marcas: la tarea no toca los documentos.
