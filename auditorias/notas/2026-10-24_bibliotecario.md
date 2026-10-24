# Nota del bibliotecario · Iteración 3b (fase 0) · 24 de octubre de 2026

**Agente:** bibliotecario (`.claude/agents/bibliotecario.md`). **Rama:** `iteracion-3b`, sin commit ni
push (los hace el orquestador). **Encargo:** tareas B1 a B4 de `asesoria/2026-10-21_plan-iteracion-3b.md`
(sección 4), con prioridad en B1. Rigen D7 (fechado por el evento o anuncio externo; ±3/±6 meses;
un episodio sin fin con fuente es puntual) y D8 (nulo mixto con HAC de Newey-West).

**Archivos modificados:** `tesis/referencias.bib` (19 entradas nuevas), `tesis/registro_verificacion.md`,
19 fichas nuevas en `papers/` y 13 fichas existentes (ver §5). No se tocó `R/`, `src/`, `notebooks/`,
`data/`, `tesis_latex/` ni `tesis/_capitulos/`.

## 0. Condiciones de acceso

- Como en 3a, la verificación se hizo con WebSearch/WebFetch. **No fueron accesibles:** bcrp.gob.pe
  (el PDF del Reporte de Inflación de junio de 2013 devolvió solo metadatos, sin texto), gob.pe
  (ficha del D. S. 044-2020-PCM), who.int/news (sede de la OMS), ScienceDirect, HAL (bloqueo
  antibots), econbiz, el PDF del texto del acuerdo de «fase uno» en ustr.gov, la versión HTML/PDF
  de MDPI con las referencias de Camiz y Pillar (2018) y el repositorio abierto del Banco Mundial.
  No se buscaron rutas para sortear esos bloqueos.
- Regla aplicada: un dato visto solo en una fuente secundaria (RePEc, documentación de software,
  bibliografías especializadas) queda en `verificar = {VERIFICAR: …}`.

## 1. B1 · Episodios: propuesta de fechas según D7

Cada fecha sale del texto de una fuente externa, nunca de las series ni de un indicador (regla 6).

| Episodio | Inicio (clave) | Fin (clave) | Tipo |
|---|---|---|---|
| Crisis financiera global | 2008-09 (`lehman_brothers_2008`) | 2009-06 (`nber_2010`) | Período |
| *Taper tantrum* | 2013-05 (`bernanke_2013`) | 2013-12 (`reserva_federal_2013`) | Período |
| COVID-19 | 2020-03 (`oms_2020b`) | 2020-04 (`nber_2021`) | Período |
| Colapso de las materias primas | 2014-06 (`stocker_et_al_2015`) | 2016-01 (`fmi_2016`) | Período |
| Kuczynski / Odebrecht | 2018-03 (`congreso_2018`) | — | Puntual |
| Guerra comercial EE. UU.–China | 2018-06 (`ustr_2018`) | 2020-01 (`ustr_2020`) | Período |

Fuente de cada dato nuevo:

- **COVID-19, fin 2020-04 (`nber_2021`).** NBER, comunicado del 19-07-2021, leído en nber.org: «a
  trough in monthly economic activity occurred in the US economy in April 2020». Usa el mismo
  criterio que el fin de la crisis global (valle del NBER). **Alternativas fichadas:** inicio
  2020-01 con `oms_2020a` (ESPII, dentro de ±3 meses de 2020-03) y fin 2023-05 con `oms_2023`
  (fin de la ESPII; leído en la página de la Oficina Regional para Europa). Este último se
  descarta como principal porque deja un episodio de más de tres años, poco discriminante.
- **D. S. 044-2020-PCM (`pcm_2020`).** El título completo y la fecha de publicación (15-03-2020)
  constan en el D. S. 072-2020-PCM, leído en busquedas.elperuano.pe. El texto (art. 1: estado de
  emergencia por 15 días calendario; «Dado en la Casa de Gobierno, en Lima, a los quince días del
  mes de marzo del año dos mil veinte») se leyó en una reproducción no oficial (jurispol.pe). Es
  un evento interno: bajo D7 da contexto, no fecha.
