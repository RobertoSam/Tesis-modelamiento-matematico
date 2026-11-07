# Nota del redactor LaTeX · 7-11-2026 · iteración 3c (borrador para MMC102)

Rama `iteracion-3c`. Encargo de Roberto (vía orquestador): presentar cuanto antes el avance del
borrador en LaTeX para MMC102, con orden, estado del arte, **avance de resultados** (autorizado por
Roberto hoy; regla 7: no se publica en el sitio), conclusiones preliminares y capítulo de pendientes.

## Commits

| Commit | Bloque |
|---|---|
| `34ae44a` | A y B: portada UNI, resumen/abstract, índices, abreviaturas, reorganización en 7 capítulos, D18 y D19, demostraciones al anexo A, anexos B, D y E |
| `35ddd49` | C: capítulo 2 (estado del arte), con las 30 fichas nuevas del bibliotecario |
| `4b21d64` | D: capítulo 5 (avance de resultados y discusión); 113 macros pedidas en `cifras_stub.tex` |
| `f2ac854` | E: capítulo 6 (conclusiones preliminares C1–C9 y recomendaciones R1–R4) |
| `54fa7dd` | F: capítulo 7 (16 temas pendientes, con qué/por qué/de quién/efecto) |
| `de6e544` | G: README y ajuste del resumen (244 palabras) |

## Estructura final

Preliminares: portada (guía MMC102: UNI / Facultad de Ciencias / Unidad de Posgrado / maestría /
título entre comillas / curso / firmas de asesor y tesista / código UNI y nota final en blanco /
Dr. Rosendo Ochoa Jiménez / Lima – Perú / 2026-II), resumen (244 palabras, 4 palabras clave),
abstract, índice de contenidos, índice de tablas, índice de figuras, lista de abreviaturas.

1. Introducción (+ hoja de ruta y `sec:estructura`, alcance de esta versión).
2. Antecedentes y estado del arte (nuevo, `cap:estado-arte`): ciclo financiero y su medición;
   índices compuestos y de estrés; regímenes y cambios estructurales; puntos de cambio; métodos
   factoriales franceses y Camiz; aprendizaje profundo; Perú y América Latina (`sec:antecedentes`,
   movida del marco); síntesis y vacío (`sec:vacios`, movida, con `tab:sintesis-ea`).
3. Marco teórico (`cap:marco`, antes cap. 2), con hoja de ruta y transiciones.
4. Metodología y desarrollo del modelo (antes cap. 3), con hoja de ruta; D18 y D19 en `tab:decisiones`.
5. Resultados (avance) y discusión.
6. Conclusiones preliminares y recomendaciones.
7. Temas pendientes y agenda de investigación.

Referencias. Anexos: A demostraciones técnicas (`prop:ganancia`, `prop:kish`, `lem:hac`,
`prop:oe4`); B robustez en transformadas (D15); C notación (lista de símbolos); D reproducibilidad
(md5 de D4, paridad, orden de ejecución, estados anteriores); E documentación complementaria
(tablas vacías: la completa el tesista).

Todas las etiquetas anteriores se conservan; las referencias cruzadas resuelven. Los archivos se
renombraron con `git mv` (historia conservada).

## Decisiones aplicadas

- **D18** en `def:episodio` («externo» = externo al análisis, evento peruano o extranjero) y en el
  párrafo de advertencias de `sec:validacion` (Kuczynski es evento peruano).
- **D19** en `def:nulo-mixto` (a) (índices con $n'=n$) y `obs:nulo-mixto` (c) (la rama TS sortea
  sus propios inicios en $\{1,\dots,n-L+1\}$; descripción del estado anterior y de N-04).

## Compilación

`latexmk -lualatex -cd tesis_latex/tesis.tex`: exit 0, **133 páginas**, 0 avisos en `tesis.log`
(sin referencias ni citas indefinidas), 0 avisos en `tesis.blg`, caja desbordada máxima 1,7 pt.
Se instalaron `biber`, `texlive-bibtex-extra`, `texlive-lang-spanish`, `texlive-luatex` y
`texlive-latex-extra` con apt. Paquetes nuevos del preámbulo: `totcount`, `seqsplit`, `xurl`
(todos en TeX Live); babel carga además `english` para el abstract.

Conteos automáticos (`\total{nverificar}`, `\total{npendiente}`, cap. 7): **82 notas VERIFICAR y
140 marcas PENDIENTE** en el PDF (antes 52 y 14). El aumento de VERIFICAR se debe a las citas del
cap. 2 (cada primera cita de una obra con ficha preliminar lleva su nota, como ya se hacía) y a las
cinco entradas con campo `verificar` del bibliotecario; el de PENDIENTE, sobre todo a las cifras
pedidas (cada uso de una macro faltante cuenta una vez).

## Dependencia del commit del bibliotecario

