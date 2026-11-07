# Nota del editor del informe · 31-10-2026 · vuelta 2 de la auditoría 3b (N-03 y M-03)

Sesión automática de seguimiento diario, sin Roberto presente. Rama `iteracion-3b`, a partir de
`c40b7bf` (redactor, commits `74a1ac6` y `c40b7bf`).

## Lo redactado

No cambia el contenido ni las referencias. Los parámetros de diseño escritos a mano pasan a las
claves de `tesis/_cifras.yml` (generadas desde `data/results/final/parametros_diseno.csv`) con el
shortcode `{{< meta cifras.… >}}`, como el resto de las cifras del informe. Se sigue el criterio
del redactor para «PCA-MM12»: la clave va también dentro del nombre. Quarto 1.10 resuelve el
shortcode dentro de `$…$` y en el atributo `name` de un *div* (se comprobó con un documento de
prueba antes de editar).

| Archivo:línea (antes del cambio) | Antes | Clave |
|---|---|---|
| `_capitulos/02_marco_teorico.qmd:422` | título de `def-datacion`, «PCA-MM12» | `ventanaMediaMovil` |
| `_capitulos/03_metodologia.qmd:60` | «Particiones en 3 y 4 clases» (`tbl-etapas`) | `clasesHfcMenor`, `clasesHfcMayor` |
| `_capitulos/03_metodologia.qmd:61` | «Trayectoria PCA-MM12» (`tbl-etapas`) | `ventanaMediaMovil` |
| `_capitulos/03_metodologia.qmd:91` | $\nu=3$ (dos veces) | `nuGauss` |
| `_capitulos/03_metodologia.qmd:102` | $\nu=3$ (título de `tbl-kish`) | `nuGauss` |
| `_capitulos/03_metodologia.qmd:106` | $\mathsf{s}=3$, $\ell_0=2$ | `pasoReglaSeis`, `ejeReglaSeis` |
| `_capitulos/03_metodologia.qmd:117` | «en 3 y en 4 clases» | `clasesHfcMenor`, `clasesHfcMayor` |
| `_capitulos/03_metodologia.qmd:121` | «PCA-MM12» (dos veces), «media móvil causal de 12 meses» | `ventanaMediaMovil` (tres veces) |
| `_capitulos/03_metodologia.qmd:132` | $E^{(95)}_a$ (dos veces), «percentil 95» | `percentilWalkforward` (tres veces) |

Antes de cada párrafo, tabla o definición afectada va un comentario HTML que indica el origen y que
los valores son provisionales (siete comentarios; no se ven en la salida). `tesis/README.md` deja
constancia de las siete claves, de su carácter provisional (no están en `decisiones.qmd`) y de los
casos que se escriben a mano. La fila de `tbl-kish` en la tabla de correspondencias se actualizó.

## Casos dejados sin cambio

- `02_marco_teorico.qmd:272`: el «parámetro igual a 3» de Atoche y Murrieta (2022). Es una cifra de
  una fuente fichada.
- `02_marco_teorico.qmd:222, 310`: «paso 2», «paso 3», «paso 4». Es la numeración de los algoritmos.
- `03_metodologia.qmd:121` (ahora 126): $n_{\min}=12$ meses (D17.1, no es la ventana).
- $d=3$ y «tres ejes» (D9) y las tolerancias $h=3$ y $h=6$ o «3 y 6 meses» (D7):
  `02_marco_teorico.qmd:58, 369, 586`; `03_metodologia.qmd:91, 116, 121, 141, 161`.
- $\nu=0$ (pesos uniformes) en `03_metodologia.qmd:91`: no es el parámetro `nuGauss`.
- «percentil» sin número (Horn): `02_marco_teorico.qmd:166, 339, 691`.
- Capítulos 4 y 5: regla 7. Los capítulos 0 y 1 no contienen ninguno de los parámetros.

## M-03

Resuelto en el informe: `02_marco_teorico.qmd:80` cita `[@fmi_2015b][^v2-fmi]`, y la nota
`[^v2-fmi]` (línea 701) es la marca `VERIFICAR` del DOI (commit `09b9c26`). Es la única cita de la
clave en `tesis/_capitulos/`. `git grep -o VERIFICAR -- tesis/_capitulos` da 52, como el registro.
Esta vuelta no añade ni quita marcas.

## Compilación

- `quarto render tesis/ --to docx` (Quarto 1.10.20) termina con exit 0 antes y después del cambio.
- El texto de los nueve `.docx` (`quarto pandoc -t plain`) es idéntico antes y después: los valores
  mostrados no cambian. No queda ningún `?@`, ningún `{{<` ni ningún `meta cifras` en la salida.
- Las salidas (`_site/`) no se versionan.

## Pendientes

- Los parámetros siguen siendo provisionales mientras Roberto no los registre en `decisiones.qmd`.

## Contradicciones detectadas

Ninguna nueva.
