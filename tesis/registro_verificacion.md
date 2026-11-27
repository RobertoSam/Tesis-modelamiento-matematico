Estado al commit `e97530c` de la rama `iteracion-3b` (29-10-2026), después de L1–L4 y E1–E3;
puesto al día en la vuelta 1 de la auditoría de la iteración 3b (hallazgo M-01) y, el 30-10-2026,
al commit `09b9c26` (hallazgo M-03: marca de `fmi_2015b`). El 07-11-2026 (iteración 3c, rama
`iteracion-3c`) se cerró N-02 con D18, se agregaron 30 obras del estado del arte (sección «Estado
del arte (iteración 3c)») y se recontaron las marcas sobre `605803a`. El 09-11-2026 (sesión de seguimiento, sobre `c564c35`) se
ficharon Bry y Boschan (1971), Harding y Pagan (2006) y Christiano y Fitzgerald (2003), se verificaron
los metadatos de Kwiatkowski et al. (1992) con su entrada en el `.bib`, y Camiz y Diblasi (2013) siguió
sin localizarse (sección «Pendientes del cap. 2 (09-11-2026)»). El 11-11-2026 (seguimiento, sobre
`780450d`) se ficharon Said y Dickey (1984) y Frontier (1976); Denimal (2001) y la fuente del
bootstrap por bloques conjunto siguen sin localizarse (sección «Pendientes fuera de resultados
(11-11-2026)»). El 13-11-2026 (seguimiento, sobre `c0fa997`) se ficharon Guttman (1953) —fuente de
la anti-imagen desde la inversa de la matriz de correlaciones— y Escofier y Pagès (2023) —fuente
verificada de la terminología cos²/contribuciones—, cerrando los dos `\pendiente` del marco teórico
del encargo (sección «Pendientes del marco teórico (13-11-2026)»). El 15-11-2026 (seguimiento, sobre
`9aa3b33`) se fichó Lavit, Escoufier, Sabatier y Traissac (1994) —fuente en revista del STATIS
dual—; Camiz y Diblasi (2013) y Denimal (2001) siguen sin localizarse y el bootstrap por bloques
conjunto no se buscó (sección «Pendientes bibliográficos (15-11-2026)»). El 17-11-2026 (seguimiento,
sobre `d4841e9`) se halló en Lahiri (2003, sec. 2.5, p. 29) la fuente del bootstrap por bloques
conjunto y se fichó Aue, Hörmann, Horváth y Reimherr (2009) para la detección de cambios en la
matriz de covarianzas (sección «Pendientes bibliográficos (17-11-2026)»). El 19-11-2026 (seguimiento,
sobre `67a9979`) se ficharon Pang et al. (2021), Su et al. (2019) y Audibert et al. (2020) —fuentes
revisadas por pares sobre detección de anomalías con aprendizaje profundo y error de reconstrucción en
series multivariadas— y Kingma y Ba (2015), fuente del optimizador Adam (sección «Pendientes
bibliográficos (19-11-2026)»). El 21-11-2026 (seguimiento, sobre `b864902`) se ficharon Tölö (2020)
—LSTM y GRU para predecir crisis sistémicas, *Journal of Financial Stability*— y Beutel, List y von
Schweinitz (2019) —sobreajuste del aprendizaje automático en alerta temprana, misma revista, sin redes
neuronales—; Sakurada y Yairi (2014) no se fichó (sección «Pendientes bibliográficos (21-11-2026)»).
El 24-11-2026 (vuelta 1 de 3c, hallazgo M-03 d, sobre `594e826`) se trajeron de `main` las fichas y
el estado del registro de la revisión del informe preliminar del 8-11-2026 (commit `63c6914`): Camiz y
Diblasi (2013) pasa de «no localizada» a fichada (texto leído por Roberto), Fisher (1958) y Horn (1965)
pasan a «texto completo leído», y se incorporan seis fichas (sección «Reconciliación con `main`
(24-11-2026, M-03 d)»).
El 25-11-2026 (vuelta 1 de 3c, aviso del redactor, sobre `34a7181`) `camiz_diblasi_2013` pasó de
`@unpublished` a `@presentation` para que biblatex-apa imprima el nombre del coloquio, y se intentó de
nuevo cotejar `camiz_spada_2024` (sección «Ponencia y cotejo de Camiz y Spada (25-11-2026)»).
El 27-11-2026 (vuelta 2 de 3c, fase 0, tareas F0-5 y F0-6, sobre `402f6f3`) se intentó otra vez cotejar
`camiz_spada_2024`, sin resultado en fuente oficial, y se inventariaron los dos `.bib` del informe en
`origin/main` y las nueve fichas en conflicto con `main`, sin modificar ningún `.bib` (sección «Fase 0
de la vuelta 2: Camiz y Spada, `.bib` de `main` y fichas en conflicto (27-11-2026)»).
Las marcas se contaron con
`git grep`, no a mano (sección «Conteo de marcas abiertas», al final).

Las ubicaciones remiten a secciones y bloques, no a números de línea, que cambian con cada
edición. Abreviaturas de la columna «Marcas en los documentos»:

- **Tesis**, capítulos de `tesis_latex/capitulos/` (marcas `\verificar` y `\pendiente`, con la
  etiqueta de la sección cuando la tiene);
- **Informe**, capítulos de `tesis/_capitulos/` (notas `[^…]` con `VERIFICAR`, marcas
  `[CITA PENDIENTE]` y recuadros «Pendiente»);
- **RmdF**, `R/ciclo_financiero_final.Rmd`, el documento R vigente desde D15 (sección numerada o
  nombre del chunk; marcas `[VERIFICAR: …]`);
- **Rmd**, `R/tesis_ciclo_financiero.Rmd`, documento de exploración. Desde D15 queda **congelado
  como antecedente** (md5 igual al del commit `2be3665`): sus marcas se registran pero no se
  corrigen en el archivo;
- **NB05**, `notebooks/05_pca.ipynb` (número de celda);
- **src**, módulo y función.