- **Materias primas.**
  - *Metales (`fmi_2015b`).* Recuadro del WEO de octubre de 2015, pp. 38–50, leído en imf.org:
    «metal prices have been declining since 2011» (p. 40). Da el año, sin mes: el inicio mensual
    sigue siendo el del petróleo (2014-06). **Advertencia para el texto:** para los metales que
    exporta el Perú, la caída empieza antes que el episodio fechado.
  - *Fin (`fmi_2016`).* *Commodity Market Monthly* del FMI, 15-03-2016: «Metals prices rose by 5.0
    percent in February, first increase in five months»; el índice general sube por primera vez en
    nueve meses. El fin se toma de esa frase del FMI (el último mes de caída es 2016-01), no del
    mínimo del índice del cuadro 2, que solo concuerda.
  - *Concordancia (`baffes_streifel_2016`).* Blog del Banco Mundial del 26-07-2016: «multi-year lows
    plumbed in January». Al ser un blog, sirve solo como concordancia.
- **Guerra comercial, fin 2020-01 (`ustr_2020`).** Hoja informativa de la USTR leída en ustr.gov:
  encabezado «… / JANUARY 15, 2020 / FACT SHEET» y «On January 15, 2020, the United States and China
  signed an historic and enforceable agreement». Con esto se cierra el pendiente de 3a, cuando la
  fecha solo tenía fuentes secundarias.
- **Kuczynski.** No hay fuente nueva. Se propone tratarlo como **puntual**, con la renuncia, porque
  el cap. 2 nombra el episodio como «renuncia de Kuczynski». Como sensibilidad queda un período de
  2016-12 (`doj_2016`, evento externo) a 2018-03. La juramentación (`congreso_2016`) no es un
  evento del episodio.

**Advertencias para D9 y L1:**

1. El fin de la guerra comercial (2020-01) y el inicio del COVID-19 (2020-03) distan dos meses.
   Con ±3 meses, una transición en ese tramo no puede atribuirse a uno solo.
2. Los inicios 2008-07 y 2013-04 y los fines 2016-03, 2020-09 y 2020-12 (archivos `06a`, `06b`,
   Rmd y `modelos_dl.py`) **no tienen fuente**. Desaparecen al unificar.
3. **La propuesta no es una decisión metodológica nueva:** aplica D7. Donde hay dos fuentes
   posibles (COVID-19 al inicio y al fin; Kuczynski como puntual o como período), la tabla da la
   que mejor encaja con D7 y la alternativa queda fichada. Si el orquestador o Roberto prefieren
   la alternativa, las claves ya existen.

## 2. B2 · Fuentes que 3b usa

| Pedido | Resultado | Clave |
|---|---|---|
| Camiz y Diblasi (2013) | **No localizada** tras cuatro búsquedas. La descripción «Actas Coloquio Argentino de Estadística» viene del anexo C del manuscrito, no verificado. | — (pedir al Dr. Camiz) |
| Kish (1965), página de $1/\sum\omega^2$ | **Sin resultado.** Solo fuentes secundarias (viñeta de PracTools, Wikipedia), sin una página verificable. | `kish_1965` (sin cambios) |
| Vara quebrada | Fuente secundaria revisada por pares: Camiz y Pillar (2018) atribuyen la regla a Frontier (1976), que no se localizó en fuente oficial. | `camiz_pillar_2018` |
| Criterio de Rencher | **Precisado:** generalización de Rencher de la prueba de Bartlett, que contrasta con χ² si cada valor propio sucesivo difiere de los restantes (Camiz y Pillar, 2018). Fuente directa candidata: 3.ª ed., §12.6, p. 423 (preliminar). | `camiz_pillar_2018`, `rencher_christensen_2012` |
| Denimal (2001, 2007) | 2007 verificado en Numdam y corregido (título, revista y pp. 29–63). 2001 es una presentación en el ASMDA de Compiègne sin actas localizadas: sin ficha. | `denimal_2007` |
| Bruynooghe | *Cahiers de l'Analyse des Données*, 3(1), 7–33, 1978 (Numdam). | `bruynooghe_1978` |
| Lavit (1988) | Masson, París, 1988 (catálogo de Patras); autoría según la bibliografía de Leiden. | `lavit_1988` |
| Tukey (1977) | Addison-Wesley, Reading (MA), 1977 (dos catálogos). | `tukey_1977` |
| Jolliffe (2002) | 2.ª ed., Springer, DOI 10.1007/b98835 (SpringerLink). No se verificó la página del umbral 0,7. | `jolliffe_2002` |
| Atoche Murrieta (2022) | **Fichada.** Registro del Repositorio PUCP (handle 20.500.12404/23378, 22-09-2022) y portada del PDF (Magíster en Estadística, asesor Sergio Camiz). El título difiere entre la portada («2000-2020») y el registro («2000-2021»). | `atoche_murrieta_2022` |