El cap. 2 (`35ddd49`) cita 30 claves nuevas que están en `tesis/referencias.bib` y en `papers/`
**en el árbol de trabajo, sin commit todavía** (nota del bibliotecario de hoy). Si ese commit no se
hace, la tesis compila con citas indefinidas. Claves: borio_2014, borio_lowe_2002,
claessens_kose_terrones_2011/2012, aikman_haldane_nelson_2015, schuler_hiebert_peltonen_2015/2020,
galati_et_al_2016, runstler_vlekke_2018, strohsal_proano_wolters_2019, hamilton_2018,
harding_pagan_2002, hollo_kremer_lo_duca_2012, illing_liu_2006, hamilton_1989, kim_nelson_1999,
krolzig_1997, bai_perron_1998/2003, truong_oudre_vayatis_2020, aminikhanghahi_cook_2017,
pearson_1901, hotelling_1933, lebart_morineau_piron_1995, goodfellow_bengio_courville_2016,
chalapathy_chawla_2019, gomez_gonzalez_et_al_2013, brandao_marques_perez_ruiz_2017,
minaya_lupu_cabello_2017, alvarado_vargas_2021; además se citan por primera vez
granger_newbold_1974, phillips_1986, perron_1989, josse_pages_husson_2008 y pcm_2020 (ya
versionadas). Se respetaron las reglas de la nota: «resumen» solo lo del resumen; «solo
localizada» sin hallazgos (aikman, krolzig, pearson, hotelling, lebart, goodfellow); `\verificar` en
las cinco entradas con campo `verificar`; chalapathy_chawla_2019 solo como exploración;
alvarado_vargas_2021 solo para registrar su existencia.

## Fuentes por sección (cap. 5)

| Sección | Archivos |
|---|---|
| `sec:res-datos` | 05_dimensiones, 05_adecuacion, 05_n_efectivo_resumen, 05_correlaciones; fig. final/05_correlaciones.png |
| `sec:res-pca` | 05_pca_valores_propios, 05_pca_retencion, 05_pca_cargas, 05_bootstrap_congruencia; fig. final/05_pca_sedimentacion.png |
| `sec:res-tendencia` | 05_pca_tendencia_componentes, 05_tendencia_series, 05_clasificacion_d5_resumen, 05_nulo_tendencias (tras D19), 05_pca_contraste_tendencia; fig. final/05_pca_residuos_tendencia.png |
| `sec:res-dinamica` | 06c_aede_valores_propios_resumen, 06c_aede_cortes, 06c_aede_cruces, 07b_nulo_estructura_kstar_posicion, 07b_nulo_estructura_oe4, 07b_transiciones_d10, 07b_clasificacion_2017_10, 07b_tabla_2017_10; figs. final/06_epca_*.png (notebook 06, nw = 60) |
| `sec:res-hfc` | 07c_hfc_clases3, 07c_hfc_bootstrap, 07c_hfc_correlaciones3 |
| `sec:res-datacion` | 09a_datacion_criterios, 09a_regimenes_pca, 09a_estabilidad_cortes, 09a_datacion_dimension |
| `sec:res-validacion` | 09a_regimenes_pca (episodios contenidos), tab:episodios |
| `sec:res-dl` | D17.4; ningún resultado del antecedente (`data/results/LEEME.md`: «no se consumen») |
| Anexo B | anexo/05c_pasos, 05c_ganancia, 05c_espectro, 09b_discriminacion_episodios |
| Anexo D | decisiones.qmd (D4, D6), R_paridad_python |

Las lecturas cualitativas (signos de cargas, composición de clases, etiquetas de fase, banderas de
borde y fuera del nulo, «en todas las ventanas», «la mayoría») se tomaron de esos archivos; no se
escribió a mano ningún número de datos.

## Macros que faltan (pedido al desarrollador)

Se usan ya en el texto con su nombre definitivo; `cifras_stub.tex` las define con
`\providecommand{\X}{\cifrafalta{X}{archivo}}`. Al agregarlas a
`herramientas/cifras_mapa.csv` y correr `generar_cifras.py`, aparecen en el PDF sin editar el texto.

### 79 macros directas (filas listas para `cifras_mapa.csv`; cada filtro se comprobó: selecciona exactamente una fila)

