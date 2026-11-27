# Nota del bibliotecario — 27-11-2026 (vuelta 2 de la iteración 3c, fase 0: F0-5 y F0-6)

Rama `iteracion-3c`, commit de partida `402f6f3`. `origin/main` en `1bb4dcb` (después de `git fetch`);
*merge-base* `b893b23`. Encargo: tareas F0-5 y F0-6 de `asesoria/2026-11-26_plan-cierre-iteracion-3c.md`
(secciones 5.1 y 5.3, criterio 4). **No se modificó ningún `.bib`**: `git diff 7c58906 --
tesis/referencias.bib` sale vacío. No se tocaron `tesis_latex/`, `tesis/` (salvo el registro),
`decisiones.qmd`, `CLAUDE.md`, `data/`, `src/`, `R/` ni `notebooks/`. Sin commit ni push (lo hace el
orquestador).

## 1. F0-5 · Cotejo de `camiz_spada_2024`

### Intentos y fuente

| Fuente | Vía | Resultado |
|---|---|---|
| doi.org/10.12899/asr-2455 | WebFetch | Permiso no respondido; no se reintentó |
| doi.org/10.12899/asr-2455 con negociación de contenido (CSL-JSON) | `curl` | Proxy de la sesión: `CONNECT tunnel failed, response 403` (política de salida); no se reintentó |
| api.crossref.org/works/10.12899/asr-2455 | `curl` | 403 del proxy, igual que el anterior |
| api.crossref.org/works/10.12899/asr-2455 | WebFetch | Permiso no respondido; no se reintentó |
| journals-crea.4science.it/index.php/asr/article/view/2455 (página del artículo, hallada en el buscador) | WebFetch | 302 a creajournals.crea.gov.it/… |
| journals-crea.4science.it/…/article/download/2455/2227/8414 (PDF, hallado en el buscador) | WebFetch | 302 a creajournals.crea.gov.it/… |
| creajournals.crea.gov.it/index.php/asr/article/view/2455 (destino de la redirección, dominio oficial de la revista) | WebFetch | Permiso no respondido; no se reintentó ni se buscó otra ruta |
| cris.pucp.edu.pe (registro del artículo) | WebFetch | Página antirrobots (Anubis, «Access Denied») |
| iris.uniroma1.it, hdl 11573/507241 (buscador) | WebFetch | **Otra obra:** Camiz y Roig (2011), E-ICES 6 (ver el § 3) |
| core.ac.uk/download/354494486.pdf (buscador) | WebFetch | **Otra obra:** Camiz, Spada, Denimal y Piraino (2020), ASR 45(1), 62–75 (`camiz_et_al_2020`) |

DOAJ (artículo c45929613a3546edac0ae7ed00dfa63d) no se volvió a consultar: es base secundaria y su
contenido ya está registrado (25-11-2026: «Oct 2023», vol. 49, núm. 1, sin páginas).

### Conclusión

**Nada nuevo verificado.** El año (2023 en DOAJ, 2024 en la primera página del PDF según la ficha de
`main`), las páginas 13–23 y el DOI siguen sin cotejarse en fuente oficial. Se mantienen los datos de
la ficha y del `.bib`, sin cambios.

### Cambios en la ficha `papers/camiz_spada_2024.qmd`

- La marca `[VERIFICAR]` de la referencia ahora incluye el año: «año (2023 en DOAJ, 2024 en el PDF),
  volumen, número, páginas y DOI vistos solo en la primera página del PDF; doi.org, Crossref y la
  página de la revista no se pudieron abrir (24, 25 y 27-11-2026)».
- Se agregaron al bloque de verificación los cotejos del 25-11 (DOAJ y la discrepancia de año, que hasta
  ahora solo constaba en el registro y en la nota del 25-11) y del 27-11 (tabla anterior).
- Ningún dato bibliográfico nuevo ni cambio de contenido.

### Para W-5 y W-7

- El campo `verificar` de `tesis/referencias.bib:1251` **no** menciona el año en duda. Hay que
  agregarlo cuando el `.bib` pueda tocarse (después de la fase 0). Si el redactor cita la obra (R-4),
  el `\verificar` del texto debe decir: «año (2023 en DOAJ, 2024 en el PDF), volumen, número, páginas
  y DOI no cotejados en la revista».
