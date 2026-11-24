# Nota del bibliotecario — 24-11-2026 (vuelta 1 de la iteración 3c, hallazgo M-03 d)

Rama `iteracion-3c`, commit de partida `594e826`. *Merge-base* con `origin/main`: `b893b23`. Las fichas
y la sección del registro que la rama no tenía vienen del commit `63c6914` de `main` («Informe
preliminar UNI: versión del 8-11-2026»). No se tocaron `main`, `tesis/informe_mmc102/`,
`tesis/informe_preliminar_uni/`, los `.bib` del informe, `tesis_latex/`, `data/`, `src/`, `R/`,
`notebooks/` ni `decisiones.qmd`.

## 1. Lo hecho

### Fichas traídas de `main` (seis nuevas)

Las fichas de `main` tenían solo cuatro secciones. Se pasaron al formato de la Ficha Estándar
(secciones 1 a 7, código FB, tipo de fuente, recuadro de estado) **sin agregar contenido**: el resumen
analítico es el texto de Roberto, y las secciones 5 a 7 solo reordenan lo que ya decía. Las
declaraciones de lectura («texto completo leído», «lectura parcial») son de Roberto y se conservan; el
bibliotecario **no** tuvo acceso a los PDF (carpeta de Dropbox del asesor).

| Ficha | Código | Lectura (Roberto) | Metadatos: qué se verificó y dónde | `.bib` |
|---|---|---|---|---|
| `camiz_diblasi_2013` | FB-115 | Completa, 7-11-2026 | Nada en fuente oficial. Búsqueda web (título, autores, coloquio, Mendoza 2013): sin actas ni programa. Datos solo del PDF | Agregada, `@unpublished`, con `verificar` |
| `camiz_spada_2024` | FB-116 | Parcial, 8-11-2026 | Título exacto: página de la revista (journals-crea.4science.it, artículo 2455) vista **en el buscador**; 2455 coincide con el sufijo del DOI. doi.org/10.12899/asr-2455 y creajournals.crea.gov.it: permiso no respondido en la sesión (no se reintentó). Vol. 49(1), pp. 13–23: solo del PDF | Agregada, con `verificar` |
| `abdi_2010` | FB-117 | Completa, 7-11-2026 | **SAGE Knowledge** (sk.sagepub.com, editorial): entrada «Congruence», *Encyclopedia of Research Design*, ed. Neil J. Salkind, SAGE Publications, 2010, **pp. 223–229**, DOI **10.4135/9781412961288.n71**. La página no muestra el autor ni el subtítulo (vienen del PDF) | No (la tesis no la necesita) |
| `camiz_2021_pca` | FB-118 | Parcial, 7-11-2026 | No aplica: material de clase no publicado. Tratado como exploración (criterio de Plaut, 2018) | No (no citable) |
| `purizaca_2023` | FB-119 | Completa, 8-11-2026 | No verificado: tesis.pucp.edu.pe devolvió una página antirrobots («Access Denied»); no se buscó una ruta alternativa. Tres registros de ALICIA (CONCYTEC) que el buscador asoció eran otras tesis | No |
| `torres_baltazar_2023` | FB-120 | Parcial, 8-11-2026 | No verificado: una búsqueda no halló el registro de ESAN | No |

### Fichas combinadas a mano

- **`fisher_1958`:** se reemplazó el recuadro «Ficha PRELIMINAR» por la nota de lectura de Roberto
  (8-11-2026), con su procedencia. Se conservó la verificación del 20-10-2026 y se agregó la del
  24-11-2026: las páginas 789–798 constan en el artículo (lectura de Roberto), así que se retiró el campo
  `verificar` del `.bib`. La sección 4 se actualizó solo con lo que dice la nota: el artículo distingue
  el problema sin restricción del restringido (contiguo), prueba en un apéndice que la partición de
  mínimos cuadrados es contigua en el caso sin restricción, usa el ejemplo del lago Michigan-Huron
  (1860–1955) y **sugiere reducir un problema multivariado con el primer componente principal**. La
  pregunta abierta sobre el caso multivariado queda así: la nota no dice que el artículo resuelva la
  partición sobre vectores; la formulación con $q>1$ sigue siendo una adaptación de la tesis. Una
  búsqueda web del 24-11-2026 no devolvió la página de Taylor & Francis.