```csv
macro,archivo,filtro,columna,formato,descripcion
kmoTasaReferencia,data/results/final/05_adecuacion.csv,ambito=Tasa de referencia;medida=kmo_individual,valor,decimal:2,KMO individual de la tasa de referencia
kmoTasaInterbancaria,data/results/final/05_adecuacion.csv,ambito=Tasa interbancaria;medida=kmo_individual,valor,decimal:2,KMO individual de la tasa interbancaria
kmoEmbig,data/results/final/05_adecuacion.csv,ambito=EMBIG Perú;medida=kmo_individual,valor,decimal:2,KMO individual del EMBIG
inerciaAcumTresNiveles,data/results/final/05_pca_valores_propios.csv,componente=3,inercia_acumulada,decimal:1,Inercia acumulada (%) de los tres primeros ejes
lambdaTresNiveles,data/results/final/05_pca_valores_propios.csv,componente=3,valor_propio,decimal:2,Tercer valor propio del PCA global
hornUmbralTresNiveles,data/results/final/05_pca_valores_propios.csv,componente=3,horn_umbral_p95,decimal:2,Umbral de Horn del tercer valor propio
varaQuebradaNiveles,data/results/final/05_pca_retencion.csv,criterio=vara_quebrada,componentes,entero,Componentes retenidos por la vara quebrada
congruenciaBootPCUnoNiveles,data/results/final/05_bootstrap_congruencia.csv,L=24;componente=1,p5,decimal:3,p5 de la congruencia bootstrap de PC1 (L = 24)
congruenciaBootPCTresNiveles,data/results/final/05_bootstrap_congruencia.csv,L=24;componente=3,p5,decimal:3,p5 de la congruencia bootstrap de PC3 (L = 24)
nuloMixtoTsPCUno,data/results/final/05_nulo_tendencias.csv,version=mixto_ind_ts;medida=inercia_pc1,proporcion,decimal:3,"Proporción del nulo mixto (mixto_ind_ts, D8 y D19) con PC1 >= observado"
nuloMixtoTsPCDos,data/results/final/05_nulo_tendencias.csv,version=mixto_ind_ts;medida=inercia_pc2,proporcion,decimal:3,"Proporción del nulo mixto (mixto_ind_ts, D8 y D19) con PC2 >= observado"
nuloMixtoTsPCTres,data/results/final/05_nulo_tendencias.csv,version=mixto_ind_ts;medida=inercia_pc3,proporcion,decimal:3,"Proporción del nulo mixto (mixto_ind_ts, D8 y D19) con PC3 >= observado"
nuloMixtoDsPCUno,data/results/final/05_nulo_tendencias.csv,version=mixto_ind_ds;medida=inercia_pc1,proporcion,decimal:3,"Proporción del nulo mixto (mixto_ind_ds, D8 y D19) con PC1 >= observado"
nuloMixtoDsPCDos,data/results/final/05_nulo_tendencias.csv,version=mixto_ind_ds;medida=inercia_pc2,proporcion,decimal:3,"Proporción del nulo mixto (mixto_ind_ds, D8 y D19) con PC2 >= observado"
nuloMixtoDsPCTres,data/results/final/05_nulo_tendencias.csv,version=mixto_ind_ds;medida=inercia_pc3,proporcion,decimal:3,"Proporción del nulo mixto (mixto_ind_ds, D8 y D19) con PC3 >= observado"
ventanasAedeVeinticuatro,data/results/final/06c_aede_valores_propios_resumen.csv,nw=24;pesos=uniformes;eje=1,ventanas,entero,Ventanas de aede con nw = 24
ventanasAedeTreintayseis,data/results/final/06c_aede_valores_propios_resumen.csv,nw=36;pesos=uniformes;eje=1,ventanas,entero,Ventanas de aede con nw = 36
ventanasAedeCuarentayocho,data/results/final/06c_aede_valores_propios_resumen.csv,nw=48;pesos=uniformes;eje=1,ventanas,entero,Ventanas de aede con nw = 48
ventanasAedeSesenta,data/results/final/06c_aede_valores_propios_resumen.csv,nw=60;pesos=uniformes;eje=1,ventanas,entero,Ventanas de aede con nw = 60
bajoHornDosVeinticuatroU,data/results/final/06c_aede_valores_propios_resumen.csv,nw=24;pesos=uniformes;eje=2,bajo_horn,entero,"Ventanas con lambda_2 bajo el umbral de Horn (nw = 24, uniformes)"
bajoHornDosVeinticuatroG,data/results/final/06c_aede_valores_propios_resumen.csv,nw=24;pesos=gaussianos_nsd3;eje=2,bajo_horn,entero,"Ventanas con lambda_2 bajo el umbral de Horn (nw = 24, gaussianos_nsd3)"
bajoHornDosTreintayseisU,data/results/final/06c_aede_valores_propios_resumen.csv,nw=36;pesos=uniformes;eje=2,bajo_horn,entero,"Ventanas con lambda_2 bajo el umbral de Horn (nw = 36, uniformes)"
bajoHornDosTreintayseisG,data/results/final/06c_aede_valores_propios_resumen.csv,nw=36;pesos=gaussianos_nsd3;eje=2,bajo_horn,entero,"Ventanas con lambda_2 bajo el umbral de Horn (nw = 36, gaussianos_nsd3)"
bajoHornDosCuarentayochoU,data/results/final/06c_aede_valores_propios_resumen.csv,nw=48;pesos=uniformes;eje=2,bajo_horn,entero,"Ventanas con lambda_2 bajo el umbral de Horn (nw = 48, uniformes)"
bajoHornDosCuarentayochoG,data/results/final/06c_aede_valores_propios_resumen.csv,nw=48;pesos=gaussianos_nsd3;eje=2,bajo_horn,entero,"Ventanas con lambda_2 bajo el umbral de Horn (nw = 48, gaussianos_nsd3)"
bajoHornDosSesentaU,data/results/final/06c_aede_valores_propios_resumen.csv,nw=60;pesos=uniformes;eje=2,bajo_horn,entero,"Ventanas con lambda_2 bajo el umbral de Horn (nw = 60, uniformes)"
bajoHornDosSesentaG,data/results/final/06c_aede_valores_propios_resumen.csv,nw=60;pesos=gaussianos_nsd3;eje=2,bajo_horn,entero,"Ventanas con lambda_2 bajo el umbral de Horn (nw = 60, gaussianos_nsd3)"
bajoHornTresVeinticuatroU,data/results/final/06c_aede_valores_propios_resumen.csv,nw=24;pesos=uniformes;eje=3,bajo_horn,entero,"Ventanas con lambda_3 bajo el umbral de Horn (nw = 24, uniformes)"
bajoHornTresVeinticuatroG,data/results/final/06c_aede_valores_propios_resumen.csv,nw=24;pesos=gaussianos_nsd3;eje=3,bajo_horn,entero,"Ventanas con lambda_3 bajo el umbral de Horn (nw = 24, gaussianos_nsd3)"
bajoHornTresTreintayseisU,data/results/final/06c_aede_valores_propios_resumen.csv,nw=36;pesos=uniformes;eje=3,bajo_horn,entero,"Ventanas con lambda_3 bajo el umbral de Horn (nw = 36, uniformes)"
bajoHornTresTreintayseisG,data/results/final/06c_aede_valores_propios_resumen.csv,nw=36;pesos=gaussianos_nsd3;eje=3,bajo_horn,entero,"Ventanas con lambda_3 bajo el umbral de Horn (nw = 36, gaussianos_nsd3)"
bajoHornTresCuarentayochoU,data/results/final/06c_aede_valores_propios_resumen.csv,nw=48;pesos=uniformes;eje=3,bajo_horn,entero,"Ventanas con lambda_3 bajo el umbral de Horn (nw = 48, uniformes)"
bajoHornTresCuarentayochoG,data/results/final/06c_aede_valores_propios_resumen.csv,nw=48;pesos=gaussianos_nsd3;eje=3,bajo_horn,entero,"Ventanas con lambda_3 bajo el umbral de Horn (nw = 48, gaussianos_nsd3)"
bajoHornTresSesentaU,data/results/final/06c_aede_valores_propios_resumen.csv,nw=60;pesos=uniformes;eje=3,bajo_horn,entero,"Ventanas con lambda_3 bajo el umbral de Horn (nw = 60, uniformes)"
bajoHornTresSesentaG,data/results/final/06c_aede_valores_propios_resumen.csv,nw=60;pesos=gaussianos_nsd3;eje=3,bajo_horn,entero,"Ventanas con lambda_3 bajo el umbral de Horn (nw = 60, gaussianos_nsd3)"
ventanasSerieConstanteVeinticuatro,data/results/final/06c_aede_valores_propios_resumen.csv,nw=24;pesos=uniformes;eje=1,serie_constante,entero,Ventanas de 24 meses con alguna serie constante
kCodoVeinticuatroU,data/results/final/06c_aede_cortes.csv,nw=24;maxcl=10;pesos=uniformes;criterio=codo (caída máxima),k,entero,"Segmentos del codo de aede (nw = 24, uniformes, maxcl = 10)"
corteCodoVeinticuatroG,data/results/final/06c_aede_cortes.csv,nw=24;maxcl=10;pesos=gaussianos_nsd3;criterio=codo (caída máxima),cortes,fecha_mes,"Único corte del codo de aede (nw = 24, gaussianos_nsd3, maxcl = 10)"
corteCodoTreintayseisU,data/results/final/06c_aede_cortes.csv,nw=36;maxcl=10;pesos=uniformes;criterio=codo (caída máxima),cortes,fecha_mes,"Único corte del codo de aede (nw = 36, uniformes, maxcl = 10)"
corteCodoTreintayseisG,data/results/final/06c_aede_cortes.csv,nw=36;maxcl=10;pesos=gaussianos_nsd3;criterio=codo (caída máxima),cortes,fecha_mes,"Único corte del codo de aede (nw = 36, gaussianos_nsd3, maxcl = 10)"
corteCodoCuarentayochoU,data/results/final/06c_aede_cortes.csv,nw=48;maxcl=10;pesos=uniformes;criterio=codo (caída máxima),cortes,fecha_mes,"Único corte del codo de aede (nw = 48, uniformes, maxcl = 10)"
corteCodoCuarentayochoG,data/results/final/06c_aede_cortes.csv,nw=48;maxcl=10;pesos=gaussianos_nsd3;criterio=codo (caída máxima),cortes,fecha_mes,"Único corte del codo de aede (nw = 48, gaussianos_nsd3, maxcl = 10)"
corteCodoSesentaU,data/results/final/06c_aede_cortes.csv,nw=60;maxcl=10;pesos=uniformes;criterio=codo (caída máxima),cortes,fecha_mes,"Único corte del codo de aede (nw = 60, uniformes, maxcl = 10)"
corteCodoSesentaG,data/results/final/06c_aede_cortes.csv,nw=60;maxcl=10;pesos=gaussianos_nsd3;criterio=codo (caída máxima),cortes,fecha_mes,"Único corte del codo de aede (nw = 60, gaussianos_nsd3, maxcl = 10)"
pOEcuatroVeinticuatroU,data/results/final/07b_nulo_estructura_oe4.csv,principal=True;nw=24;pesos=uniformes,p_valor,decimal:2,"p-valor del criterio de OE4 (nw = 24, uniformes, objeto principal)"
propOEcuatroVeinticuatroU,data/results/final/07b_nulo_estructura_oe4.csv,principal=True;nw=24;pesos=uniformes,prop_obs,decimal:3,"Proporción observada de pares bajo el p5 (nw = 24, uniformes)"
pOEcuatroVeinticuatroG,data/results/final/07b_nulo_estructura_oe4.csv,principal=True;nw=24;pesos=gaussianos_nsd3,p_valor,decimal:2,"p-valor del criterio de OE4 (nw = 24, gaussianos_nsd3, objeto principal)"
propOEcuatroVeinticuatroG,data/results/final/07b_nulo_estructura_oe4.csv,principal=True;nw=24;pesos=gaussianos_nsd3,prop_obs,decimal:3,"Proporción observada de pares bajo el p5 (nw = 24, gaussianos_nsd3)"
pOEcuatroTreintayseisU,data/results/final/07b_nulo_estructura_oe4.csv,principal=True;nw=36;pesos=uniformes,p_valor,decimal:2,"p-valor del criterio de OE4 (nw = 36, uniformes, objeto principal)"
propOEcuatroTreintayseisU,data/results/final/07b_nulo_estructura_oe4.csv,principal=True;nw=36;pesos=uniformes,prop_obs,decimal:3,"Proporción observada de pares bajo el p5 (nw = 36, uniformes)"
pOEcuatroTreintayseisG,data/results/final/07b_nulo_estructura_oe4.csv,principal=True;nw=36;pesos=gaussianos_nsd3,p_valor,decimal:2,"p-valor del criterio de OE4 (nw = 36, gaussianos_nsd3, objeto principal)"
propOEcuatroTreintayseisG,data/results/final/07b_nulo_estructura_oe4.csv,principal=True;nw=36;pesos=gaussianos_nsd3,prop_obs,decimal:3,"Proporción observada de pares bajo el p5 (nw = 36, gaussianos_nsd3)"
pOEcuatroCuarentayochoU,data/results/final/07b_nulo_estructura_oe4.csv,principal=True;nw=48;pesos=uniformes,p_valor,decimal:2,"p-valor del criterio de OE4 (nw = 48, uniformes, objeto principal)"
propOEcuatroCuarentayochoU,data/results/final/07b_nulo_estructura_oe4.csv,principal=True;nw=48;pesos=uniformes,prop_obs,decimal:3,"Proporción observada de pares bajo el p5 (nw = 48, uniformes)"
pOEcuatroCuarentayochoG,data/results/final/07b_nulo_estructura_oe4.csv,principal=True;nw=48;pesos=gaussianos_nsd3,p_valor,decimal:2,"p-valor del criterio de OE4 (nw = 48, gaussianos_nsd3, objeto principal)"
propOEcuatroCuarentayochoG,data/results/final/07b_nulo_estructura_oe4.csv,principal=True;nw=48;pesos=gaussianos_nsd3,prop_obs,decimal:3,"Proporción observada de pares bajo el p5 (nw = 48, gaussianos_nsd3)"
pOEcuatroSesentaU,data/results/final/07b_nulo_estructura_oe4.csv,principal=True;nw=60;pesos=uniformes,p_valor,decimal:2,"p-valor del criterio de OE4 (nw = 60, uniformes, objeto principal)"
propOEcuatroSesentaU,data/results/final/07b_nulo_estructura_oe4.csv,principal=True;nw=60;pesos=uniformes,prop_obs,decimal:3,"Proporción observada de pares bajo el p5 (nw = 60, uniformes)"
pOEcuatroSesentaG,data/results/final/07b_nulo_estructura_oe4.csv,principal=True;nw=60;pesos=gaussianos_nsd3,p_valor,decimal:2,"p-valor del criterio de OE4 (nw = 60, gaussianos_nsd3, objeto principal)"
propOEcuatroSesentaG,data/results/final/07b_nulo_estructura_oe4.csv,principal=True;nw=60;pesos=gaussianos_nsd3,prop_obs,decimal:3,"Proporción observada de pares bajo el p5 (nw = 60, gaussianos_nsd3)"
replicasHfc,data/results/final/07c_hfc_correlaciones3.csv,version=original;tipo=factores;clase_a=C1;clase_b=C2,replicas,entero,Réplicas del bootstrap de la HFC
rFactoresUnoTres,data/results/final/07c_hfc_correlaciones3.csv,version=original;tipo=factores;clase_a=C1;clase_b=C3,r,decimal:2,r de la correlación entre los factores C1 y C3 (original)
rFactoresUnoTresPcinco,data/results/final/07c_hfc_correlaciones3.csv,version=original;tipo=factores;clase_a=C1;clase_b=C3,p5,decimal:2,p5 de la correlación entre los factores C1 y C3 (original)
rFactoresUnoTresPnoventaycinco,data/results/final/07c_hfc_correlaciones3.csv,version=original;tipo=factores;clase_a=C1;clase_b=C3,p95,decimal:2,p95 de la correlación entre los factores C1 y C3 (original)
rFactoresUnoDosSinTendencia,data/results/final/07c_hfc_correlaciones3.csv,version=sin_tendencia;tipo=factores;clase_a=C1;clase_b=C2,r,decimal:2,r de la correlación entre los factores C1 y C2 (sin_tendencia)
rFactoresUnoDosSinTendenciaPcinco,data/results/final/07c_hfc_correlaciones3.csv,version=sin_tendencia;tipo=factores;clase_a=C1;clase_b=C2,p5,decimal:2,p5 de la correlación entre los factores C1 y C2 (sin_tendencia)
rFactoresUnoDosSinTendenciaPnoventaycinco,data/results/final/07c_hfc_correlaciones3.csv,version=sin_tendencia;tipo=factores;clase_a=C1;clase_b=C2,p95,decimal:2,p95 de la correlación entre los factores C1 y C2 (sin_tendencia)
nRegimenesPrincipal,data/results/final/09a_datacion_criterios.csv,maxcl=10;criterio=regla K (D12),k,entero,Regímenes de la regla K con maxcl = 10 (D17.1)
nRegimenesQuince,data/results/final/09a_datacion_criterios.csv,maxcl=15;criterio=regla K (D12),k,entero,Regímenes de la regla K con maxcl = 15
nRegimenesVeinte,data/results/final/09a_datacion_criterios.csv,maxcl=20;criterio=regla K (D12),k,entero,Regímenes de la regla K con maxcl = 20
nRegimenesDimDos,data/results/final/09a_datacion_dimension.csv,d=2;maxcl=10;criterio=regla K (D12),k,entero,Regímenes de la regla K con d = 2
nRegimenesDimCuatro,data/results/final/09a_datacion_dimension.csv,d=4;maxcl=10;criterio=regla K (D12),k,entero,Regímenes de la regla K con d = 4
congruenciaLogPCUno,data/results/final/anexo/05c_pasos.csv,version=solo_logaritmo;medida=congruencia_con_sin_transformar;componente=1,valor,decimal:3,Congruencia del eje 1 tras el logaritmo
congruenciaLogPCDos,data/results/final/anexo/05c_pasos.csv,version=solo_logaritmo;medida=congruencia_con_sin_transformar;componente=2,valor,decimal:3,Congruencia del eje 2 tras el logaritmo
congruenciaLogPCTres,data/results/final/anexo/05c_pasos.csv,version=solo_logaritmo;medida=congruencia_con_sin_transformar;componente=3,valor,decimal:3,Congruencia del eje 3 tras el logaritmo
inerciaPCUnoDiferencia,data/results/final/anexo/05c_pasos.csv,version=solo_diferencia;medida=inercia;componente=1,valor,decimal:1,Inercia (%) de PC1 con solo la primera diferencia
falsasAlarmasTransformadasTres,data/results/final/anexo/09b_discriminacion_episodios.csv,via=transformadas;series=16;metodo=pca;tolerancia_meses=3;medida=falsas_alarmas_%,valor,decimal:1,"Falsas alarmas (%) en transformadas, h = 3"
sensibilidadCovidTransformadasTres,data/results/final/anexo/09b_discriminacion_episodios.csv,via=transformadas;series=16;metodo=pca;tolerancia_meses=3;medida=sensibilidad_%;episodio=COVID-19,valor,decimal:1,"Sensibilidad (%) en la pandemia, transformadas, h = 3"
falsasAlarmasNivelesTres,data/results/final/anexo/09b_discriminacion_episodios.csv,via=niveles;series=16;metodo=pca;tolerancia_meses=3;medida=falsas_alarmas_%,valor,decimal:1,"Falsas alarmas (%) sin transformar, h = 3"
```

