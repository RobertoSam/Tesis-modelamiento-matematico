# -*- coding: utf-8 -*-
"""Construye el documento consolidado con la estructura del curso MMC102 (Seminario de Tesis II).

Pasos:
1. Ensambla los preliminares, los cinco capítulos y los anexos, y numera tablas y figuras.
2. Convierte a .docx con pandoc (citas APA 7 con citeproc y la plantilla del repositorio).
3. Ajusta el .docx con python-docx: carátula UNI, índices con campos de Word, saltos de página,
   numeración romana/arábiga, rótulos APA de tablas y figuras, referencias con sangría francesa,
   matriz de consistencia en hoja apaisada.

Uso: python3 build_mmc102.py <ruta_repo> <salida.docx>
"""
import copy
import re
import subprocess
import sys
from pathlib import Path

import docx
import pandas as pd
import yaml
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

REPO = Path(sys.argv[1])
SALIDA = Path(sys.argv[2])
AQUI = Path(__file__).parent


# ---------------------------------------------------------------- 1. Ensamblado
CAPITULOS = [("01_introduccion.md", "CAPÍTULO I. INTRODUCCIÓN"),
             ("02_marco_teorico.md", "CAPÍTULO II. MARCO TEÓRICO"),
             ("03_metodologia_modelo.md", "CAPÍTULO III. METODOLOGÍA Y DESARROLLO DEL MODELO"),
             ("04_resultados_discusion.md", "CAPÍTULO IV. RESULTADOS Y DISCUSIÓN"),
             ("05_conclusiones.md", "CAPÍTULO V. CONCLUSIONES Y RECOMENDACIONES")]
partes = ["---\nlang: es-PE\nlink-citations: false\n---\n",
          (AQUI / "00_preliminares.md").read_text(encoding="utf-8")]
for archivo, titulo in CAPITULOS:
    t = (AQUI / archivo).read_text(encoding="utf-8")
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    t = re.sub(r"^# .*$", "# " + titulo, t, count=1, flags=re.M)
    partes.append(t)
partes.append((AQUI / "06_anexos.md").read_text(encoding="utf-8"))
md = "\n\n".join(partes)
md = re.sub(r"(?<![\d,])[−-]0,00(?!\d)", "0,00", md)
assert "preliminar" not in md.lower().replace("titulo preliminar", ""), "aparece «preliminar» en el cuerpo"

# Numeración de tablas y figuras en el orden de sus rótulos
numeros = {}
for tipo, letra in (("Tabla", "T"), ("Figura", "F")):
    for k, clave in enumerate(re.findall(r"\*\*" + tipo + r" \{" + letra + r":(\w+)\}\*\*", md), start=1):
        numeros[(letra, clave)] = k
def numero(m):
    clave = (m.group(1), m.group(2))
    if clave not in numeros:
        sys.exit(f"Referencia sin rótulo: {clave}")
    return str(numeros[clave])
md = re.sub(r"\{([TF]):(\w+)\}", numero, md)

tmp = AQUI / "_tmp_informe.md"
tmp.write_text(md, encoding="utf-8")

# ---------------------------------------------------------------- 2. Pandoc
intermedio = AQUI / "_tmp_informe.docx"
subprocess.run(["pandoc", str(tmp), "-o", str(intermedio), "--citeproc",
                "--bibliography", str(AQUI / "referencias.bib"),
                "--bibliography", str(AQUI / "referencias_extra.bib"), "--csl", str(AQUI / "apa.csl"),
                "--reference-doc", str(AQUI / "plantilla_uni.docx"), "--resource-path", str(AQUI)],
               check=True)

# ---------------------------------------------------------------- 3. Ajustes con python-docx
d = docx.Document(str(intermedio))
cuerpo = d.element.body
NEGRO = RGBColor(0, 0, 0)


def E(nombre):
    """Busca un estilo por su nombre visible (pandoc escribe 'Heading 1' con mayúscula)."""
    for st in d.styles:
        if st.name == nombre:
            return st
    raise KeyError(nombre)


def estilo_parrafo(nombre):
    try:
        return E(nombre)
    except KeyError:
        return d.styles.add_style(nombre, 1)


