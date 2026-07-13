import json

path = 'notebooks/01_extraccion_bcrp.ipynb'
nb = json.load(open(path, encoding='utf-8'))

nuevo_bloque = '''# Códigos de series del BCRP (mensuales, salvo el índice de inmuebles que es trimestral
# y se carga aparte en la sección 4)
#
# CORRECCIÓN (verificada contra BCRPData): los códigos PN01208PM/PN01209PM/PN01210PM
# NO son series de crédito -- son "Tipo de Cambio Bancario Compra/Venta/Promedio".
# Se reemplazan por el desglose real de crédito por tipo (Cuadro 19 del BCRP:
# "Crédito al sector privado de las sociedades de depósito, por tipo de crédito
# y por moneda"). Además se elimina 'Crédito bancario SP' (PN00522MM) por ser
# un subconjunto casi colineal de 'Crédito SF sector privado' (PN00518MM).
#
# Nota de colinealidad: Total ≈ Empresarial + Consumo + Hipotecario.
# No uses el total junto con los tres componentes en el mismo PCA/HFC.
SERIES = {
    # CRÉDITO (desglose por tipo, en soles, ambas monedas -- Cuadro 19 BCRP)
    'Crédito SF sector privado': 'PN00518MM',  # Total
    'Crédito empresarial':       'PN00532MM',  # Saldos - A Empresas
    'Crédito consumo':           'PN00533MM',  # Saldos - Consumo
    'Crédito hipotecario':       'PN00534MM',  # Saldos - Hipotecario
    # TASAS
    'Tasa activa TAMN':          'PN07807NM',
    'Tasa pasiva TIPMN':         'PN07816NM',
    'Tasa referencia BCRP':      'PD04722MM',
    # TIPO DE CAMBIO Y MERCADO
    'Tipo de cambio':            'PN01246PM',
    'Índice BVL':                'PN01142MM',
    'IPC Lima':                  'PN38705PM',
    # ACTIVIDAD
    'PBI desestacionalizado':    'PN01773AM',
    'Demanda interna':           'PN01774AM',
    'Reservas internacionales':  'PN00027MM',
}'''

encontrado = False
for celda in nb['cells']:
    if celda['cell_type'] == 'code':
        src = ''.join(celda['source'])
        if "SERIES = {" in src:
            celda['source'] = nuevo_bloque.splitlines(keepends=True)
            encontrado = True
            break

print("Bloque reemplazado:", encontrado)

with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

# Verificación de integridad del JSON
json.load(open(path, encoding='utf-8'))
print("Notebook válido, guardado correctamente")