| Clave | Referencia | Qué falta verificar | Marcas en los documentos | Estado |
|---|---|---|---|---|
| `baldi_hornik_1989` | Baldi y Hornik (1989), *Neural Networks*, 2(1), 53–58 | Solo el DOI (doi.org y ScienceDirect no accesibles). Texto completo leído; volumen, número y páginas verificados en el catálogo de la Koninklijke Bibliotheek | Tesis: cap. 1, «Justificación» (`sec:justificacion`), `\verificar` conjunto con Bourlard y Kamp, y cap. 2, «Autoencoders» (`sec:dl`), `\verificar` propio. Informe: cap. 1 (`v1-bk`, conjunta) y cap. 2 (`v2-bh`). Ficha `papers/baldi_hornik_1989.qmd` | Pendiente (solo DOI) |
| `bourlard_kamp_1988` | Bourlard y Kamp (1988), *Biological Cybernetics*, 59 | Número del fascículo (4–5); alcance del resultado sobre las no linealidades | Tesis: cap. 1, «Justificación» (`\verificar` conjunto con Baldi y Hornik), y cap. 2, «Autoencoders», `\verificar` propio. Informe: cap. 1 (`v1-bk`) y cap. 2 (`v2-bk`). Ficha preliminar | Pendiente |
| `camiz_cerda_atoche_2026` | Camiz, Cerda Hernández y Atoche Murrieta (2026), manuscrito | Estado de publicación (revista, volumen, DOI); confirmar con el Dr. Camiz. Además, en la Tabla 1: correspondencia de «reservas» (grupo de riesgo) y «RIN» (grupo de salud) con las series del BCRP | Tesis: cap. 1, «Planteamiento» (`sec:planteamiento`); cap. 2, «Antecedentes peruanos» (`sec:antecedentes`), dos `\verificar` (publicación y reservas). Informe: `v1-cca`, `v2-cca`, `v2-res`. Ficha, sección 1 | Pendiente |
| `camiz_maulucci_roig_2010` | Camiz, Maulucci y Roig (2010), Actas E-ICES 5 | Datos de edición (ISBN o DOI); grafía del editor («Papu» en esta ficha, «Papú» en la de 2011) | Tesis: cap. 1, «Objetivos exploratorios condicionales» (OC2), y cap. 2, «Análisis evolutivo de componentes principales» (`sec:epca`), un `\verificar` en cada uno. Informe: `v1-cmr` y `v2-cmr` | Pendiente |
| `camiz_roig_2011` | Camiz y Roig (2011), Actas E-ICES 6 | Editor (O. Papú) inferido por analogía; año ambiguo en la ficha («E-ICES 6, 2010/2011») | Tesis: cap. 1, «Justificación», y cap. 2, «El algoritmo `aede`» (`sec:epca`), un `\verificar` en cada uno. Informe: `v1-cr` y `v2-cr`. Ficha, sección 2 | Pendiente |
| `fisher_1958` | Fisher (1958), *JASA*, 53(284), 789–798 | **24-11-2026 (M-03 d):** texto completo leído por Roberto el 8-11-2026 (ficha de `main`, `63c6914`); las páginas 789–798 constan en el artículo, y se retiró el campo `verificar` del `.bib`. Volumen, número y DOI respaldados por el título de la página de Taylor & Francis (20-10-2026). La editorial y doi.org siguen sin abrirse desde las sesiones del bibliotecario. Caso multivariado: el artículo sugiere reducirlo con el primer componente principal; la aplicación a trayectorias de 3 dimensiones es extensión de la tesis | Tesis: cap. 1, «Justificación», y cap. 2 (`02_estado_arte.tex:212-215` y `395-397`, nota repetida, m-03), un `\verificar` en cada uno que todavía la llama preliminar. Informe: `v1-fis` y `v2-fis`. RmdF y Rmd: chunk `funciones`, sin marca | Cerrado (metadatos y lectura, 24-11-2026); las marcas de la tesis pueden cerrarse (redactor; ver la nota del 24-11-2026) |
| `gal_ghahramani_2016` | Gal y Ghahramani (2016), ICML, PMLR 48 | Editores del volumen; PDF no consultado | Tesis: cap. 1, «Objetivos específicos» (`sec:oe`), y cap. 2, «Autoencoders» (`sec:dl`). Informe: `v1-gg` y `v2-gg` | Pendiente |
| `gers_schmidhuber_cummins_2000` | Gers, Schmidhuber y Cummins (2000), *Neural Computation*, 12 | DOI contra el registro de MIT Press; texto no consultado | Tesis e Informe: cap. 2, «Redes LSTM» (`sec:dl`; `v2-gsc`). Ficha preliminar | Pendiente |
| `hinton_salakhutdinov_2006` | Hinton y Salakhutdinov (2006), *Science*, 313 | Se procesó el material suplementario; leer el artículo principal | Tesis: cap. 1, «Justificación» (`\verificar` conjunto con Tuhin et al.), y cap. 2, «Autoencoders». Informe: `v1-ht` y `v2-hs`. Ficha, sección 2 | Pendiente |
| `hochreiter_schmidhuber_1997` | Hochreiter y Schmidhuber (1997), *Neural Computation*, 9 | Se procesó el informe técnico FKI-207-95; contrastar con la versión publicada | Tesis e Informe: cap. 2, «Redes LSTM» (`v2-hoch`). Ficha, sección 2 | Pendiente |
| `plaut_2018` | Plaut (2018), arXiv:1804.10253 | *Preprint* sin revisión por pares; usar solo como apoyo técnico secundario | Tesis e Informe: cap. 2, «Autoencoders» (`v2-pl`) | Pendiente |
| `robert_escoufier_1976` | Robert y Escoufier (1976), *JRSS C*, 25 | Volumen, número, páginas y DOI en JSTOR; texto no consultado | Tesis e Informe: cap. 2, «Comparación de configuraciones» (`sec:comparacion`; `v2-re`). RmdF y Rmd: chunk `funciones`, comentario del coeficiente RV, sin marca. Ficha preliminar | Pendiente |
| `srivastava_mansimov_salakhutdinov_2015` | Srivastava, Mansimov y Salakhutdinov (2015), ICML, PMLR 37 | Páginas 843–852 y editores del volumen | Tesis e Informe: cap. 2, «LSTM-autoencoder» (`v2-sms`) | Pendiente |
| `tuhin_et_al_2025` | Tuhin, Nobi, Rakib y Lee (2025), *HSSC*, 12 | Lista completa de autores | Tesis: cap. 1, «Justificación» (`\verificar` conjunto con Hinton y Salakhutdinov); cap. 2, «Validación externa» (`sec:validacion`) y «LSTM-autoencoder», un `\verificar` en cada uno. Informe: `v1-ht`, `v2-tu` y `v2-tu2`. Ficha, sección 2 | Pendiente |
| `vincent_et_al_2008` | Vincent et al. (2008), ICML | DOI en ACM Digital Library | Tesis e Informe: cap. 2, «Autoencoders» (`v2-vi`) | Pendiente |
| `atoche_murrieta_2022` | Atoche Murrieta (2022), tesis de maestría, PUCP | Fichada el 24-10-2026 (registro del Repositorio PUCP y portada del PDF; texto leído hasta el cap. 5.2). **Falta:** el título difiere entre la portada («periodo 2000-2020», el que se usa) y el registro («2000-2021»); referencias y conclusiones no leídas | Tesis: tres `\verificar` (título): cap. 1, «Planteamiento»; cap. 2, «Antecedentes peruanos», y cap. 2, «Ventanas, fechado y pesos» (`sec:epca`, donde además consta que en la parte leída no cita la fuente del esquema gaussiano). Informe: `v1-atm`, `v2-atm` y `v2-atm2`. Los `\pendiente` de 3a se sustituyeron por la cita en L1–L2 | Fichada (texto parcial); pendiente (título) |
| `benzecri_1973` | Benzécri (1973), *L'analyse des données*, t. 2, Dunod | Ficha preliminar. Autoría del tomo 2 (Open Library añade a F. Benzécri); editorial (Dunod o Bordas); tomo 1 sin verificar; **tomo y página del principio «dejar hablar a los datos», que no se localizó en ninguna fuente consultada** | Tesis e Informe: cap. 2, «Posición epistemológica» (`sec:epistemologia`; `v2-bz`). Rmd: sección 2, «Balance de los argumentos» (tabla de argumentos) | Pendiente |
| `calinski_harabasz_1974` | Caliński y Harabasz (1974), *Communications in Statistics*, 3(1) | Páginas 1–27 (solo en fuentes secundarias); texto no consultado: la forma del índice y la variante del código de `aede` no se atribuyen hasta leerlo. Grafía según la fuente: «Harabasz», sin tilde | Tesis: cap. 2, «Antecedentes peruanos» y «Índice de Caliński y Harabasz» (`sec:fisher`), un `\verificar` en cada uno. Informe: `v2-ch` y `v2-ch2`. RmdF: chunk `funciones` (comentario del índice). Rmd: chunk `funciones`, pie de tabla del chunk `b4-aede` y texto de A.3, «EPCA del asesor (`aede`)» | Fichada (preliminar); pendiente |
| `horn_1965` | Horn (1965), *Psychometrika*, 30(2), 179–185 | Ninguno en los metadatos (Cambridge Core y SpringerLink, 20-10-2026). **24-11-2026 (M-03 d):** texto completo leído por Roberto el 8-11-2026 (ficha de `main`, `63c6914`): Horn usa el **promedio** de los valores propios de matrices aleatorias; el percentil 95 es una elección de la tesis | Tesis: cap. 1, «Objetivos específicos» (`01_introduccion.tex:107`), y cap. 3, «Número de componentes» (`03_marco_teorico.tex:495`), un `\verificar` en cada uno que todavía la llama preliminar. Informe: `v1-horn` y `v2-horn`. RmdF: chunk `funciones` (análisis paralelo) y 2.4, «Nulo de tendencias independientes». Rmd: chunk `funciones` y sección 2, «El argumento a favor de transformar». src: `multivariado.horn` | Cerrado (metadatos, 20-10-2026; lectura, 24-11-2026); las marcas de la tesis pueden actualizarse (redactor) |
| `camiz_pillar_2018`, `rencher_christensen_2012` | Fuentes del criterio de Rencher y de la atribución de la vara quebrada (OE6) | **Rencher:** `camiz_pillar_2018` (*Mathematics*, 6(11), 269; metadatos verificados en MDPI) define el criterio como la generalización de Rencher de la prueba de Bartlett. Fuente directa: `rencher_christensen_2012`, 3.ª ed., sección 12.6 (p. 423), ficha preliminar; falta confirmar la edición que citan Camiz y Pillar y leer la sección. **Vara quebrada:** ver la fila de Frontier (1976) | `camiz_pillar_2018` se cita sin marca propia (Tesis: cap. 1, «Objetivos específicos», y cap. 2, «Número de componentes»; Informe: las mismas secciones); la marca que la acompaña es el `\pendiente` de Frontier. `rencher_christensen_2012`: Tesis, cap. 2, «Número de componentes», `\verificar`; Informe, `v2-ren` | `camiz_pillar_2018`: cerrado (metadatos). Rencher: fichada (preliminar); pendiente |
| `frontier_1976` | Frontier (1976), *Journal of Experimental Marine Biology and Ecology*, 25(1), 67–75, fuente primaria del modelo de vara quebrada | Camiz y Pillar (2018) atribuyen a Frontier (ref. [10]) la aplicación al PCA. **11-11-2026:** metadatos y DOI verificados en Crossref; ficha preliminar. Falta: texto (Crossref sin resumen; ScienceDirect no accesible) y cotejar que sea la ref. [10] de Camiz y Pillar | Tesis: `\pendiente` en cap. 1, «Objetivos específicos» (`sec:oe`), y cap. 2, «Número de componentes» (`sec:retencion`). Informe: `[CITA PENDIENTE]` en las mismas secciones. RmdF: 3.1, «¿Cuántas componentes retener?» (`[VERIFICAR: fuente primaria no localizada]`). Rmd: A.2, «¿Cuántas componentes retener?» (marca conjunta con Kaiser) | Cerrado (metadatos, 11-11-2026); contenido no leído. El redactor puede sustituir los `\pendiente` por la cita con `\verificar` |
| `eckart_young_1936` | Eckart y Young (1936), *Psychometrika*, 1(3), 211–218 | Metadatos verificados en Cambridge Core. Pendiente de contenido: la condición de unicidad (p. 216) quedó cortada en la copia leída | Tesis e Informe: cap. 2, «Definición y propiedad de reconstrucción» (`sec:pca`; `v2-ey`) | Cerrado (metadatos); contenido parcial |
| `jolliffe_2002` | Jolliffe (2002), *Principal component analysis*, 2.ª ed., Springer | Metadatos verificados en SpringerLink (DOI 10.1007/b98835). Texto no consultado: **no se verificó la página del umbral 0,7** que le atribuyen Camiz et al. (2020) | Tesis: cap. 2, «Definición y propiedad de reconstrucción» (`sec:pca`), cita como obra general con `\verificar` (sustituye al `\pendiente` de 3a). Informe: `v2-jol` | Cerrado (metadatos, 24-10-2026); contenido no consultado |
| `denimal_2007` | Denimal (2007), *JSFdS & Revue de statistique appliquée*, 148(2), 29–63; Denimal (2001) | 2007: metadatos y resumen verificados en Numdam; **corrige** el título, la revista y las páginas que daba la ficha de Camiz et al. (2020). 2001: según la bibliografía de Denimal (2007), es una presentación en el 10.º ASMDA (Compiègne, 12–15 de junio de 2001) sin actas localizadas: sin ficha. **11-11-2026:** dos búsquedas más (título en inglés con «ASMDA Compiègne proceedings»; «ASMDA 2001» con «Applied Stochastic Models and Data Analysis» y Denimal) solo devuelven Denimal (2007) y otra ponencia del mismo congreso (Lorga da Silva, Bacelar-Nicolau y Saporta, página del CNAM), sin datos de actas: siguen sin verse editorial, páginas o ISBN. **15-11-2026:** dos búsquedas más de las actas del ASMDA 2001 (editores y UTC; «Applied Stochastic Models and Data Analysis» 2001 Compiègne con ISBN) sin registro pertinente; un registro de Serval (UNIL) no se pudo abrir (permiso no respondido). **Pedido:** que Roberto solicite la referencia al Dr. Camiz | 2007: Tesis, cap. 2, «Clasificación Factorial Jerárquica» (`sec:hfc`), citada sin marca; Informe, nota `v2-c20` (sin `VERIFICAR`). 2001: Tesis, `\pendiente` en `sec:hfc`; Informe, `[CITA PENDIENTE]` dentro de la nota `v2-c20` | Cerrado (2007, metadatos; contenido: solo resumen); 2001 pendiente de fichar |
| `camiz_diblasi_2013` | Camiz y Diblasi (2013), *Evolutionary principal component analysis*, ponencia, XLI Coloquio Argentino de Estadística, Mendoza | **24-11-2026 (M-03 d): fichada.** Roberto leyó el texto completo el 7-11-2026 (PDF «Camiz Diblasi 2013 XLI CAE.pdf», carpeta del asesor; ficha de `main`, `63c6914`), lo que cierra el pedido al Dr. Camiz. Metadatos solo del PDF; una octava búsqueda (24-11-2026) tampoco halló actas, ISBN ni URL: queda `verificar` en el `.bib`. Historial: **No localizada** (24-10-2026) tras cuatro búsquedas (título, autores, «Coloquio Argentino de Estadística», «evolutionary PCA»). La única descripción («Actas Coloquio Argentino de Estadística») viene del anexo C del manuscrito `camiz_cerda_atoche_2026`, no verificado. Atoche Murrieta (2022) usa pesos gaussianos (*k* = 3) sin citarla en la parte leída. El 09-11-2026 se hicieron dos búsquedas más («Camiz» «Diblasi» con «componentes principales evolutivo» y «actas»; «Sergio Camiz Angela Diblasi 2013 Coloquio Argentino de Estadística»), sin resultado pertinente: siguen sin verse el título, el lugar y las actas. El nombre de pila «Angela» es solo el término de búsqueda, no un dato verificado. **15-11-2026:** una búsqueda más (ventana móvil, ponderación gaussiana, Coloquio Argentino de Estadística) llevó a las actas de E-ICES 8 (CNEA, 2013, ISBN 978-987-1323-33-3; evento de 2012): su índice, completo, tiene tres trabajos con Camiz y ninguno con Diblasi ni sobre análisis evolutivo; descartadas. **Pedido:** que Roberto solicite la referencia o el PDF al Dr. Camiz | Tesis: `\pendiente` en cap. 2, `sec:ea-factoriales` (`02_estado_arte.tex:302`), y en cap. 3 (`03_marco_teorico.tex:778`) (marco teórico, ponderación de las ventanas); listado en cap. 7. Informe: `[CITA PENDIENTE]` en la sección de EPCA | Fichada (24-11-2026); entrada en el `.bib` con `verificar` (datos de edición). Los `\pendiente` pueden pasar a cita con `\verificar` (redactor) |
| `tukey_1977` | Tukey (1977), *Exploratory data analysis*, Addison-Wesley | Metadatos verificados en dos catálogos (Universidad de Patras; Universidad de Carleton). Sin ISBN ni extensión. Texto no consultado: solo para el encuadre general | Tesis: cap. 2, «El algoritmo `aede`», `\verificar` (sustituye al `\pendiente` de 3a). Informe: `v2-tuk` | Cerrado (metadatos, 24-10-2026); contenido no consultado |
| `lavit_1988` | Lavit (1988), *Analyse conjointe de tableaux quantitatifs*, Masson | Título, editorial, lugar, año y colección verificados en el catálogo de la Universidad de Patras, cuyo campo de autor está vacío. Autoría tomada de la *Three-Mode Bibliography* (Leiden). Falta la autoría en un catálogo y el ISBN | Tesis: cap. 2, «Comparación de configuraciones» (`sec:comparacion`), `\verificar` (sustituye al `\pendiente` de 3a). Informe: `v2-lav`. **15-11-2026:** para el STATIS dual se fichó además `lavit_et_al_1994` (ver «Pendientes bibliográficos (15-11-2026)») | Fichada (preliminar); pendiente (autoría) |
| `tucker_1951` | Tucker (1951), *A method for synthesis of factor analysis studies* (PRS Report 984) | Autor, año, título, número del informe y extensión (120 p.) verificados en el repositorio de publicaciones de ETS. Falta: **entidad emisora y lugar** (el registro de ETS no los da; la lectura «Personnel Research Section, Department of the Army» no se vio en fuente oficial ni se halló registro en DTIC); no hay DOI. Texto no consultado: **no se comprobó que el informe defina el coeficiente de congruencia**; la atribución es la habitual | Tesis: cap. 2, «Comparación de configuraciones», `def:tucker` (`\verificar`). Informe: `@def-tucker` (`v2-tk`). RmdF: 2.5, «Diagnóstico: el PCA de las series sin su tendencia lineal». Rmd: sección 2, nota sobre los umbrales de congruencia | Fichada (preliminar, 20-10-2026); pendiente |
| `granger_newbold_1974` | Granger y Newbold (1974), *Journal of Econometrics*, 2, 111–120 | Número del fascículo y DOI (no figuran en la copia leída; Elsevier no accesible). Texto completo leído | RmdF: 2.1, «Tendencia de cada serie (regla D5) y deriva (D8)»; 2.4, «Nulo de tendencias independientes», y 3.3, «Regresión sobre el tiempo y análisis de los residuos (regla D5)». Rmd: sección 2, «El argumento a favor de transformar», y A.2, «Regresión sobre el tiempo… (regla D5)». NB05, celda 15 | Pendiente (número y DOI) |
| `phillips_1986` | Phillips (1986), *Journal of Econometrics*, 33(3), 311–340 | Metadatos tomados de RePEc/IDEAS (secundaria): contrastar con Elsevier y añadir el DOI. Resumen leído; texto no consultado | RmdF: 2.1, 2.4 y 3.3 (mismos pasajes que Granger y Newbold). Rmd: sección 2, «El argumento a favor de transformar», y A.2. NB05, celda 15 | Pendiente |
| — | Engle y Granger (1987) | Sin ficha en `papers/` | Rmd: sección 2, «Balance de los argumentos» (tabla de argumentos, cointegración). No figura en RmdF | Pendiente |
| — | Fuentes de los filtros pasa-banda y de Hodrick-Prescott para la brecha del ciclo financiero | Christiano y Fitzgerald (2003) fichada el 09-11-2026 (`christiano_fitzgerald_2003`); Hodrick y Prescott (1997) sigue sin ficha. Desde 3c hay fichas que **discuten** esos filtros: `hamilton_2018` (crítica del HP) y `strohsal_proano_wolters_2019` (los filtros fijan la frecuencia de antemano); no sustituyen a las fuentes primarias | Rmd: sección 2, «Balance de los argumentos». No figuran en RmdF | Pendiente |
| — | Fuente de los modelos de cambio de régimen de Markov | Desde 3c, fichada: `hamilton_1989` (resumen leído; metadatos verificados), con `kim_nelson_1999` y `krolzig_1997` como manuales. El Rmd está congelado (D15): la marca no se corrige en el archivo | Rmd: A.5, «Alternativas consideradas». No figura en RmdF | Pendiente |
| `dickey_fuller_1979` | Dickey y Fuller (1979), *JASA*, 74(366a) | Páginas 427–431 (solo en fuentes secundarias). La versión **aumentada** que usa el código no se le atribuye (ver la fila de Said y Dickey) | Tesis: cap. 3, «Diagnóstico de las series sin transformar» (`sec:met-diagnostico`), `\verificar`. Informe: `v3-df`. RmdF: 2.1 y 3.3. Rmd: sección 2, «Estacionariedad en las dos versiones», y A.2, «Regresión sobre el tiempo… (regla D5)» | Fichada (preliminar); pendiente |
| `said_dickey_1984` | Said y Dickey (1984), *Biometrika*, 71(3), 599–607, versión aumentada de la prueba ADF | **11-11-2026:** metadatos y DOI verificados en Crossref y en Oxford Academic; resumen leído. Falta el texto: el resumen no da la regla de rezagos ni el origen de las tablas, que no se le atribuyen | Tesis: `\pendiente` en `sec:met-diagnostico`. Informe: `[CITA PENDIENTE]` en cap. 3, «Diagnóstico de las series sin transformar». Rmd: sección 2, «Estacionariedad en las dos versiones» (marca «sin ficha») | Cerrado (metadatos, 11-11-2026); contenido: solo resumen. El redactor puede sustituir el `\pendiente` |
| `kwiatkowski_et_al_1992` | Kwiatkowski, Phillips, Schmidt y Shin (1992), *Journal of Econometrics*, 54(1–3), 159–178, DOI 10.1016/0304-4076(92)90104-y | **Metadatos cerrados el 09-11-2026** en el registro de Crossref: cuatro autores (Kwiatkowski, Phillips, Schmidt y Shin), título sin subtítulo, volumen, número, páginas y DOI. Entrada en el `.bib` creada. Contenido: solo el resumen del documento de trabajo de Cowles (tres autores); texto no consultado | Tesis: `\pendiente` en cap. 2, `sec:ea-regimenes`, y en cap. 4, `sec:met-diagnostico` (se nombra sin `\cite`); listado en cap. 7. Informe: `[CITA PENDIENTE]` en cap. 3, «Diagnóstico de las series sin transformar». RmdF: 2.1 y 3.3. Rmd: sección 2, «Estacionariedad en las dos versiones», y A.2. **El redactor y el editor pueden sustituir los `\pendiente` por la cita** | Cerrado (metadatos, 09-11-2026); contenido: solo resumen |
| `bartlett_1950`, `bartlett_1951` | Bartlett (1950), *British Journal of Statistical Psychology*, 3(2); Bartlett (1951), *Biometrika*, 38(3–4), 337–344 | 1950: páginas 77–85 (secundarias). 1951: metadatos verificados en Oxford Academic. En ambos, texto no consultado: no se verificó en cuál se formula la prueba de esfericidad sobre la matriz de correlaciones | Tesis e Informe: cap. 2, «Adecuación muestral» (`sec:adecuacion`; `\verificar` y nota `v2-bk-kmo`, conjuntos de las cuatro fichas). RmdF: 2.3, «Adecuación de la matriz de correlaciones». Rmd: A.2, «¿Tiene sentido un PCA con estos datos?». src: `multivariado.bartlett_esfericidad` | Fichadas (preliminares); pendiente |
| `kaiser_1970`, `kaiser_rice_1974` | Kaiser (1970), *Psychometrika*, 35(4); Kaiser y Rice (1974), *EPM*, 34(1) | Metadatos verificados (Cambridge Core; SAGE). Texto no consultado: la forma de la MSA que usa el código solo consta en la documentación de `psych` | Tesis e Informe: la misma marca conjunta de «Adecuación muestral». RmdF: 2.3. Rmd: A.2, «¿Tiene sentido un PCA con estos datos?» (KMO). src: `multivariado.kmo` | Cerrado (metadatos); atribución de la fórmula pendiente |
| `kaiser_1960` | Kaiser (1960), *EPM*, 20(1), 141–151 | Volumen, número y páginas (solo en fuentes secundarias; SAGE no accesible). La atribución del criterio $\lambda > 1$ es la habitual y no se verificó en el texto | Tesis e Informe: cap. 2, «Número de componentes» (`v2-kai`). RmdF: 3.1, «¿Cuántas componentes retener?». Rmd: A.2, «¿Cuántas componentes retener?» (marca conjunta con la vara quebrada) | Fichada (preliminar); pendiente |
| `guttman_1953` | Fuente de la relación entre la inversa de la matriz de correlaciones y la anti-imagen (matriz anti-imagen); contexto del KMO | **13-11-2026:** Guttman (1953), *Psychometrika*, 18(4), 277–296, DOI 10.1007/BF02289264, metadatos y resumen verificados en Cambridge Core. El resumen define imagen/anti-imagen por regresión sobre las demás variables y un cálculo «basado en la inversa de la matriz de correlaciones», pero **no** menciona las «correlaciones parciales». Kaiser (1970) y Kaiser y Rice (1974) usan la anti-imagen en la MSA, pero sus registros oficiales tampoco tratan la relación con las correlaciones parciales | Tesis: `\pendiente` en cap. 3, «Adecuación muestral» (`sec:adecuacion`, l. ~544). Informe: `[CITA PENDIENTE]` en la misma sección | Cerrado en parte: se ficha la fuente de la anti-imagen desde $\mathbf{R}^{-1}$ (Guttman, 1953); la **igualdad** anti-imagen = correlación parcial sigue sin fuente vista (ver «Regla para el redactor») |
| `escofier_pages_2023` | Fuente de la terminología de calidad de representación (cos²) y contribuciones de la escuela francesa | **13-11-2026:** no se localizó una tabla de contenidos oficial de `lebart_morineau_piron_1995` (ed. 1995) que muestre la sección de cos²/contribuciones; la ficha de Lebart queda como marco general. En su lugar se verificó Escofier y Pagès (2023), *Analyses factorielles simples et multiples*, 5e éd., Dunod, ISBN 978-2-10-085957-3: el extracto oficial de Dunod (Feuilletage_3448.pdf) incluye la sección 1.9 «Aides à l'interprétation» (p. 24), con «qualité de représentation» definida como **coseno cuadrado** y «contribution d'un élément à l'inertie d'un axe», para individuos y variables. Metadatos de la portada/créditos del extracto; total de páginas no visto | Tesis: `\pendiente` en cap. 3, «Calidad de representación y contribuciones» (`sec:cos2`, l. ~429) y cap. 2, estado del arte (`02_estado_arte.tex`, l. ~291). Informe: `[CITA PENDIENTE]` en la misma sección | Cerrado (terminología y conceptos; no las fórmulas exactas de `def:cos2`). La fila de `lebart_morineau_piron_1995` sigue abierta en cuanto a su sección de cos² |
| `bruynooghe_1978` | Bruynooghe (1978), *Les Cahiers de l'Analyse des Données*, 3(1), 7–33 | Metadatos verificados en Numdam. Texto no consultado: la propiedad de reducibilidad que exige el índice de la HFC no se le atribuye | Tesis: cap. 2, «Clasificación Factorial Jerárquica» (`sec:hfc`), `\verificar` (sustituye al `\pendiente` de 3a). Informe: `v2-bru` | Cerrado (metadatos, 24-10-2026); contenido no consultado |
| `hubert_arabie_1985` | Hubert y Arabie (1985), *Journal of Classification*, 2(1), 193–218 | Metadatos tomados de RePEc/IDEAS: contrastar con SpringerLink. La atribución del índice de Rand ajustado no se verificó en el texto | Tesis: cap. 3, «Clasificación Factorial Jerárquica» (`sec:met-hfc`), `\verificar`. Informe: `v3-ha`. Rmd: A.4, «HFC evolutiva» | Fichada (preliminar); pendiente |
| `kingma_ba_2015` | Fuente del optimizador Adam | **19-11-2026:** fichada (FB-112). Metadatos en arXiv:1412.6980 (nota de los autores: ICLR 2015, San Diego) y en UvA-DARE; resumen leído | Rmd: A.5, «Diseño del autoencoder» (tabla de parámetros), `[VERIFICAR: sin ficha]`. No figura en RmdF (la sección 7 no desarrolla las redes) | Fuente identificada; sustitución de la marca del Rmd pendiente del desarrollador |
| `kunsch_1989` | Künsch (1989), *The Annals of Statistics*, 17(3) | Páginas 1217–1241 (secundarias; Project Euclid bloquea el acceso automatizado). **No se verificó que el artículo defina el esquema de bloques móviles solapados del código** | Tesis: cap. 2, «Nulos de referencia y criterio del ancho de ventana» (`sec:nulos`), dos `\verificar` (uno propio y uno conjunto con Lahiri). Informe: `v2-kun` (y `v2-lah`, conjunta). RmdF y Rmd: chunk `funciones` (bootstrap por bloques). src: `remuestreo` (docstring del módulo) | Fichada (preliminar); pendiente |
| `pyper_peterman_1998` | Pyper y Peterman (1998), *Canadian Journal of Fisheries and Aquatic Sciences*, 55, 2127–2140 | Volumen y páginas (solo en una fuente secundaria); fe de erratas sin consultar; **no se comprobó que la fórmula de $n_{\text{ef}}$ del código, con truncamiento $J = \lfloor n/5 \rfloor$, sea la de este artículo** (una fuente secundaria atribuye la estructura de la fórmula, sin truncamiento, a Quenouille, 1947) | Tesis e Informe: cap. 2, «Adecuación muestral» (`v2-pp`). RmdF: chunk `funciones` y 2.2, «Persistencia y tamaño muestral efectivo». Rmd: chunk `funciones` y A.2, «Autocorrelación, muestra efectiva y sensibilidad de Bartlett». NB05, celda 5. src: `series_tiempo.n_efectivo` | Fichada (preliminar); pendiente |
| `kish_1965` | Kish (1965), *Survey sampling*, Wiley | Metadatos verificados en el catálogo de la Universidad de Pensilvania. Texto no consultado: capítulo y página de la fórmula $1/\sum\omega^2$. Intento del 24-10-2026 (tarea B2) sin resultado: las fuentes accesibles que la atribuyen a Kish (viñeta de PracTools, Wikipedia) son secundarias y no dan una página verificable. Se pidió a Roberto la página del libro | Tesis: cap. 2, «Tamaño efectivo de una ventana y umbrales por ventana» (`sec:kish`), `\verificar`. Informe: `v2-kish`. RmdF: sección 4 y 4.2 nombran «el $n$ efectivo de Kish», sin año ni marca | Fichada (preliminar); pendiente |
| `lorenzo_seva_ten_berge_2006` | Lorenzo-Seva y ten Berge (2006), *Methodology*, 2(2), 57–64 | Metadatos: ninguno (repositorio de la Universidad de Groningen y Hogrefe). **Contenido: solo se leyó el resumen oficial**, que da los umbrales: 0,85–0,94 «similitud aceptable» y más de 0,95 «iguales». Precisión para el texto: 0,85 no indica equivalencia, y que por debajo de 0,85 la componente sea «distinta» no está en el resumen | Tesis e Informe: cap. 2, «Comparación de configuraciones», sin marca (lo que se le atribuye está en el resumen). RmdF: 2.5 y pies de tabla de congruencia, sin marca. Rmd: sección 2, «Diagnóstico: el PCA de las series sin su tendencia lineal», sin marca | Cerrado (metadatos, 20-10-2026); contenido: solo resumen |
| `perron_1989` | Perron (1989), *Econometrica*, 57(6), 1361–1401 | DOI (la Econometric Society solo da el enlace de JSTOR). **Cubre solo las pruebas de raíz unitaria (ADF)**: no puede sostener la parte de la frase referida a KPSS, prueba posterior (1992) | Ninguna: no se cita en ningún documento. Candidata para la parte ADF de la marca sobre quiebres estructurales (fila siguiente) | Fichada (resumen leído); pendiente |
| — | Fuente del efecto de los quiebres estructurales sobre las pruebas ADF y KPSS | Sin identificar para KPSS; para ADF, candidata `perron_1989`. La frase «pierden potencia» debería revisarse para KPSS | RmdF: 2.1 y 3.3 (`[VERIFICAR: fuente]`). Rmd: A.2, «Regresión sobre el tiempo… (regla D5)» | Pendiente de identificar |
| `newey_west_1987` | Newey y West (1987), *Econometrica*, 55(3), 703–708 | Verificados en la Econometric Society: título, revista, volumen, número, páginas, mayo de 1987 y JSTOR 1913610. **Falta:** orden de los autores (la página de la Econometric Society lista primero a West; RePEc y el NBER, a Newey) y DOI 10.2307/1913610 sin comprobar en doi.org. Texto no consultado: el núcleo y los 12 rezagos son elecciones de la tesis | Tesis: cap. 2, «Nulo de tendencias mixto» (`sec:nulo-mixto`), `\verificar`. Informe: `v2-nw`. RmdF: chunk `funciones` (nulo mixto) y 2.1. src: `series_tiempo.t_hac_media` | Fichada (resumen); pendiente (orden de autores, DOI) |
| `josse_pages_husson_2008` | Josse, Pagès y Husson (2008), *CSDA*, 53(1), 82–91 | Solo RePEc (secundaria); la documentación de FactoMineR da otro orden de autores y el año 2007. ScienceDirect, HAL y doi.org no accesibles. Supone filas intercambiables: sirve como antecedente del contraste del RV, **no** como el nulo de D7 | Ninguna: no se cita en ningún documento | Fichada (resumen, preliminar); pendiente |
| `hennig_2007` | Hennig (2007), *CSDA*, 52(1), 258–271 | RePEc y documentación de `fpc` (secundarias); DOI y contraste con ScienceDirect pendientes. Texto no consultado: el método (Jaccard por grupo bajo remuestreo) solo consta en la documentación del software | Tesis: cap. 3, «Clasificación Factorial Jerárquica» (`sec:met-hfc`), `\verificar`. Informe: `v3-hen` | Fichada (preliminar); pendiente |
| `lahiri_2003` | Lahiri (2003), *Resampling methods for dependent data*, Springer | Metadatos e índice verificados en SpringerLink (DOI). **17-11-2026:** sec. 2.5 leída en parte en una copia no oficial (sitio docente): p. 29, la descripción del bootstrap de bloques móviles «applies almost verbatim» si las observaciones son vectores aleatorios. Sostiene el bloque conjunto (ver la fila siguiente); no se leyeron demostraciones ni caps. 3–6 | Tesis: cap. 2, `sec:nulos`, `\verificar` conjunto con Künsch («manual del bootstrap por bloques»). Informe: `v2-lah` | Cerrado (metadatos, 24-10-2026); contenido: texto parcial (17-11-2026) |
| — | Fuente del bootstrap por bloques conjunto (mismos inicios de bloque para todas las series) | Sin ficha que lo trate. **11-11-2026:** el resumen del cap. 2 de `lahiri_2003` en SpringerLink («Bootstrap methods», pp. 17–43) solo dice que las secciones 2.5–2.7 describen métodos por bloques; no menciona datos multivariados (el texto es de pago). Una búsqueda general solo dio documentación de programas y un *preprint* de arXiv, que no sirven. Künsch (1989) no se pudo revisar (Project Euclid no accesible). Ninguna obra fichada. **15-11-2026:** no se buscó (sin margen en la jornada; queda para otra). **17-11-2026:** Künsch (1989) volvió a dar el control antibots de Project Euclid; Lahiri (2003), sec. 2.5, p. 29, extiende el método a observaciones vectoriales (copia no oficial de los caps. 2 y 7, paginación coherente con el índice de la editorial) | Tesis: `\pendiente` en cap. 2, «Nulo de estructura constante» (`sec:nulo-estructura`). Informe: `[CITA PENDIENTE]` en la misma sección (observación sobre los supuestos del nulo) | Identificada: `lahiri_2003`, sec. 2.5, p. 29, con `\verificar` (texto en copia no oficial). Integración pendiente del redactor (ver «Pendientes bibliográficos (17-11-2026)») |
| `bernanke_2013` | Bernanke (2013), *The economic outlook*, testimonio ante el Joint Economic Committee, 22-05-2013 (página del BIS) | La ficha registra la fecha y la descripción del testimonio; **no se leyó el pasaje** sobre la reducción del ritmo de compras de activos | Tesis: cap. 2, «Validación externa» (`sec:validacion`), `\verificar`. Informe: `v2-bern`. Fuente del inicio del *taper tantrum* (tabla de episodios) | Fichada; pendiente (pasaje) |
| `congreso_2018` | Congreso de la República (2018), aceptación de la renuncia de P. P. Kuczynski, 23-03-2018 | Ficha elaborada con la nota oficial del Congreso; **no se leyó el texto de la resolución ni su publicación en *El Peruano***. N-02 cerrado por D18 (07-11-2026): la ficha ya no califica el hecho como «interno», sino como evento peruano externo al análisis | Tesis: cap. 2, «Validación externa», `\verificar`. Informe: `v2-cong`. Fuente del episodio puntual de Kuczynski | Fichada; pendiente (resolución); N-02 cerrado (D18) |
| `congreso_2016` | Congreso de la República (2016), temas tratados del 28 de julio de 2016 | Denominación oficial exacta del documento (el título se compuso con su encabezado) | Ninguna: no se cita y no fecha ningún episodio (la juramentación no es un evento del episodio; ver la tabla) | Pendiente (sin uso) |
| `doj_2016`, `oms_2020a`, `fmi_2015` | Fuentes de episodios | `oms_2020a`: ubicar la versión en who.int (se leyó una copia en extranet.who.int). `fmi_2015`: páginas del recuadro en el WEO completo. `doj_2016`: sin pendientes de metadatos | Ninguna: no se citan en la tesis ni en el informe ni fechan un extremo del archivo de episodios (alternativas de la tabla) | Pendiente (`oms_2020a`, `fmi_2015`) |
| `oms_2023`, `pcm_2020`, `fmi_2015b`, `baffes_streifel_2016`, `nber_2021`, `ustr_2020`, `fmi_2016` | Fuentes de episodios de la tarea B1 (tabla siguiente) | `oms_2023`: leída en la página de la Oficina Regional para Europa; falta la de la sede. `pcm_2020`: texto leído en una reproducción no oficial; falta la URL oficial (gob.pe o *El Peruano*); con D18 la ficha dejó de tratarlo como «interno» (ver el episodio COVID-19). `fmi_2015b`: DOI del informe completo sin comprobar en doi.org (campo `verificar` en el `.bib`). `baffes_streifel_2016`: es un blog; conviene sustituirlo por el *Commodity Markets Outlook* de julio de 2016 (no leído). `nber_2021`, `ustr_2020` y `fmi_2016`: sin pendientes | `nber_2021`, `ustr_2020` y `fmi_2016`: Tesis e Informe, «Validación externa», sin marca (sin pendientes). `fmi_2015b`: Tesis, cap. 2, «Validación externa» (`sec:validacion`), `\verificar` sobre el DOI (commit `d7302e0`, hallazgo M-03); Informe, la misma sección, nota `v2-fmi` (commit `09b9c26`). Intento del 30-10-2026 de comprobar el DOI 10.5089/9781513520735.081 en doi.org: el proxy de la sesión rechazó la conexión (403); el DOI sigue sin comprobar y la marca sigue abierta. `oms_2023`, `pcm_2020` y `baffes_streifel_2016`: no se citan | Pendiente (metadatos menores); marca de `fmi_2015b` puesta (M-03) |
| — | Descarga de control de la API del BCRP (consulta del 08/10/2026) | Ninguno. El Rmd citaba dos valores de diciembre de 2025 tomados de una consulta a la API del BCRP no versionada, contra la regla 3 de `CLAUDE.md`. Se retiraron las cifras | Rmd: chunk `funciones` y sección 1, «Fuente, periodo y cobertura»; auditoría 2026-10-19, M-06 y N-03 | Cerrado: cifras retiradas del Rmd por decisión de Roberto (20-10-2026) |

