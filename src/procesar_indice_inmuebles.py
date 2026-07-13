"""
Procesa el Índice de Precios Hedónicos de Inmuebles del BCRP
Serie trimestral 2007-2025 (índice base 2013=100)
Autor: Roberto Samaniego
"""

import pandas as pd

# Datos pegados directamente del portal BCRP
datos_raw = """T407 37.4
T108 38.2
T208 43.8
T308 49.4
T408 50.5
T109 49.1
T209 49.1
T309 53.4
T409 54.1
T110 59.4
T210 62.0
T310 63.7
T410 64.9
T111 70.3
T211 74.1
T311 78.4
T411 78.2
T112 84.0
T212 88.9
T312 91.3
T412 93.5
T113 100.0
T213 101.8
T313 102.8
T413 102.4
T114 106.9
T214 111.4
T314 106.0
T414 106.4
T115 106.4
T215 105.1
T315 104.7
T415 102.4
T116 100.4
T216 102.2
T316 103.2
T416 104.6
T117 105.5
T217 103.8
T317 105.7
T417 104.8
T118 104.7
T218 103.6
T318 106.2
T418 106.4
T119 107.4
T219 108.5
T319 108.3
T419 105.7
T120 107.1
T220 108.3
T320 108.8
T420 109.8
T121 109.4
T221 109.9
T321 108.1
T421 106.5
T122 107.1
T222 108.1
T322 108.2
T422 108.2
T123 107.9
T223 109.2
T323 109.4
T423 111.3
T124 109.5
T224 109.7
T324 109.5
T424 109.7
T125 110.3
T225 112.1
T325 113.9
T425 116.4"""

def parse_periodo(p):
    """Convierte 'T407' -> Q4 2007, 'T125' -> Q1 2025."""
    trimestre = int(p[1])
    anio_corto = int(p[2:])
    anio = 2000 + anio_corto
    mes_fin = trimestre * 3
    # Usar el último mes del trimestre como fecha representativa
    fecha = pd.Timestamp(year=anio, month=mes_fin, day=1) + pd.offsets.MonthEnd(0)
    return fecha, trimestre, anio

registros = []
for linea in datos_raw.strip().split('\n'):
    periodo, valor = linea.split()
    fecha, trimestre, anio = parse_periodo(periodo)
    registros.append({
        'periodo': periodo,
        'fecha': fecha,
        'trimestre': trimestre,
        'anio': anio,
        'indice_precios_inmuebles': float(valor)
    })

df = pd.DataFrame(registros).sort_values('fecha').reset_index(drop=True)

print("Índice de Precios Hedónicos de Inmuebles — BCRP")
print("=" * 60)
print(f"Periodo: {df['fecha'].min().strftime('%Y-%m')} a {df['fecha'].max().strftime('%Y-%m')}")
print(f"Observaciones: {len(df)}")
print(f"Frecuencia: Trimestral")
print(f"Base: 100 = 2013")
print("\nPrimeras filas:")
print(df.head())
print("\nÚltimas filas:")
print(df.tail())

# Guardar
df.to_csv('data/raw/indice_precios_inmuebles_bcrp.csv', index=False)
print("\n✅ Guardado en data/raw/indice_precios_inmuebles_bcrp.csv")

# Estadísticas básicas
print(f"\nVariación total del periodo: {((df['indice_precios_inmuebles'].iloc[-1] / df['indice_precios_inmuebles'].iloc[0]) - 1) * 100:.1f}%")
print(f"Valor mínimo: {df['indice_precios_inmuebles'].min()} ({df.loc[df['indice_precios_inmuebles'].idxmin(), 'periodo']})")
print(f"Valor máximo: {df['indice_precios_inmuebles'].max()} ({df.loc[df['indice_precios_inmuebles'].idxmax(), 'periodo']})")
