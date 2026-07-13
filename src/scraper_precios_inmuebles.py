"""
Scraper de precios de departamentos Lima - Notas de Estudios BCRP
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
    'Accept': 'application/pdf,application/octet-stream,*/*',
    'Accept-Language': 'es-PE,es;q=0.9,en;q=0.8',
    'Referer': 'https://www.bcrp.gob.pe/',
    'Connection': 'keep-alive',
}

NOTAS = [
    {"url": "https://www.bcrp.gob.pe/docs/Publicaciones/Notas-Estudios/2024/nota-de-estudios-38-2024.pdf", "periodo": "2024-Q1"},
    {"url": "https://www.bcrp.gob.pe/docs/Publicaciones/Notas-Estudios/2023/nota-de-estudios-43-2023.pdf", "periodo": "2023-Q1"},
    {"url": "https://www.bcrp.gob.pe/docs/Publicaciones/Notas-Estudios/2023/nota-de-estudios-16-2023.pdf", "periodo": "2022-Q4"},
    {"url": "https://www.bcrp.gob.pe/docs/Publicaciones/Notas-Estudios/2022/nota-de-estudios-16-2022.pdf", "periodo": "2021-Q4"},
    {"url": "https://www.bcrp.gob.pe/docs/Publicaciones/Notas-Estudios/2021/nota-de-estudios-77-2021.pdf", "periodo": "2021-Q3"},
    {"url": "https://www.bcrp.gob.pe/docs/Publicaciones/Notas-Estudios/2020/nota-de-estudios-30-2020.pdf", "periodo": "2020-Q1"},
    {"url": "https://www.bcrp.gob.pe/docs/Publicaciones/Notas-Estudios/2019/nota-de-estudios-76-2019.pdf", "periodo": "2019-Q3"},
]

def descargar_pdf(url):
    session = requests.Session()
    # Primero visitar la página principal para obtener cookies
    try:
        session.get('https://www.bcrp.gob.pe/', headers=HEADERS, timeout=15)
        time.sleep(1)
        r = session.get(url, headers=HEADERS, timeout=30)
        print(f"  Status: {r.status_code} | Content-Type: {r.headers.get('Content-Type', 'unknown')} | Size: {len(r.content)} bytes")
        if r.status_code == 200 and len(r.content) > 10000:
            return BytesIO(r.content)
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None

def extraer_texto(pdf_bytes):
    with pdfplumber.open(pdf_bytes) as pdf:
        texto = ""
        for page in pdf.pages[:4]:
            texto += page.extract_text() or ""
    return texto

def buscar_precio_usd(texto):
    # Buscar valores numéricos cerca de "dólar" o "US$"
    patrones = [
        r'(\d{3,4}(?:[,.]\d+)?)\s*(?:US\$|dólares)\s*(?:por\s*)?(?:m2|metro)',
        r'(\d{3,4}(?:[,.]\d+)?)\s*US\$/m2',
        r'precio[^\n]{0,50}?(\d{3,4}(?:[,.]\d+)?)[^\n]{0,20}(?:dólar|US\$)',
    ]
    for patron in patrones:
        matches = re.findall(patron, texto, re.IGNORECASE)
        if matches:
            return matches
    # Buscar cualquier número de 3-4 dígitos cerca de dólar
    idx = texto.lower().find('dólar')
    if idx > 0:
        fragmento = texto[max(0, idx-100):idx+200]
        nums = re.findall(r'\b(\d{3,4}(?:[,.]\d{1,2})?)\b', fragmento)
        return nums
    return []

print("Descargando PDFs del BCRP...")
print("=" * 60)

resultados = []
for nota in NOTAS:
    print(f"\n📄 {nota['periodo']} — {nota['url'].split('/')[-1]}")
    pdf_bytes = descargar_pdf(nota['url'])
    
    if pdf_bytes:
        try:
            texto = extraer_texto(pdf_bytes)
            precios = buscar_precio_usd(texto)
            print(f"  Precios USD encontrados: {precios[:5]}")
            
            # Mostrar contexto
            for kw in ['1 8', '1 7', 'dólar', 'US$']:
                idx = texto.find(kw)
                if idx > 0:
                    print(f"  Contexto '{kw}': ...{texto[max(0,idx-30):idx+80].strip()}...")
                    break
                    
            resultados.append({
                'periodo': nota['periodo'],
                'precios_encontrados': precios[:5],
                'texto_muestra': texto[:300]
            })
        except Exception as e:
            print(f"  Error procesando PDF: {e}")
    
    time.sleep(2)

print("\n✅ Scraping completado")
print(f"PDFs procesados: {len(resultados)}/{len(NOTAS)}")
