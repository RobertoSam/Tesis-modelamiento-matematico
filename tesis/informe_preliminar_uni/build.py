# -*- coding: utf-8 -*-
"""Construye el informe preliminar de tesis con la estructura de la Guía N.° 2 (UNI, 2023).

Pasos:
1. Sustituye en el Markdown las cifras ({{clave}}) leídas de tesis/_cifras.yml y las tablas
   generadas por el pipeline (tesis/avance/_avance_tabla_*.md).
2. Convierte a .docx con pandoc (citas APA 7 con citeproc y la plantilla del repositorio).
3. Ajusta el .docx con python-docx: carátula UNI, índices con campos de Word, saltos de página,
   numeración romana/arábiga, rótulos APA de tablas y figuras, referencias con sangría francesa,
   matriz de consistencia en hoja apaisada.

Uso: python3 build.py <ruta_repo> <salida.docx>
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

# ---------------------------------------------------------------- 1. Sustituciones
cifras = yaml.safe_load(open(REPO / "tesis/_cifras.yml", encoding="utf-8"))["cifras"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]


def mes_texto(aaaa_mm):
    """'2008-12' -> 'diciembre de 2008'."""
    a, m = aaaa_mm.split("-")
    return f"{MESES[int(m) - 1]} de {a}"


cortes = cifras["datacionCortesPrincipal"].split()
textos = [mes_texto(c) for c in cortes]
cifras["datacionCortesTexto"] = ", ".join(textos[:-1]) + " y " + textos[-1]
cifras["datacionCorteFrecMinTexto"] = mes_texto(cifras["datacionCorteFrecMin"])
cifras["epcaTransicionesSesenta"] = ", ".join(
    mes_texto(c.strip()) for c in cifras["epcaTransicionesSesenta"].split(","))
NUM_EN = {"16": "Sixteen", "17": "Seventeen"}
cifras["nSeriesEn"] = NUM_EN[cifras["nSeries"]]
cifras["inerciaPCUnoNivelesEn"] = cifras["inerciaPCUnoNiveles"].replace(",", ".")
cifras["oePMinEn"] = cifras["oePMin"].replace(",", ".")

# Resultados de los programas del asesor (resultados_camiz.py)
CAMIZ = Path(sys.argv[3]) if len(sys.argv) > 3 else AQUI / "camiz"
cz = pd.read_csv(CAMIZ / "camiz_resumen.csv", index_col=0)["valor"]


def coma(x, dec):
    return f"{float(x):.{dec}f}".replace(".", ",")


MESES_EN = ["January", "February", "March", "April", "May", "June", "July", "August",
            "September", "October", "November", "December"]
cortes_aede = cz["aede_cortes"].split()
txt = [mes_texto(c) for c in cortes_aede]
cifras["czAedeCortesTexto"] = ", ".join(txt[:-1]) + " y " + txt[-1] if len(txt) > 1 else txt[0]
cifras["czAedeCortesEn"] = " and ".join(f"{MESES_EN[int(c[5:]) - 1]} {c[:4]}" for c in cortes_aede)
cifras["czAedeK"] = str(int(float(cz["aede_k_ch"])))
cifras["czAlturaRaiz"] = coma(cz["altura_raiz"], 2)
cifras["czClasesCorte"] = str(int(float(cz["clases_corte_07"])))
cifras["czInerciaRepr"] = coma(cz["inercia_repr_pct"], 1)
cifras["czInerciaJer"] = coma(cz["inercia_jerarquia_pct"], 1)
cifras["czLambdaMin"] = coma(cz["aede_lambda1_min"], 2)
cifras["czLambdaMax"] = coma(cz["aede_lambda1_max"], 2)
cifras["czFechaLambdaMin"] = mes_texto(cz["fecha_lambda1_min"])
cifras["czClaedeVentanas"] = str(int(float(cz["claede_ventanas"])))
cifras["czClaedeMin"] = str(int(float(cz["claede_clases_min"])))
cifras["czClaedeMax"] = str(int(float(cz["claede_clases_max"])))
cifras["czClaedeModa"] = str(int(float(cz["claede_clases_moda"])))
cifras["czClaedeProp3"] = coma(cz["claede_prop_3clases"], 2)

md = open(AQUI / "informe_preliminar.md", encoding="utf-8").read()
faltan = set()


def reemplazar(m):
    clave = m.group(1)
    if clave not in cifras:
        faltan.add(clave)
        return m.group(0)
    return str(cifras[clave])


md = re.sub(r"\{\{(\w+)\}\}", reemplazar, md)
if faltan:
    sys.exit(f"Cifras no encontradas: {faltan}")

TABLAS = {"TABLA_SERIES": "series", "TABLA_CARGAS": "cargas", "TABLA_HFC": "hfc",
          "TABLA_REGIMENES": "regimenes"}
for marca, nombre in TABLAS.items():
    t = open(REPO / f"tesis/avance/_avance_tabla_{nombre}.md", encoding="utf-8").read().strip()
    md = md.replace(f"[[{marca}]]", t)
md = md.replace("| Etiqueta preliminar |", "| Fase (preliminar) |")


def csv_a_md(nombre):
    """Tabla Markdown desde un CSV de resultados, con coma decimal."""
    t = pd.read_csv(CAMIZ / nombre)
    if "Une" in t.columns:
        t = t.drop(columns=["Une"])
    def fmt(v):
        if isinstance(v, float):
            return f"{v:.3f}".rstrip("0").rstrip(".").replace(".", ",") if abs(v) < 1000 else f"{v:,.1f}"
        return str(v)
    filas = ["| " + " | ".join(t.columns) + " |", "|" + "---|" * len(t.columns)]
    for r in t.itertuples(index=False):
        filas.append("| " + " | ".join(fmt(v) for v in r) + " |")
    return "\n".join(filas)


md = re.sub(r"\[\[CSV:([\w.]+)\]\]", lambda m: csv_a_md(m.group(1)), md)

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
marc = E("Marcador")
marc.font.italic = True
marc.font.color.rgb = RGBColor(0x59, 0x59, 0x59)

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
    minimos, pesos = [], []
    for col in tabla.columns:
        textos = [c.text for c in col.cells]
        palabra = max((len(w) for t in textos for w in t.split()), default=4)
        minimos.append(0.22 * palabra + 0.35)
        pesos.append(max(len(t) for t in textos))
    libre = max(0.0, total_cm - sum(minimos))
    anchos = [Cm(m + libre * w / sum(pesos)) for m, w in zip(minimos, pesos)]
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
    letra_tabla(t, 10)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER

# ---------------------------------------------------------------- Carátula
p0 = d.paragraphs[0]
LINEAS = [
    ("UNIVERSIDAD NACIONAL DE INGENIERÍA", "Poppins", 22, True, 6),
    ("UNIDAD DE POSGRADO FACULTAD DE CIENCIAS", "Arial", 16, True, 12),
    ("[LOGO]", None, None, None, 12),
    ("TESIS", "Arial", 14, True, 4),
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
H = ["Problema de estudio", "Problemas", "Objetivos", "Hipótesis", "Variables y dimensiones",
     "Diseño metodológico"]
ESTUDIO = ("Los indicadores macrofinancieros del BCRP están muy correlacionados, comparten una "
           "tendencia común y su relación puede cambiar en el tiempo. Los trabajos peruanos previos "
           "no clasifican los regímenes en fases, no usan aprendizaje profundo ni cubren el período "
           "posterior a 2020.")
FILA1 = [
    "Problema general:\n¿Cómo identificar, fechar y caracterizar los regímenes del ciclo financiero "
    "peruano a partir de los indicadores mensuales del BCRP, combinando métodos exploratorios "
    "evolutivos y aprendizaje automático, y cómo se comparan esos métodos entre sí?",
    "Objetivo general:\nProponer y evaluar una metodología que combine PCA, HFC y EPCA con "
    "autoencoders y redes LSTM para identificar cambios de régimen en el ciclo financiero peruano "
    "con indicadores del BCRP.",
    "Hipótesis general:\nLa estructura conjunta de los indicadores del BCRP (2007–2025) contiene "
    "regímenes identificables, organizados en pocos bloques de series, cuyos cortes se corresponden "
    "con episodios fechados externamente; el aprendizaje profundo aporta información que el PCA no "
    "capta.",
    "Variable independiente:\nMetodología híbrida de reducción dimensional y aprendizaje automático.\n"
    "Dimensiones:\n- Métodos exploratorios (PCA, HFC, EPCA, Fisher)\n- Aprendizaje profundo "
    "(autoencoder, LSTM-autoencoder)",
    "Tipo de investigación: cuantitativa.\nNivel de investigación: exploratorio y descriptivo, "
    "con componente comparativo.\nMétodos: analítico e inductivo, con contrastación frente a nulos "
    "simulados.\nDiseño: no experimental, longitudinal y retrospectivo.",
]
FILA2 = [
    "Problemas específicos:\nPE1. Base de datos trazable del BCRP.\nPE2. Estructura de correlación, "
    "grupos y estabilidad.\nPE3. Representaciones latentes no lineales.\nPE4. Datación, fases y "
    "correspondencia con episodios.\nPE5. Comparación de métodos.",
    "Objetivos específicos:\nOE1. Construir la base de datos mensual del BCRP.\nOE2. Analizar "
    "correlación, grupos y estabilidad con PCA, HFC y EPCA.\nOE3. Construir representaciones "
    "latentes con autoencoders y LSTM.\nOE4. Fechar regímenes, clasificarlos en fases y "
    "contrastarlos con episodios.\nOE5. Comparar los métodos, también en un contexto simulado.",
    "Hipótesis específicas:\nHE1. La estructura de correlación no es constante.\nHE2. Las series "
    "forman pocos grupos homogéneos.\nHE3. Los regímenes corresponden a episodios externos.\n"
    "HE4. El aprendizaje profundo complementa al PCA.",
    "Variable dependiente:\nRegímenes del ciclo financiero peruano.\nDimensiones:\n- Estructura "
    "de correlación\n- Grupos de series\n- Estabilidad temporal\n- Datación y fase",
    "Población y muestra: indicadores mensuales del BCRP; 16 series, enero de 2007 a diciembre de "
    "2025 (228 meses), selección por criterio.\nTécnicas e instrumentos de recolección: análisis "
    "documental; base de datos congelada.\nTécnicas de análisis: PCA, HFC, EPCA, partición de "
    "Fisher, autoencoders y LSTM; nulos simulados y bootstrap por bloques (Python y R).",
]
anexo1 = next(p for p in d.paragraphs if p.text.strip() == "[[MATRIZ]]")
tabla = d.add_table(rows=3, cols=6)
anchos = [3.2, 4.3, 4.3, 4.3, 3.9, 5.0]
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
                    "Técnicas de análisis"):
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
nota_m = d.add_paragraph("Nota. Autor: Roberto Carlos Samaniego Salcedo. Elaboración propia "
                         "con el formato del Anexo I de la Guía N.° 2.", style=nota)
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
re_ = pe.add_run("Informe preliminar de tesis — versión del 7 de noviembre de 2026")
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
