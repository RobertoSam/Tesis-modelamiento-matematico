"""Prueba de no regresión del notebook 05 con parámetros (adenda 3b, §3; sustituye al criterio 3).

Ejecuta `notebooks/05_pca.ipynb` con las 17 series y las dos vías del antecedente
(`TESIS_VIA=ambas`, `TESIS_EXCLUIDAS=[]`), con salidas en una carpeta temporal y leyendo los
índices y los CSV R_* del antecedente (`data/results/niveles/` y `data/results/`). Comprueba que:

- todo CSV `05_*` que ya existía en el antecedente se reproduce **byte a byte**;
- las únicas excepciones son las ampliaciones declaradas: filas nuevas del nulo mixto (D8) al final
  de `05_nulo_tendencias.csv` y `05_nulo_simulaciones.csv`, y columnas nuevas de la deriva HAC al
  final de `05_tendencia_series.csv`; en ellas, las filas o columnas antiguas son idénticas;
- `05_pca_valores_propios.csv` (archivo que nombra la adenda) es idéntico en las dos vías.

El notebook versionado no se modifica (se ejecuta con --output en la carpeta temporal).
Uso, desde la raíz: python3 herramientas/no_regresion_05.py
"""

import filecmp
import os
import subprocess
import sys
import tempfile

import pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AMPLIADOS_FILAS = {'05_nulo_tendencias.csv', '05_nulo_simulaciones.csv'}
AMPLIADOS_COLUMNAS = {'05_tendencia_series.csv'}


def main():
    tmp = tempfile.mkdtemp(prefix='no_regresion_05_')
    salida = os.path.join(tmp, 'resultados')
    env = dict(os.environ, TESIS_VIA='ambas', TESIS_EXCLUIDAS='[]', TESIS_CARPETA=salida,
               TESIS_R_NIVELES=os.path.join(RAIZ, 'data/results/niveles'),
               TESIS_R_TRANSFORMADAS=os.path.join(RAIZ, 'data/results'))
    subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute',
                    '--ExecutePreprocessor.kernel_name=python3', '--ExecutePreprocessor.timeout=1800',
                    '--output-dir', tmp, '--output', '05_no_regresion.ipynb',
                    os.path.join(RAIZ, 'notebooks/05_pca.ipynb')], check=True, env=env, cwd=RAIZ)
    pares = [(os.path.join(salida, '05_dimensiones.csv'), os.path.join(RAIZ, 'data/results/05_dimensiones.csv'))]
    for sub, ref in [('', 'data/results/niveles'), ('anexo', 'data/results')]:
        for f in sorted(os.listdir(os.path.join(RAIZ, ref))):
            if f.startswith('05_') and f.endswith('.csv') and f != '05_dimensiones.csv':
                pares.append((os.path.join(salida, sub, f), os.path.join(RAIZ, ref, f)))
    fallos = []
    for nuevo, viejo in pares:
        nombre = os.path.basename(viejo)
        if not os.path.exists(nuevo):
            if nombre.startswith(('05b_',)):
                continue
            fallos.append(f'falta {nuevo}')
            continue
        if filecmp.cmp(nuevo, viejo, shallow=False):
            print(f'idéntico   {os.path.relpath(viejo, RAIZ)}')
        elif nombre in AMPLIADOS_FILAS:
            a, b = open(nuevo).read().splitlines(), open(viejo).read().splitlines()
            ok = a[:len(b)] == b and {l.split(',')[0] for l in a[len(b):]} <= {'mixto_ind_ts', 'mixto_ind_ds'}
            print(f'{"ampliado " if ok else "DISTINTO "} {os.path.relpath(viejo, RAIZ)} (filas antiguas idénticas: {a[:len(b)] == b})')
            if not ok:
                fallos.append(nombre)
        elif nombre in AMPLIADOS_COLUMNAS:
            a, b = pd.read_csv(nuevo, dtype=str), pd.read_csv(viejo, dtype=str)
            ok = list(a.columns[:len(b.columns)]) == list(b.columns) and a[b.columns].equals(b)
            print(f'{"ampliado " if ok else "DISTINTO "} {os.path.relpath(viejo, RAIZ)} (columnas antiguas idénticas: {ok})')
            if not ok:
                fallos.append(nombre)
        else:
            print(f'DISTINTO   {os.path.relpath(viejo, RAIZ)}')
            fallos.append(nombre)
    if fallos:
        print('FALLA la no regresión:', fallos)
        sys.exit(1)
    print(f'No regresión del 05 superada ({len(pares)} archivos). Carpeta temporal: {tmp}')


if __name__ == '__main__':
    main()
