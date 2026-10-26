"""Prueba de no regresión de la parte dinámica con parámetros (adenda 3b, §3; sustituye al criterio 3).

Con las 17 series y las dos vías del antecedente (`TESIS_VIA=ambas`, `TESIS_EXCLUIDAS=[]`), en
carpetas temporales y leyendo los índices y los CSV R_* del antecedente (`data/results/niveles/` y
`data/results/`), comprueba que el código parametrizado reproduce el antecedente:

1. **Notebooks 06, 06c, 07c y 09a** (Python): todo CSV que ya existía en el antecedente se reproduce
   **byte a byte**, salvo las ampliaciones declaradas, en las que las columnas antiguas son idénticas:
   - `09a_datacion_criterios.csv`: columnas nuevas de D17.1 (`n_segmentos_en_minimo`,
     `segmentos_en_minimo`) al final;
   - `09a_regimenes_pca.csv`: columna `episodios_contenidos` al final (D9; el antecedente no la
     tenía en el 09a).
2. **Rmd final** con `excluidas = character(0)` (solo vía en niveles): `R_aede_cortes.csv`,
   `R_hfc_clases3.csv` y los demás R_* de las secciones 4 a 6 que existían en `data/results/niveles/`
   se reproducen byte a byte (con la misma excepción de columnas nuevas en `R_datacion_criterios.csv`).
3. **Nulo de estructura** (por su costo, solo la serie observada en Python y las réplicas 0 a 2 en R):
   con el RV del antecedente (cargas centradas, `TESIS_RV=antecedente`), el guion R y
   `src/nulo_estructura.medir` reproducen los k* exactos y los perfiles RV del antecedente con
   tolerancia 1e-14 (no byte a byte: la adenda no lo exige para estos archivos).

`05_pca_valores_propios.csv` lo cubre `herramientas/no_regresion_05.py`. Los notebooks y el Rmd
versionados no se modifican (se ejecutan con --output y output_dir en la carpeta temporal).
Uso, desde la raíz: python3 herramientas/no_regresion_dinamica.py
"""

import filecmp
import os
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
ANT_N = os.path.join(RAIZ, 'data/results/niveles')
ANT_T = os.path.join(RAIZ, 'data/results')
AMPLIADOS_COLUMNAS = {'09a_datacion_criterios.csv', '09a_regimenes_pca.csv', 'R_datacion_criterios.csv'}
NOTEBOOKS = ['06_epca', '06c_aede_grilla', '07c_hfc_clases', '09a_datacion_pca']
fallos = []


def comparar(nuevo, viejo):
    nombre = os.path.basename(viejo)
    rel = os.path.relpath(viejo, RAIZ)
    if not os.path.exists(nuevo):
        fallos.append(f'falta {nuevo}')
        print(f'FALTA      {rel}')
        return
    if filecmp.cmp(nuevo, viejo, shallow=False):
        print(f'idéntico   {rel}')
    elif nombre in AMPLIADOS_COLUMNAS:
        a, b = pd.read_csv(nuevo, dtype=str, keep_default_na=False), pd.read_csv(viejo, dtype=str, keep_default_na=False)
        ok = list(a.columns[:len(b.columns)]) == list(b.columns) and a[b.columns].equals(b)
        print(f'{"ampliado " if ok else "DISTINTO "} {rel} (columnas antiguas idénticas: {ok}; nuevas: {list(a.columns[len(b.columns):])})')
        if not ok:
            fallos.append(nombre)
    else:
        print(f'DISTINTO   {rel}')
        fallos.append(nombre)


def notebooks(tmp):
    salida = os.path.join(tmp, 'py')
    env = dict(os.environ, TESIS_VIA='ambas', TESIS_EXCLUIDAS='[]', TESIS_CARPETA=salida,
               TESIS_R_NIVELES=ANT_N, TESIS_R_TRANSFORMADAS=ANT_T)
    for nb in NOTEBOOKS:
        subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute',
                        '--ExecutePreprocessor.kernel_name=python3', '--ExecutePreprocessor.timeout=3600',
                        '--output-dir', tmp, '--output', f'{nb}_no_regresion.ipynb',
                        os.path.join(RAIZ, 'notebooks', f'{nb}.ipynb')], check=True, env=env, cwd=RAIZ,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    pares = []
    # Notebook 06: los archivos del antecedente están en data/results/ (los de niveles con sufijo)
    for f in sorted(os.listdir(ANT_T)):
        if f.startswith('06_epca_') and f.endswith('.csv'):
            sub = '' if f.endswith('_niveles.csv') else 'anexo'
            pares.append((os.path.join(salida, sub, f), os.path.join(ANT_T, f)))
    for prefijo in ('06c_', '07c_', '09a_'):
        for sub, ref in [('', ANT_N), ('anexo', ANT_T)]:
            for f in sorted(os.listdir(ref)):
                if f.startswith(prefijo) and f.endswith('.csv'):
                    pares.append((os.path.join(salida, sub, f), os.path.join(ref, f)))
    print(f'--- Notebooks {", ".join(NOTEBOOKS)} ({len(pares)} archivos del antecedente)')
    for nuevo, viejo in pares:
        comparar(nuevo, viejo)