### 34 macros que requieren un resumen o una columna nueva

| Macro | Archivo | Filtro | Columna | Formato | Qué hace falta |
|---|---|---|---|---|---|
| `nTransicionesCandidatas` | `07b_transiciones_d10.csv` | `objeto=cargas_sin_centrar` | `(conteo de filas)` | `entero` | RESUMEN: contar filas |
| `nTransicionesCuentan` | `07b_transiciones_d10.csv` | `objeto=cargas_sin_centrar;es_borde_3=False;fuera_del_nulo=True` | `(conteo de filas)` | `entero` | RESUMEN: contar filas |
| `transicionCuentaFecha` | `07b_transiciones_d10.csv` | `objeto=cargas_sin_centrar;es_borde_3=False;fuera_del_nulo=True` | `fecha` | `fecha_mes` | RESUMEN: depende de que sea única |
| `ariTresMediana` | `07c_hfc_bootstrap.csv` | `—` | `ari_3` | `decimal:2` | RESUMEN: mediana de la columna |
| `ariTresMedia` | `07c_hfc_bootstrap.csv` | `—` | `ari_3` | `decimal:2` | RESUMEN: media de la columna |
| `ariCuatroMedia` | `07c_hfc_bootstrap.csv` | `—` | `ari_4` | `decimal:2` | RESUMEN: media de la columna |
| `cofeneticaMediana` | `07c_hfc_bootstrap.csv` | `—` | `cofenetica` | `decimal:2` | RESUMEN: mediana de la columna |
| `corteDatacionUno` | `09a_estabilidad_cortes.csv` | `orden=1` | `corte` | `fecha_mes` | REQUIERE columna orden |
| `estabilidadCorteUno` | `09a_estabilidad_cortes.csv` | `orden=1` | `frecuencia` | `decimal:2` | REQUIERE columna orden |
| `corteDatacionDos` | `09a_estabilidad_cortes.csv` | `orden=2` | `corte` | `fecha_mes` | REQUIERE columna orden |
| `estabilidadCorteDos` | `09a_estabilidad_cortes.csv` | `orden=2` | `frecuencia` | `decimal:2` | REQUIERE columna orden |
| `corteDatacionTres` | `09a_estabilidad_cortes.csv` | `orden=3` | `corte` | `fecha_mes` | REQUIERE columna orden |
| `estabilidadCorteTres` | `09a_estabilidad_cortes.csv` | `orden=3` | `frecuencia` | `decimal:2` | REQUIERE columna orden |
| `corteDatacionCuatro` | `09a_estabilidad_cortes.csv` | `orden=4` | `corte` | `fecha_mes` | REQUIERE columna orden |
| `estabilidadCorteCuatro` | `09a_estabilidad_cortes.csv` | `orden=4` | `frecuencia` | `decimal:2` | REQUIERE columna orden |
| `corteDatacionCinco` | `09a_estabilidad_cortes.csv` | `orden=5` | `corte` | `fecha_mes` | REQUIERE columna orden |
| `estabilidadCorteCinco` | `09a_estabilidad_cortes.csv` | `orden=5` | `frecuencia` | `decimal:2` | REQUIERE columna orden |
| `replicasDatacion` | `09a_estabilidad_cortes.csv` | `orden=1` | `replicas` | `entero` | REQUIERE columna orden |
| `regimenUnoInicio` | `09a_regimenes_pca.csv` | `orden=1` | `inicio` | `fecha_mes` | REQUIERE columna orden |
| `regimenUnoFin` | `09a_regimenes_pca.csv` | `orden=1` | `fin` | `fecha_mes` | REQUIERE columna orden |
| `regimenDosInicio` | `09a_regimenes_pca.csv` | `orden=2` | `inicio` | `fecha_mes` | REQUIERE columna orden |
| `regimenDosFin` | `09a_regimenes_pca.csv` | `orden=2` | `fin` | `fecha_mes` | REQUIERE columna orden |
| `regimenTresInicio` | `09a_regimenes_pca.csv` | `orden=3` | `inicio` | `fecha_mes` | REQUIERE columna orden |
| `regimenTresFin` | `09a_regimenes_pca.csv` | `orden=3` | `fin` | `fecha_mes` | REQUIERE columna orden |
| `regimenCuatroInicio` | `09a_regimenes_pca.csv` | `orden=4` | `inicio` | `fecha_mes` | REQUIERE columna orden |
| `regimenCuatroFin` | `09a_regimenes_pca.csv` | `orden=4` | `fin` | `fecha_mes` | REQUIERE columna orden |
| `regimenCincoInicio` | `09a_regimenes_pca.csv` | `orden=5` | `inicio` | `fecha_mes` | REQUIERE columna orden |
| `regimenCincoFin` | `09a_regimenes_pca.csv` | `orden=5` | `fin` | `fecha_mes` | REQUIERE columna orden |
| `regimenSeisInicio` | `09a_regimenes_pca.csv` | `orden=6` | `inicio` | `fecha_mes` | REQUIERE columna orden |
| `regimenSeisFin` | `09a_regimenes_pca.csv` | `orden=6` | `fin` | `fecha_mes` | REQUIERE columna orden |
| `espectroLentoMedianaNivelesSinTendencia` | `anexo/05c_espectro.csv` | `—` | `niv_det` | `decimal:1` | RESUMEN: mediana x 100 |
| `espectroLentoMedianaTransformadas` | `anexo/05c_espectro.csv` | `—` | `tr` | `decimal:1` | RESUMEN: mediana x 100 |
| `filasParidad` | `R_paridad_python.csv` | `—` | `(conteo de filas)` | `entero` | RESUMEN: contar filas |
| `filasParidadCoinciden` | `R_paridad_python.csv` | `coincide=sí` | `(conteo de filas)` | `entero` | RESUMEN: contar filas |