- Pedido a Roberto (sin cambios): si puede abrir la página del artículo en creajournals.crea.gov.it,
  basta con el encabezado del número y la cita sugerida por la revista. También puede preguntarlo en la
  consulta al Dr. Camiz (R-8).

## 2. F0-6 · Inventario del `.bib` del informe en `main` y de las fichas en conflicto

### (a) Claves de `origin/main:tesis/informe_mmc102/referencias.bib` y `referencias_extra.bib`

Método: `git show origin/main:<ruta>`, claves extraídas con expresión regular (67 y 21 entradas; las
cuentas coinciden con las líneas que empiezan con `@`). Cotejo con las 115 claves de
`tesis/referencias.bib` y con `papers/<clave>.qmd` en la rama y en `origin/main`. Se buscó además una
ficha con otro nombre para las claves sin ficha (`ls papers`, `grep` del apellido): no la hay.

**`referencias.bib` (67 entradas): las 67 ya están en `tesis/referencias.bib` y tienen ficha.**
`baldi_hornik_1989`, `bourlard_kamp_1988`, `camiz_cerda_atoche_2026`, `camiz_et_al_2020`,
`camiz_maulucci_roig_2010`, `camiz_roig_2011`, `drehmann_borio_tsatsaronis_2012`, `fisher_1958`,
`gal_ghahramani_2016`, `gers_schmidhuber_cummins_2000`, `hinton_salakhutdinov_2006`,
`hochreiter_schmidhuber_1997`, `plaut_2018`, `robert_escoufier_1976`,
`srivastava_mansimov_salakhutdinov_2015`, `tuhin_et_al_2025`, `vincent_et_al_2008`, `bartlett_1950`,
`bartlett_1951`, `benzecri_1973`, `calinski_harabasz_1974`, `dickey_fuller_1979`, `eckart_young_1936`,
`granger_newbold_1974`, `horn_1965`, `hubert_arabie_1985`, `kaiser_1960`, `kaiser_1970`,
`kaiser_rice_1974`, `kish_1965`, `kunsch_1989`, `lorenzo_seva_ten_berge_2006`, `perron_1989`,
`phillips_1986`, `pyper_peterman_1998`, `tucker_1951`, `bernanke_2013`, `congreso_2016`,
`congreso_2018`, `doj_2016`, `fmi_2015`, `lehman_brothers_2008`, `nber_2010`, `oms_2020a`, `oms_2020b`,
`reserva_federal_2013`, `stocker_et_al_2015`, `ustr_2018`, `nber_2021`, `oms_2023`, `pcm_2020`,
`ustr_2020`, `fmi_2015b`, `fmi_2016`, `baffes_streifel_2016`, `atoche_murrieta_2022`, `jolliffe_2002`,
`denimal_2007`, `bruynooghe_1978`, `lavit_1988`, `tukey_1977`, `camiz_pillar_2018`,
`rencher_christensen_2012`, `newey_west_1987`, `josse_pages_husson_2008`, `hennig_2007`, `lahiri_2003`.

**`referencias_extra.bib` (21 entradas):**

| Clase | Claves |
|---|---|
| Ya en `tesis/referencias.bib` (8) | `camiz_diblasi_2013`, `camiz_spada_2024`, `kwiatkowski_et_al_1992`, `goodfellow_bengio_courville_2016`, `borio_2014`; repetidas de `referencias.bib`: `lorenzo_seva_ten_berge_2006`, `robert_escoufier_1976`, `josse_pages_husson_2008` |
| Con ficha en `papers/`, sin entrada (4) | `abdi_2010`, `camiz_2021_pca`, `purizaca_2023`, `torres_baltazar_2023` |
| Sin ficha, ni en la rama ni en `main` (9) | `camiz_aedeclahfac` (`@software`), `camiz_claede_2025` (`@software`), `samaniego_2026` (`@report`), `alcaraz_cabello_nivin_2024` (`@techreport`, BCRP), `winkelried_2017` (`@article`, *Revista Estudios Económicos*), `rumelhart_hinton_williams_1986`, `jolliffe_cadima_2016`, `lecun_bengio_hinton_2015`, `srivastava_et_al_2014` |