# Estilos base: Arial 12, interlineado 1,5 (plantilla); encabezados en negro
for nombre in ["Heading 1", "Heading 2", "Heading 3"]:
    e = E(nombre)
    e.font.name = "Arial"
    e.font.color.rgb = NEGRO
    e.font.bold = True
    e.font.italic = False
    e.paragraph_format.keep_with_next = True
E("Heading 1").font.size = Pt(14)
E("Heading 1").paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
E("Heading 1").paragraph_format.page_break_before = True
E("Heading 1").paragraph_format.space_after = Pt(18)
E("Heading 2").font.size = Pt(12)
E("Heading 3").font.size = Pt(12)
E("Heading 3").font.italic = True
for nombre in ["Body Text", "First Paragraph", "Compact"]:
    try:
        E(nombre).paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    except KeyError:
        pass

rt = estilo_parrafo("Rótulo tabla")
rf = estilo_parrafo("Rótulo figura")
for e in (rt, rf):
    e.base_style = E("Normal")
    e.font.name = "Arial"
    e.font.size = Pt(12)
    e.paragraph_format.space_before = Pt(12)
    e.paragraph_format.space_after = Pt(6)
    e.paragraph_format.line_spacing = 1.0
    e.paragraph_format.keep_with_next = True
    e.paragraph_format.first_line_indent = Cm(0)
    e.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

nota = E("Nota")
nota.font.size = Pt(10)
nota.paragraph_format.line_spacing = 1.0
nota.paragraph_format.space_before = Pt(4)
nota.paragraph_format.space_after = Pt(14)
nota.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

tp = E("Titulo preliminar")
tp.font.name = "Arial"
tp.font.size = Pt(14)
tp.font.bold = True
tp.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
tp.paragraph_format.space_after = Pt(18)
tp.paragraph_format.page_break_before = True

bib = E("Bibliography")
bib.paragraph_format.line_spacing = 2.0
bib.paragraph_format.left_indent = Cm(1.27)
bib.paragraph_format.first_line_indent = Cm(-1.27)
bib.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
bib.paragraph_format.space_after = Pt(0)

# Rótulos: separar tablas y figuras en estilos propios (para las listas de Word)
rotulos = {"tabla": [], "figura": []}
for p in d.paragraphs:
    if p.style.name == "Rotulo":
        tipo = "tabla" if p.text.startswith("Tabla") else "figura"
        p.style = rt if tipo == "tabla" else rf
        rotulos[tipo].append(p.text.replace("\n", ". ", 1))

# Saltos de página
for p in list(d.paragraphs):
    if p.style.name == "Salto":
        nuevo = d.add_paragraph()
        nuevo.add_run().add_break(WD_BREAK.PAGE)
        p._element.addprevious(nuevo._element)
        p._element.getparent().remove(p._element)

for p in d.paragraphs:
    if p.style.name == "Titulo preliminar" and p.text.strip() == "LISTA DE FIGURAS":
        p.paragraph_format.page_break_before = False
        p.paragraph_format.space_before = Pt(24)

# Imágenes centradas
for p in d.paragraphs:
    if p._element.findall(".//" + qn("w:drawing")):
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.keep_with_next = True


# Campos de índice
def run_campo(p, tipo):
    r = OxmlElement("w:r")
    f = OxmlElement("w:fldChar")
    f.set(qn("w:fldCharType"), tipo)
    if tipo == "begin":
        f.set(qn("w:dirty"), "true")
    r.append(f)
    p._element.append(r)


def campo_indice(marca, instruccion, entradas):
    """Reemplaza el párrafo marcador por un campo TOC con un resultado provisional."""
    obj = next(p for p in d.paragraphs if p.text.strip() == marca)
    parrafos = []
    for i, (texto, nivel) in enumerate(entradas or [("Actualice el campo (F9).", 0)]):
        p = d.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.6 * nivel)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(3)
        if i == 0:
            run_campo(p, "begin")
            r = OxmlElement("w:r")
            it = OxmlElement("w:instrText")
            it.set(qn("xml:space"), "preserve")
            it.text = f" {instruccion} "
            r.append(it)
            p._element.append(r)
            run_campo(p, "separate")
        p.add_run(texto)
        parrafos.append(p)
    run_campo(parrafos[-1], "end")
    for p in parrafos:
        obj._element.addprevious(p._element)
    obj._element.getparent().remove(obj._element)


