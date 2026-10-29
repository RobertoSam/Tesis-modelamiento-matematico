# -*- coding: utf-8 -*-
"""Guion del auditor (3b, criterios 5 y 6 con la adenda: p = 16): valores propios por ventana y k*."""
import sys
import numpy as np
import pandas as pd
raiz = sys.argv[1]; sys.path.insert(0, raiz)
from src.datos import cargar_vias
from src import camiz_port as cp
F = f'{raiz}/data/results/final'
for f in ('06c_aede_valores_propios.csv', 'R_aede_valores_propios.csv'):
    v = pd.read_csv(f'{F}/{f}')
    lam = [c for c in v.columns if c.lower().startswith(('lambda', 'l1', 'l2', 'l3', 'λ'))]
    print(f, v.shape, v.columns.tolist()[:14])
v = pd.read_csv(f'{F}/06c_aede_valores_propios.csv')
cols = [c for c in v.columns if c in ('lambda1', 'lambda2', 'lambda3', 'l1', 'l2', 'l3')]
print('columnas λ:', cols)
s = v[cols].sum(axis=1)
print('max λ1+λ2+λ3 =', s.max(), '<= 16:', bool((s <= 16 + 1e-9).all()))
ncol = [c for c in v.columns if 'omega' in c][0]
u = v[v.pesos == 'uniformes']
print('n_omega = nw (uniformes):', bool(np.allclose(u[ncol], u.nw)))
X, _ = cargar_vias(raiz, excluidas=('Liquidez M2',))
print('X', X.shape)
a = cp.aede(X, nw=60, ndim=3, nsd=0, maxcl=10)
e = a['eigenvalues']
g = u[u.nw == 60]
fc = [c for c in v.columns if 'fecha' in c][0]
m = g.set_index(fc)[cols]
print('nw=60 uniformes reproduce aede:', bool(np.allclose(m.to_numpy(), e.loc[m.index].to_numpy(), atol=1e-12)), len(m))
k = pd.read_csv(f'{F}/07b_nulo_estructura_kstar_posicion.csv'); print('kstar_posicion', k.shape, k.columns.tolist())
c = pd.read_csv(f'{F}/06c_aede_cortes.csv'); print('06c_aede_cortes k_en_tope' , 'k_en_tope' in c.columns, c.shape)
