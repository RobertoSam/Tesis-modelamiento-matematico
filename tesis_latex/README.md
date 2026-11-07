# Tesis maestra en LaTeX

Documento maestro de la tesis. El informe del curso (`tesis/`) se deriva de él y no puede
afirmar nada que la tesis no sostenga. El PDF no se versiona; se publica solo con el conforme de
Roberto.

## Compilar

Desde la raíz del repositorio:

```
latexmk -lualatex -cd tesis_latex/tesis.tex
```

El PDF queda en `tesis_latex/tesis.pdf` (ignorado por git, igual que los auxiliares).
Paquetes de Debian necesarios, además de `texlive-latex-extra`: `texlive-lang-spanish` (babel),
`texlive-bibtex-extra` (biblatex y biblatex-apa), `biber` y `texlive-luatex` (luaotfload). En la
sesión del 27-10-2026 faltaban los cuatro y se instalaron con `apt-get`.
`tesis.tex` empieza con `\nonstopmode` porque, con `-cd`, latexmk no lee `tesis_latex/latexmkrc`
(solo lo lee si se ejecuta desde dentro de `tesis_latex/`).

## Archivos

| Archivo | Contenido |
|---|---|
| `tesis.tex` | Documento principal: clase, orden de los capítulos, bibliografía y apéndices |
| `preambulo.tex` | Paquetes, formato de página, entornos `amsthm`, `cleveref`, `\pendiente{}` y `\verificar{}` |
| `notacion.tex` | **Notación única**: macros y lista de símbolos (`\listadesimbolos`) |
| `cifras.tex` | **Generado** por `herramientas/generar_cifras.py` desde `data/results/final/` (cifras vigentes, D15 y D16) y `data/referencia/` (fechas de los episodios, D7). No se edita a mano |
| `cifras_stub.tex` | Define como `\pendiente{cifra}` toda macro de cifras que falte en `cifras.tex` (`\providecommand`) |
| `capitulos/NN_*.tex` | Portada y capítulos 1 a 5 (el 3, de métodos sin resultados, desde la iteración 3b; el 4 y el 5 siguen vacíos por la regla 7) |
| `apendices/apendices.tex` | Índice de apéndices (vacío) |
| `latexmkrc` | Configuración de latexmk cuando se compila desde `tesis_latex/` |

La bibliografía es `../tesis/referencias.bib` (compartida con el informe; solo la modifica el
bibliotecario). Las figuras se buscan en `../reports/figures/` (`\graphicspath`).

## Formato (decisión B, provisional)

- Clase `book`, 12 pt, A4, una cara (`oneside`): margen izquierdo de 3 cm y 2,5 cm en los demás
  lados; interlineado 1,5 (`\onehalfspacing`), como `tesis/plantilla_uni.docx`. La plantilla
  Word no fija el papel; se adoptó A4.
- **Fuente:** Nimbus Sans (paquete `helvet`), clon de Helvetica. Arial reproduce los anchos de
  Helvetica, de modo que es su equivalente métrico más cercano disponible en TeX Live.
  Matemáticas en Computer Modern.
- No se usa `fontspec`. Hasta la iteración 3a el entorno no traía `luaotfload` (paquete Debian
  `texlive-luatex`) y el log mostraba `Error in luaotfload: reverting to OT1`; desde la vuelta 2
  de la auditoría 3a está instalado y el aviso desapareció. Se mantienen las fuentes Type 1 con
  codificación T1, que compilan igual en cualquier TeX Live; `fontspec` y una fuente OpenType
  se evaluarán al adoptar la plantilla de la UNI. Los signos que en T1 no coinciden con Latin-1
  (« » ¿ ¡ — – “ ” ·) se declaran con `newunicodechar`; si se usa uno nuevo, hay que declararlo.
- La portada usa numeración `Alph` propia para que no se repita el destino `page.I` de
  `hyperref` (auditoría 3a, N-07).
- Debe revisarse cuando estén las pautas de la UNI.

## Reglas de redacción

- Definiciones, supuestos, proposiciones y observaciones con los entornos de `amsthm`, numerados
  por capítulo; referencias con `\cref`, nunca a mano.
- Ningún número de datos a mano: solo macros de `cifras.tex`. Las únicas excepciones admitidas
  son las de la lista siguiente (auditoría 3a, N-10).