titulos = [(p.text, int(p.style.name[-1]) - 1) for p in d.paragraphs
           if p.style.name in ("Heading 1", "Heading 2", "Heading 3")]
campo_indice("[[TOC]]", 'TOC \\o "1-3" \\h \\z \\u', titulos)
campo_indice("[[LISTA_TABLAS]]", 'TOC \\h \\z \\t "Rótulo tabla,1"',
             [(t, 0) for t in rotulos["tabla"]])
campo_indice("[[LISTA_FIGURAS]]", 'TOC \\h \\z \\t "Rótulo figura,1"',
             [(t, 0) for t in rotulos["figura"]])

# Tablas: estilo APA (líneas horizontales), letra de 10 pt
def bordes_apa(tabla):
    tblPr = tabla._tbl.tblPr
    for viejo in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(viejo)
    b = OxmlElement("w:tblBorders")
    for lado, val in [("top", "single"), ("bottom", "single"), ("left", "nil"), ("right", "nil"),
                      ("insideH", "nil"), ("insideV", "nil")]:
        e = OxmlElement(f"w:{lado}")
        e.set(qn("w:val"), val)
        if val == "single":
            e.set(qn("w:sz"), "8")
            e.set(qn("w:color"), "000000")
        b.append(e)
    tblPr.append(b)
    for celda in tabla.rows[0].cells:
        tcPr = celda._tc.get_or_add_tcPr()
        tb = OxmlElement("w:tcBorders")
        e = OxmlElement("w:bottom")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "8")
        e.set(qn("w:color"), "000000")
        tb.append(e)
        tcPr.append(tb)
        for p in celda.paragraphs:
            for r in p.runs:
                r.bold = True


def letra_tabla(tabla, tam):
    for fila in tabla.rows:
        for celda in fila.cells:
            for p in celda.paragraphs:
                p.paragraph_format.line_spacing = 1.0
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.first_line_indent = Cm(0)
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    r.font.size = Pt(tam)


def ancho_completo(tabla):
    tblPr = tabla._tbl.tblPr
    for viejo in tblPr.findall(qn("w:tblW")):
        tblPr.remove(viejo)
    w = OxmlElement("w:tblW")
    w.set(qn("w:w"), "5000")
    w.set(qn("w:type"), "pct")
    tblPr.append(w)


def repartir_columnas(tabla, total_cm=15.5):
    """Mínimo por la palabra más larga de cada columna; el resto, según el largo del texto."""
    minimos, pesos, largos, palabras = [], [], [], []
    for col in tabla.columns:
        textos = [c.text for c in col.cells]
        palabra = max((len(w) for t in textos for w in t.split()), default=4)
        palabras.append(max(palabra, max([len(t) for t in textos[1:] if len(t) <= 11], default=0)))
        # Celdas cortas del cuerpo (p. ej., «5,00 → 6,50» o «2009-01 a 2015-01») no deben partirse
        largos.append(max([palabra] + [len(t) for t in textos[1:] if len(t) <= 17]))
        minimos.append(0.24 * largos[-1] + 0.45)
        pesos.append(max(len(t) for t in textos))
    if sum(minimos) > total_cm:
        # Tabla ancha: letra de 9 puntos; si aun así no cabe, se permite partir las celdas largas
        minimos, letra = [0.2 * n + 0.45 for n in largos], 9
        if sum(minimos) > total_cm:
            minimos = [0.2 * n + 0.45 for n in palabras]
        if sum(minimos) > total_cm:
            minimos, letra = [0.175 * n + 0.42 for n in palabras], 8
        letra_tabla(tabla, letra)
        tabla._letra9 = True
    libre = max(0.0, total_cm - sum(minimos))
    anchos = [Cm(m + libre * w / sum(pesos)) for m, w in zip(minimos, pesos)]
    tblPr = tabla._tbl.tblPr
    if tblPr.find(qn("w:tblLayout")) is None:
        lay = OxmlElement("w:tblLayout")
        lay.set(qn("w:type"), "fixed")
        tblPr.append(lay)
    grid = tabla._tbl.tblGrid
    for gc, a in zip(grid.findall(qn("w:gridCol")), anchos):
        gc.set(qn("w:w"), str(int(a.twips)))
    for fila in tabla.rows:
        for c, celda in enumerate(fila.cells):
            celda.width = anchos[c]