Total: 85 claves distintas = 72 en el `.bib` único + 4 con ficha y sin entrada + 9 sin ficha.

**Diferencias de campos** entre las versiones de `main` y de la rama de las 72 compartidas (tipo, `year`,
`date`, `volume`, `number`, `pages`, `doi`; script de comparación en el directorio temporal de la
sesión, no versionado):

- `camiz_diblasi_2013`: `@misc` en `main`, `@presentation` en la rama (cambio del 25-11-2026).
- `kwiatkowski_et_al_1992`: DOI `…90104-Y` en `main` y `…90104-y` en la rama (los DOI no distinguen
  mayúsculas: no es una discrepancia de contenido).
- `lorenzo_seva_ten_berge_2006`: sin DOI en `main`; con DOI 10.1027/1614-2241.2.2.57 en la rama.

**Uso en el informe de `main`** (`git grep` en los `.md` de `tesis/informe_mmc102/`, sin los `.bib`;
los `.docx` no se revisaron):

- `alcaraz_cabello_nivin_2024`: se cita en `01_introduccion.md` y `02_marco_teorico.md` **sin ficha**.
- `winkelried_2017`: se cita en `02_marco_teorico.md` **sin ficha** (`papers/ciclo_economico.qmd`
  menciona «Paper de Winkelried en la *Revista de Estudios Económicos*», sin ficha propia).
- `purizaca_2023`: se cita en `02_marco_teorico.md`; tiene ficha, no tiene entrada.
- Las otras diez claves sin entrada no se citan en los `.md` (tampoco `samaniego_2026` ni los
  programas del asesor).

**Para W-7 (R-7), por prioridad:** (1) fichar y verificar `alcaraz_cabello_nivin_2024` y
`winkelried_2017`, que el informe cita; (2) incorporar `purizaca_2023` con su `verificar` (el *handle*
de la PUCP sigue pendiente); (3) `abdi_2010` y `torres_baltazar_2023` solo si se citan;
`camiz_2021_pca` no se incorpora (material docente no publicado, criterio de su ficha);
(4) `camiz_aedeclahfac`, `camiz_claede_2025` y `samaniego_2026`: `[CITA PENDIENTE]` hasta que el Dr.
Camiz diga cómo citarlos; (5) `rumelhart_hinton_williams_1986`, `jolliffe_cadima_2016`,
`lecun_bengio_hinton_2015` y `srivastava_et_al_2014` no se citan: no hace falta incorporarlos. Ningún
metadato de esas entradas de `main` se dio por verificado en esta tarea.

### (b) Nueve fichas en conflicto entre la rama y `main`

`git merge-tree --write-tree HEAD origin/main` confirma los nueve conflictos en `papers/`: seis
*add/add* (fichas creadas en `main` en `63c6914` y llevadas a la Ficha Estándar en la rama en
`f7712cc`) y tres de contenido (`fisher_1958` y `horn_1965`, `63c6914` frente a `f7712cc`;
`congreso_2018`, `23c0f8e` frente a `08c4015`). Método: lectura completa de ambas versiones; en las
tres de contenido, `git diff b893b23 origin/main` y `git diff b893b23 HEAD`; además, un script que
lista las frases de la versión de `main` que no aparecen literalmente en la de la rama (cada aviso se
revisó a mano: casi todos son reformulaciones o datos movidos a otra sección).