- **`horn_1965`:** estado de lectura actualizado («texto completo leído el 8-11-2026», declaración de
  Roberto). La sección 4 registra que Horn usa el **promedio** de los valores propios de matrices
  aleatorias y que critica a Kaiser por la inflación muestral de los primeros valores propios; ejemplo:
  65 variables, 297 adultos, 16 raíces > 1, 9 factores. El percentil 95 sigue siendo elección de la
  tesis. Se corrigió el tamaño de muestra desactualizado de la sección 5 (228 × 17 → 228 × 16, D16).
- **`congreso_2018`:** sin cambios. La versión de la rama ya contiene la corrección de `main` (D18) y la
  amplía. Al integrar, debe prevalecer la de la rama (es uno de los conflictos de M-02).

### Registro

`tesis/registro_verificacion.md`: párrafo inicial con la fecha; filas de `fisher_1958`, `horn_1965` y
Camiz y Diblasi (ahora `camiz_diblasi_2013`) actualizadas con su historial; las tres filas históricas
de Camiz y Diblasi (09, 11 y 15-11-2026) llevan «superado el 24-11-2026»; sección nueva «Reconciliación
con `main` (24-11-2026, M-03 d)», que **copia como rastro** la tabla de `main` del 8-11-2026 y da el estado
en la rama después de la reconciliación.

### `.bib`

115 entradas (113 + 2), sin claves duplicadas, llaves balanceadas, todas con ficha (expresión regular).
**No se compiló con biber** (no instalado en el entorno): el redactor debe comprobar al compilar que
`@unpublished` con `titleaddon`, `eventtitle` y `venue` se imprime como «[Ponencia]. XLI Coloquio
Argentino de Estadística, Mendoza, Argentina» en biblatex-apa.

## 2. Pendiente y motivo

- `camiz_diblasi_2013`: actas, ISBN o URL; nombre de pila de la segunda autora. Ocho búsquedas sin
  resultado: sigue el pedido a Roberto de preguntar al Dr. Camiz si hubo actas.
- `camiz_spada_2024`: cotejar volumen, número, páginas y DOI en doi.org o en la revista (permiso no
  respondido hoy).
- `purizaca_2023`, `torres_baltazar_2023`: *handle* del repositorio (PUCP bloqueado por un sistema
  antirrobots; ESAN no localizado).
- `fisher_1958`: la editorial y doi.org siguen sin abrirse; no afecta a la cita (las páginas están en el
  artículo).
- `camiz_aedeclahfac`, `camiz_claede_2025`, `samaniego_2026` (en `main`, solo en el `.bib` del informe
  preliminar): sin ficha; dependen de M-03 c y de cómo pida citarlos el Dr. Camiz.

## 3. Aviso: contradicción con la tesis (no corregida)

Según la ficha de Roberto, **Camiz y Spada (2024) proponen una HFC evolutiva (EHFC)** con ventana móvil y
pesos gaussianos, y la ficha de `main` dice que «corrige la afirmación previa de que no había una EHFC
publicada». La tesis afirma lo contrario en `02_estado_arte.tex:484-487` (vacío 2: «No existe en la
literatura revisada un algoritmo EHFC publicado») y `:515-516` («no existe una especificación previa
contra la cual validarla»), y la auditoría (C.10) lo tomó como coherente. También afecta a
`01_introduccion.tex:135-137` (OC1, «en lugar de la aplicación secuencial de HFC y EPCA de la
literatura»). El bibliotecario no corrige el texto: lo decide Roberto, porque toca el aporte declarado
de la tesis.

## 4. Regla para el redactor

Aplica solo después de leer esta nota y las fichas; ninguna cifra ni detalle fuera de lo que sigue.

