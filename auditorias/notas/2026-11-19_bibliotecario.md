# Nota del bibliotecario — 19-nov-2026 (iteración 3c, seguimiento diario)

Rama `iteracion-3c`, commit de partida `67a9979`. Encargo:

1. Prioridad: fuentes revisadas por pares para el `\pendiente` de `02_estado_arte.tex` (l. ~345):
   uso del error de reconstrucción de autoencoders como señal de anomalía en series multivariadas,
   y aprendizaje profundo con series macrofinancieras cortas. Antecedente: la nota del 07-11-2026
   dejó `chalapathy_chawla_2019` y `plaut_2018` solo como exploración.
2. Secundario: fuente del optimizador Adam (registro, fila «Fuente del optimizador Adam»).

No se tocaron `tesis_latex/`, `tesis/_capitulos/`, `data/`, `src/`, `R/` ni `notebooks/`.

## Archivos

- Fichas nuevas (la mayor existente era FB-108):
  - `papers/pang_et_al_2021.qmd` (FB-109, preliminar, resumen);
  - `papers/su_et_al_2019.qmd` (FB-110, preliminar, resumen);
  - `papers/audibert_et_al_2020.qmd` (FB-111, preliminar, texto parcial);
  - `papers/kingma_ba_2015.qmd` (FB-112, resumen).
- `tesis/referencias.bib`: las cuatro entradas; las tres primeras con campo `verificar`. Conteo con
  expresión regular: 111 entradas, sin claves duplicadas, todas con ficha, llaves balanceadas
  (pybtex no estaba instalado y no se instaló).
- `tesis/registro_verificacion.md`: encabezado al día, fila de Adam cerrada en cuanto a la fuente,
  nota en la fila de `chalapathy_chawla_2019` y nueva sección «Pendientes bibliográficos
  (19-11-2026)».

## Lo verificado y la fuente de cada dato

### 1. `audibert_et_al_2020` (USAD) · texto parcial · la fuente más directa

- **Repositorio de EURECOM** (eurecom.fr/en/node/4901803): título; autores Julien Audibert, Pietro
  Michiardi, Frederic Guyard, Sebastien Marti, Maria A. Zuluaga; KDD 2020, 26th ACM SIGKDD
  Conference on Knowledge Discovery and Data Mining, San Diego (virtual), 23–27 ago. 2020; DOI
  10.1145/3394486.3403392. Sin páginas ni editorial.
- **Versión de los autores** en el mismo repositorio (PDF, bloque «ACM Reference Format»): mismos
  datos, 10 páginas, sin rango de páginas.
- **Leído (con una herramienta que resume):**
  - sec. 3.2: «Autoencoder-based anomaly detection uses the reconstruction error as the anomaly
    score»; la puntuación de USAD (ec. 9) combina dos errores de reconstrucción cuadráticos;
  - sec. 3.3: el entrenamiento debe recoger el comportamiento normal de semanas o meses de datos
    (unos 32 días en Orange);
  - sec. 5.2: robusto hasta alrededor de 5 % de anomalías en el entrenamiento; empeora desde 10 %;
  - no fija un tamaño mínimo de muestra.
- **Falta:** páginas, título exacto del volumen de actas y editorial (inferida del DOI y del formato
  ACM) → campo `verificar`.

### 2. `su_et_al_2019` (OmniAnomaly) · resumen

- **Stevens Pure** (researchwith.stevens.edu): título; KDD 2019 – Proceedings of the 25th ACM SIGKDD
  International Conference on Knowledge Discovery and Data Mining; Anchorage, 4–8 ago. 2019;
  pp. 2828–2837; ISBN 9781450362016; DOI 10.1145/3292500.3330672; «peer-review»; © ACM.
- **Orden de autores:** el repositorio da Su, Liu, Zhao, Sun, Niu, Pei; una base secundaria
  (bibtex.github.io) da Su, Zhao, Niu, Liu, Sun, Pei. Se usa el del repositorio con `verificar`;
  el primer autor coincide, así que «Su et al. (2019)» no cambia.
- **Resumen:** red recurrente estocástica para series multivariadas industriales; aprende patrones
  normales y señala anomalías por la **probabilidad de reconstrucción**; interpreta cada anomalía por
  las probabilidades de reconstrucción de las series univariadas.

### 3. `pang_et_al_2021` · resumen

- **OPUS (UTS):** *ACM Computing Surveys*, 54(2), 1–38, fascículo 2021-03, ACM, DOI 10.1145/3439950.
- **InK (SMU):** título completo, autores Pang, Shen, Cao, van den Hengel; mismos volumen, número y
  páginas; **fecha 2022-03**.
- **arXiv:2007.02500v3:** título, autores y DOI.
- Se adopta 2021 con `verificar` (año y número de artículo).
- **Resumen:** revisión de la detección de anomalías con aprendizaje profundo; taxonomía de 3
  categorías generales y 11 finas; supuestos, ventajas y desventajas de cada método. **No menciona
  autoencoders, error de reconstrucción ni series de tiempo.**

### 4. `kingma_ba_2015` (Adam) · resumen

- **arXiv:1412.6980:** autores Diederik P. Kingma y Jimmy Ba; «Published as a conference paper at the
  3rd International Conference for Learning Representations, San Diego, 2015»; DOI
  10.48550/arXiv.1412.6980.
