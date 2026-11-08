# Informe preliminar con la estructura de la Guía N.° 2 (UNI, 2023)

Reorganiza el avance de la rama `avance-mmc102` según la estructura de tesis de maestría de
investigación de la Guía N.° 2 de la Escuela de Posgrado UNI: carátula, cuerpo preliminar,
capítulos I–IV, referencias APA 7 y matriz de consistencia (Anexo I).

Generación, desde la raíz del repositorio (requiere pandoc y python-docx):

    python3 tesis/informe_preliminar_uni/build.py . Informe_preliminar_tesis_UNI.docx

Las cifras se leen de `tesis/_cifras.yml`; las tablas, de `tesis/avance/_avance_tabla_*.md`, y
las figuras, de `tesis/avance/figuras/` (copiarlas a `fig/` junto al script). Resultados
preliminares: solo en Word, no se publican en el sitio.