1. **Camiz y Diblasi (2013)**, `02_estado_arte.tex:302` y `03_marco_teorico.tex:778`: los dos
   `\pendiente{… sin ficha}` pueden pasar a `\textcite{camiz_diblasi_2013}` o
   `\parencite{camiz_diblasi_2013}` con un `\verificar{ponencia sin actas localizadas; metadatos solo del
   PDF}`. Se le puede atribuir: (a) la formalización del EPCA como un PCA en cada posición de una ventana
   móvil, resumido en la evolución de los primeros valores propios y de las correlaciones de las series
   con los primeros ejes; (b) la propuesta de pesos gaussianos que privilegian el centro de la ventana;
   (c) el motivo: con pesos uniformes, dos ventanas consecutivas difieren solo en dos observaciones;
   (d) que los pesos gaussianos suavizan las curvas en su ejemplo (diez acciones de París, 2009–2010,
   ventana de 15 días); (e) que el signo de los ejes se fija con las series más correlacionadas y que el
   cambio progresivo de signo es difícil de controlar. **No** atribuirle: la fórmula exacta de los pesos
   ni que su parametrización (pesos en [−4, 4]) sea el $\nu$ de `eq:pesos`; ningún ancho mensual.
   Actualizar también `07_pendientes.tex:202`, que la lista entre las fuentes sin ficha.
2. **Fisher (1958)**, `01_introduccion.tex:58`, `02_estado_arte.tex:212-215` y `395-397`: las notas
   `\verificar` pueden **retirarse** (páginas confirmadas en el artículo; volumen, número y DOI ya
   verificados; texto leído). Si se deja alguna marca, que sea solo para el alcance multivariado. Se le
   puede atribuir: la partición que minimiza la suma de cuadrados ponderada; la distinción entre el
   problema sin restricción y el restringido a grupos contiguos (datos ordenados); la solución exacta
   (lema de suboptimización); que la variación de D con el número de grupos G ayuda a elegir G; la
   sugerencia de reducir un problema multivariado con el primer componente principal. En
   `03_marco_teorico.tex:1098-1103`, la frase «La formulación con $q>1$ […] se declara como adaptación
   mientras no se verifique el alcance del artículo original» puede quedar como **adaptación**, ahora
   verificada: el artículo no la trata, solo sugiere reducir a una dimensión con el primer componente.
   Esto cierra, de paso, la nota duplicada de m-03 (queda ninguna o una por capítulo).
3. **Horn (1965)**, `01_introduccion.tex:107` y `03_marco_teorico.tex:495`: cambiar «ficha preliminar:
   se leyó el resumen, no el texto» por la lectura completa. El `\verificar` de `03_marco_teorico.tex:495`
   puede retirarse si el texto dice explícitamente que Horn usa la **media** de los valores propios de
   matrices aleatorias y que el percentil superior es una elección de la tesis. Se le puede atribuir:
   la crítica al criterio de Kaiser por la inflación muestral de los primeros valores propios y el
   procedimiento con el promedio de los valores propios de matrices de variables aleatorias. **No**
   atribuirle el número de réplicas ni la distribución de las variables simuladas.
4. **Camiz y Spada (2024)**: hay entrada en el `.bib` (con `verificar`), pero **no** se cita hasta que
   Roberto decida cómo tratar la contradicción de la sección 3. Si la cita, puede atribuirle: EPCA y EHFC
   sobre ventana móvil de 10 años (el doble del número de series) con pesos gaussianos (k = 3), en cinco
   cronologías de *Pinus pinea* (1925–2003); criterios del ancho (ruido, ventana mucho mayor que p,
   múltiplo de la periodicidad); seguimiento de las inercias de los nodos y de la topología de los
   dendrogramas (Newick, Robinson-Foulds); Fisher sobre el primer valor propio con número de intervalos
   por máximos locales del CH entre 2 y 10, con siete intervalos. Con
   `\verificar{volumen, número, páginas y DOI vistos solo en el PDF}`.
5. **Abdi (2010), Purizaca (2023), Torres y Baltazar (2023), Camiz (2021):** fichadas, sin entrada en el
   `.bib`. Si el redactor quiere citar alguna, la pide al bibliotecario; `camiz_2021_pca` no es citable
   como fuente (material no publicado).
6. El informe (`tesis/informe_mmc102/`) queda fuera: depende de M-03 c.
