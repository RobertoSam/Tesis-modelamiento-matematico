#!/usr/bin/env python3
"""
Exporta los parámetros de diseño provisionales a `data/results/final/parametros_diseno.csv`
(hallazgo N-03 de la auditoría de la iteración 3b).

Son seis parámetros fijados en el plan aprobado de la iteración 3b o en el código anterior a ella,
que `decisiones.qmd` no recoge (clase «Parámetros de diseño del plan (provisional)» de
`tesis_latex/README.md`):

1. ν = 3: desviaciones estándar de los pesos gaussianos de `aede` (`nsd`);
2. paso de 3 meses de la regla del notebook 06;
3. eje 2 (PC2) que sigue la regla del 06 en la vía sin transformar;
4. media móvil causal de 12 meses de la datación PCA-MM12;
5. particiones de la HFC en 3 y 4 clases (dos filas: menor y mayor);
6. percentil 95 del error de entrenamiento que normaliza la razón de error *walk-forward*.

**Este script no fija ningún valor.** Cada valor se lee, con una expresión regular, del código que
lo usa en la cadena vigente de Python (notebooks y `src/`) y se contrasta con el mismo parámetro en
el Rmd final (`R/ciclo_financiero_final.Rmd`). Si el patrón no aparece exactamente una vez, o si
Python y R no coinciden, el script se detiene sin escribir. Así, el CSV refleja lo que el código
ejecuta, y cualquier cambio futuro de un parámetro en el código obliga a volver a exportarlo
(`--comprobar` lo detecta).

Es idempotente: sin marcas de tiempo; dos ejecuciones sobre el mismo código dan el mismo archivo.

Uso (desde cualquier carpeta):

    python3 herramientas/exportar_parametros_diseno.py
    python3 herramientas/exportar_parametros_diseno.py --comprobar
"""

import argparse
import csv
import io
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, 'data', 'results', 'final', 'parametros_diseno.csv')
RMD = 'R/ciclo_financiero_final.Rmd'

# Fuente documental común: ninguno de estos valores está en decisiones.qmd (por eso son provisionales)
ESTADO = 'provisional: fijado en el plan 3b o en el código previo; no figura en decisiones.qmd'

# Cada parámetro: (clave, símbolo, descripción, unidad,
#                  (archivo Python, patrón), (archivo R, patrón), fuente documental)
# El patrón tiene un único grupo con el valor; debe aparecer exactamente una vez en el archivo.
PARAMETROS = [
    ('nu_pesos_gaussianos', 'ν (nsd)',
     'Desviaciones estándar de los pesos gaussianos de aede', 'desviaciones estándar',
     ('notebooks/06c_aede_grilla.ipynb', r"PESOS = \{'uniformes': 0, 'gaussianos_nsd3': (\d+)\}"),
     (RMD, r'pesos_grilla <- c\(uniformes = 0, gaussianos_nsd3 = (\d+)\)'),
     'plan de la iteración 3b (asesoria/2026-10-21_plan-iteracion-3b.md, tarea D4 del desarrollador: pesos gaussianos con nsd = 3)'),
    ('paso_regla06', 'paso',
     'Paso entre ventanas consecutivas de la regla del notebook 06', 'meses',
     ('notebooks/06_epca.ipynb', r'^PASO = (\d+)$'),
     (RMD, r'^PASO <- (\d+) +#'),
     'código previo a la iteración 3b (notebook 06, EPCA de la iteración 2)'),
    ('eje_regla06_niveles', 'eje',
     'Eje que sigue la regla del 06 en la vía sin transformar (PC2; índice Python 1 + 1)', 'número de eje',
     ('notebooks/06_epca.ipynb', r"corridas06 = \[\('niveles', df_niveles, (\d+), transiciones_n\)\]"),
     (RMD, r'^r06 <- regla06_grilla\(X, fechas, (\d+)\)$'),
     'código previo a la iteración 3b (notebook 06, sección 4.3: PC2 en niveles)'),
    ('ventana_media_movil', 'L_MM',
     'Ventana de la media móvil causal de la datación PCA-MM12', 'meses',
     ('notebooks/09a_datacion_pca.ipynb', r'^L_MM = (\d+) +#'),
     (RMD, r'^L_mm <- (\d+)$'),
     'plan de la iteración 3b (asesoria/2026-10-21_plan-iteracion-3b.md, tareas D3 y D12: datación PCA-MM12 en el 09a); antes, notebook 09'),
    ('clases_hfc_menor', 'K',
     'Partición menor de la HFC (número de clases)', 'clases',
     ('notebooks/07c_hfc_clases.ipynb', r'for ncl in \((\d+), \d+\):'),
     (RMD, r'^for \(ncl in (\d+):\d+\) \{$'),
     'plan de la iteración 3b (asesoria/2026-10-21_plan-iteracion-3b.md, tarea D8: partición en 3 y 4 clases)'),
    ('clases_hfc_mayor', 'K',
     'Partición mayor de la HFC (número de clases)', 'clases',
     ('notebooks/07c_hfc_clases.ipynb', r'for ncl in \(\d+, (\d+)\):'),
     (RMD, r'^for \(ncl in \d+:(\d+)\) \{$'),
     'plan de la iteración 3b (asesoria/2026-10-21_plan-iteracion-3b.md, tarea D8: partición en 3 y 4 clases)'),
    ('percentil_walkforward', 'q',
     'Percentil del error de entrenamiento que normaliza la razón de error walk-forward', 'percentil',
     ('src/deteccion.py', r'ref = np\.percentile\(np\.mean\(\(E - rec\(E\)\) \*\* 2, axis=1\), (\d+)\)'),
     (RMD, r'ref <- unname\(quantile\(rowMeans\(\(E - rec\(E\)\)\^2\), 0\.(\d+)\)\)'),
     'código previo a la iteración 3b (notebook 09, razón respecto del percentil 95)'),
]


