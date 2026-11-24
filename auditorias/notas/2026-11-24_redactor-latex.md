# Nota del redactor LaTeX — 24-11-2026 (vuelta 1 de la iteración 3c, fuera del cap. 5)

Rama `iteracion-3c`, commit de partida `f7712cc`. Insumos: `auditorias/2026-11-23_iteracion-3c.md`
(hallazgos M-01, m-02, m-03, m-04) y `auditorias/notas/2026-11-24_bibliotecario.md` (sección 4,
«Regla para el redactor»). **No se tocaron** `05_resultados.tex`, `06_conclusiones.tex`, `tesis/`,
`referencias.bib`, `cifras.tex`, `data/`, `src/`, `R/`, `notebooks/`, `decisiones.qmd` ni `CLAUDE.md`.
No se cita Camiz y Spada (2024) ni se cambió la afirmación de que no existe una EHFC publicada
(`02_estado_arte.tex`, vacío 2): ambas cosas esperan la decisión de Roberto.

## 1. Archivos tocados y qué cambió

| Archivo | Cambio | Hallazgo |
|---|---|---|
| `capitulos/00_resumen.tex` | «tres bloques» / «three blocks» → `\clasesHfcMenor{}` (la misma macro que usa el cap. 5) | m-02 |
| `capitulos/01_introduccion.tex` | Retirados los `\verificar` de Fisher (1958) y Horn (1965) | Regla 2 y 3 |
| `capitulos/02_estado_arte.tex` | Fisher: se retiran las dos notas y se amplía lo atribuido; Caliński y Harabasz: queda una sola nota (la primera); Camiz y Diblasi (2013): `\pendiente` → `\textcite` con `\verificar`; «menos de veinte años» → «de `\anioInicioDatos{}` a `\anioFinDatos{}`»; ancho de columna de `tab:sintesis-ea` (0,25 → 0,248) | Regla 1–2, m-03, m-02, m-04 |
| `capitulos/03_marco_teorico.tex` | Camiz y Diblasi: `\pendiente` → `\textcite` con `\verificar`; Horn: nota retirada y texto explícito (media en Horn, percentil elección de la tesis); Fisher: la formulación con $q>1$ queda como adaptación verificada; «las fuentes primarias tienen ficha preliminar» → solo la de la vara quebrada; «menos de veinte años» (l. 61) → macros de años | Regla 1–3, m-02 |
| `capitulos/07_pendientes.tex` | `sec:pend-cifras` y `sec:pend-productos` reescritas; Camiz y Diblasi retirado de las fuentes sin ficha; dos filas de `tab:pendientes` | M-01 (solo cap. 7), regla 1 |
| `preambulo.tex` | `\@pnumwidth` = 2 em (los números de página de tres cifras desbordaban el índice y la lista de tablas) | m-04 |
| `apendices/reproducibilidad.tex` | Ancho de la primera columna de `tab:md5` (0,5 → 0,49) | m-04 |

## 2. Qué se atribuye a cada fuente

- **`camiz_diblasi_2013`** (ficha FB-115; cap. 2, `sec:ea-factoriales`, y cap. 3, `def` de pesos):
  formalización del EPCA como un PCA en cada posición de una ventana móvil, resumido en la evolución
  de los primeros valores propios y de las correlaciones de las series con los primeros ejes;
  propuesta de pesos gaussianos que privilegian el centro; motivo (con pesos uniformes, dos ventanas
  consecutivas difieren solo en dos observaciones); en su ejemplo (diez acciones de París, 2009–2010,
  ventana de 15 días) los pesos suavizan las curvas; signo de los ejes fijado con las series más
  correlacionadas y dificultad del cambio progresivo de signo. **No** se le atribuye la fórmula de los
  pesos ni el $\nu$ de `eq:pesos`: el cap. 3 dice expresamente que la forma de `eq:pesos` y $\nu$ son de
  la tesis. Una nota `\verificar{ponencia sin actas localizadas; metadatos solo del PDF.}` por capítulo.
- **`fisher_1958`** (cap. 1, 2 y 3): partición que minimiza la suma de cuadrados intragrupo ponderada;
  distinción entre el problema sin restricción y el restringido a grupos contiguos; solución exacta
  mediante un lema de suboptimización («que hoy se expresa como programación dinámica» es lectura de la
  tesis); la variación de la suma con el número de grupos ayuda a elegirlo; sugerencia de reducir un
  problema multivariado con el primer componente principal. La formulación con $q>1$ y longitud
  mínima se declara adaptación de la tesis. Sin notas `\verificar`.
- **`horn_1965`** (cap. 1 y 3): crítica al criterio de Kaiser por la inflación muestral de los primeros
  valores propios; referencia con la **media** de los valores propios de matrices de variables
  aleatorias. El percentil superior, la distribución gaussiana y la simulación se declaran de la tesis;
  no se le atribuyen réplicas ni distribución. Sin notas `\verificar`.
- **`calinski_harabasz_1974`**: sin cambio de contenido; una nota en el cap. 2 (l. 222) y otra en el
  cap. 3 (l. 1263).

## 3. Conteos (totcount, `tesis.aux`)

| Marca | Antes | Después | Diferencia |
|---|---|---|---|
| `\pendiente` | 12 | 10 | −2 (Camiz y Diblasi, cap. 2 y 3) |
| `\verificar` | 94 | 90 | −6 (Fisher ×3, Horn ×2, Caliński duplicada ×1) +2 (Camiz y Diblasi) |
| *Overfull \hbox* | 15 | 0 | — |

Compilación con `latexmk -lualatex -cd tesis_latex/tesis.tex` (se instalaron con `apt-get` `biber`,
`texlive-bibtex-extra`, `texlive-lang-spanish` y `texlive-luatex`): sin errores, sin citas ni
referencias indefinidas. El PDF no se versiona.

## 4. Aviso al bibliotecario: la ponencia no se imprime completa

El driver `unpublished` de biblatex-apa (`apa.bbx`) **no imprime** `eventtitle`: solo `title`,
`titleaddon`, `howpublished`, `venue` e `institution`. La entrada sale así:

> Camiz, S., & Diblasi, A. (2013). Evolutionary principal component analysis [Ponencia]. Mendoza, Argentina.

Falta «XLI Coloquio Argentino de Estadística». El driver `presentation` de biblatex-apa sí usa la
macro `eventinfo` (`eventtitle`, `venue`), conforme a APA 10.5. La corrección es del bibliotecario
(tipo `@presentation`, o el nombre del coloquio en otro campo); el redactor no tocó el `.bib`.

## 5. Lo que queda para la vuelta del cap. 5 (requiere a Roberto, regla 7)

- M-01: integrar `09a_compatibilidad_cortes.csv` (y su paridad `R_compatibilidad_cortes.csv`),
  `07c_hfc_dendrograma.png` y `09a_trayectoria_pca_mm12.png`; retirar los tres `\pendiente` del cap. 5;
  revisar la lectura de HT3, C8, R4 y `tab:estado-objetivos`. El cap. 7 ya dice que los productos
  existen y que su integración queda para esa vuelta, sin adelantar lectura alguna.
- m-01: empate del representante de C3 (EMBIG) en `tab` de la HFC.
- m-02 en el cap. 5: etiquetas de fase de `tab:res-regimenes` (l. 445-450).
- Decisión de Roberto sobre Camiz y Spada (2024) y el vacío 2 (EHFC publicada).
