# Nota del redactor LaTeX · 31-10-2026 · vuelta 2 de la auditoría 3b (N-03)

Sesión automática de seguimiento diario, sin Roberto presente. Rama `iteracion-3b`.

## Lo redactado

No cambia el contenido. Los valores de diseño escritos a mano pasan a las macros de
`tesis_latex/cifras.tex`, que salen de `data/results/final/parametros_diseno.csv`.

| Archivo:línea | Antes | Macro |
|---|---|---|
| `capitulos/02_marco_teorico.tex:1262` | título de `def:datacion`, «PCA-MM12» | `PCA-MM\ventanaMediaMovil{}` |
| `capitulos/03_metodologia.tex:121` | «Particiones en 3 y 4 clases» (tabla) | `\clasesHfcMenor{}`, `\clasesHfcMayor{}` |
| `capitulos/03_metodologia.tex:122` | «Trayectoria PCA-MM12» (tabla) | `PCA-MM\ventanaMediaMovil{}` |
| `capitulos/03_metodologia.tex:182` | $\nu=3$ | `\nuGauss` |
| `capitulos/03_metodologia.tex:183` | $\nu=3$ | `\nuGauss` |
| `capitulos/03_metodologia.tex:197` | $\nu=3$ (pie de `tab:kish`) | `\nuGauss` |
| `capitulos/03_metodologia.tex:216` | $\paso=3$, $\ell_0=2$ | `\pasoReglaSeis`, `\ejeReglaSeis` |
| `capitulos/03_metodologia.tex:242` | «en 3 y en 4 clases» | `\clasesHfcMenor{}`, `\clasesHfcMayor{}` |
| `capitulos/03_metodologia.tex:260` | «media móvil causal de 12 meses» | `\ventanaMediaMovil{}` |
| `capitulos/03_metodologia.tex:261` | «PCA-MM12» | `PCA-MM\ventanaMediaMovil` |
| `capitulos/03_metodologia.tex:291` | $E^{(95)}_a$ | `\percentilWalkforward` |
| `capitulos/03_metodologia.tex:292` | $E^{(95)}_a$, «percentil 95» | `\percentilWalkforward` (dos veces) |
| `notacion.tex:207` | «PCA-MM12» | `PCA-MM\ventanaMediaMovil{}` |
| `notacion.tex:242` | $E^{(95)}_a$, «percentil 95» | `\percentilWalkforward` (dos veces) |

**Criterio para «PCA-MM12».** El texto dice que el nombre viene del parámetro («de ahí el nombre
PCA-MM12»). Por eso el nombre se escribe con la macro en los capítulos 2 y 3 y en la lista de
símbolos: si cambia la ventana, el nombre cambia con ella. El PDF se ve igual. Los capítulos 4 y 5
conservan el literal, porque no se tocan (regla 7).

Otros cambios:

- se añadieron a `cifras_stub.tex` los siete `\providecommand` (como `\pendiente{cifra}`), como
  en el resto del contrato;
- se quitó el «Pendiente» de la fila «Parámetros de diseño del plan (provisional)» en
  `tesis_latex/README.md:83`. La fila deja constancia de que los valores siguen siendo
  provisionales y no están en `decisiones.qmd`.

## Casos dejados sin cambio

- `02_marco_teorico.tex:813`: el «parámetro igual a 3» de Atoche y Murrieta (2022). Es una
  cifra de una fuente fichada, y el propio texto no confirma que sea nuestro $\nu$.
- `02_marco_teorico.tex:901-905`: los «pasos 3 y 4» y el «paso 3» de `alg:aede`. Es la numeración
  del algoritmo.
- `03_metodologia.tex:261`: $n_{\min}=12$ meses. Es D17.1, no la ventana de la media móvil.
- `03_metodologia.tex:167, 180, 230, 259, 298`: $d=3$ y «tres ejes» (D9) y los ±3 y ±6 meses
  (D7, línea 298). Son parámetros de decisiones registradas y no forman parte de N-03.
- `02_marco_teorico.tex:532-534, 999`: «percentil» sin número. Es el percentil de Horn, que es
  otro parámetro.
- Los capítulos 4 y 5: regla 7.

## M-03

Está resuelto. `02_marco_teorico.tex:222` lleva `\verificar{…}` inmediatamente después de
`\parencite{fmi_2015b}` (commit `d7302e0`). No hay otra cita de `fmi_2015b` en `tesis_latex/`.

## Compilación y comprobaciones

- `latexmk -lualatex -cd tesis_latex/tesis.tex` termina con exit 0: 75 páginas, 0 avisos, sin
  referencias ni citas indefinidas y sin cajas desbordadas. Biber termina sin avisos. Hay 18
  *underfull*, los mismos que en `HEAD` (636cc70).
- El texto del PDF (`pdftotext -layout`) es idéntico byte a byte al de `636cc70`, compilado en un
  *worktree* aparte. Los valores mostrados no cambian.
- `python3 herramientas/generar_cifras.py --comprobar` termina con exit 0.
- Para compilar en este entorno hubo que instalar `biber`, `texlive-bibtex-extra`,
  `texlive-lang-spanish` y otros paquetes de TeX Live.

## Pendientes

- El editor del informe debe hacer las mismas sustituciones en `tesis/_capitulos/` (N-03, parte
  del informe).
- Los parámetros siguen siendo provisionales mientras no se registren en `decisiones.qmd`. Esa
  decisión es de Roberto.

## Inconsistencias detectadas

Ninguna nueva.
