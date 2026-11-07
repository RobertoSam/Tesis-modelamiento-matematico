# Nota del desarrollador · 29-oct-2026 · Iteración 3b, vuelta 1 de auditoría

Responde al hallazgo **M-02** de `auditorias/2026-10-29_iteracion-3b.md`. N-01, N-03 y N-04 no se
tratan en esta vuelta (N-04 requiere una decisión de Roberto).

## Archivos modificados

- `herramientas/cifras_mapa.csv`: 32 macros repuntadas de `data/results/niveles/` a
  `data/results/final/`; 14 filas eliminadas (transformadas, sin equivalente vigente). El mapa pasa
  de 78 a 64 macros.
- `herramientas/generar_cifras.py`: `CARPETAS_ADMITIDAS` pasa de `data/results/` a
  `data/results/final/` (más `data/referencia/`), de modo que el script rechaza cualquier ruta del
  antecedente (recomendación opcional del auditor); se actualizan el docstring y la cabecera del
  `.tex`.
- `tesis_latex/cifras.tex` y `tesis/_cifras.yml`: regenerados.

No se re-ejecutó ningún notebook ni el Rmd, y no se tocó `data/results/`.

Comandos:

```
python3 herramientas/generar_cifras.py
python3 herramientas/generar_cifras.py --comprobar
```

Resultado: 64 cifras escritas; `--comprobar` termina con exit 0.

## Macros repuntadas (32) y valores antes → después

Origen nuevo: el mismo nombre de archivo, filtro y columna, pero en `data/results/final/`.

| Macro | Antes (17 series) | Después (16 series, vigente) | CSV vigente |
|---|---|---|---|
| `inerciaPCUnoNiveles` | 67,2 | 65,2 | `final/05_pca_valores_propios.csv`, componente=1, `inercia` |
| `inerciaPCDosNiveles` | 18,3 | 19,4 | ídem, componente=2 |
| `inerciaPCTresNiveles` | 7,1 | 7,6 | ídem, componente=3 |
| `inerciaPCCuatroNiveles` | 2,9 | 3,1 | ídem, componente=4 |
| `kmoGlobalNiveles` | 0,86 | 0,84 | `final/05_adecuacion.csv`, medida=kmo_global, `valor` |
| `chiBartlettNiveles` | 12 210 | 10 492 | ídem, medida=bartlett_chi2_n |
| `glBartlett` | 136 | 120 | ídem, medida=bartlett_gl (16·15/2) |
| `pBartlettNefNiveles` | 0,06 | 0,01 | ídem, medida=bartlett_p_nef |
| `numCondicionNiveles` | 67 647 | 10 968 | ídem, medida=num_condicion |
| `nEfMedianaNiveles` | 10,4 | 10,6 | `final/05_n_efectivo_resumen.csv`, version=original, `n_ef_mediana` |
| `nSeriesDS` | 13 | 12 | `final/05_clasificacion_d5_resumen.csv`, conjunto=series_niveles, `DS` |
| `nuloConDerivaPCUno` | 0,902 | 0,910 | `final/05_nulo_tendencias.csv`, con_deriva/inercia_pc1, `proporcion` |
| `nuloConDerivaPCDos` | 0,015 | 0,014 | ídem, con_deriva/inercia_pc2 |
| `nuloSinDerivaPCUno` | 0,004 | 0,008 | ídem, sin_deriva/inercia_pc1 |
| `nuloSinDerivaPCDos` | 0,592 | 0,474 | ídem, sin_deriva/inercia_pc2 |
| `nuloSinTendenciaPCUno` | 0,124 | 0,208 | ídem, sin_tendencia/inercia_pc1 |
| `nuloSinTendenciaPCDos` | 0,595 | 0,489 | ídem, sin_tendencia/inercia_pc2 |
| `nuloConDerivaMedianaPCUno` | 74,6 | 73,3 | ídem, con_deriva/inercia_pc1, `p50` |
| `inerciaPCUnoSinTendencia` | 40,0 | 38,5 | `final/05_pca_contraste_tendencia.csv`, niveles_sin_tendencia/inercia/1 |
| `kmoSinTendencia` | 0,70 | 0,68 | ídem, niveles_sin_tendencia/kmo |
| `congruenciaBootPCDosNiveles` | 0,793 | 0,786 | `final/05_bootstrap_congruencia.csv`, L=24, componente=2, `p5` |
| `congruenciaBootPCCuatroNiveles` | 0,608 | 0,604 | ídem, componente=4 |

Sin cambio de valor (repuntadas igualmente): `hornNiveles` (2), `kaiserNiveles` (3),
`chiBartlettNefNiveles` (162), `rTiempoPCUnoNiveles` (0,993), `claseDCincoPC{Uno,Dos,Tres,Cuatro}Niveles`
(DS), `nSeriesTS` (1) y `nSeriesIndeterminadas` (3). Con esto, TS + DS + indeterminadas = 1 + 12 + 3
= 16 = `\nSeries`.

Interpretación (una línea): el paso de 17 a 16 series (D16, sin la Liquidez M2) baja la inercia de PC1
en dos puntos y la traslada a PC2 y PC3; la lectura cualitativa (PC1 tendencial DS, PC2 por encima
del nulo con deriva) se mantiene.

Dudas abiertas para Roberto:

- `pBartlettNefNiveles` pasa de 0,06 a 0,01: con 16 series, Bartlett con la mediana de $n_{ef}$ ya
  rechaza al 5 %. Si el capítulo 4 llega a argumentar sobre esa prueba, la conclusión cambia respecto
  del antecedente.
- `nuloSinDerivaPCDos` y `nuloSinTendenciaPCDos` bajan unas 0,1; conviene revisar si la lectura de PC2
  frente a esos nulos sigue siendo «no distinguible».

## Macros sin equivalente vigente (14, eliminadas del mapa)

Leían la vía transformada del antecedente (`data/results/05_*.csv`). Por D15, la vía transformada
pasó a anexo de robustez, y `data/results/final/anexo/` solo contiene 05c y 09b: el notebook 05 con
16 series no produce PCA, adecuación, $n_{ef}$ ni clasificación D5 de la vía transformada. No se
inventaron valores ni se re-ejecutó nada.

`inerciaPC{Uno,Dos,Tres,Cuatro}Transformadas`, `hornTransformadas`, `kaiserTransformadas`,
`kmoGlobalTransformadas`, `chiBartlettTransformadas`, `nEfMedianaTransformadas`,
`numCondicionTransformadas` y `claseDCincoPC{Uno,Dos,Tres,Cuatro}Transformadas`.

Propuesta (no ejecutada): si el anexo de robustez necesita estas cifras, añadir al 05 una salida
`final/anexo/05_*` para la vía transformada con 16 series y volver a mapearlas.

## Uso en capítulos

Búsqueda de los 46 nombres en todo el repositorio, sin contar `.git`, `cifras.tex`, `_cifras.yml`,
el mapa y el dictamen: ninguna coincidencia en `tesis_latex/capitulos/`, `tesis/_capitulos/`, el
Rmd ni los notebooks. Solo `herramientas/README.md:33` cita `inerciaPCUnoNiveles` como ejemplo de
nombre, y la referencia sigue siendo válida. Por eso no hay texto que corregir, y la eliminación de las
14 macros no rompe la compilación.

## Desviaciones respecto de `decisiones.qmd`

Ninguna. Las restricciones aplicadas son las de D15, D16 y `data/results/LEEME.md`.