- `\textcite`/`\parencite` solo con claves que tengan entrada en el `.bib` **y** ficha en
  `papers/`. Lo demás va como `\pendiente{qué falta}`. Los datos por verificar de obras con ficha
  van como `\verificar{motivo}` (nota al pie), equivalente a `[VERIFICAR: motivo]` del informe.
- Antes de introducir un símbolo, buscarlo en `notacion.tex`.

## Lista de excepciones a la regla de cifras

Un dígito escrito a mano en `capitulos/*.tex` solo es admisible si pertenece a una de estas
clases. Todo lo demás (tamaños muestrales, fechas del dataset, inercias, estadísticos, umbrales
que dependan de los datos) entra por una macro de `cifras.tex`.

| Clase | Qué cubre | Ejemplos |
|---|---|---|
| Años de las citas | El año dentro de una referencia o del nombre de una obra | Fisher (1958), Drehmann et al. (2012) |
| Cifras atribuidas a una fuente fichada | Hechos de la literatura, citados junto a la obra que los sostiene y respaldados por su ficha en `papers/` | Duración de 8 a 30 años y de 1 a 8 años (`drehmann_borio_tsatsaronis_2012`); 17 indicadores, 1999–2020, grupos de 7/4/4 series y ventana de 48 meses (`camiz_cerda_atoche_2026`); umbral de 0,7 (`camiz_et_al_2020`) |
| Fechas de episodios externos | Año o mes de un evento citado como hecho histórico, con su fuente o su `\pendiente` | 2008, 2013, 2020 en la descripción de los episodios |
| Constantes y parámetros matemáticos | Números que forman parte de una definición, proposición o demostración y no dependen de los datos | $P\ge2$, $\pi/6$, $1/2$, $\gamma(2)=2$ |
| Numeración y estructura | Capítulos, secciones, ítems, apuntes o decisiones (D1–D6) | «apunte 11», «decisión D5» |
| Parámetros fijados de antemano | Valores de diseño declarados en `decisiones.qmd` antes de calcular | Nivel de 5 % y rezagos de la regla D5; grilla {24, 36, 48, 60} (D10); ±3 y ±6 meses (D7); d = 3, 2 y 4 (D9); 12 rezagos y \|t\| > 2 (D8); 10 % (D12); maxcl 10, 15 y 20 y n_min = 12 (D17.1); maxcl = 20 del nulo (D11); 2017-10 (D13) |
| Identificadores y fechas de registro | Fechas de las decisiones de `decisiones.qmd`, de versionado de los datos (D4) y de los manuscritos; nombres de archivos, notebooks y etiquetas de versión | «16 de octubre de 2026» (D4), `05_tendencia_series.csv`, notebook 09 |
| Metadatos bibliográficos | Páginas, números de informe y fechas dentro de las notas `\verificar` | 789–798, FKI-207-95 |
| Parámetros de diseño del plan (provisional) | Valores fijados en el plan aprobado de la iteración 3b o en el código anterior a ella, que `decisiones.qmd` no recoge. Desde la vuelta 1 de la auditoría 3b (N-03) están en `data/results/final/parametros_diseno.csv` (generado por `herramientas/exportar_parametros_diseno.py`) y tienen macros (`\nuGauss`, `\pasoReglaSeis`, `\ejeReglaSeis`, `\ventanaMediaMovil`, `\clasesHfcMenor`, `\clasesHfcMayor`, `\percentilWalkforward`). Desde la vuelta 2 (31-10-2026) los capítulos 2 y 3 y la lista de símbolos usan esas macros, también en el nombre del método (`PCA-MM\ventanaMediaMovil`), para que nombre y parámetro no diverjan; los capítulos 4 y 5 no se tocaron (regla 7). Los valores siguen siendo **provisionales**: no están en `decisiones.qmd` y no se declaran decididos. No se sustituyen el parámetro igual a 3 que se atribuye a Atoche y Murrieta (2022) (cifra de una fuente fichada), los «pasos 3 y 4» de `alg:aede` (numeración) ni n_min = 12 (D17.1) | ν = 3 (`nsd`), paso 3 y eje 2 de la regla del 06, media móvil de 12 meses (PCA-MM12), particiones en 3 y 4 clases de la HFC, percentil 95 de la razón de error *walk-forward* |

Si un número no encaja en ninguna clase, se reemplaza por una macro o se lleva al auditor.
