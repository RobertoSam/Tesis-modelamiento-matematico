# Bibliotecario · 29 de octubre de 2026 · Iteración 3b, vuelta 1 (hallazgo M-01)

**Alcance.** Solo `tesis/registro_verificacion.md`. No se tocaron `tesis_latex/`, el informe, el Rmd
ni `tesis/referencias.bib` (no se halló ningún error en el `.bib`). N-02 no se resolvió: depende de
una decisión de Roberto y solo se dejó registrado como abierto.

## Qué se hizo

Se rehízo B4 sobre el estado de `e97530c`, contra las marcas reales de cada documento:

1. **Filas nuevas:** Frontier (1976), Said y Dickey (1984), fuente del bootstrap por bloques
   conjunto, `bernanke_2013` y `congreso_2018` (ambas con `\verificar` desde L1). En la tabla no
   bibliográfica: «Qué vía mide qué» (`sec:met-vias`) y AE/LSTM con 16 series
   (`sec:met-validacion`), con sus recuadros del informe, y el recuadro del resumen del informe.
   La fila «capítulo 3 por redactar» queda cerrada (L3).
2. **Columna de marcas corregida** en `atoche_murrieta_2022`, `camiz_pillar_2018` y
   `rencher_christensen_2012`, `jolliffe_2002`, `denimal_2007`, `tukey_1977`, `lavit_1988`,
   `bruynooghe_1978`, `kish_1965`, `newey_west_1987`, `hennig_2007`, `lahiri_2003`, `kunsch_1989`,
   `dickey_fuller_1979`, `kwiatkowski_et_al_1992` y `hubert_arabie_1985`. Se corrigió además la nota
   de Baldi y Hornik en el informe (`v2-bh`, no `v2-bk`).
3. **RmdF registrado:** nueva abreviatura para `R/ciclo_financiero_final.Rmd`; sus 25 marcas
   `[VERIFICAR]` quedan asignadas a filas (desglose al final del registro). El Rmd de exploración
   se declara congelado (D15): sus marcas se registran y no se corrigen.
4. **Episodios:** se retiraron los anuncios obsoletos («cinco `\pendiente`», «unificación
   pendiente (D9)», NB05 celdas 1 y 16, «confirmar al cerrar D9»). La tabla ahora muestra la fecha
   del archivo único, la clave de cada extremo y el estado tras D9 (`3c416c2`) y L1 (`f904b5c`).
   Las marcas que quedan en los antecedentes (Rmd de exploración, 10; `06a`, 4; `06b`, 6) se listan
   como congeladas.
5. **Conteo antes/después** con `git grep -o` sobre `4624802` (origin/main), `d1bf179` y
   `e97530c`. Patrones: `\\verificar\{` y `\\pendiente\{` en `tesis_latex/capitulos/*.tex`;
   `^\[\^[^]]+\]: VERIFICAR`, `\[CITA PENDIENTE` y `callout-note title="Pendiente"` en
   `tesis/_capitulos/*.qmd`; `VERIFICAR` en el RmdF, el Rmd, `src/*.py`, NB05, `06a`/`06b` y
   `modelos_dl.py`. Resultado en la tesis: `\pendiente`, de 22 a 14; `\verificar`, de 34 a 51.
   La lista de marcas cerradas, acotadas y nuevas coincide con la diferencia.

## Hallazgos para otros agentes (no corregidos aquí)

- **`fmi_2015b` sin marca.** Se cita en `sec:validacion` de la tesis y del informe sin `\verificar`
  ni nota, aunque su entrada del `.bib` tiene `verificar` (DOI del informe completo no comprobado
  en doi.org). Le corresponde al redactor LaTeX y al editor del informe; otra salida es que el
  bibliotecario compruebe el DOI en una vuelta próxima.
- **RmdF, menciones sin marca (código y texto):** Fisher (1958) y Robert y Escoufier (1976) en
  comentarios del chunk `funciones`, y «el $n$ efectivo de Kish» en la sección 4 y en la 4.2, sin
  año ni marca. Le corresponden al desarrollador. Son menores: las tres obras tienen ficha y
  entrada en el `.bib`.

## Pendiente

- N-02: falta definir qué significa «externo» en `def:episodio`. Lo decide Roberto y lo redacta el
  redactor LaTeX; después, el bibliotecario ajusta `congreso_2018`, `pcm_2020` y el registro.
- Ninguna verificación se cerró en esta vuelta, porque no se consultaron fuentes nuevas.