### Episodios de referencia

Los episodios se fechan con fuentes externas, nunca a partir de las propias series (regla 6 de
`CLAUDE.md`). La convención está decidida desde el 24-10-2026 (**D7**: evento o anuncio externo;
tolerancia de ±3 meses y ±6 como sensibilidad; un episodio sin fin con fuente es puntual). Desde el
07-11-2026, **D18** precisa que «externo» significa *externo al análisis* (fuente fichada ajena a las
series, a los indicadores y a los cortes estimados), sea el evento peruano o extranjero. La
**tarea D9** del plan 3b (commit `3c416c2`) unificó las fechas en el archivo único
`data/referencia/episodios_referencia.csv`, que leen el Rmd final, los notebooks 05, 09a, 09b y
07b, y `notebooks/modelos_dl.py`. La **tarea L1** (commit `f904b5c`) sustituyó los cinco
`\pendiente` de `sec:validacion` por las citas fichadas, con las fechas por macro; E1 hizo lo
mismo en el informe. Las fuentes del BCRP no son necesarias para el fechado bajo D7 y siguen sin
poder consultarse (lista de descarga manual en `auditorias/notas/2026-10-24_bibliotecario.md`).

Marcas de episodios que siguen abiertas:

- **Tesis**, cap. 2, «Validación externa» (`sec:validacion`): dos `\verificar` de contenido
  (`bernanke_2013` y `congreso_2018`) y uno de metadatos (DOI de `fmi_2015b`, M-03); filas de la
  tabla anterior. No queda ningún `\pendiente`.
