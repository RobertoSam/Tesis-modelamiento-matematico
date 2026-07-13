import json

def reemplazar(path, viejo, nuevo, descripcion):
    nb = json.load(open(path, encoding='utf-8'))
    encontrado = False
    for celda in nb['cells']:
        if celda['cell_type'] == 'code':
            src = ''.join(celda['source'])
            if viejo.strip() in src:
                celda['source'] = [l if viejo.strip() not in l else None for l in celda['source']]
                # reemplazo simple por bloque completo
                nueva_src = src.replace(viejo, nuevo)
                celda['source'] = nueva_src.splitlines(keepends=True)
                encontrado = True
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    json.load(open(path, encoding='utf-8'))  # valida JSON
    print(f"{descripcion}: {'OK' if encontrado else 'NO ENCONTRADO'}")

# --- 03_analisis_exploratorio.ipynb ---
viejo_03 = """'Crédito':   ['Crédito SF sector privado', 'Crédito bancario SP',
                  'Crédito hipotecario', 'Crédito consumo', 'Crédito en ME'],"""
nuevo_03 = """'Crédito':   ['Crédito SF sector privado', 'Crédito empresarial',
                  'Crédito consumo', 'Crédito hipotecario'],"""
reemplazar('notebooks/03_analisis_exploratorio.ipynb', viejo_03, nuevo_03, "03_analisis_exploratorio")

# --- 04_preprocesamiento.ipynb ---
viejo_04 = """VARS_LOG_DIFF = [
    'Crédito SF sector privado', 'Crédito bancario SP', 'Crédito hipotecario',
    'Crédito consumo', 'Crédito en ME', 'Tipo de cambio', 'Índice BVL', 'IPC Lima',
    'PBI', 'Demanda interna', 'Reservas internacionales', 'indice_precios_inmuebles'
]"""
nuevo_04 = """VARS_LOG_DIFF = [
    # 'Crédito SF sector privado',  # Total -- excluir si se usan los 3 componentes
    'Crédito empresarial', 'Crédito consumo', 'Crédito hipotecario',
    'Tipo de cambio', 'Índice BVL', 'IPC Lima',
    'PBI desestacionalizado', 'Demanda interna', 'Reservas internacionales',
    'indice_precios_inmuebles'
]"""
reemplazar('notebooks/04_preprocesamiento.ipynb', viejo_04, nuevo_04, "04_preprocesamiento")
