# Informe preliminar con la estructura de la Guía N.° 2 (UNI, 2023)

Reorganiza el avance de la rama `avance-mmc102` según la estructura de tesis de maestría de
investigación de la Guía N.° 2 de la Escuela de Posgrado UNI: carátula, cuerpo preliminar,
capítulos I–IV, referencias APA 7 y matriz de consistencia (Anexo I).

Generación, desde la raíz del repositorio (requiere pandoc y python-docx):

    python3 tesis/informe_preliminar_uni/build.py . Informe_preliminar_tesis_UNI.docx

Las cifras se leen de `tesis/_cifras.yml`; las tablas, de `tesis/avance/_avance_tabla_*.md`, y
las figuras, de `tesis/avance/figuras/` (copiarlas a `fig/` junto al script). Resultados
preliminares: solo en Word, no se publican en el sitio.

## Versión del 8 de noviembre de 2026 (tras la revisión del asesor-agente)

Antes de compilar, generar los resultados de los programas del asesor y las tablas auxiliares:

    python3 tesis/informe_preliminar_uni/resultados_camiz.py
    python3 tesis/informe_preliminar_uni/sensibilidad_media_movil.py
    python3 tesis/informe_preliminar_uni/tablas_extra.py

Todo se escribe en `data/results/final/informe_uni/` (figuras en `fig/`, que deben copiarse
a `fig/` junto al script). La revisión que motivó esta versión está en
`asesoria/2026-11-08_revision-informe-preliminar.md`. Las ecuaciones se ven en Word; para
revisarlas en un PDF con LibreOffice hace falta el módulo `libreoffice-math`.
