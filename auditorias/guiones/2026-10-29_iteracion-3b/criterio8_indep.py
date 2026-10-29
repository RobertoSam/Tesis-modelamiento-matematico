# -*- coding: utf-8 -*-
"""Guion del auditor (3b, criterio 8): recálculo independiente de 09_discriminacion_episodios.csv
con las fechas antiguas (Rmd y modelos_dl.py de 3a) a partir de 09_walkforward_errores.csv, sin src/."""
import sys
import numpy as np
import pandas as pd
raiz = sys.argv[1]
antiguas = {'Crisis financiera global': ('2008-09-01', '2009-06-01'), 'Taper tantrum': ('2013-05-01', '2013-12-01'),
            'COVID-19': ('2020-03-01', '2020-12-01')}
ok = True
for sub in ('', 'niveles/'):
    wf = pd.read_csv(f'{raiz}/data/results/{sub}09_walkforward_errores.csv', parse_dates=['fecha']).set_index('fecha')
    ref = pd.read_csv(f'{raiz}/data/results/{sub}09_discriminacion_episodios.csv').set_index('metodo')
    dentro = pd.Series('', index=wf.index)
    for nom, (a, b) in antiguas.items():
        dentro[(wf.index >= a) & (wf.index <= b)] = nom
    for m in ('pca', 'ae', 'lstm'):
        fuera = wf.loc[dentro == '', m]
        calc = {'mediana_fuera_de_episodios': fuera.median(), 'falsas_alarmas_%': 100 * (fuera > 1).mean()}
        for nom in [n for n in antiguas if (dentro == n).any()]:
            v = wf.loc[dentro == nom, m]
            calc[f'mediana_{nom}'] = v.median(); calc[f'sensibilidad_{nom}_%'] = 100 * (v > 1).mean()
        for k, v in calc.items():
            if abs(round(v, 2) - ref.loc[m, k]) > 1e-9:
                ok = False; print('DIFIERE', sub, m, k, round(v, 2), ref.loc[m, k])
    print(sub or 'transformadas', 'columnas', list(ref.columns) == list(calc.keys()))
print('criterio 8 reproducido:', ok)
