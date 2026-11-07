"""Portada UNI e índices de tablas y figuras para el Word del borrador (MMC102).

Quarto genera el título con sus propios estilos (Title, Subtitle, Author, Date). El formato del
curso MMC102 (Seminario de Tesis II, 2026-II) pide, en cambio, la portada de la Unidad de Posgrado
de la Facultad de Ciencias. Este script, aplicado al .docx que produce Quarto:

1. retira el bloque de título de Quarto y escribe la portada del formato MMC102;
2. después del índice de contenidos, agrega los índices de tablas y de figuras a partir de las
   leyendas (lista sin números de página: las leyendas de Quarto no usan campos SEQ);
3. hace que cada capítulo empiece en página nueva;
4. pide a Word que actualice los campos al abrir el archivo (índice de contenidos).

Uso, desde la raíz del repositorio:
    python3 herramientas/portada_mmc102.py _site/tesis/borrador_completo.docx salida.docx
"""

import copy
import re
import sys

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Pt

ENTRADA, SALIDA = [a for a in sys.argv[1:] if not a.startswith("--")][:2]

# Datos de la portada (ficha de inscripción de la tesis, n.º 01)
TITULO = ("Detección evolutiva de regímenes del ciclo financiero peruano mediante "
          "Clasificación Factorial Jerárquica y aprendizaje automático")
ASESOR = "Dr. Sergio Camiz"
TESISTA = "Roberto Carlos Samaniego Salcedo"
CODIGO_UNI = "20256037E"
DIRECTOR = "DR. ROSENDO OCHOA JIMÉNEZ"
SEMESTRE = "2026-II"

d = docx.Document(ENTRADA)
cuerpo = d.element.body

# 1. Retirar el bloque de título de Quarto
for p in list(d.paragraphs[:6]):
    if p.style.name in ("Title", "Subtitle", "Author", "Date"):
        p._element.getparent().remove(p._element)

# 2. Portada: se construye al final del documento y se mueve al inicio
lineas = [
    ("UNIVERSIDAD NACIONAL DE INGENIERÍA", True, 14, 0),
    ("FACULTAD DE CIENCIAS", True, 13, 0),
    ("Unidad de Posgrado", True, 12, 18),
    ("MAESTRÍA EN CIENCIAS EN MODELIZACIÓN MATEMÁTICA Y COMPUTACIONAL", False, 12, 30),
    (f"«{TITULO}»", True, 14, 24),
    ("CURSO: MMC102 – Seminario de Tesis II", True, 12, 4),
    ("Informe de avance", False, 12, 36),
    ("__________________________", False, 12, 0),
    ("ASESOR", False, 11, 0),
    (ASESOR, True, 12, 24),
    ("__________________________", False, 12, 0),
    ("TESISTA", False, 11, 0),
    (TESISTA, True, 12, 0),
    (f"Código UNI: {CODIGO_UNI}", True, 12, 24),
    ("NOTA FINAL: ________", True, 12, 30),
    (DIRECTOR, True, 12, 0),
    ("Director de la Unidad de Posgrado", True, 11, 30),
    ("Lima – Perú", True, 12, 0),
    (SEMESTRE, True, 12, 0),
]
nuevos = []
for texto, negrita, tam, despues in lineas:
    p = d.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(despues)
    p.paragraph_format.first_line_indent = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    r = p.add_run(texto)
    r.bold = negrita
    r.font.size = Pt(tam)
    nuevos.append(p._element)
salto = d.add_paragraph()
salto.add_run().add_break(WD_BREAK.PAGE)
nuevos.append(salto._element)
for i, el in enumerate(nuevos):
    cuerpo.remove(el)
    cuerpo.insert(i, el)

# 3. Índices de tablas y figuras, a partir de las leyendas
leyendas = {"Tabla": [], "Figura": []}
patron = re.compile(r"^(Tabla|Figura)\s+(\d+):\s*(.*)$")
for el in cuerpo.iter(qn("w:p")):
    texto = "".join(t.text or "" for t in el.iter(qn("w:t"))).strip()
    m = patron.match(texto)
    if m:
        # Solo la primera oración de la leyenda, para un índice legible
        titulo = re.split(r"(?<=[a-záéíóúñ0-9)])\. ", m.group(3))[0].rstrip(".")
        # Las fórmulas (OMML) no están en w:t: se limpian los restos que dejan
        titulo = re.sub(r"\s*\(\s*\)", "", titulo).replace(", ,", ",")
        leyendas[m.group(1)].append(f"{m.group(1)} {m.group(2)}. {titulo}")

sdt = cuerpo.find(qn("w:sdt"))  # índice de contenidos de Quarto
ancla = sdt if sdt is not None else nuevos[-1]
bloque = []
for nombre, clave in (("Índice de tablas", "Tabla"), ("Índice de figuras", "Figura")):
    if not leyendas[clave]:
        continue
    h = d.add_paragraph(nombre, style="TOC Heading")
    bloque.append(h._element)
    for item in leyendas[clave]:
        p = d.add_paragraph(item)
        p.paragraph_format.first_line_indent = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        bloque.append(p._element)
fin = d.add_paragraph()
fin.add_run().add_break(WD_BREAK.PAGE)
bloque.append(fin._element)
# Salto de página entre el índice de contenidos y los demás índices
antes = d.add_paragraph()
antes.add_run().add_break(WD_BREAK.PAGE)
bloque.insert(0, antes._element)
pos = list(cuerpo).index(ancla) + 1
for i, el in enumerate(bloque):
    cuerpo.remove(el)
    cuerpo.insert(pos + i, el)

# 4. Cada capítulo (Heading 1) empieza en página nueva
# (con --sin-saltos, solo el resumen empieza en página nueva: informes con límite de páginas)
SIN_SALTOS = "--sin-saltos" in sys.argv
for p in d.paragraphs:
    if p.style.name == "Heading 1" and (not SIN_SALTOS or p.text.strip() in ("Resumen", "Referencias")):
        p.paragraph_format.page_break_before = True

# 5. Tablas al ancho de la página (las de Quarto salen con ancho automático y columnas estrechas)
for tbl in cuerpo.iter(qn("w:tbl")):
    tblPr = tbl.find(qn("w:tblPr"))
    if tblPr is None:
        continue
    # Las tablas de una sola celda que envuelven figuras y leyendas no se tocan
    if len(tbl.findall(qn("w:tr"))) < 2:
        continue
    tblW = tblPr.find(qn("w:tblW"))
    if tblW is None:
        tblW = OxmlElement("w:tblW")
        tblPr.append(tblW)
    tblW.set(qn("w:type"), "pct")
    tblW.set(qn("w:w"), "5000")

# 6. Word actualiza los campos (índice de contenidos) al abrir
ajustes = d.settings.element
if ajustes.find(qn("w:updateFields")) is None:
    uf = OxmlElement("w:updateFields")
    uf.set(qn("w:val"), "true")
    ajustes.append(uf)

d.save(SALIDA)
print(f"{SALIDA}: portada MMC102, {len(leyendas['Tabla'])} tablas y {len(leyendas['Figura'])} figuras en los índices")