**Hallazgo para el redactor:** en la parte leída, Atoche Murrieta (2022) usa pesos gaussianos con
*k* = 3, elegido «tras una experimentación con valores variados», y no cita a Camiz y Diblasi.

## 3. B3 · Propuestas del asesor

| Propuesta | Resultado | Clave |
|---|---|---|
| Estimador HAC de Newey-West (D8) | **Encontrada.** *Econometrica*, 55(3), 703–708, mayo de 1987 (Econometric Society, JSTOR 1913610). Pendientes: orden de los autores (la Econometric Society lista primero a West) y DOI sin comprobar. **Los 12 rezagos y el umbral |t| > 2 son elecciones de la tesis.** | `newey_west_1987` |
| Estabilidad de clasificaciones jerárquicas bajo remuestreo (OE5) | **Encontrada, sin verificar en la editorial.** Hennig (2007), *CSDA*, 52(1), 258–271 (RePEc y `fpc`). Trata grupos de observaciones; la HFC agrupa variables, y la analogía debe declararse. | `hennig_2007` |
| Contraste del RV bajo independencia o por permutación | **Encontrada, sin verificar en la editorial.** Josse, Pagès y Husson (2008), *CSDA*, 53(1), 82–91 (RePEc). Supone filas intercambiables: es un antecedente, no el nulo de D7. | `josse_pages_husson_2008` |
| Bootstrap por bloques **conjunto** multivariado (D7) | **No encontrada como tal.** Lahiri (2003), con metadatos verificados, es el manual del bootstrap por bloques, pero no se verificó que trate los inicios de bloque comunes a todas las series. Esa afirmación lleva `\pendiente` y no se le atribuye. | `lahiri_2003` (parcial) |

## 4. Documentos para que Roberto los descargue a mano

**BCRP** (Incapsula bloquea el acceso automático). Con D7 ya no son necesarios para fechar; sirven
para describir el impacto en el Perú en el texto, si el redactor lo quiere. Las URL salen del
buscador:

1. Memoria 2008: https://www.bcrp.gob.pe/docs/Publicaciones/Memoria/2008/Memoria-BCRP-2008.pdf
2. Reporte de Inflación de marzo de 2009: https://www.bcrp.gob.pe/docs/Publicaciones/Reporte-Inflacion/2009/marzo/Reporte-Inflacion-Marzo-2009.pdf
3. Reporte de Inflación de junio de 2013: https://www.bcrp.gob.pe/docs/Publicaciones/Reporte-Inflacion/2013/junio/reporte-de-inflacion-junio-2013.pdf
4. Reporte de Inflación de diciembre de 2015: https://www.bcrp.gob.pe/docs/Publicaciones/Reporte-Inflacion/2015/diciembre/reporte-de-inflacion-diciembre-2015.pdf
5. Reporte de Inflación de marzo de 2016: https://www.bcrp.gob.pe/docs/Publicaciones/Reporte-Inflacion/2016/marzo/reporte-de-inflacion-marzo-2016.pdf
6. Reporte de Inflación de junio de 2020: https://www.bcrp.gob.pe/docs/Publicaciones/Reporte-Inflacion/2020/junio/reporte-de-inflacion-junio-2020.pdf
7. Memoria 2020: https://www.bcrp.gob.pe/docs/Publicaciones/Memoria/2020/memoria-bcrp-2020-4.pdf

**Otros documentos que cerrarían pendientes:**