- **Informe**, cap. 2, «Validación externa»: las notas `v2-bern`, `v2-cong` y `v2-fmi`. No queda
  ningún `[CITA PENDIENTE]` de episodios.
- **RmdF**, **NB05** y `modelos_dl.py`: ninguna (leen el archivo único). Las marcas de las celdas 1
  y 16 de NB05 se retiraron con D9.
- **Antecedentes congelados**, cuyas marcas se conservan y no se cierran porque esos archivos ya
  no se reescriben: Rmd de exploración, 10 marcas `[VERIFICAR: fuente externa para fechar el
  episodio]` (chunk `funciones`, A.1, A.2 y pies de los chunks `b4-transiciones`, `b8-fases`,
  `bB3-transiciones`, `bB6-fases` y `bC4-episodios`); `06a` (4 marcas) y `06b` (6 marcas), con la
  nota de D9 que remite al archivo único. Sus fechas no se usan en la tesis ni en el informe.

| Episodio | Fecha vigente (`episodios_referencia.csv`) | Fuente de cada extremo (clave) | Alternativas fichadas y advertencias | Estado |
|---|---|---|---|---|
| Crisis financiera global | 2008-09 a 2009-06 | `lehman_brothers_2008` (15-09-2008); `nber_2010` (valle de la recesión de EE. UU.) | Pico del NBER en 12-2007 (no se usa: el anuncio externo del episodio financiero es Lehman). El inicio 2008-07 de `06a`/`06b` no tiene fuente (antecedente) | Cerrado (D9, L1) |
| *Taper tantrum* | 2013-05 a 2013-12 | `bernanke_2013` (22-05-2013); `reserva_federal_2013` (18-12-2013) | El inicio 2013-04 de `06a`/`06b` no tiene fuente (antecedente). Falta leer el pasaje del testimonio (`\verificar`) | Fechas cerradas; contenido de `bernanke_2013` pendiente |
| Colapso de los precios de las materias primas | 2014-06 a 2016-01 | `stocker_et_al_2015` (caída del petróleo); `fmi_2016` (febrero de 2016: primer aumento en cinco meses de los metales y en nueve del índice general) | Metales: caída «since 2011» (`fmi_2015b`), sin mes; `fmi_2015b` lleva `\verificar` y nota `v2-fmi` por el DOI (M-03; ver su fila). Comparación desde 09-2014 (`fmi_2015`), no es un inicio. Fin concordante: `baffes_streifel_2016`. **Advertencia:** el inicio es del petróleo; para los metales solo hay año | Cerrado (D9, L1); DOI de `fmi_2015b` pendiente (marca puesta) |
| Kuczynski / Odebrecht | Puntual, 2018-03 | `congreso_2018` (aceptación de la renuncia, 23-03-2018) | Período alternativo para sensibilidad: 2016-12 (`doj_2016`, declaración de culpabilidad de Odebrecht en EE. UU.) a 2018-03. El inicio 2016-07 (`congreso_2016`, juramentación) no es un evento del episodio. Falta el texto de la resolución en *El Peruano* (`\verificar`). **N-02 (auditoría del 29-10-2026), cerrado por D18 (07-11-2026):** «externo» es externo al análisis; la renuncia aceptada por el Congreso es un evento peruano con fuente ajena a las series y cumple D7. Ficha `congreso_2018` alineada | Fechado como puntual (D9); N-02 cerrado (D18) |
| Guerra comercial entre Estados Unidos y China | 2018-06 a 2020-01 | `ustr_2018` (anuncio del 15-06-2018); `ustr_2020` (firma de la «fase uno», 15-01-2020) | Inicio alternativo 2018-07 (cobro de aranceles, 06-07-2018; misma fuente). **Advertencia:** el fin (2020-01) y el inicio del COVID-19 (2020-03) distan dos meses: con ±3 meses, una transición en ese tramo no se atribuye a uno solo | Cerrado (D9, L1) |
| COVID-19 | 2020-03 a 2020-04 | `oms_2020b` (pandemia, 11-03-2020); `nber_2021` (valle de la recesión de EE. UU., mismo criterio que `nber_2010`) | Inicio alternativo 2020-01 (`oms_2020a`, ESPII), dentro de ±3 meses. Fin alternativo 2023-05 (`oms_2023`, fin de la ESPII), poco discriminante. `pcm_2020` (15-03-2020) se trató hasta 3b como contexto por ser «interno». **Con D18 es una fuente admisible.** Tema pendiente (no lo decide el bibliotecario): si `pcm_2020` debe fechar un extremo, por ejemplo el inicio del episodio en el Perú. Caería en el mismo mes que el inicio vigente (2020-03, `oms_2020b`), de modo que la fecha mensual no cambiaría, pero sí la fuente citada. **No se modificó `episodios_referencia.csv`.** Falta además su URL oficial. Las fechas 2020-09 y 2020-12 de los antecedentes no tienen fuente | Cerrado (D9, L1); N-02 cerrado (D18); tema pendiente: uso de `pcm_2020` como fuente de un extremo (Roberto) |