def rmd(tmp):
    salida = os.path.join(tmp, 'rmd')
    os.makedirs(salida, exist_ok=True)
    expr = (f"rmarkdown::render('R/ciclo_financiero_final.Rmd', output_dir = '{tmp}', quiet = TRUE, "
            f"params = list(excluidas = character(0), carpeta = '{salida}'))")
    subprocess.run(['Rscript', '-e', expr], check=True, cwd=RAIZ, stdout=subprocess.DEVNULL)
    nuevos = sorted(f for f in os.listdir(salida) if f.startswith(('R_aede_', 'R_hfc_', 'R_epca_regla06_',
                                                                    'R_estabilidad_cortes', 'R_datacion_criterios')))
    pares = [(os.path.join(salida, f), os.path.join(ANT_N, f)) for f in nuevos if os.path.exists(os.path.join(ANT_N, f))]
    print(f'--- Rmd final con 17 series ({len(pares)} archivos R_* del antecedente en niveles)')
    for nombre in ('R_aede_cortes.csv', 'R_hfc_clases3.csv'):
        assert any(os.path.basename(v) == nombre for _, v in pares), nombre
    for nuevo, viejo in pares:
        comparar(nuevo, viejo)


def nulo(tmp):
    from src import nulo_estructura as ne
    from src.datos import cargar_vias
    print('--- Nulo de estructura (RV del antecedente: serie observada en Python, réplicas 0 a 2 en R)')
    X, Xt = cargar_vias(RAIZ, excluidas=())
    for via, M, ref in [('niveles', X, ANT_N), ('transformadas', Xt, ANT_T)]:
        k0, rv0, _ = ne.medir(M, objetos_rv=ne.OBJETOS_ANTECEDENTE)
        rk = pd.read_csv(os.path.join(ref, '07b_nulo_estructura_kstar.csv'))
        rk = rk[rk.replica == 0].set_index(['nw', 'pesos', 'criterio']).k
        ok_k = (k0.set_index(['nw', 'pesos', 'criterio']).k.sort_index() == rk.sort_index()).all()
        rr = pd.read_csv(os.path.join(ref, '07b_nulo_estructura_rv.csv'))
        rr = rr[rr.replica == 0].reset_index(drop=True)
        dif = float(np.max(np.abs(rv0.rv.to_numpy() - rr.rv.to_numpy())))
        ok_rv = len(rr) == len(rv0) and (rv0.fecha_a.to_numpy() == rr.fecha_a.to_numpy()).all() and dif < 1e-14
        print(f'{"idéntico " if ok_k and ok_rv else "DISTINTO "}  Python {via}: k* de la réplica 0 y perfil RV centrado (dif. máx. {dif:.1e})')
        if not (ok_k and ok_rv):
            fallos.append(f'07b {via}')
    salida = os.path.join(tmp, 'nulo_r')
    env = dict(os.environ, TESIS_VIA='ambas', TESIS_EXCLUIDAS='[]', TESIS_CARPETA=salida, TESIS_RV='antecedente')
    subprocess.run(['Rscript', 'R/07b_nulo_estructura.R', '2'], check=True, cwd=RAIZ, env=env, stdout=subprocess.DEVNULL)
    for sub, ref in [('', ANT_N), ('anexo', ANT_T)]:
        nk = pd.read_csv(os.path.join(salida, sub, 'R_nulo_estructura_kstar.csv'))
        vk = pd.read_csv(os.path.join(ref, 'R_nulo_estructura_kstar.csv'))
        clave = ['L', 'replica', 'nw', 'pesos', 'criterio']
        m = nk.merge(vk, on=clave, suffixes=('', '_v'))
        ok_k = len(m) == len(nk) and (m.k == m.k_v).all()
        nr = pd.read_csv(os.path.join(salida, sub, 'R_nulo_estructura_rv.csv'))
        vr = pd.read_csv(os.path.join(ref, 'R_nulo_estructura_rv.csv'))
        m = nr.merge(vr, on=['replica', 'nw', 'pesos', 'fecha_a', 'fecha_b'], suffixes=('', '_v'))
        dif = float(np.max(np.abs(m.rv - m.rv_v)))
        ok_rv = len(m) == len(nr) and dif < 1e-14
        print(f'{"idéntico " if ok_k and ok_rv else "DISTINTO "}  R {sub or "niveles"}: k* y perfil RV de las réplicas 0 a 2 '
              f'({len(nk)} k*, {len(m)} pares; dif. máx. {dif:.1e})')
        if not (ok_k and ok_rv):
            fallos.append(f'R 07b {sub or "niveles"}')


def main():
    tmp = tempfile.mkdtemp(prefix='no_regresion_dinamica_')
    notebooks(tmp)
    rmd(tmp)
    nulo(tmp)
    if fallos:
        print('FALLA la no regresión:', fallos)
        sys.exit(1)
    print(f'No regresión de la parte dinámica superada. Carpeta temporal: {tmp}')


if __name__ == '__main__':
    main()
