# Borrador de tesis (MMC102 — Seminario de Tesis II)

- `_capitulos/NN_*.qmd`: cuerpo de cada capítulo. Los subtítulos empiezan en `##`. Es el único
  lugar donde se redacta.
- `NN_*.qmd`: página web de cada capítulo (solo incluye el cuerpo).
- `borrador_completo.qmd`: reúne los capítulos y genera HTML y **.docx** con
  `plantilla_uni.docx`.
- `referencias.bib`: **solo** las obras citadas en el borrador, cada una con ficha en `papers/`.
- `registro_verificacion.md`: referencias con verificación pendiente.
- `apa.csl`: estilo APA 7 (CSL oficial); con `lang: es` genera «y», «et al.» y «Recuperado de».
- `herramientas/generar_plantilla_docx.py`: regenera la plantilla Word (Arial 12, interlineado
  1,5, márgenes de 3 cm a la izquierda y 2,5 cm en el resto, número de página centrado).

**Formato institucional:** las «Pautas para redactar el Trabajo de Tesis de Maestría de la UNI»
que cita MMC102 aún no están en el proyecto. La guía disponible (2018) es de la Universidad
Nacional del Centro del Perú y se usa solo de forma provisional para el formato. Debe
reemplazarse por la pauta de la UNI.

Generar el Word:

```
quarto render tesis/borrador_completo.qmd --to docx
```