### Estado del arte (iteración 3c)

Obras fichadas el 07-11-2026 para el capítulo de antecedentes y estado del arte (tarea 1 del
bibliotecario en 3c). Ninguna se cita todavía en la tesis ni en el informe: no tienen marcas. La
fuente de cada dato está en la ficha y en `auditorias/notas/2026-11-07_bibliotecario.md`.
«Crossref» es el registro del DOI en api.crossref.org (doi.org no se pudo consultar directamente,
salvo para `borio_2014`, cuyo DOI resolvió hacia Elsevier).

| Clave | Metadatos verificados en | Lectura | Qué falta | Estado |
|---|---|---|---|---|
| `borio_2014` | Crossref; BIS (WP 395) | Resumen | Texto (hechos estilizados) | Cerrado (metadatos); contenido: solo resumen |
| `borio_lowe_2002` | BIS | Resumen | Texto (construcción de las brechas) | Cerrado (metadatos); contenido: solo resumen |
| `claessens_kose_terrones_2011` | Crossref; NBER; FMI (WP 11/76) | Resumen | Método de datación | Cerrado (metadatos); contenido: solo resumen |
| `claessens_kose_terrones_2012` | Crossref | Resumen (EconPapers, secundaria) | Resumen en la editorial; lista de países | Cerrado (metadatos); contenido pendiente |
| `aikman_haldane_nelson_2015` | Crossref | Ninguna | **Resumen y texto**: no atribuirle hallazgos (campo `verificar`) | Fichada (solo localizada); pendiente |
| `schuler_hiebert_peltonen_2015` | BCE (PDF) | Texto parcial (~72 %) | Resto del texto | Cerrado (metadatos) |
| `schuler_hiebert_peltonen_2020` | Crossref | Resumen (IDEAS, secundaria) | Resumen en la editorial | Cerrado (metadatos); contenido pendiente |
| `galati_et_al_2016` | Crossref; DNB (WP 495) | Resumen del WP (otro título) | Texto del artículo | Cerrado (metadatos) |
| `runstler_vlekke_2018` | Crossref (con resumen) | Resumen | — | Cerrado (metadatos); contenido: solo resumen |
| `strohsal_proano_wolters_2019` | Crossref; Universidad de Bamberg | DP 22/2015 del Bundesbank | Artículo publicado (parte internacional) | Cerrado (metadatos) |
| `hollo_kremer_lo_duca_2012` | BCE (PDF) | Texto parcial (~67 %) | Resto del texto | Cerrado (metadatos) |
| `illing_liu_2006` | Crossref; Banco de Canadá (WP 2003-14) | WP 2003-14, parcial | Artículo publicado | Cerrado (metadatos) |
| `harding_pagan_2002` | Crossref; ANU | Resumen | — | Cerrado (metadatos); contenido: solo resumen |
| `hamilton_2018` | Crossref; NBER (WP 23429) | Resumen del WP | — | Cerrado (metadatos); contenido: solo resumen |
| `hamilton_1989` | Econometric Society; Crossref | Resumen | — | Cerrado (metadatos); contenido: solo resumen |
| `kim_nelson_1999` | Catálogo de Texas A&M; Universidad de Washington | Descripción institucional | **DOI** solo en el catálogo (campo `verificar`) | Fichada (preliminar); pendiente (DOI) |
| `krolzig_1997` | Crossref | Ninguna | Texto; número de volumen de la serie | Cerrado (metadatos); contenido no consultado |
| `bai_perron_1998` | Econometric Society; Crossref | Resumen | — | Cerrado (metadatos); contenido: solo resumen |
| `bai_perron_2003` | Crossref (con resumen) | Resumen | — | Cerrado (metadatos); contenido: solo resumen |
| `truong_oudre_vayatis_2020` | Crossref | Texto del *preprint* (arXiv v3) | Fecha de aceptación del arXiv no cuadra con Crossref (anotado) | Cerrado (metadatos) |
| `aminikhanghahi_cook_2017` | Crossref; repositorio de WSU | Resumen | Texto (PMC no accesible) | Cerrado (metadatos); contenido: solo resumen |
| `pearson_1901` | Crossref | Ninguna | Texto | Cerrado (metadatos); contenido no consultado |
| `hotelling_1933` | Crossref | Ninguna | Texto; continuación en el n.º 7 (no se cita) | Cerrado (metadatos); contenido no consultado |
| `lebart_morineau_piron_1995` | Base Horizon del IRD; autoridad de la BnF | Ninguna | Texto (sección de cos²) | Cerrado (metadatos); contenido no consultado |
| `goodfellow_bengio_courville_2016` | Catálogo de la TUAT | Ninguna | Texto | Cerrado (metadatos); contenido no consultado |
| `chalapathy_chawla_2019` | arXiv | Resumen | *Preprint*: solo exploración (campo `verificar`). **19-11-2026:** la revisión publicada `pang_et_al_2021` puede ocupar su lugar | Fichada; *preprint* |
| `gomez_gonzalez_et_al_2013` | Repositorio del Banco de la República | Texto parcial | **Orden de autores** (campo `verificar`) | Fichada; pendiente (orden de autores) |
| `brandao_marques_perez_ruiz_2017` | FMI (PDF) | Resumen | **Grafía del primer autor** y DOI (campo `verificar`) | Fichada; pendiente (grafía) |
| `minaya_lupu_cabello_2017` | BIS | Resumen | — | Cerrado (metadatos); contenido: solo resumen |
| `alvarado_vargas_2021` | Repositorio de la Universidad de Lima | Resumen | Trabajo de pregrado: usar con cautela | Cerrado (metadatos); contenido: solo resumen |

**Obras candidatas no agregadas al `.bib`** (sin ficha; quedan pendientes):

| Obra | Motivo | Estado |
|---|---|---|
| Nivin y Pérez (2019), «Estimación de un índice de condiciones financieras para el Perú» (BCRP, Documento de Trabajo 2019-006; *Revista Estudios Económicos*, 37) | Localizada en búsquedas y en RePEc (secundaria). Los sitios del BCRP (bcrp.gob.pe e investigacion.bcrp.gob.pe) bloquean el acceso automatizado (Incapsula): no se verificó. No se buscaron rutas alternativas | Pendiente (descarga manual de Roberto) |
| BCRP, Documento de Trabajo 2022-002, «Financial stress and macroeconomic fluctuations in Peru» | Igual que la anterior: solo título en resultados de búsqueda; autores no vistos | Pendiente (descarga manual) |
| BCRP, *Revista Moneda* 188, «Financial stress index for Peru» | Igual: solo título en resultados de búsqueda; autores no vistos | Pendiente (descarga manual) |
| BCRP, Documento de Trabajo 2024-012, «Estimating new financial conditions indexes for the Peruvian economy» | Igual: solo título en resultados de búsqueda; autores no vistos | Pendiente (descarga manual) |
| Pérez Forero (2016), BCRP, Documento de Trabajo 2016-013 | Localizado solo en IDEAS (secundaria); además trata el ciclo económico, no el financiero | Sin prioridad |
| Repositorio PUCP, «El ciclo financiero global y las condiciones crediticias en el Perú» | El repositorio bloqueó el acceso automatizado (Anubis): ni autor, ni tipo, ni año vistos | Pendiente (descarga manual) |
| Rabanal (2022), *Ola Financiera*, 15(43), 30–52 (DOI 10.22201/fe.18701442e.2022.43.83496) | Verificada en la página de la revista (UNAM), pero **no incluye al Perú** y la página no da el nombre completo del autor | No agregada (relevancia baja); puede ficharse si el redactor la necesita |
| Amaral, Guerra, Shim y Tombini (2025), BIS Bulletin 113, «Financial conditions indices in Latin America» | Verificada en la página del BIS (29-09-2025), pero la página no menciona al Perú ni el método | No agregada hasta leer el PDF |
| Hodrick y Prescott (1997); Hamilton (1994), *Time series analysis* | No buscadas (fuentes primarias de filtros o manuales que la tesis no cita todavía). Harding y Pagan (2006) y Christiano y Fitzgerald (2003) se ficharon el 09-11-2026 (sección siguiente) | Sin ficha |

### Pendientes del cap. 2 (09-11-2026)

Encargo de la sesión de seguimiento del 09-11-2026 (rama `iteracion-3c`, commit de partida
`c564c35`): cerrar los `\pendiente` bibliográficos de `sec:ea-ciclo` y `sec:ea-regimenes`. Detalle
y fuente de cada dato en las fichas y en `auditorias/notas/2026-11-09_bibliotecario.md`. Las citas
**no** se integraron en la tesis ni en el informe: es tarea del redactor y del editor.

| Clave | Metadatos verificados en | Lectura | Qué falta | Marcas en los documentos | Estado |
|---|---|---|---|---|---|
| `bry_boschan_1971` | Página del libro en el NBER (título, autores, 1971, ISBN, capítulos); catálogo de la Universidad de Filipinas (lugar y serie *Technical Paper* 20) | Texto parcial: cap. 2 (pp. 7–63), lectura asistida por una herramienta que resume | DOI (no existe en las fuentes vistas); extensión del volumen; cotejar en el PDF las cifras del procedimiento antes de citarlas textualmente. Discrepancia anotada: el NBER atribuye cada capítulo solo a Boschan | Tesis: `\pendiente` conjunto en cap. 2, `sec:ea-ciclo`; listado en cap. 7 | Cerrado (metadatos); contenido parcial |
| `harding_pagan_2006` | Crossref; portal de la ANU | Resumen | **Ambigüedad registrada:** hay tres documentos de trabajo de los mismos autores fechados en 2006 (Melbourne WP 963 y 966; NCER WP 1; vistos solo en IDEAS). Se fichó el artículo de *Journal of Econometrics*, único revisado por pares y único sobre sincronización. **No se verificó** si el índice de concordancia se define aquí o en Harding y Pagan (2002) | Tesis: `\pendiente` conjunto en cap. 2, `sec:ea-ciclo`; listado en cap. 7 | Cerrado (metadatos); contenido: solo resumen; atribución del índice pendiente |
| `christiano_fitzgerald_2003` | Crossref; NBER (WP 7257, con la versión publicada) | Resumen del WP | Texto del artículo | Tesis: `\pendiente` conjunto en cap. 2, `sec:ea-ciclo`; listado en cap. 7 | Cerrado (metadatos); contenido: solo resumen |
| `kwiatkowski_et_al_1992` | Crossref | Resumen del WP de Cowles | Texto | Ver su fila en la tabla principal | Cerrado (metadatos, 09-11-2026) |
| Camiz y Diblasi (2013) | — | — | No localizada (seis búsquedas en total) | Ver su fila en la tabla principal | Pendiente de fichar (superado el 24-11-2026: fichada, M-03 d) |

Conteo de marcas en `c564c35` (sin cambios por esta tarea, que no toca los documentos):
`tesis_latex/capitulos/02_estado_arte.tex` tiene 7 ocurrencias de `\pendiente{`; las de las líneas
de Bry-Boschan/Harding-Pagan/Christiano-Fitzgerald y de Kwiatkowski et al. pueden cerrarse ahora.
El conteo general por documento no se rehízo en esta sesión.