- `09a_estabilidad_cortes.csv` y `09a_regimenes_pca.csv` necesitan una columna `orden` (1, 2, …).
- Resúmenes: conteos de filas (`07b_transiciones_d10`, `R_paridad_python`), medianas y medias de
  `07c_hfc_bootstrap` y medianas × 100 de `05c_espectro` (convendría un CSV de resumen por notebook).
- `transicionCuentaFecha` supone que hay una sola candidata que cuenta; si hay más, el texto de
  `sec:res-transiciones` debe cambiar (avisar).

### Productos pedidos (no son macros)

1. Tabla de compatibilidad corte × episodio con h = 3 y h = 6 (`sec:res-validacion`).
2. Figura del dendrograma de la HFC con la partición en 3 clases, en `reports/figures/final/`.
3. Figura de la trayectoria PCA-MM12 con los cortes y los episodios, en `reports/figures/final/`.

## Pendientes del estado del arte (cap. 2)

Quedan `\pendiente` en:
- `sec:ea-ciclo`: Bry y Boschan (1971), Harding y Pagan (2006), Christiano y Fitzgerald (2003).
- `sec:ea-regimenes`: Kwiatkowski et al. (1992) sin entrada en el `.bib`.
- `sec:ea-cambio`: detección de cambios en la matriz de covarianzas de series multivariadas.
- `sec:ea-factoriales`: fuentes de cos² y contribuciones (Lebart et al. 1995 candidato, sección no
  verificada), STATIS dual y Camiz y Diblasi (2013).
