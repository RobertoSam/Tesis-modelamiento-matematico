"""
Repara data/raw/embi_peru_raw.csv sin volver a descargar del BCRP.
Las filas de septiembre ("Set") se guardaron con la fecha vacía, en orden.
A cada bloque sin fecha (entre agosto y octubre) se le asignan los días
hábiles de septiembre de ese año. Se respalda el original antes de escribir.
Uso: python notebooks/reparar_embi_septiembre.py
"""
import os, shutil
import pandas as pd

RUTA = 'data/raw/embi_peru_raw.csv'
RESPALDO = 'data/raw/embi_peru_raw_ORIGINAL_sin_septiembre.csv'

# Se lee sin parsear fechas para conservar el orden y las celdas vacías
df = pd.read_csv(RUTA, dtype={0: str})
col_fecha = df.columns[0]
fechas = pd.to_datetime(df[col_fecha], errors='coerce')
sin_fecha = fechas.isna()
print(f'Filas totales: {len(df)} | sin fecha: {sin_fecha.sum()}')
if sin_fecha.sum() == 0:
    raise SystemExit('No hay filas sin fecha: no se requiere reparación.')

# Bloques consecutivos de filas sin fecha
id_bloque = (sin_fecha != sin_fecha.shift()).cumsum()
reporte = []
for _, idx in df[sin_fecha].groupby(id_bloque[sin_fecha]).groups.items():
    ini, fin = idx.min(), idx.max()
    previa = fechas.iloc[ini - 1] if ini > 0 else pd.NaT
    siguiente = fechas.iloc[fin + 1] if fin + 1 < len(df) else pd.NaT
    # Validación: el bloque debe estar entre agosto y octubre del mismo año
    if pd.isna(previa) or previa.month != 8:
        raise ValueError(f'Filas {ini}-{fin}: la fecha previa ({previa}) no es agosto')
    if not pd.isna(siguiente) and (siguiente.month != 10 or siguiente.year != previa.year):
        raise ValueError(f'Filas {ini}-{fin}: la fecha siguiente ({siguiente}) no es octubre')
    anio = previa.year
    habiles = pd.bdate_range(f'{anio}-09-01', f'{anio}-09-30')
    n = len(idx)
    if n > len(habiles):
        raise ValueError(f'{anio}: {n} filas, pero septiembre tiene {len(habiles)} días hábiles')
    fechas.iloc[list(idx)] = habiles[:n]
    reporte.append({'anio': anio, 'filas': n, 'dias_habiles': len(habiles), 'exactas': n == len(habiles)})

print(pd.DataFrame(reporte).to_string(index=False))

# Verificaciones antes de escribir
assert fechas.notna().all(), 'Quedaron filas sin fecha'
assert fechas.is_monotonic_increasing, 'Las fechas no quedaron en orden'
assert not fechas.duplicated().any(), 'Hay fechas duplicadas'

if not os.path.exists(RESPALDO):
    shutil.copy2(RUTA, RESPALDO)
    print(f'Respaldo del original: {RESPALDO}')
df[col_fecha] = fechas.dt.strftime('%Y-%m-%d')
df.to_csv(RUTA, index=False)
meses = pd.Series(1, index=fechas).resample('MS').sum()
print(f'Reparado. Septiembres con datos: {(meses[meses.index.month == 9] > 0).sum()} | meses vacíos: {(meses == 0).sum()}')