### Pendientes fuera de resultados (11-11-2026)

Encargo de la sesión de seguimiento del 11-11-2026 (rama `iteracion-3c`, commit de partida
`780450d`): cerrar los `\pendiente` bibliográficos de la tesis LaTeX fuera del capítulo de
resultados. Detalle y fuente de cada dato en las fichas y en
`auditorias/notas/2026-11-11_bibliotecario.md`. Las citas **no** se integraron en la tesis ni en
el informe: es tarea del redactor y del editor.

| Clave | Metadatos verificados en | Lectura | Qué falta | Marcas en los documentos | Estado |
|---|---|---|---|---|---|
| `said_dickey_1984` | Crossref; Oxford Academic (página del artículo) | Resumen | Texto (regla de rezagos, tablas) | Tesis: `\pendiente` en cap. 4, `sec:met-diagnostico`; listado en cap. 7 | Cerrado (metadatos); contenido: solo resumen |
| `frontier_1976` | Crossref | Ninguna (sin resumen oficial visto) | Texto; cotejo con la ref. [10] de Camiz y Pillar (2018) | Tesis: `\pendiente` en cap. 1, `sec:oe`, y cap. 3, `sec:retencion` | Cerrado (metadatos); ficha preliminar |
| Denimal (2001) | — | — | No localizada (dos búsquedas más, 11-11-2026) | Tesis: `\pendiente` en cap. 3, `sec:hfc` | Pendiente de fichar |
| Bootstrap por bloques conjunto | — | Resumen del cap. 2 de `lahiri_2003` (no lo trata) | Obra cuyo resumen o texto sustente el esquema con los mismos inicios de bloque | Tesis: `\pendiente` en cap. 3, `obs:nulo-estructura` | Pendiente de identificar |
| Camiz y Diblasi (2013) | — | — | No se repitió la búsqueda (seis fallidas) | Ver su fila en la tabla principal | Pendiente de fichar (superado el 24-11-2026: fichada, M-03 d) |

Entradas del `.bib`: 103 (101 + `said_dickey_1984` y `frontier_1976`), sin claves duplicadas y
todas con ficha en `papers/`; comprobado con un parseo de pybtex. Conteo de marcas no rehecho (la
tarea no toca los documentos).

### Pendientes del marco teórico (13-11-2026)

Encargo de la sesión de seguimiento del 13-11-2026 (rama `iteracion-3c`, commit de partida
`c0fa997`): cerrar, en lo verificable contra fuentes oficiales, dos `\pendiente` del marco teórico.
Detalle y fuente de cada dato en las fichas y en `auditorias/notas/2026-11-13_bibliotecario.md`.
Las citas **no** se integraron en la tesis ni en el informe: es tarea del redactor y del editor.

