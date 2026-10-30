# herramientas/

Scripts compartidos por la tesis (`tesis_latex/`) y el informe (`tesis/`).

## `generar_cifras.py` · cifras desde `data/results/` y `data/referencia/`

Regla 3 de `CLAUDE.md`: ninguna cifra se escribe a mano. Este script lee las cifras de los CSV de
`data/results/` (y, para las fechas de los episodios de D7, de `data/referencia/`) según el mapa
versionado `cifras_mapa.csv` y escribe:

| Salida | Uso |
|---|---|
| `tesis_latex/cifras.tex` | `\newcommand{\macro}{valor}`; la tesis lo carga con `\input{cifras}` |
| `tesis/_cifras.yml` | clave `cifras:` con un valor por macro, para Quarto |

Uso, desde la raíz del repositorio:

```
python3 herramientas/generar_cifras.py
python3 herramientas/generar_cifras.py --comprobar
```

`--comprobar` no escribe y termina con código 1 si alguna salida no está al día con los CSV. El
script es idempotente: no escribe marcas de tiempo, de modo que dos ejecuciones sobre los mismos
CSV dan archivos idénticos byte a byte. Solo crea esos dos archivos; no toca el resto de
`tesis_latex/` ni de `tesis/`.

### El mapa `cifras_mapa.csv`

Una fila por cifra, con las columnas `macro, archivo, filtro, columna, formato, descripcion`:

- `macro`: nombre de la macro, solo letras (los nombres de macro de LaTeX no admiten dígitos; por
  eso `inerciaPCUnoNiveles` y no `inerciaPC1Niveles`). El mismo nombre es la clave en el YAML.
- `archivo`: CSV dentro de `data/results/` o de `data/referencia/` (el script rechaza cualquier otra
  carpeta). Desde D15 y D16, las cifras vigentes salen de `data/results/final/`; las carpetas del
  antecedente con 17 series no deben consumirse (`data/results/LEEME.md`).
- `filtro`: condiciones `columna=valor` separadas por `;`, que deben seleccionar **exactamente una
  fila**; la comparación es de texto, con el valor tal como está escrito en el CSV (p. ej.
  `ambito=global;medida=kmo_global` o `L=24;componente=2`).
- `columna`: columna del CSV que contiene el valor.
- `formato`:
  - `entero` (redondeado; con espacio fino de miles desde 1 000: `12\,210` en LaTeX);
  - `decimal:N` (N decimales con coma decimal: `67{,}2` en LaTeX y `67,2` en el YAML; las llaves
    evitan el espacio que LaTeX agrega tras una coma en modo matemático);
  - `texto` (sin caracteres especiales de LaTeX);
  - `fecha_mes` (`2007-01` → «enero de 2007»);
  - `anio` (`2007-01` → «2007»).
- `descripcion`: se copia como comentario junto a cada macro, con el archivo, el filtro y la
  columna de origen.

Si una fila del mapa remite a un archivo, una columna o un filtro que no existen, o si el filtro no
selecciona una sola fila, el script se detiene con un mensaje y no escribe nada.

### Uso en Quarto (informe MMC102)

El archivo `tesis/_cifras.yml` contiene:

```yaml
cifras:
  nMesesNiveles: "228"
```

Para usarlo en un capítulo, se declara como archivo de metadatos (en `tesis/_metadata.yml` o en el
YAML del documento) y se cita con el *shortcode* `meta`:

```yaml
metadata-files:
  - _cifras.yml
```

```markdown
La vía en niveles tiene {{< meta cifras.nMesesNiveles >}} meses.
```

La integración en `tesis/` la hace el editor del informe.

### Cifras que el mapa define hoy (iteración 3a)

- Contrato con el redactor LaTeX (desde `05_dimensiones.csv`): `\nMesesNiveles`,
  `\nMesesTransformadas`, `\nSeries`, `\fechaInicioNiveles`, `\fechaInicioTransformadas`,
  `\fechaFinDatos`, y además `\anioInicioDatos` y `\anioFinDatos`, pedidas en la nota del redactor.
- Resultados del notebook 05 (PCA estático mensual, apuntes 1, 3, 4, 5, 10 y 11): inercias, Horn,
  Kaiser, KMO, Bartlett, $n_{\text{ef}}$, número de condición, clase D5 de cada componente, conteos
  D5 de las series, proporciones del nulo de tendencias, contraste sin tendencia y congruencias
  bootstrap. **Regla 7:** estas macros existen para que las cifras tengan origen trazable; el
  capítulo de resultados no se publica sin la aprobación de Roberto.

## `exportar_parametros_diseno.py` · parámetros de diseño provisionales (auditoría 3b, N-03)

Escribe `data/results/final/parametros_diseno.csv` con los seis parámetros de diseño que
`decisiones.qmd` no recoge (ν = `nsd` de los pesos gaussianos, paso y eje de la regla del 06,
ventana de la media móvil de PCA-MM12, particiones de la HFC y percentil de la razón
*walk-forward*). No fija valores: cada uno se lee del código vigente en Python (notebooks o `src/`)
y se contrasta con `R/ciclo_financiero_final.Rmd`; si el patrón no aparece una sola vez o Python y R
difieren, se detiene sin escribir. Las macros correspondientes están en `cifras_mapa.csv`.

```
python3 herramientas/exportar_parametros_diseno.py
python3 herramientas/exportar_parametros_diseno.py --comprobar
```

Si se cambia uno de esos parámetros en el código, hay que volver a exportar y luego ejecutar
`generar_cifras.py`.