for t in d.tables:
    ancho_completo(t)
    repartir_columnas(t)
    bordes_apa(t)
    if not getattr(t, '_letra9', False):
        letra_tabla(t, 10)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER

# ---------------------------------------------------------------- Carátula
p0 = d.paragraphs[0]
LINEAS = [
    ("UNIVERSIDAD NACIONAL DE INGENIERÍA", "Poppins", 22, True, 6),
    ("UNIDAD DE POSGRADO FACULTAD DE CIENCIAS", "Arial", 16, True, 12),
    ("[LOGO]", None, None, None, 12),
    ("INFORME PRELIMINAR DE TESIS", "Arial", 14, True, 4),
    ("“DETECCIÓN EVOLUTIVA DE REGÍMENES DEL CICLO FINANCIERO PERUANO MEDIANTE "
     "CLASIFICACIÓN FACTORIAL JERÁRQUICA Y APRENDIZAJE AUTOMÁTICO”", "Arial", 14, True, 14),
    ("PARA OBTENER EL GRADO ACADÉMICO DE MAESTRO EN CIENCIAS CON MENCIÓN EN:", "Arial", 12, False, 0),
    ("MODELIZACIÓN MATEMÁTICA Y COMPUTACIONAL", "Arial", 12, False, 14),
    ("ELABORADA POR:", "Arial", 12, True, 6),
    ("ROBERTO CARLOS SAMANIEGO SALCEDO", "Arial", 12, True, 14),
    ("ASESOR:", "Arial", 12, True, 6),
    ("DR. SERGIO CAMIZ", "Arial", 14, True, 14),
    ("LIMA, PERÚ", "Arial", 14, True, 6),
    ("2026", "Arial", 12, True, 0),
]
for texto, fuente, tam, negrita, despues in LINEAS:
    p = d.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.space_before, pf.space_after, pf.line_spacing = Pt(0), Pt(despues), 1.0
    pf.first_line_indent = Cm(0)
    if texto == "[LOGO]":
        p.add_run().add_picture(str(AQUI / "logo_uni.png"), width=Cm(5.6))
    else:
        r = p.add_run(texto)
        r.bold = negrita
        r.font.size = Pt(tam)
        r.font.name = fuente
        r._element.rPr.rFonts.set(qn("w:hAnsi"), fuente)
        r._element.rPr.rFonts.set(qn("w:cs"), fuente)
    p0._element.addprevious(p._element)

# ---------------------------------------------------------------- Matriz de consistencia
H = ["Problema de estudio", "Problemas", "Objetivos", "Variables y dimensiones", "Diseño metodológico"]
ESTUDIO = ("La multiplicidad de indicadores macrofinancieros, con información redundante, señales "
           "divergentes y relaciones que pueden cambiar en el tiempo, impide establecer con un criterio "
           "objetivo el régimen financiero del país. Los estudios peruanos con reducción de dimensión "
           "llegan hasta 2020, no validan la segmentación en regímenes ni evalúan modelos no lineales.")