| Clave | Metadatos verificados en | Lectura | Qué falta | Marcas en los documentos | Estado |
|---|---|---|---|---|---|
| `guttman_1953` | Cambridge Core (página del artículo) | Resumen | Texto; que el resumen **no** menciona las correlaciones parciales (solo imagen/anti-imagen y la inversa de $\mathbf{R}$) | Tesis: `\pendiente` en cap. 3, `sec:adecuacion` (l. ~544). Informe: `[CITA PENDIENTE]` en la misma sección | Ficha preliminar (resumen). Sostiene la anti-imagen desde $\mathbf{R}^{-1}$, **no** la igualdad con la correlación parcial |
| `escofier_pages_2023` | Portada y créditos del extracto oficial de Dunod (Feuilletage_3448.pdf) | Texto parcial: pp. iii–viii y 1–28 (incluye la sección 1.9) | Total de páginas; fórmulas exactas; secciones 3.9 y 9.2 | Tesis: `\pendiente` en cap. 3, `sec:cos2` (l. ~429), y cap. 2, `02_estado_arte.tex` (l. ~291). Informe: `[CITA PENDIENTE]` en la misma sección | Cerrado (terminología: qualité de représentation = cos², contribution à l'inertie, para individuos y variables) |
| `lebart_morineau_piron_1995` | Base Horizon del IRD; autoridad de la BnF (metadatos, 07-11-2026) | Ninguna | La sección de cos²/contribuciones no se localizó en 3c | Era la candidata de `sec:cos2`; se sustituye por `escofier_pages_2023` | Sigue abierta en cuanto a su sección de cos²; queda como marco general de la escuela francesa |

Búsquedas (dos o tres por tema, según el encargo): tema 1 (anti-imagen/correlación parcial) —
Dempster «Covariance selection» (Crossref bloqueado y sin hallazgo útil) y Guttman (1953), hallado
y verificado en Cambridge Core. Tema 2 (cos²/contribuciones) — tabla de contenidos de Lebart et al.
(no localizada en las bases vistas), página de Dunod de la 4.ª ed. de Lebart (sommaire sin esas
entradas) y, al seguir el enlace de «feuilletage» de esa página, el extracto de Escofier y Pagès
(2023), cuya sección 1.9 sí las trae. Entradas del `.bib`: 105, sin claves duplicadas y todas con
ficha en `papers/` (parseo de pybtex). Conteo de marcas no rehecho (la tarea no toca los documentos).

### Pendientes bibliográficos (15-11-2026)

Encargo de la sesión de seguimiento del 15-11-2026 (rama `iteracion-3c`, commit de partida
`9aa3b33`): cerrar, en lo verificable contra fuentes oficiales, tres `\pendiente` bibliográficos
fuera del capítulo de resultados y, si quedaba margen, el del bootstrap por bloques conjunto.
Detalle y fuente de cada dato en las fichas y en `auditorias/notas/2026-11-15_bibliotecario.md`.
Las citas **no** se integraron en la tesis ni en el informe: es tarea del redactor y del editor.

| Clave | Metadatos verificados en | Lectura | Qué falta | Marcas en los documentos | Estado |
|---|---|---|---|---|---|
| `lavit_et_al_1994` | Cabecera impresa del artículo (facsímil en la *Three-Mode Bibliography*, Leiden): revista, volumen 18, 1994, pp. 97–119, autores y filiaciones. DOI solo en MaRDI (secundaria); doi.org bloqueado | Texto parcial: resumen y pasajes de la sección 1 sobre el «dual STATIS method» | Número del fascículo; DOI en la editorial; secciones que desarrollan el método | Tesis: `\pendiente` en cap. 2, `sec:ea-factoriales` (l. ~294, parte «STATIS dual»). Informe: sin marca equivalente (`git grep` del 15-11-2026) | Ficha preliminar. Sostiene que el STATIS dual trata *K* grupos de observaciones con las mismas *J* variables y matrices de covarianzas por etapa; **no** sus fórmulas |
| Camiz y Diblasi (2013) | — | — | No localizada (siete búsquedas en total; E-ICES 8 descartada) | Tesis: `\pendiente` en cap. 2 (l. ~294) y cap. 3 (l. ~778) | Pendiente de fichar; pedido a Roberto (superado el 24-11-2026: Roberto ya había leído el PDF el 7-11-2026 en `main`; fichada, M-03 d) |
| Denimal (2001) | — | — | No localizada (cuatro búsquedas en total) | Tesis: `\pendiente` en cap. 3, `sec:hfc` (l. ~609) | Pendiente de fichar; pedido a Roberto |
| Bootstrap por bloques conjunto | — | — | No se buscó hoy | Tesis: `\pendiente` en cap. 3, `obs:nulo-estructura` (l. ~1599) | Pendiente; para otra jornada |

Entradas del `.bib`: 106 (105 + `lavit_et_al_1994`), sin claves duplicadas y todas con ficha en
`papers/` (parseo de pybtex). Conteo de marcas no rehecho (la tarea no toca los documentos).

### Pendientes bibliográficos (17-11-2026)

Encargo de la sesión de seguimiento del 17-11-2026 (rama `iteracion-3c`, commit de partida
`d4841e9`): fuente del bootstrap por bloques conjunto (prioridad) y, si quedaba margen, una
referencia revisada por pares sobre detección de cambios en la matriz de covarianzas. Detalle y
fuente de cada dato en las fichas y en `auditorias/notas/2026-11-17_bibliotecario.md`. Las citas
**no** se integraron en la tesis ni en el informe: es tarea del redactor y del editor.

| Clave | Metadatos verificados en | Lectura | Qué falta | Marcas en los documentos | Estado |
|---|---|---|---|---|---|
| `lahiri_2003` (bootstrap por bloques conjunto) | SpringerLink (24-10-2026) | Texto parcial: sec. 2.5 (pp. 25 y 29) y p. 176, en una copia de los caps. 2 y 7 de un sitio docente (no editorial; sin portada; paginación coherente con el índice de Springer) | Lectura en una copia de la editorial o de biblioteca; demostraciones y caps. 3–6 | Tesis: `\pendiente` en cap. 3, `obs:nulo-estructura` (l. ~1599), y `\verificar` de l. ~1465. Informe: `[CITA PENDIENTE]` en la observación sobre los supuestos del nulo (`02_marco_teorico.qmd`) | Fuente identificada. Sostiene que la descripción del MBB se aplica a observaciones vectoriales; que eso equivale a los mismos inicios para todas las series es lectura de la tesis |
| `kunsch_1989` | — (Project Euclid bloqueado otra vez) | — | Páginas y contenido | Sin cambios | Ficha preliminar; no se le atribuye el caso vectorial |
| `aue_et_al_2009` | Penn State Pure (repositorio institucional) y referencia de revista de arXiv:0911.3796; no en Project Euclid (bloqueado) ni en Crossref (sin permiso) | Resumen | Metadatos en la editorial; texto | Tesis: `\pendiente` en cap. 2, `sec:ea-cambio` (l. ~235). Informe: sin marca equivalente localizada | Ficha preliminar (FB-108). Sostiene que existe un contraste no paramétrico asintótico de estabilidad de volatilidades y covolatilidades de series multivariadas; **no** su estadístico ni sus supuestos |

Entradas del `.bib`: 107 (106 + `aue_et_al_2009`), sin claves duplicadas y todas con ficha en
`papers/` (parseo de pybtex). Conteo de marcas no rehecho (la tarea no toca los documentos).

### Pendientes bibliográficos (19-11-2026)

Encargo de la sesión de seguimiento del 19-11-2026 (rama `iteracion-3c`, commit de partida
`67a9979`): fuentes revisadas por pares para el `\pendiente` de `02_estado_arte.tex` (l. ~345) sobre
el error de reconstrucción de autoencoders como señal de anomalía en series multivariadas y sobre
aprendizaje profundo con series macrofinancieras cortas; en segundo lugar, la fuente de Adam. Detalle
y fuente de cada dato en las fichas y en `auditorias/notas/2026-11-19_bibliotecario.md`. Las citas
**no** se integraron en la tesis, el informe ni el Rmd.

| Clave | Metadatos verificados en | Lectura | Qué falta | Marcas en los documentos | Estado |
|---|---|---|---|---|---|
| `audibert_et_al_2020` (USAD, KDD 2020) | Repositorio de EURECOM (registro y versión de los autores); no en ACM DL ni Crossref (sin permiso) | Texto parcial: sec. 3.2 («Autoencoder-based anomaly detection uses the reconstruction error as the anomaly score»), 3.3, 5.2 y 6 | Páginas, título del volumen y editorial (campo `verificar`) | Tesis: `\pendiente` en cap. 2, `sec:dl` (l. ~345). Informe: sin marca equivalente | Ficha preliminar (FB-111). Sostiene la primera mitad del `\pendiente` |
| `su_et_al_2019` (OmniAnomaly, KDD 2019) | Stevens Pure (repositorio institucional; revisado por pares); no en ACM DL ni Crossref | Resumen | **Orden de autores** (difiere de una base secundaria) | Ídem | Ficha preliminar (FB-110). Sostiene el uso de la probabilidad de reconstrucción en series multivariadas |
| `pang_et_al_2021` (*ACM Computing Surveys*) | Repositorios de UTS y SMU; arXiv:2007.02500; no en ACM DL ni Crossref | Resumen | **Año** (2021 en UTS, 2022 en SMU) y número de artículo | Puede sustituir a `chalapathy_chawla_2019` en `sec:dl` | Ficha preliminar (FB-109). El resumen no menciona autoencoders ni series de tiempo |
| `kingma_ba_2015` (Adam) | arXiv (nota de los autores) y UvA-DARE | Resumen | Sitio de ICLR no consultado | Rmd: A.5, `[VERIFICAR: sin ficha]` (fila «Fuente del optimizador Adam» de la tabla principal) | Cerrado (metadatos) |
| — (aprendizaje profundo con series macrofinancieras cortas) | — | — | Una fuente revisada por pares; la búsqueda solo dio *preprints* y documentos sin revisión | Segunda mitad del `\pendiente` de `sec:dl` | **Sigue pendiente** |

Entradas del `.bib`: 111 (107 + 4), sin claves duplicadas y todas con ficha en `papers/` (conteo con
expresión regular; pybtex no estaba instalado y no se instaló). Conteo de marcas no rehecho (la tarea
no toca los documentos).

### Pendientes bibliográficos (21-11-2026)

Encargo de la sesión de seguimiento del 21-11-2026 (rama `iteracion-3c`, commit de partida
`b864902`): búsqueda dirigida de fuentes revisadas por pares sobre redes recurrentes o autoencoders con
datos macrofinancieros de baja frecuencia y la limitación del tamaño de muestra, para el `\pendiente`
de `02_estado_arte.tex`, `sec:ea-dl` (l. ~355); en segundo lugar, Sakurada y Yairi (2014). Detalle y
fuente de cada dato en las fichas y en `auditorias/notas/2026-11-21_bibliotecario.md`. Las citas **no**
se integraron en la tesis ni en el informe.

| Clave | Metadatos verificados en | Lectura | Qué falta | Marcas en los documentos | Estado |
|---|---|---|---|---|---|
| `tolo_2020` (*Journal of Financial Stability*, 49) | Repositorio del Banco de Finlandia (urn.fi: volumen 49, agosto de 2020) y research.fi (revista, ISSN, tipo A1 arbitrado); DOI y número de artículo solo en RePEc. doi.org y ScienceDirect sin permiso | Resumen | Número de artículo (100746) y DOI en la editorial; texto (validación y tamaño de muestra no leídos) | Tesis: `\pendiente` en cap. 2, `sec:ea-dl` (l. ~355); listado en cap. 7, `sec:pend-marcas`. Informe: sin marca equivalente | Ficha preliminar (FB-113). Sostiene que hay LSTM/GRU revisadas por pares sobre datos macrofinancieros (17 países, 1870–2016); **no** sostiene nada sobre el tamaño de muestra |
| `beutel_list_von_schweinitz_2019` (*Journal of Financial Stability*, 45) | Repositorio del IWH (autores, revista, vol. 45, diciembre de 2019, DOI); número de artículo en el repositorio de código del autor | Resumen del artículo; texto parcial del DP 48/2018 del Bundesbank | Número de artículo en la editorial; pasajes sobre el sobreajuste en la versión publicada | Ídem | Ficha preliminar (FB-114). Sostiene que el aprendizaje automático flexible logra un ajuste alto dentro de la muestra y pierde frente al logit fuera de ella. **No incluye redes neuronales** |
| — (aprendizaje **profundo** y tamaño de muestra, en revista) | — | Chung (arXiv:2310.17571) sí lo discute, pero es *preprint* sin revista localizada | Fuente revisada por pares que trate explícitamente la limitación para redes profundas | Segunda mitad del `\pendiente` de `sec:ea-dl` | **Cerrable en parte** con las dos fichas (ver la «Regla para el redactor» de la nota) |
| `sakurada_yairi_2014` (sin ficha) | — | — | Metadatos en ACM Digital Library: solo se localizó en fuentes secundarias (BibBase, Springer Professional) | Ninguna | Pendiente de fichar |

Entradas del `.bib`: 113 (111 + 2), sin claves duplicadas, llaves balanceadas y todas con ficha en
`papers/` (conteo con expresión regular; pybtex no instalado). Conteo de marcas no rehecho (la tarea
no toca los documentos).

### Reconciliación con `main` (24-11-2026, M-03 d)

Encargo del seguimiento del 24-11-2026, vuelta 1 de la iteración 3c (rama `iteracion-3c`, commit de
partida `594e826`; hallazgo M-03 d de `auditorias/2026-11-23_iteracion-3c.md`). `origin/main` tenía,
respecto del *merge-base* `b893b23`, seis fichas nuevas, tres fichas modificadas y una sección del
registro («Actualización del 8-11-2026», commit `63c6914`) que la rama no tenía. Las lecturas son de
Roberto (PDF de la carpeta de Dropbox del asesor); el bibliotecario **no** tuvo acceso a esos PDF y
conserva sus declaraciones de lectura tal cual. Las seis fichas se pasaron al formato de la Ficha
Estándar sin agregar contenido. Detalle y fuente de cada dato en las fichas y en
`auditorias/notas/2026-11-24_bibliotecario.md`. El informe y sus `.bib` propios de `main`
(`tesis/informe_mmc102/`, `tesis/informe_preliminar_uni/`) **no** se tocaron (M-03 c, decisión de
Roberto pendiente).

**Sección de `main` conservada como rastro** (texto de `63c6914`; las referencias de esa tabla estaban
en `tesis/informe_preliminar_uni/referencias_extra.bib`):

| Clave | Estado (en `main`, 8-11-2026) | Pendiente (en `main`) |
|---|---|---|
| `fisher_1958` | Texto completo leído (ficha actualizada) | Revisar las secciones 4 a 6 de la ficha |
| `horn_1965` | Texto completo leído (ficha actualizada) | — |
| `camiz_diblasi_2013` | **Localizada** y leída completa (antes «no localizada») | Datos de edición de las actas |
| `abdi_2010` | Leída completa; ficha nueva | Páginas y DOI del capítulo |
| `camiz_2021_pca` | Leída (secciones 1–2.1); material de clase no publicado | Usar junto con fuentes publicadas |
| `camiz_spada_2024` | Leída (métodos y conclusiones); ficha nueva | Resultados completos |
| `purizaca_2023` | Leída completa; ficha nueva | URL del repositorio PUCP |
| `torres_baltazar_2023` | Lectura parcial; ficha nueva | URL del repositorio |
| `camiz_aedeclahfac`, `camiz_claede_2025` | Programas del asesor (no publicados) | Confirmar con el Dr. Camiz cómo citarlos |
| `samaniego_2026` | Informe propio del curso MMC101 | — |

**Estado en la rama después de la reconciliación:**

| Clave | Ficha | Metadatos verificados en (24-11-2026) | Lectura (declarada) | `.bib` | Qué falta | Estado |
|---|---|---|---|---|---|---|
| `camiz_diblasi_2013` | FB-115, nueva | Ninguna fuente oficial: solo el PDF (ficha de Roberto). Octava búsqueda web sin actas | Completa (Roberto, 7-11-2026) | Agregada (`@unpublished`, con `verificar`) | Actas, ISBN o URL; nombre de pila de la segunda autora | **Fichada** (antes «No localizada») |
| `fisher_1958` | Combinada (rama + `main`) | Páginas: en el artículo (lectura de Roberto). Vol., núm. y DOI: título de la página de Taylor & Francis (20-10-2026) | Completa (Roberto, 8-11-2026) | Se retira `verificar` | Abrir la editorial o doi.org (bloqueados) | **Cerrado** (antes «Pendiente», preliminar) |
| `horn_1965` | Combinada (rama + `main`) | Cambridge Core y SpringerLink (20-10-2026) | Completa (Roberto, 8-11-2026) | Sin cambios | — | **Cerrado** (antes «contenido: solo resumen») |
| `congreso_2018` | Sin cambios: la versión de la rama ya contiene la corrección de `main` (D18) y la amplía | — | — | Sin cambios | Texto de la resolución en *El Peruano* | Igual que antes |
| `camiz_spada_2024` | FB-116, nueva | Título: página de la revista vista en el buscador (artículo 2455 = sufijo del DOI). Vol. 49(1), pp. 13–23 y DOI: solo del PDF. doi.org y la revista: permiso no respondido | Parcial (Roberto, 8-11-2026) | Agregada (con `verificar`) | Cotejo en doi.org o la revista; resultados completos | Fichada. **Contradice** el vacío 2 de `02_estado_arte.tex` (no hay EHFC publicada): decide Roberto |
| `abdi_2010` | FB-117, nueva | SAGE Knowledge (editorial): entrada «Congruence», Salkind (Ed.), 2010, pp. 223–229, DOI 10.4135/9781412961288.n71. Autor y subtítulo: solo del PDF | Completa (Roberto, 7-11-2026) | No (la tesis no la necesita; el RV se cita con `robert_escoufier_1976`) | — | Fichada; metadatos cerrados |
| `camiz_2021_pca` | FB-118, nueva | No aplica (material no publicado) | Parcial (Roberto, 7-11-2026) | No (no citable) | — | Fichada como exploración |
| `purizaca_2023` | FB-119, nueva | No: el repositorio de la PUCP devolvió una página antirrobots; tres registros de ALICIA eran otras tesis | Completa (Roberto, 8-11-2026) | No | *Handle* y año de registro | Fichada; metadatos pendientes |
| `torres_baltazar_2023` | FB-120, nueva | No: una búsqueda no halló el registro de ESAN | Parcial (Roberto, 8-11-2026) | No | URL del repositorio | Fichada; metadatos pendientes |
| `camiz_aedeclahfac`, `camiz_claede_2025`, `samaniego_2026` | Sin ficha (en `main` solo están en el `.bib` del informe preliminar) | — | — | No | Confirmar con el Dr. Camiz cómo citar los programas | Fuera del encargo (dependen de M-03 c) |

Entradas del `.bib`: 115 (113 + `camiz_diblasi_2013` y `camiz_spada_2024`), sin claves duplicadas,
llaves balanceadas y todas con ficha en `papers/` (conteo con expresión regular; pybtex y biber no
instalados: el `.bib` **no** se compiló con biber). Conteo de marcas no rehecho (la tarea no toca los
documentos).

### Ponencia y cotejo de Camiz y Spada (25-11-2026)

Vuelta 1 de la iteración 3c, sobre `34a7181`, a pedido del redactor (`auditorias/notas/2026-11-24_redactor-latex.md`,
sección 4). Detalle y fuentes en `auditorias/notas/2026-11-25_bibliotecario.md`.

| Clave | Qué se hizo | Fuente consultada | Resultado | Estado |
|---|---|---|---|---|
| `camiz_diblasi_2013` | Tipo de entrada `@unpublished` → `@presentation` (biblatex-apa, APA 10.5). Clave, campos y `verificar` sin cambios; ningún dato nuevo | `apa.bbx` v9.17: el *driver* `unpublished` no imprime `eventtitle`; el *driver* `presentation` lo imprime con `venue` (macro `eventinfo`) | Compilado con `latexmk` (biber): «Camiz, S., & Diblasi, A. (2013). *Evolutionary principal component analysis* [Ponencia]. XLI Coloquio Argentino de Estadística, Mendoza, Argentina.» Sin citas indefinidas | Corregida la impresión; metadatos siguen con `verificar` (solo del PDF) |
| `camiz_spada_2024` | Nuevo intento de cotejo | doi.org/10.12899/asr-2455: permiso no respondido (no se reintentó). Página de la revista (journals-crea.4science.it, artículo 2455): redirige a creajournals.crea.gov.it, permiso no respondido. DOAJ (directorio, base secundaria): título, autores «Sergio Camiz» y «Francesco Spada», vol. 49, núm. 1, DOI 10.12899/asr-2455, **fecha «Oct 2023»**, sin páginas | No confirmado en fuente oficial. **Discrepancia de año:** DOAJ fecha el número en octubre de 2023; la entrada dice 2024 (del PDF). Páginas 13–23 sin segunda fuente | Sin cambios en ficha ni `.bib` (`verificar` se mantiene); año en duda |

Para el informe (Quarto, `tesis/apa.csl`): pandoc 3.1.3 lee `@presentation` sin tipo CSL (`""`) y
`@unpublished` con evento como `speech`; con el CSL del proyecto ambas salen igual: «… analysis.
Ponencia. XLI Coloquio Argentino de Estadística, Mendoza, Argentina.» (la descripción no va entre
corchetes). El informe aún no cita la obra; si la cita, el editor debe revisar esa salida con el pandoc
de Quarto.

### Fase 0 de la vuelta 2: Camiz y Spada, `.bib` de `main` y fichas en conflicto (27-11-2026)

Tareas F0-5 y F0-6 de `asesoria/2026-11-26_plan-cierre-iteracion-3c.md`, rama `iteracion-3c` sobre
`402f6f3`; `origin/main` en `1bb4dcb` (tras `git fetch`). Detalle y fuentes en
`auditorias/notas/2026-11-27_bibliotecario.md`. **Ningún `.bib` se modificó**
(`git diff 7c58906 -- tesis/referencias.bib` vacío).

**F0-5 · `camiz_spada_2024`.**

| Fuente | Resultado |
|---|---|
| doi.org/10.12899/asr-2455 (WebFetch) | Permiso no respondido; no se reintentó |
| doi.org (negociación de contenido) y api.crossref.org (`curl`) | Proxy de la sesión: 403 (política de salida); no se reintentó |
| api.crossref.org/works/10.12899/asr-2455 (WebFetch) | Permiso no respondido |
| Revista: journals-crea.4science.it, artículo 2455 (vista y PDF) | 302 a creajournals.crea.gov.it; ese dominio: permiso no respondido |
| CRIS de la PUCP | Página antirrobots («Access Denied») |
| IRIS Sapienza (hdl 11573/507241) y core.ac.uk (354494486), hallados por el buscador | Otras obras (`camiz_roig_2011` y `camiz_et_al_2020`); sin datos de este artículo |

Resultado: **sin verificar** en fuente oficial el año (2023 en DOAJ, base secundaria; 2024 en el PDF),
las páginas 13–23 ni el DOI. Ficha: solo se agregó el año a la marca `[VERIFICAR]` y se registraron los
intentos del 25 y del 27-11-2026. `.bib`: sin cambios; su campo `verificar` **no** menciona el año en
duda (anotado para W-5/W-7: lo corrige el bibliotecario cuando se pueda tocar el `.bib`). Sigue sin
cita en la tesis hasta R-4.

**Hallazgo colateral (`camiz_roig_2011`).** El registro de IRIS Sapienza (repositorio institucional
de la universidad del primer autor; hdl 11573/507241, tipo «Atto di comunicazione a congresso») muestra:
autores Camiz y Roig, F. A.; título «Evolutionary analysis applied to tree-ring series»; «Actas E-ICES
6»; «Comisión Nacional de Energía Atómica - CNEA»; 2011; pp. 30-37; ISBN 9789871323210. Coincide con la
entrada del `.bib`. **No lista editor:** el editor «O. Papú» sigue inferido y su `verificar` se
mantiene. Ni la ficha ni el `.bib` se tocaron (fuera del encargo); queda para la próxima vuelta del
bibliotecario.

**F0-6 (a) · claves de los `.bib` del informe en `origin/main`.** `tesis/informe_mmc102/referencias.bib`:
67 entradas; `referencias_extra.bib`: 21 (3 repetidas en ambos: `lorenzo_seva_ten_berge_2006`,
`robert_escoufier_1976`, `josse_pages_husson_2008`). 85 claves distintas.

| Clase | Claves | N.º |
|---|---|---|
| Ya en `tesis/referencias.bib` | Las 67 de `referencias.bib`; de `referencias_extra.bib`: `camiz_diblasi_2013`, `camiz_spada_2024`, `kwiatkowski_et_al_1992`, `goodfellow_bengio_courville_2016`, `borio_2014` (más las 3 repetidas) | 72 |
| Con ficha en `papers/`, sin entrada | `abdi_2010`, `camiz_2021_pca`, `purizaca_2023`, `torres_baltazar_2023` | 4 |
| Sin ficha (ni en la rama ni en `main`) | `camiz_aedeclahfac`, `camiz_claede_2025`, `samaniego_2026`, `alcaraz_cabello_nivin_2024`, `winkelried_2017`, `rumelhart_hinton_williams_1986`, `jolliffe_cadima_2016`, `lecun_bengio_hinton_2015`, `srivastava_et_al_2014` | 9 |

Diferencias de campos clave (tipo, año, volumen, número, páginas, DOI) en las 72 compartidas: solo tres.
`camiz_diblasi_2013` es `@misc` en `main` y `@presentation` en la rama (cambio del 25-11-2026);
`kwiatkowski_et_al_1992`, DOI con «Y» final en `main` y «y» en la rama (los DOI no distinguen
mayúsculas); `lorenzo_seva_ten_berge_2006`, sin DOI en `main` y con DOI en la rama.

Citas en el informe de `main` (`git grep` en los `.md` de `tesis/informe_mmc102/`; los conteos de
líneas incluyen la copia concatenada `_tmp_informe.md`): `alcaraz_cabello_nivin_2024` (6 líneas;
`01_introduccion.md` y `02_marco_teorico.md`) y `winkelried_2017` (2; `02_marco_teorico.md`) se citan
**sin ficha**; `purizaca_2023` (6; `02_marco_teorico.md`) se cita con ficha y sin entrada en el `.bib`
único. Las otras diez claves sin entrada no se citan. Estas tres son prioritarias
para W-7 (R-7). `camiz_2021_pca` no se agrega por criterio de la ficha (material no publicado).

**F0-6 (b) · nueve fichas en conflicto.** Comparación de `git show origin/main:papers/<f>.qmd` con la
rama (lectura completa y búsqueda automática de frases de `main` ausentes en la rama).

| Ficha | Conflicto | ¿La rama pierde algo de `main`? |
|---|---|---|
| `abdi_2010` | *add/add* | **Sí, menor:** la remisión «(§2.2.7 del informe)» del aporte. El resto está o se superó con datos verificados (páginas y DOI de SAGE) |
| `camiz_2021_pca` | *add/add* | No |
| `camiz_diblasi_2013` | *add/add* | No |
| `camiz_spada_2024` | *add/add* | No |
| `purizaca_2023` | *add/add* | No |
| `torres_baltazar_2023` | *add/add* | No |
| `fisher_1958` | contenido | No: la nota de lectura de `main` está literal; la pregunta abierta de `main` sobre el caso multivariado se respondió con esa misma nota |
| `horn_1965` | contenido | No: la declaración de lectura de `main` está literal; «228 × 17» pasó a «228 × 16» por D16 |
| `congreso_2018` | contenido | No: «evento nacional, externo al análisis en el sentido de la decisión D18» (`main`) y «evento peruano; externo al análisis en el sentido de D18» (rama) dicen lo mismo |

Resolución propuesta para la fusión: tomar la versión de la rama en las nueve y, en `abdi_2010`,
reponer la remisión al §2.2.7 del informe. No se editó la ficha (no es un dato bibliográfico
verificado).

### Marcas `\pendiente` no bibliográficas de la tesis LaTeX y recuadros «Pendiente» del informe

Se registran para que cada `\pendiente` tenga su fila. No son referencias y no las cierra el
bibliotecario.

| Ubicación | Marca | Responsable | Estado |
|---|---|---|---|
| Tesis: `00_portada.tex`, denominación del grado | Denominación exacta del grado según las pautas de la UNI | Roberto / redactor LaTeX | Pendiente |
| Informe: `00_resumen.qmd`, recuadro «Pendiente» | Resumen y *abstract*, cuando los capítulos 1 a 5 estén aprobados (sin equivalente en la tesis) | Editor del informe | Pendiente |
| Tesis: `03_metodologia.tex`, «Qué vía mide qué» (`sec:met-vias`). Informe: cap. 3, recuadro «Pendiente» de la misma sección | Sección por redactar después de la reunión con el Dr. Camiz sobre la Parte C de D2 (decisión N del plan 3b) | Roberto (reunión N); después, redactor LaTeX y editor del informe | Pendiente (nueva en L3/E2) |
| Tesis: `03_metodologia.tex`, «Validación externa» (`sec:met-validacion`). Informe: cap. 3, recuadro «Pendiente» de la misma sección | Autoencoders y redes LSTM con las 16 series vigentes, a la espera de la iteración 4 (entorno con `torch`) | Desarrollador (iteración 4); después, redactor LaTeX y editor del informe | Pendiente (nueva en L3/E2) |
| Tesis: `03_metodologia.tex`, inicio del capítulo | Capítulo por redactar (marca de la iteración 3a) | Redactor LaTeX | **Cerrado** en L3 (el capítulo está redactado; la marca ya no existe) |
| Tesis: `04_resultados.tex`, inicio del capítulo. Informe: `04_resultados.qmd`, recuadro «Pendiente» | Capítulo por redactar; requiere la Parte C y la aprobación de Roberto (regla 7) | Redactor LaTeX y editor del informe, con la aprobación de Roberto | Pendiente |
| Tesis: `05_conclusiones.tex`, inicio del capítulo. Informe: `05_conclusiones.qmd`, recuadro «Pendiente» | Capítulo por redactar a partir del capítulo de resultados | Redactor LaTeX y editor del informe | Pendiente |

### Conteo de marcas abiertas (tarea B4 del plan 3b)

Conteo de ocurrencias con `git grep -o` sobre cada commit (guion del bibliotecario en el
*scratchpad* de la sesión del 29-10-2026; patrones en `auditorias/notas/2026-10-29_bibliotecario.md`).
«Antes» es `origin/main` (`4624802`, inicio de la iteración 3b); «registro anterior», el commit de
B1–B4 (`d1bf179`); «después», `e97530c`, y «M-03», `09b9c26` (marca de `fmi_2015b`, vuelta 1).
El 30-10-2026 se volvió a correr el mismo guion con los mismos patrones: reproduce las cifras de
`e97530c` y da las de `09b9c26`; entre ambos, el commit de la auditoría (`bc17259`) no cambia nada.
El 07-11-2026 (iteración 3c) se contó sobre `605803a`, último commit de la rama `iteracion-3c` al
empezar la tarea, con los mismos patrones (en la tesis, `git grep -o -F '\verificar{'` y
`'\pendiente{'`): no hay cambios respecto de `09b9c26`. El trabajo en curso del redactor (sin
commit al momento del conteo) no se contó. Las 30 obras de 3c no agregan marcas porque aún no se
citan; las que llevan campo `verificar` en el `.bib` son `aikman_haldane_nelson_2015`,
`kim_nelson_1999`, `chalapathy_chawla_2019`, `gomez_gonzalez_et_al_2013` y
`brandao_marques_perez_ruiz_2017`: si se citan, el texto debe llevar la marca.

| Documento y marca | Antes (`4624802`) | Registro anterior (`d1bf179`) | Después (`e97530c`) | M-03 (`09b9c26`) | 3c (`605803a`) |
|---|---|---|---|---|---|
| Tesis, `\verificar` | 34 | 34 | 51 | 52 | 52 |
| Tesis, `\pendiente` | 22 | 22 | 14 | 14 | 14 |
| Informe, notas con `VERIFICAR` | 34 | 34 | 51 | 52 | 52 |
| Informe, `[CITA PENDIENTE]` | 18 | 18 | 9 | 9 | 9 |
| Informe, recuadros «Pendiente» | 5 | 5 | 5 | 5 | 5 |
| RmdF, `VERIFICAR` | — (no existía) | — (no existía) | 25 | 25 | 25 |
| Rmd de exploración, `VERIFICAR` (congelado) | 37 | 38 | 38 | 38 | 38 |
| src, `VERIFICAR` | 5 | 5 | 6 | 6 | 6 |
| NB05, `VERIFICAR` | 5 | 5 | 3 | 3 | 3 |
| `06a` y `06b`, `VERIFICAR` (antecedentes) | 10 | 10 | 10 | 10 | 10 |
| `notebooks/modelos_dl.py`, `VERIFICAR` | 4 | 4 | 0 | 0 | 0 |

Lectura del cambio en la tesis:

- **`\pendiente`, de 22 a 14.** Se cerraron 13: los cinco de episodios (L1); Atoche Murrieta (dos),
  Jolliffe, Rencher, Bruynooghe, Tukey y Lavit, que pasaron a cita con `\verificar` (L1–L2), y
  «capítulo 3 por redactar» (L3). Se acotaron sin cerrarse: «fuentes de la vara quebrada y del
  criterio de Rencher» (cap. 1) y «fuente del modelo de vara quebrada» (cap. 2), que hoy son
  Frontier (1976), y «Denimal (2001, 2007)», que hoy es Denimal (2001). Se abrieron 5: bootstrap
  por bloques conjunto (L2), «Qué vía mide qué», Said y Dickey (1984), Kwiatkowski et al. (1992) y
  autoencoders/LSTM con 16 series (L3). Siguen el grado, cos², la matriz anti-imagen, Camiz y
  Diblasi, y los capítulos 4 y 5.
- **`\verificar`, de 34 a 51.** Las 17 nuevas corresponden a Atoche Murrieta (tres), Bernanke,
  Congreso 2018, Jolliffe, Rencher, Bruynooghe, Tukey, Kish, Lavit, Künsch, Lahiri, Newey y West
  (L1–L2), Dickey y Fuller, Hubert y Arabie y Hennig (L3). Ninguna se cerró.
- **`\verificar`, de 51 a 52 (M-03).** La nueva es la del DOI de `fmi_2015b` en `sec:validacion`
  (`d7302e0`); en el informe, la nota `v2-fmi` (`09b9c26`) lleva las notas `VERIFICAR` de 51 a 52.
  Las demás marcas no cambian.
- **Correspondencia con el informe:** 52 notas `VERIFICAR` frente a 52 `\verificar` (`09b9c26`). Los 14
  `\pendiente` de la tesis frente a 9 `[CITA PENDIENTE]` más 5 recuadros «Pendiente» del informe:
  la portada de la tesis no tiene equivalente en el informe, y el recuadro del resumen del informe
  no lo tiene en la tesis.
- **Entradas del `.bib`:** 97 (67 antes de 3c y 30 nuevas), todas con ficha en `papers/`. El
  09-11-2026 pasan a 101 (`bry_boschan_1971`, `harding_pagan_2006`, `christiano_fitzgerald_2003` y
  `kwiatkowski_et_al_1992`), todas con ficha; comprobado con un parseo de pybtex.
- **RmdF, 25 marcas:** Horn (2), Caliński y Harabasz (1), Künsch (1), Pyper y Peterman (2), Newey
  y West (2), Granger y Newbold (3), Phillips (3), Dickey y Fuller (2), Kwiatkowski et al. (2),
  quiebres estructurales (2), Bartlett (1), Kaiser y Rice (1), Tucker (1), Kaiser 1960 (1) y
  Frontier (1). Cada una tiene su fila arriba.