- `sec:ea-dl`: fuentes revisadas por pares sobre error de reconstrucción como señal de anomalía y
  sobre aprendizaje profundo con series macrofinancieras cortas.
- `sec:antecedentes`: documentos del BCRP (condiciones financieras y estrés), informes de
  estabilidad financiera del BCRP y la SBS, tesis de la PUCP (bloqueados; Roberto debe descargarlos).
- La línea «índices de estrés» ya no tiene `\pendiente`: la cubren illing_liu_2006 y
  hollo_kremer_lo_duca_2012.

## Inconsistencias y avisos

1. **Paridad de marcas tesis–informe rota a propósito.** La tesis pasa de 52 a 82 `\verificar`. El
   informe (editor) y el registro (bibliotecario) deben actualizar sus conteos o dejar de exigir la
   igualdad; el informe además debe seguir la nueva estructura de 7 capítulos.
2. **Diseño de D19 sin validar.** El desarrollador implementó un sorteo aparte para la rama TS; D19
   no lo fija. Se lleva al cap. 7 (`sec:pend-d19`) como decisión de Roberto o del asesor.
3. **OE4 no discrimina en niveles.** Con todos los anchos y pesos, el p-valor del criterio está lejos
   de 5 %: HT1 no queda sostenida en niveles. No es un error de código, pero condiciona la Parte C;
   se recomienda un estudio de potencia con datos simulados (R3, `sec:pend-simulado`).
4. **La regla K con maxcl = 10 no elige en su primer paso** y cae en el codo; con 15 y 20 elige otro
   número de regímenes. Se informa como dependencia de la regla (HT3).
5. **El CSV escribe «Calinski-Harabász»** (con tilde en la a) en `06c_aede_cortes.csv` y
   `09a_*`; el texto usa Caliński y Harabasz. Cosmético; afecta solo a filtros que lo usen.
6. Los capítulos 4 y 5 ya no están vacíos: la fila «Parámetros de diseño» del README conserva la
   frase histórica «los capítulos 4 y 5 no se tocaron (regla 7)», que se refería a la numeración
   anterior.

## Lo que no se hizo

- No se tocaron `tesis/`, `src/`, `R/`, `data/`, `papers/` ni `tesis/referencias.bib`.
- No se calculó ninguna cifra: las que faltan están pedidas arriba.
- No se publicó nada ni se hizo push.