FILA1 = [
    "Problema general:\n¿Cómo construir un modelo matemático-computacional de reducción de dimensión de "
    "los indicadores macrofinancieros mensuales del Perú observados en 2007–2025 que identifique los "
    "regímenes del ciclo financiero con un criterio de segmentación explícito y validado estadísticamente, "
    "y que permita interpretarlos en términos de los indicadores originales?",
    "Objetivo general:\nConstruir un modelo matemático-computacional de reducción de dimensión de los "
    "indicadores macrofinancieros mensuales del Perú observados en 2007–2025 que identifique los regímenes "
    "del ciclo financiero con un criterio de segmentación explícito y validado estadísticamente, y que "
    "permita interpretarlos en términos de los indicadores originales.",
    "Variable dependiente:\nRegímenes del ciclo financiero (de estructura y de posición).\nDimensiones:\n"
    "- Estructura factorial global\n- Evolución de la estructura\n- Regímenes\n- Caracterización y fase",
    "Tipo de investigación: cuantitativa.\nNivel de investigación: exploratorio y descriptivo, con "
    "componente comparativo.\nDiseño: no experimental, longitudinal y retrospectivo.\nHipótesis: no se "
    "formulan, por tratarse de un estudio exploratorio y descriptivo.",
]
FILA2 = [
    "Problemas específicos:\nPE1. Estructura factorial de los indicadores.\nPE2. Evolución de la estructura.\n"
    "PE3. Partición en regímenes, contrastada y evaluada por remuestreo.\nPE4. Caracterización, fase y "
    "episodios.\nPE5. Representaciones no lineales frente a la lineal.",
    "Objetivos específicos:\nOE1. Determinar la estructura factorial (PCA y HFC).\nOE2. Caracterizar su "
    "evolución (EPCA y HFC evolutiva).\nOE3. Delimitar los regímenes con la partición de Fisher y "
    "validarla.\nOE4. Caracterizar los regímenes, su fase y su correspondencia con episodios.\nOE5. Comparar "
    "autoencoder y autoencoder LSTM con el PCA.",
    "Variable independiente:\nModelo de reducción de dimensión y segmentación temporal.\nDimensiones:\n"
    "- Representación lineal y evolutiva\n- Segmentación y validación\n- Representación no lineal",
    "Población y muestra: indicadores macrofinancieros mensuales del BCRP; 16 series, enero de 2007 a "
    "diciembre de 2025 (228 meses), muestreo intencional.\nTécnicas e instrumentos de recolección: análisis "
    "documental; base de datos congelada.\nTécnicas de análisis: PCA, HFC, EPCA, HFC evolutiva, partición "
    "de Fisher, series de referencia simuladas, remuestreo por bloques, autoencoders (R y Python).",
]
anexo1 = next(p for p in d.paragraphs if p.text.strip() == "[[MATRIZ]]")
tabla = d.add_table(rows=3, cols=5)
anchos = [4.0, 5.2, 5.2, 4.3, 6.0]
for fila_idx, valores in enumerate([H, [ESTUDIO] + FILA1, [""] + FILA2]):
    for c, v in enumerate(valores):
        celda = tabla.cell(fila_idx, c)
        celda.width = Cm(anchos[c])
        celda.text = ""
        partes = v.split("\n")
        par = celda.paragraphs[0]
        for i, linea in enumerate(partes):
            if i:
                par = celda.add_paragraph()
            run = par.add_run(linea)
            if fila_idx == 0 or (linea.endswith(":") and not linea.startswith("-")):
                run.bold = True
            elif ":" in linea and linea.split(":")[0] in (
                    "Tipo de investigación", "Nivel de investigación", "Métodos", "Diseño",
                    "Población y muestra", "Técnicas e instrumentos de recolección",
                    "Técnicas de análisis", "Hipótesis"):
                cab, resto = linea.split(":", 1)
                run.text = ""
                rb = par.add_run(cab + ":")
                rb.bold = True
                par.add_run(resto)
tabla.autofit = False
for c, a in enumerate(anchos):
    tabla.columns[c].width = Cm(a)
tabla.cell(1, 0).merge(tabla.cell(2, 0))
# Bordes completos (formato de la guía)
tblPr = tabla._tbl.tblPr
b = OxmlElement("w:tblBorders")
for lado in ["top", "left", "bottom", "right", "insideH", "insideV"]:
    e = OxmlElement(f"w:{lado}")
    e.set(qn("w:val"), "single")
    e.set(qn("w:sz"), "6")
    e.set(qn("w:color"), "000000")
    b.append(e)
tblPr.append(b)
letra_tabla(tabla, 8.5)
for celda in tabla.rows[0].cells:
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:fill"), "E7E6E6")
    celda._tc.get_or_add_tcPr().append(sh)
anexo1._element.addprevious(tabla._tbl)
nota_m = d.add_paragraph("Nota. Elaboración propia.", style=nota)
anexo1._element.addprevious(nota_m._element)
anexo1._element.getparent().remove(anexo1._element)

# ---------------------------------------------------------------- Secciones y numeración
sect_final = cuerpo.find(qn("w:sectPr"))