def texto_fuente(ruta):
    """Devuelve el texto del archivo; de un notebook, solo el código de sus celdas (sin salidas)."""
    with open(os.path.join(RAIZ, ruta), encoding='utf-8') as f:
        if ruta.endswith('.ipynb'):
            nb = json.load(f)
            return '\n'.join(''.join(c['source']) for c in nb['cells'] if c['cell_type'] == 'code')
        return f.read()


def extraer(ruta, patron, clave):
    """Lee el valor del grupo del patrón, que debe aparecer exactamente una vez."""
    hallados = re.findall(patron, texto_fuente(ruta), flags=re.MULTILINE)
    if len(hallados) != 1:
        raise SystemExit(f'ERROR: {clave}: el patrón aparece {len(hallados)} veces en {ruta} (debe ser 1)')
    return int(hallados[0])


def construir():
    filas = []
    for clave, simbolo, desc, unidad, (f_py, p_py), (f_r, p_r), fuente in PARAMETROS:
        v_py = extraer(f_py, p_py, clave)
        v_r = extraer(f_r, p_r, clave)
        if clave == 'eje_regla06_niveles':
            v_py += 1                       # Python indexa los ejes desde 0; R y el texto, desde 1
        if v_py != v_r:
            raise SystemExit(f'ERROR: {clave}: Python ({f_py}) da {v_py} y R ({f_r}) da {v_r}')
        filas.append({'parametro': clave, 'simbolo': simbolo, 'valor': v_py, 'unidad': unidad,
                      'descripcion': desc, 'codigo_python': f_py, 'codigo_r': f_r,
                      'fuente': fuente, 'estado': ESTADO})
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(filas[0].keys()), lineterminator='\n')
    w.writeheader()
    w.writerows(filas)
    return buf.getvalue()


def main():
    ap = argparse.ArgumentParser(description='Exporta los parámetros de diseño provisionales (N-03).')
    ap.add_argument('--comprobar', action='store_true', help='no escribe; falla si el CSV no está al día')
    args = ap.parse_args()
    contenido = construir()
    actual = open(SALIDA, encoding='utf-8').read() if os.path.exists(SALIDA) else None
    if args.comprobar:
        if actual != contenido:
            print(f'NO ESTÁ AL DÍA: {os.path.relpath(SALIDA, RAIZ)}', file=sys.stderr)
            return 1
        print('parametros_diseno.csv al día')
        return 0
    with open(SALIDA, 'w', encoding='utf-8', newline='') as f:
        f.write(contenido)
    print(f'Escrito {os.path.relpath(SALIDA, RAIZ)} ({len(PARAMETROS)} filas)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
