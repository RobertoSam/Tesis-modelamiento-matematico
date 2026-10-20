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
`tesis.tex` empieza con `\nonstopmode` porque, con `-cd`, latexmk no lee `tesis_latex/latexmkrc`
(solo lo lee si se ejecuta desde dentro de `tesis_latex/`).

## Archivos

| Archivo | Contenido |
|---|---|
| `tesis.tex` | Documento principal: clase, orden de los capítulos, bibliografía y apéndices |
| `preambulo.tex` | Paquetes, formato de página, entornos `amsthm`, `cleveref`, `\pendiente{}` y `\verificar{}` |
| `notacion.tex` | **Notación única**: macros y lista de símbolos (`\listadesimbolos`) |
| `cifras.tex` | **Generado** por `herramientas/generar_cifras.py` desde `data/results/`. No se edita a mano |
| `cifras_stub.tex` | Define como `\pendiente{cifra}` toda macro de cifras que falte en `cifras.tex` (`\providecommand`) |
| `capitulos/NN_*.tex` | Portada y capítulos 1 a 5 (3, 4 y 5 vacíos en la iteración 3a; el 4 sigue la regla 7) |
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
- No se usa `fontspec`: el TeX Live de este entorno no trae `luaotfload` (paquete Debian
  `texlive-luatex`). Por eso el log muestra la línea `Error in luaotfload: reverting to OT1`, que
  no detiene la compilación. Con fuentes Type 1 y codificación T1, el documento compila igual en
  cualquier TeX Live. Los signos que en T1 no coinciden con Latin-1 (« » ¿ ¡ — – “ ” ·) se
  declaran con `newunicodechar`; si se usa uno nuevo, hay que declararlo.
- Debe revisarse cuando estén las pautas de la UNI.

## Reglas de redacción

- Definiciones, supuestos, proposiciones y observaciones con los entornos de `amsthm`, numerados
  por capítulo; referencias con `\cref`, nunca a mano.
- Ningún número de datos a mano: solo macros de `cifras.tex`. Los números que quedan en el texto
  son años de cita, cifras de las fuentes citadas, constantes matemáticas y numeración.
- `\textcite`/`\parencite` solo con claves que tengan entrada en el `.bib` **y** ficha en
  `papers/`. Lo demás va como `\pendiente{qué falta}`. Los datos por verificar de obras con ficha
  van como `\verificar{motivo}` (nota al pie), equivalente a `[VERIFICAR: motivo]` del informe.
- Antes de introducir un símbolo, buscarlo en `notacion.tex`.