def cortar_seccion_en(parrafo_el):
    """Termina una sección en el párrafo dado (copia de la configuración final)."""
    s = copy.deepcopy(sect_final)
    for hijo in list(s):
        if hijo.tag in (qn("w:headerReference"), qn("w:footerReference")):
            s.remove(hijo)
    pPr = parrafo_el.find(qn("w:pPr"))
    if pPr is None:
        pPr = OxmlElement("w:pPr")
        parrafo_el.insert(0, pPr)
    pPr.append(s)


pars = d.paragraphs
i_cap1 = next(i for i, p in enumerate(pars) if p.style.name.startswith("Heading") and p.text.startswith("CAPÍTULO I."))
i_anexos = next(i for i, p in enumerate(pars) if p.style.name.startswith("Heading") and p.text.strip() == "ANEXOS")
i_anexo1 = next(i for i, p in enumerate(pars) if p.style.name.startswith("Heading") and p.text.startswith("Anexo 1"))
i_anexo2 = next(i for i, p in enumerate(pars) if p.style.name.startswith("Heading") and p.text.startswith("Anexo 2"))

# Fin de la sección preliminar: un párrafo vacío antes del Capítulo I
for indice, accion in [(i_anexo2, "fin_matriz"), (i_anexo1, "fin_cuerpo"), (i_cap1, "fin_prelim")]:
    vacio = d.add_paragraph()
    vacio.paragraph_format.space_after = Pt(0)
    pars[indice]._element.addprevious(vacio._element)
    cortar_seccion_en(vacio._element)

secciones = d.sections  # 0 preliminar, 1 cuerpo, 2 matriz (apaisada), 3 anexos


def pg_num(seccion, fmt=None, start=None):
    sp = seccion._sectPr
    for viejo in sp.findall(qn("w:pgNumType")):
        sp.remove(viejo)
    e = OxmlElement("w:pgNumType")
    if fmt:
        e.set(qn("w:fmt"), fmt)
    if start is not None:
        e.set(qn("w:start"), str(start))
    cols = sp.find(qn("w:cols"))
    if cols is not None:
        cols.addprevious(e)
    else:
        sp.append(e)


def campo_pagina(parrafo):
    run_campo(parrafo, "begin")
    r = OxmlElement("w:r")
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = " PAGE "
    r.append(it)
    parrafo._element.append(r)
    run_campo(parrafo, "separate")
    parrafo.add_run("1")
    run_campo(parrafo, "end")


for k, s in enumerate(secciones):
    s.page_width, s.page_height = (Cm(29.7), Cm(21.0)) if k == 2 else (Cm(21.0), Cm(29.7))
    s.top_margin = s.bottom_margin = Cm(2.5)
    s.left_margin = Cm(3.0) if k != 2 else Cm(2.5)
    s.right_margin = Cm(2.5)

secciones[0].different_first_page_header_footer = True
for parte in (secciones[0].first_page_footer, secciones[0].first_page_header):
    parte.is_linked_to_previous = False
    parte.paragraphs[0].text = ""
pg_num(secciones[0], "lowerRoman", 1)
pg_num(secciones[1], "decimal", 1)
for k in (0, 1):
    pie = secciones[k].footer
    pie.is_linked_to_previous = False
    pp = pie.paragraphs[0]
    pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    campo_pagina(pp)
enc = secciones[0].header
enc.is_linked_to_previous = False
pe = enc.paragraphs[0]
pe.alignment = WD_ALIGN_PARAGRAPH.RIGHT
re_ = pe.add_run("Tesis de maestría — versión del 9 de noviembre de 2026")
re_.italic = True
re_.font.size = Pt(8)
re_.font.color.rgb = RGBColor(0x59, 0x59, 0x59)

# Hoja apaisada para la matriz
m = secciones[2]
m.orientation = WD_ORIENT.LANDSCAPE

# Word actualiza los campos (índices y páginas) al abrir
ajustes = d.settings.element
u = OxmlElement("w:updateFields")
u.set(qn("w:val"), "true")
ajustes.append(u)

d.save(str(SALIDA))
print("Guardado:", SALIDA, "| tablas en lista:", len(rotulos["tabla"]) + 1,
      "| figuras:", len(rotulos["figura"]))
