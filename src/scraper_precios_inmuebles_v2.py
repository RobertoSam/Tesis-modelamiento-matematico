"""
Scraper de precios de departamentos Lima - Notas de Estudios BCRP
Versión 2 — extracción mejorada
Autor: Roberto Samaniego
"""

import requests
import re
import pandas as pd
from io import BytesIO
import pdfplumber
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/pdf,*/*',
    'Referer': 'https://www.bcrp.gob.pe/',
}

# Notas de estudios inmobiliarios del BCRP — ordenadas cronológicamente
NOTAS = [
    # 2024
    {"url": "https://www.bcrp.gob.pe/docs/Publicaciones/Notas-Estudios/2024/nota-de-estudios-38-2024.pdf", "periodo": "2024-Q1"},
    # 2023
    {"url": "https://www.bcrp.gob.pe/docs/Publicaciones/Notas-Estudios/2023/nota-de-estudios-43-2023.pdf", "periodo": "2023-Q1"},
    {"url": "https://www.bcrp.gob.pe/docs/Publicaciones/Notas-Estudios/2023/nota-de-estudios-16-2023.pdf", "periodo": "2022-Q4"},
    # 2022
    {"url": "https://www.bcrp.gob.pe/docs/Publicaciones/Notas-Estudios/2022/nota-de-estudios-16-2022.pdf", "periodo": "2021-Q4"},
    # 2021
    {"url": "https://www.bcrp.gob.pe/docs/Publicaciones/Notas-Estudios/2021/nota-de-estudios-77-2021.pdf", "periodo": "2021-Q3"},
    # 2020
    {"url": "https://www.bcrp.gob.pe/docs/Publicaciones/Notas-Estudios/2020/nota-de-estudios-30-2020.pdf", "periodo": "2020-Q1"},
    # 2019
    {"url": "https://www.bcrp.gob.pe/docs/Publicaciones/Notas-Estudios/2019/nota-de-estudios-76-2019.pdf", "periodo": "2019-Q3"},
    # 2019 Q1
    {"url": "https://www.bcrp.gob.pe/docs/Publicaciones/Notas-Estudios/2019/nota-de-estudios-22-2019.pdf", "periodo": "2018-Q4"},
    # 2018
    {"url": "https://www.bcrp.gob.pe/docs/Publicaciones/Notas-Estudios/2018/nota-de-estudios-60-2018.pdf", "periodo": "2018-Q3"},
    {"url": "https://www.bcrp.gob.pe/docs/Publicaciones/Notas-Estudios/2018/nota-de-estudios-19-2018.pdf", "periodo": "2017-Q4"},
    # 2017
    {"url": "https://www.bcrp.gob.pe/docs/Publicaciones/Notas-Estudios/2017/nota-de-estudios-68-2017.pdf", "periodo": "2017-Q3"},
    {"url": "https://www.bcrp.gob.pe/docs/Publicaciones/Notas-Estudios/2017/nota-de-estudios-19-2017.pdf", "periodo": "2016-Q4"},
    # 2016
    {"url": "https://www.bcrp.gob.pe/docs/Publicaciones/Notas-Estudios/2016/nota-de-estudios-67-2016.pdf", "periodo": "2016-Q3"},
    {"url": "https://www.bcrp.gob.pe/docs/Publicaciones/Notas-Estudios/2016/nota-de-estudios-19-2016.pdf", "periodo": "2015-Q4"},
    # 2015
    {"url": "https://www.bcrp.gob.pe/docs/Publicaciones/Notas-Estudios/2015/nota-de-estudios-68-2015.pdf", "periodo": "2015-Q3"},
    {"url": "https://www.bcrp.gob.pe/docs/Publicaciones/Notas-Estudios/2015/nota-de-estudios-19-2015.pdf", "periodo": "2014-Q4"},
]

def descargar_pdf(url):
    session = requests.Session()
    try:
        session.get('https://www.bcrp.gob.pe/', headers=HEADERS, timeout=15)
        time.sleep(1)
        r = session.get(url, headers=HEADERS, timeout=30)
        if r.status_code == 200 and len(r.content) > 10000:
            return BytesIO(r.content)
        return None
    except Exception as e:
        return None

def extraer_precio_usd(pdf_bytes):
    """Extrae precio en US$/m2 del PDF."""
    with pdfplumber.open(pdf_bytes) as pdf:
        texto = ""
        for page in pdf.pages[:4]:
            texto += page.extract_text() or ""
    
    # Buscar patrón "US$ X XXX" o "US$ X.XXX" con o sin espacios
    # Los PDFs del BCRP suelen tener el formato "US$ 1 843" o "US$ 1843" o "1 843"
    
    # Primero buscar cerca de "US$"
    patron1 = r'US\$\s*(\d[\s,]?\d{3}(?:[,.]\d+)?)'
    matches1 = re.findall(patron1, texto)
    
    # Limpiar matches — quitar espacios internos
    precios = []
    for m in matches1:
        val = m.replace(' ', '').replace(',', '')
        try:
            precio = float(val)
            if 500 < precio < 5000:  # Rango razonable US$/m2 en Lima
                precios.append(precio)
        except:
            pass
    
    # Si no encontró, buscar contexto de "dólar"
    if not precios:
        idx = texto.lower().find('dólar')
        if idx < 0:
            idx = texto.find('US$')
        if idx > 0:
            fragmento = texto[max(0, idx-200):idx+200]
            nums = re.findall(r'\b(\d[\s]?\d{3})\b', fragmento)
            for n in nums:
                val = n.replace(' ', '')
                try:
                    precio = float(val)
                    if 500 < precio < 5000:
                        precios.append(precio)
                except:
                    pass
    
    return precios[0] if precios else None

# Ejecutar scraping
print("Descargando y procesando PDFs del BCRP...")
print("=" * 60)

resultados = []
for nota in NOTAS:
    print(f"📄 {nota['periodo']}...", end=" ")
    pdf_bytes = descargar_pdf(nota['url'])
    
    if pdf_bytes:
        try:
            precio = extraer_precio_usd(pdf_bytes)
            if precio:
                print(f"✅ US$ {precio}/m2")
                resultados.append({'periodo': nota['periodo'], 'precio_usd_m2': precio})
            else:
                print(f"⚠️  No se encontró precio")
                resultados.append({'periodo': nota['periodo'], 'precio_usd_m2': None})
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print(f"❌ PDF no disponible")
    
    time.sleep(1.5)

# Guardar resultados
df = pd.DataFrame(resultados)
print("\n" + "=" * 60)
print("RESULTADOS:")
print(df.to_string(index=False))

df.to_csv('data/raw/precios_departamentos_lima.csv', index=False)
print("\n✅ Guardado en data/raw/precios_departamentos_lima.csv")