| Ficha | Tipo | ¿La rama pierde algo de `main`? | Detalle |
|---|---|---|---|
| `abdi_2010` | *add/add* | **Sí, menor** | Se perdió la remisión del aporte al informe: «Fuente de la definición conceptual y de la fórmula del coeficiente RV y del coeficiente de congruencia usados para comparar ventanas del EPCA y réplicas bootstrap (**§2.2.7 del informe**)». La rama conserva el contenido (sección 3, «Relevancia»), pero no el «§2.2.7». El «Falta: páginas del capítulo y DOI» de `main` está resuelto en la rama con SAGE Knowledge (verificado el 24-11). «Sage.» pasa a «SAGE Publications.» (dato de la editorial) |
| `camiz_2021_pca` | *add/add* | No | El nombre y la fecha del PDF, las secciones leídas, «apoyo docente, junto con fuentes publicadas» y «§2.2.3 y §2.2.4 del informe» están en la rama (recuadro inicial, sección 1 y sección 6) |
| `camiz_diblasi_2013` | *add/add* | No | El nombre del PDF, «Corrige el estado “no localizada”», el «Falta: datos de edición de las actas» (ahora `[VERIFICAR]`) y «§2.2.6» están en la rama |
| `camiz_spada_2024` | *add/add* | No | «Metadatos tomados de la primera página del PDF» está en el bloque de verificación; resumen y aporte, literales |
| `purizaca_2023` | *add/add* | No | El «Falta: URL del repositorio PUCP (las citas internas del PDF aparecen como “?”)» pasa al `[VERIFICAR]` y al bloque de verificación; resumen y aporte, conservados |
| `torres_baltazar_2023` | *add/add* | No | Las secciones leídas y el «Falta: URL del repositorio» están en la rama |
| `fisher_1958` | contenido | No | El recuadro de lectura de `main` está **literal** en la rama. La pregunta abierta «[Confirmar si el paper trata el caso multivariado…]» y la limitación «Ficha preliminar», que `main` hereda de la base, se respondieron en la rama con esa misma nota de lectura |
| `horn_1965` | contenido | No | La declaración de lectura de `main` está **literal** en la rama. «228 × 17 o 227 × 17» pasó a «228 × 16 … 227 × 16» por D16 y D15 (actualización, no pérdida). La propuesta metodológica se actualizó con la nota de lectura |
| `congreso_2018` | contenido | No | `main`: «(evento nacional, externo al análisis en el sentido de la decisión D18)»; rama: «(evento peruano; externo al análisis en el sentido de D18)». Mismo contenido; la rama, además, amplía la limitación sobre D18 |

**Resolución propuesta para la fusión (W-2):** tomar la versión de la rama en las nueve y, en
`abdi_2010`, reponer en la sección 6 («Aporte») la remisión «(§2.2.7 del informe)». No la repuse: no es
un dato bibliográfico verificado y la fusión la resuelve el orquestador con el desarrollador (F0-4).

## 3. Hallazgo colateral: `camiz_roig_2011`

El registro de IRIS Sapienza (repositorio institucional de la universidad del primer autor;
https://hdl.handle.net/11573/507241, tipo «04a Atto di comunicazione a congresso») muestra: autores
«Camiz, Sergio; F. A., Roig»; título «Evolutionary analysis applied to tree-ring series»; libro «Actas
E-ICES 6»; editorial «Comisión Nacional de Energía Atómica - CNEA»; año 2011; pp. «30-37»; ISBN
«9789871323210». Todo coincide con la entrada del `.bib` (`tesis/referencias.bib:66-76`). **El registro
no lista editor**, así que el «O. Papú» de la entrada sigue inferido y su `verificar` se mantiene. No
toqué la ficha ni el `.bib` (fuera del encargo); queda para la próxima vuelta del bibliotecario como
segunda fuente institucional de esa entrada.

## 4. Pendiente y motivo

- `camiz_spada_2024`: año, páginas y DOI. doi.org, Crossref y la revista no fueron accesibles (permisos
  no respondidos y 403 del proxy). No se reintentó ni se buscaron rutas alternativas.
- Campo `verificar` de `camiz_spada_2024` en el `.bib`: falta mencionar el año; no se tocó porque la
  fase 0 prohíbe modificar el `.bib`.
- `abdi_2010`: reponer «§2.2.7 del informe» al resolver el conflicto.
- W-7 (espera R-7): las prioridades del § 2 (a).
- `camiz_roig_2011`: anotar en la ficha la segunda fuente (IRIS Sapienza); el editor sigue sin verse.

## 5. Archivos

- Modificados: `papers/camiz_spada_2024.qmd`, `tesis/registro_verificacion.md` (frase en el párrafo
  inicial y sección «Fase 0 de la vuelta 2: Camiz y Spada, `.bib` de `main` y fichas en conflicto
  (27-11-2026)»).
- Creado: esta nota.
