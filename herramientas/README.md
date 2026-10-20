# herramientas/

Scripts compartidos por la tesis (`tesis_latex/`) y el informe (`tesis/`).

## `generar_cifras.py` · cifras desde `data/results/`

Regla 3 de `CLAUDE.md`: ninguna cifra se escribe a mano. Este script lee las cifras de los CSV de
`data/results/` según el mapa versionado `cifras_mapa.csv` y escribe:

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
- `archivo`: CSV dentro de `data/results/` (el script rechaza cualquier otra carpeta).
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