8. Camiz y Diblasi (2013): pedir la referencia exacta o el PDF al Dr. Camiz.
9. Kish (1965), *Survey sampling*: capítulo y página del tamaño efectivo con pesos.
10. Página impresa de Newey y West (1987), en JSTOR 1913610, para el orden de los autores.
11. Frontier (1976), vara quebrada, y las referencias [3] y [10] del PDF de Camiz y Pillar (2018): https://doi.org/10.3390/math6110269
12. World Bank, *Commodity Markets Outlook*, julio de 2016, que reemplazaría al blog
    `baffes_streifel_2016`.
13. El D. S. 044-2020-PCM en gob.pe (https://www.gob.pe/institucion/pcm/normas-legales/460472-044-2020-pcm) o en *El Peruano*, para la URL oficial.
14. Declaración de la OMS del 5-05-2023 en la página de la sede (who.int/news).

## 5. B4 · Registro y conteos

**Fichas existentes modificadas:**

- `camiz_et_al_2020`: corrección de los metadatos de Denimal (2007).
- `ustr_2018` y `stocker_et_al_2015`: remiten a las fuentes nuevas.
- Las 12 fichas de episodios de 3a: la línea «la convención no está decidida (decisión I)» se
  sustituyó por la referencia a D7.

**Registro:**

- Se actualizaron 9 filas: Atoche Murrieta, vara quebrada / Rencher, Jolliffe, Denimal, Camiz y
  Diblasi, Tukey, Lavit, Bruynooghe y Kish.
- Se añadieron 5 filas: `newey_west_1987`, `josse_pages_husson_2008`, `hennig_2007`, `lahiri_2003`
  y una fila de metadatos menores de las fuentes de episodios nuevas.
- Se reescribió la tabla de episodios con la propuesta según D7.

**Marcas nuevas de D1–D12 y L1–L4:**

- Al cierre de esta tarea solo están hechas **D1** (`f1c68f8`) y **D2** (`fd17c24`).
- Las marcas que D1 reescribió remiten a obras que ya tenían fila; D2 no añadió marcas.
- **No hay marcas nuevas que registrar todavía.** B4 tendrá que repetirse cuando D3–D12 y L1–L4
  produzcan marcas. Las filas de Newey-West, Josse et al., Hennig y Lahiri ya quedan listas para
  recibirlas.

| Medida | Antes | Después |
|---|---|---|
| Registro, tabla de obras: filas abiertas | 46 (de 51) | 46 (de 56) |
| Registro, tabla de obras: filas cerradas | 5 | 10 |
| Registro, episodios: filas abiertas | 6 | 6 (fuentes completas; abiertas hasta la unificación de D9) |
| Registro, `\pendiente` no bibliográficos | 4 | 4 |
| **Total de filas abiertas** | **56** | **56** |
| `.bib`: entradas | 48 | 67 |
| `.bib`: entradas con `verificar` | 32 | 41 |

El total no baja por dos motivos. Hay 5 obras cerradas en metadatos (Jolliffe, Denimal, Tukey,
Bruynooghe y Lahiri), pero entran 5 filas nuevas de B3 y de los episodios. Además, las 6 filas de
episodios pasan de «fuente o fin pendiente» a «unificación pendiente», un estado que solo cierra
D9.

**Marcas en los documentos que ya pueden cambiar** (tarea del redactor y del editor en L1 y E1; el
bibliotecario no las toca). Atoche Murrieta, Jolliffe, Denimal, Bruynooghe, Tukey y Lavit tienen
ficha. La vara quebrada y Rencher pueden citarse a través de `camiz_pillar_2018`. Los cinco
`\pendiente` de `sec:validacion` pueden pasar a citas fichadas con las claves de §1. Hoy, la tesis
tiene 22 `\pendiente` y 34 `\verificar`, el informe 18 `[CITA PENDIENTE]` y el Rmd 38 `VERIFICAR`.

## 6. Comprobaciones

- `quarto render` (citeproc + `tesis/apa.csl`) de las 19 claves nuevas: sin avisos, y ninguna
  marca VERIFICAR en la bibliografía.
- Las 19 fichas nuevas renderizan por separado sin avisos.
- **No se pudo probar con biber:** `biblatex.sty` no está instalado en este entorno. El auditor
  debe compilar `tesis_latex/` con `latexmk`. Las entradas siguen las convenciones de 3a:
  `verificar` en lugar de `note`, instituciones entre llaves dobles y fechas ISO.
