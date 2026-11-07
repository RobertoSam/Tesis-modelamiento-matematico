# -*- coding: utf-8 -*-
"""Guion del auditor (3b): comparación propia Python–R de los CSV de data/results/final, sin usar
R_paridad_python.csv. Columnas comunes; numéricas con tolerancia 1e-10, texto/booleanos exactos."""
import sys
import numpy as np
import pandas as pd
F = sys.argv[1] + '/data/results/final'
pares = [("06c_aede_cortes", "R_aede_cortes"), ("06c_aede_cruces", "R_aede_cruces"),
         ("06c_aede_valores_propios", "R_aede_valores_propios"),
         ("06c_aede_valores_propios_resumen", "R_aede_valores_propios_resumen"),
         ("07c_hfc_clases3", "R_hfc_clases3"), ("07c_hfc_bootstrap", "R_hfc_bootstrap"),
         ("07c_hfc_coclasificacion", "R_hfc_coclasificacion"), ("07c_hfc_correlaciones3", "R_hfc_correlaciones3"),
         ("09a_datacion_criterios", "R_datacion_criterios"), ("09a_datacion_dimension", "R_datacion_dimension"),
         ("09a_estabilidad_cortes", "R_estabilidad_cortes"), ("09a_regimenes_pca", "R_regimenes_pca"),
         ("07b_tabla_2017_10", "R_tabla_2017_10"), ("07b_clasificacion_2017_10", "R_clasificacion_2017_10"),
         ("07b_transiciones_d10", "R_transiciones_d10"), ("05_nulo_tendencias", "R_nulo_tendencias"),
         ("05_tendencia_series", "R_tendencia_series"), ("06_epca_estabilidad_ventanas_niveles", "R_epca_regla06_estabilidad"),
         ("05_pca_contraste_tendencia", "R_pca_contraste_tendencia"), ("05_pca_dimension", "R_pca_dimension"),
         ("05_adecuacion", "R_adecuacion"), ("05_bootstrap_congruencia", "R_bootstrap_congruencia"),
         ("05_bootstrap_valores_propios", "R_bootstrap_valores_propios"), ("05_nulo_simulaciones", "R_nulo_simulaciones"),
         ("05_pca_tendencia_componentes", "R_tendencia_componentes"),
         ("anexo/09b_walkforward_pca", "anexo/R_anexo_walkforward_pca"),
         ("anexo/09b_discriminacion_episodios", "anexo/R_anexo_discriminacion"),
         ("anexo/05c_pasos", "anexo/R_anexo_pasos"), ("anexo/05c_ganancia", "anexo/R_anexo_ganancia"),
         ("anexo/05c_espectro", "anexo/R_anexo_espectro"), ("anexo/05c_estacional", "anexo/R_anexo_estacional")]
malos = 0
for py, r in pares:
    a = pd.read_csv(f'{F}/{py}.csv', keep_default_na=False, dtype=str); b = pd.read_csv(f'{F}/{r}.csv', keep_default_na=False, dtype=str)
    comunes = [c for c in a.columns if c in b.columns]
    if len(a) != len(b):
        print(f'{py}: FILAS {len(a)} vs {len(b)}'); malos += 1; continue
    dif, texto = 0.0, 0
    for c in comunes:
        x = pd.to_numeric(a[c].replace({'': np.nan, 'NA': np.nan}), errors='coerce'); y = pd.to_numeric(b[c].replace({'': np.nan, 'NA': np.nan}), errors='coerce')
        if x.notna().all() and y.notna().all() or (x.notna().sum() > 0 and (x.isna() == y.isna()).all()):
            m = x.notna()
            dif = max(dif, float(np.max(np.abs(x[m] - y[m]))) if m.any() else 0.0)
        else:
            sa = a[c].astype(str).str.upper().replace({'TRUE': 'TRUE', 'FALSE': 'FALSE'}); sb = b[c].astype(str).str.upper()
            texto += int((sa != sb).sum())
    estado = 'OK' if dif <= 1e-10 and texto == 0 else 'DIFIERE'
    malos += estado != 'OK'
    print(f'{estado:8s} {py:45s} cols={len(comunes):2d}/{len(a.columns):2d} filas={len(a):5d} dif_max={dif:.1e} texto_dist={texto}')
print('pares con diferencias:', malos, 'de', len(pares))
