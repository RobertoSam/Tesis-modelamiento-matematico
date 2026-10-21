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
| Parámetros fijados de antemano | Valores de diseño declarados en `decisiones.qmd` antes de calcular | Nivel de 5 % y rezagos de la regla D5 |

Si un número no encaja en ninguna clase, se reemplaza por una macro o se lleva al auditor.