- **UvA-DARE:** D. P. Kingma, L. J. Ba; ICLR 2015; mayo de 2015; 13 páginas; mismo DOI.
- Sin `verificar`. No se agregaron editores ni fechas del congreso (no vistos).

### 5. Aprendizaje profundo con series macrofinancieras cortas · no cerrado

- Una búsqueda general solo dio *preprints* (arXiv, preprints.org) y documentos sin revisión por
  pares verificable. No se fichó nada. Ninguna de las tres obras anteriores sirve: todas usan datos de
  sensores o de servidores con muchas observaciones.

## Regla para el redactor (y el editor del informe)

El `\pendiente` de l. ~345 **puede cerrarse parcialmente**: la primera mitad (error de
reconstrucción como señal de anomalía en series multivariadas) queda respaldada; la segunda (series
macrofinancieras cortas) no tiene fuente.

**Redacción propuesta** (sustituye el `\pendiente` completo):

> En la literatura de detección de anomalías en series de tiempo multivariadas, los métodos basados
> en autoencoders usan el error de reconstrucción como puntuación de anomalía
> \parencite[sec.~3.2]{audibert_et_al_2020}\verificar{texto leído en parte en la versión de los
> autores; páginas de las actas sin verificar.}; una variante usa la probabilidad de reconstrucción de
> una red recurrente estocástica entrenada con patrones normales
> \parencite{su_et_al_2019}\verificar{orden de autores sin verificar en la editorial; solo resumen
> leído.}. Esas aplicaciones usan datos de sensores o de servidores, con muchas observaciones y un
> período de entrenamiento con pocas anomalías
> \parencite[sec.~3.3 y 5.2]{audibert_et_al_2020}, condiciones que no se cumplen en una muestra
> mensual corta que contiene las crisis.
> \pendiente{fuente revisada por pares sobre aprendizaje profundo con series macrofinancieras
> cortas: sin ficha}

**Sobre la oración de l. ~331–335** (Chalapathy y Chawla): puede sustituirse la cita del *preprint*
por `\parencite{pang_et_al_2021}\verificar{año del fascículo (2021/2022) y número de artículo; solo
resumen leído.}`, diciendo solo que «la detección de anomalías con aprendizaje profundo tiene
revisiones propias». Si se conserva Chalapathy y Chawla, sigue como exploración.

**Qué atribuir y qué no:**

- **Audibert et al. (2020):**
  - sí: el uso del error de reconstrucción del autoencoder como puntuación (sec. 3.2), el
    entrenamiento con datos mayormente normales y la sensibilidad a anomalías en el entrenamiento
    (sec. 3.3 y 5.2);
  - no: cifras de desempeño, arquitectura ni un tamaño mínimo de muestra (no lo fija).
- **Su et al. (2019):**
  - sí: la **probabilidad** de reconstrucción como señal en series multivariadas y la interpretación
    por serie;
  - no: equipararla con el error cuadrático de un autoencoder determinista, ni detalles del modelo.
- **Pang et al. (2021):**
  - sí: que es una revisión con taxonomía del campo;
  - no: nada sobre autoencoders, error de reconstrucción o series de tiempo (el resumen no lo trata).
- **Ninguna de las tres** sostiene nada sobre series macrofinancieras o muestras cortas; la frase de
  contraste («condiciones que no se cumplen…») es lectura de la tesis.
- **Inferencia propia:** la conexión entre el error de reconstrucción del autoencoder y el de la
  validación *walk-forward* del PCA es de la tesis, como ya se declara para Vincent et al. (2008).
- **APA en el informe:** «(Audibert et al., 2020, sec. 3.2)», «(Su et al., 2019)», «(Pang et al.,
  2021)», con notas `VERIFICAR` que repitan los `\verificar`. Hoy el informe no tiene marca
  equivalente (`git grep` de «error de reconstrucción» y «macrofinancieras cortas»).
- **Adam (Rmd, A.5):** el desarrollador puede sustituir «Adam [VERIFICAR: sin ficha]» por «Adam
  (Kingma y Ba, 2015)». Solo como fuente del algoritmo: no justifica la tasa de 0,005 ni la parada
  temprana.

## Accesos fallidos y lo que no se hizo

- **api.crossref.org:** `curl` recibió 403 del proxy (dominio no permitido en la sesión), y la
  herramienta de lectura web no obtuvo permiso para los DOI 10.1145/3439950 y
  10.1145/3292500.3330672. No se reintentó.
- **doi.org** (10.1145/3292500.3330672): no se obtuvo permiso; no se reintentó.
- **ACM Digital Library:** no se abrió. Ningún metadato de las tres obras de ACM se vio en la
  editorial.
- No se buscaron copias espejo ni en caché. La versión de los autores de USAD está en el repositorio
  institucional de EURECOM, la institución de los autores.
- **Sakurada y Yairi (2014)**, sobre autoencoders frente a PCA para detectar anomalías por error de
  reconstrucción: es un candidato pertinente, pero solo se localizó en fuentes secundarias. No se
  fichó.
- Siguen pendientes:
  - fuente sobre aprendizaje profundo con series macrofinancieras cortas;
  - metadatos de editorial de las tres obras de ACM;
  - los pendientes previos (Camiz y Diblasi, 2013; Denimal, 2001; Künsch, 1989, en la editorial).
