# Asesoría · Revisión crítica del informe preliminar de tesis (MMC102) · 8 de noviembre de 2026

**Base:** rama `avance-mmc102`, HEAD `3141a4c`. **Leído:** `CLAUDE.md`, `decisiones.qmd` (D1–D19),
`asesoria/_informe_preliminar_v2.txt` (texto renderizado) y `_informe_preliminar_v2_fuente.md`,
`tesis/_cifras.yml`, `tesis/informe_preliminar_uni/{build.py, resultados_camiz.py, referencias_extra.bib}`,
`tesis_latex/capitulos/02_marco_teorico.tex` y `03_metodologia.tex`, `01_introduccion.tex` (objetivos e
hipótesis), las fichas de `papers/` que el informe usa y `tesis/registro_verificacion.md`.
**Cifras verificadas contra:** `data/results/final/*.csv`, `data/results/final/anexo/*.csv`,
`/home/claude/informe/camiz/*.csv` y sus figuras, y la serie congelada
`data/processed/dataset_niveles_mensual.csv` (solo lectura, para describir trayectorias).

Convención de ubicación: «§3.1.3 ¶2» = sección 3.1.3, segundo párrafo; las páginas son las del
texto renderizado (numeración arábiga del cuerpo).

---

## 1. Diagnóstico

El informe cumple la **forma** de la Guía N.° 2 (carátula, protocolo, marco, desarrollo, conclusiones,
matriz) y casi todas sus cifras coinciden con los CSV. Su problema es de **fondo**, y coincide con lo
que observó Roberto: el texto *nombra* y *fórmula*, pero no *explica* ni *interpreta*.

1. **Marco teórico (Cap. II) sin desarrollo conceptual.** Cada método tiene notación (que además se
   pierde en la extracción de texto: §2.2.4–2.2.10 muestran fórmulas vacías; verificar en el .docx),
   pero no dice qué problema resuelve, por qué se elige, cómo se lee su salida, qué supone ni dónde
   falla. El ciclo financiero ocupa un párrafo de 5 líneas (§2.2.1) y el enfoque exploratorio otro
   de 7 (§2.2.2). La tesis maestra (`02_marco_teorico.tex`) ya contiene buena parte de ese desarrollo
   (posición «datos primero», ganancia de la diferencia, régimen/transición/detección, tamaño
   efectivo de Kish, bordes de ventana, lectura multiescala, monotonía del costo de Fisher) y el
   informe no lo trae.
2. **«Datación» nunca se define.** Se usa en el resumen, en §1.4.4 (Tabla 3), §2.2.8, §3.1.7, la
   discusión y las conclusiones, con dos sentidos distintos (fechar episodios con fuentes externas
   y partir una trayectoria en tramos), sin decir qué se fecha, con qué ni para qué.
3. **Resultados sin interpretación.** §3.1 describe («el eje 2 lo definen las tasas…», «el índice
   crece…») pero no dice qué significa para el sistema financiero peruano, qué episodio explica qué
   movimiento ni por qué importa para el objetivo. Las series congeladas permiten interpretaciones
   concretas que hoy faltan (sección 2.3 de este documento).
4. **Cuatro problemas de sustancia** que el jurado o el Dr. Camiz detectarán: (a) se usa el nulo
   «con deriva» global, no el **nulo mixto oficial de D8**; (b) los dos cortes del EPCA salen del
   índice de Caliński-Harabasz con maxcl = 10, lo que **contradice D11**, y con maxcl = 15 o 20 el
   mismo criterio va al tope; (c) la datación con *scores* usa una **media móvil causal de 12 meses**
   que retrasa los cortes unos 5,5 meses, y la compatibilidad ±3 meses con los episodios no lo
   corrige; (d) los resultados de «claede» provienen de una **emulación en Python** (clahfac por
   ventana, pesos uniformes) cuyo programa original no está en el repositorio ni tiene paridad, y
   las cifras del asesor se leen de `/home/claude/informe/camiz/`, fuera de `data/results/`
   (regla 3).
5. **Trazabilidad bibliográfica.** Seis referencias del informe no tienen ficha ni entrada en
   `tesis/referencias.bib` (regla 2); el informe no lleva marcas `[VERIFICAR]` aunque muchas fuentes
   no están leídas; y el Anexo 3 afirma que Horn (1965) y Fisher (1958) se leyeron completos, lo que
   contradicen sus fichas y el registro.
6. **Antecedentes fuera de ventana.** De nueve antecedentes, solo tres son de los últimos cinco años
   (Atoche Murrieta, 2022; Tuhin et al., 2025; Camiz et al., 2026).
7. **Desalineación con la tesis maestra.** El informe tiene 5 objetivos (OE1–OE5) y la tesis 12; el
   «OE4» de las decisiones D10/D17 (criterio de ventana) no existe en el informe, aunque sus
   resultados se reportan. Hipótesis HE1–HE4 frente a HT1–HT4.

**Lo sólido:** la estructura transversal (PCA + HFC + bootstrap) está bien respaldada y bien medida;
la honestidad sobre la regla de fases y sobre el nulo de estructura constante es un activo frente al
asesor. La corrección es sobre todo de **redacción conceptual e interpretación**, más cuatro ajustes
de sustancia que no requieren cálculos nuevos salvo N6 y la paridad de claede.

---

## 2. Recomendaciones priorizadas

### 2.1 Necesarias (sin esto el informe no se sostiene)

#### N1. Definir «datación» y separar sus dos sentidos (observación 2 de Roberto)

**Ubicación:** §2.2.3 (crear un párrafo «Datación»), §2.2.8 ¶1, §2.3 (nuevo término), Tabla 3
(etapa 5), §3.1.5 ¶1, §3.1.7 ¶1, Resumen.

**Problema:** el lector no sabe qué es «datar», por qué se hace ni cómo se distingue de fechar los
episodios.

**Qué debe decir el texto (contenido mínimo):**

- *Qué es.* En la literatura de ciclos, **datar** es asignar fechas a los cambios del ciclo. La
  tradición clásica fecha **puntos de giro** (picos y valles) de una serie de referencia; es lo que
  hacen los comités de fechado (el NBER, cuyas fechas se usan aquí como fin de episodios: ficha
  `nber_2010`) y lo que Drehmann et al. (2012) llaman análisis de puntos de giro (ficha
  `drehmann_borio_tsatsaronis_2012`, que lo cita según Bry y Boschan, 1971, y Harding y Pagan,
  2002). En esta tesis, **datar regímenes** es otra cosa: estimar los meses en que empieza cada
  intervalo de estructura homogénea, partiendo una **trayectoria** ordenada en el tiempo (el primer
  valor propio del EPCA o los *scores* del PCA) en tramos contiguos con la partición óptima de
  Fisher. El resultado es una lista de **cortes** (primer mes de cada tramo nuevo) y, entre ellos,
  **regímenes**.
- *Por qué se hace.* El PCA, el EPCA y la HFC evolutiva describen de forma continua; para responder
  OE4 hay que convertir esa descripción en intervalos con fecha que puedan (i) compararse con
  episodios documentados, (ii) recibir una etiqueta de fase y (iii) compararse entre métodos.
- *Qué significa un corte según la trayectoria.* En el primer valor propio del EPCA, un corte marca
  un cambio en la **intensidad** del movimiento común (las series pasan a moverse más o menos
  juntas). En los *scores* suavizados, marca un cambio en la **posición** del sistema dentro de una
  estructura fija (nivel de la tendencia, de las tasas o del riesgo). No son lo mismo y no deben
  sumarse como «coincidencias».
- *Distinción con el fechado de episodios.* **Fechar un episodio** (Tabla 4) es tomar de un
  documento externo el mes del evento (D7, D18, regla 6). La datación se obtiene de los datos; el
  fechado, nunca. Solo así la comparación entre ambos no es circular.
- *Definición en §2.3:* «Datación de regímenes: estimación de los meses de corte que dividen una
  trayectoria de representaciones en tramos contiguos de máxima homogeneidad interna (partición de
  Fisher); no debe confundirse con el fechado de episodios de referencia, que se toma de fuentes
  externas.» Añadir también **corte**, **tramo**, **trayectoria** y **transición**.

Bry y Boschan (1971) y Harding y Pagan (2002) no tienen ficha: **propuesta para el bibliotecario,
por verificar**; mientras tanto, citarlos solo «como se cita en Drehmann et al. (2012)».

#### N2. Desarrollar conceptualmente el marco teórico, método por método (observación 1)

**Ubicación:** §2.2.1–2.2.10. **Regla de redacción para cada subsección:** (1) qué problema resuelve;
(2) idea en palabras, antes de la fórmula; (3) cómo se lee la salida, con un ejemplo de esta tesis;
(4) supuestos; (5) limitaciones y qué se hace con ellas en la tesis. La fórmula queda como apoyo. La
mayor parte del material está en `02_marco_teorico.tex`; el editor debe resumirlo, no copiarlo.

| Sección | Ideas conceptuales que faltan (qué debe decir) | Fuente con ficha |
|---|---|---|
| **2.2.1 Ciclo financiero** | (a) Definición conceptual (expansión/contracción conjunta del crédito y de los precios de activos) frente a la operativa de Drehmann et al. (componente de mediano plazo de crédito, crédito/PBI y precios inmobiliarios, 8–30 años). (b) Por qué importa: los picos coinciden con crisis bancarias y las recesiones que coinciden con la contracción financiera son más profundas; la idea de «recesión inconclusa». (c) Diferencia con el ciclo económico (duración, variables, relación con crisis). (d) Dos tradiciones de medición: filtros de frecuencia y puntos de giro (Drehmann) frente a análisis exploratorio multivariado (Camiz, Atoche): la tesis pertenece a la segunda. (e) Por qué la tesis incluye bolsa y EMBIG, que Drehmann excluye: la escuela de Camiz deja que la correlación forme los grupos (`02_marco_teorico.tex:82-85`). (f) Consecuencia de tener 19 años: no se observa un ciclo completo de 8–30 años, por lo que el objeto pasa a ser **regímenes** dentro de la muestra; «fase» debe definirse en relación con un ciclo que la muestra no cubre entero. (g) Falta del índice de precios inmobiliarios mensual. | `drehmann_borio_tsatsaronis_2012`, `camiz_cerda_atoche_2026`, `atoche_murrieta_2022` |
| **2.2.2 Enfoque exploratorio, tendencia y regresión espuria** | (a) Qué es «datos primero»: describir la muestra sin modelo generador; la inferencia clásica se sustituye por **estabilidad** (remuestreo) y por **comparación con nulos**; los resultados describen el Perú 2007–2025 y no se generalizan. (b) Por qué niveles (D1) y qué cuesta: el mecanismo de Granger y Newbold explicado en palabras (dos caminatas aleatorias independientes muestran correlaciones grandes con frecuencia), y su consecuencia para el PCA: el primer eje de series con tendencia tiende a ser el tiempo. (c) Por qué no diferenciar: la diferencia es un filtro que borra las oscilaciones lentas; una oscilación de 8 años conserva 0,43 % de su varianza (`anexo/05c_ganancia.csv`, P = 96) y una de 2 años, 6,8 % (P = 24). (d) Autocorrelación y **tamaño efectivo**: meses consecutivos no son observaciones independientes. (e) Distinción tendencia determinística (TS) y estocástica (DS), con y sin deriva (D5, D8), porque define el nulo. | `granger_newbold_1974`, `camiz_maulucci_roig_2010`, `camiz_et_al_2020`; `benzecri_1973` y `tukey_1977` con `[VERIFICAR]` (no leídos) |
| **2.2.3 Régimen, fase y validación** | Traer de la tesis las definiciones de régimen, transición (abrupta/suave, total/parcial) y detección; añadir N1; explicar por qué la validación externa evita la circularidad y por qué, con seis episodios, la correspondencia es **descriptiva y sin poder estadístico** (`02_marco_teorico.tex:234-239`). Advertir que fin de guerra comercial e inicio de COVID distan menos que la tolerancia. | `lehman_brothers_2008` … `nber_2021` |
| **2.2.4 PCA** | (a) Problema: resumir 16 series muy correlacionadas en pocos factores no correlacionados. (b) Idea: rotación que ordena la inercia; mejor aproximación de rango bajo (Eckart–Young, ficha existe). (c) Lectura: carga = correlación serie–eje; círculo de correlaciones (ángulo ≈ correlación, longitud ≈ calidad); cos² = calidad; contribución = quién «construye» el eje; *score* = posición del mes; el signo es arbitrario. (d) Supuestos: relaciones lineales; la estandarización da a cada serie el mismo peso (por eso dos series casi duplicadas pesan doble: D16); ningún supuesto distribucional para describir. (e) Limitaciones: en niveles el eje 1 es casi el tiempo; los ejes son ortogonales por construcción y pueden mezclar bloques; **si dos valores propios son parecidos, sus ejes no están identificados por separado** (solo el plano); sensibilidad a picos (EMBIG 2008). (f) Criterios de retención: qué supone cada uno (Kaiser: eje que resume más que una serie; vara quebrada: reparto al azar de la inercia; Horn: filas independientes, que aquí no se cumple; Rencher–Bartlett: normalidad) y por qué se triangulan; qué recomiendan Camiz y Pillar (2018). (g) KMO y Bartlett: qué miden y que Bartlett es asintótico, exige n ≫ p e independencia. | `jolliffe_2002`, `eckart_young_1936`, `rencher_christensen_2012` (con `[VERIFICAR]`), `camiz_pillar_2018`, `horn_1965`, `kaiser_1960` |
| **2.2.5 HFC** | (a) Problema que el PCA no resuelve: sus ejes son compromisos globales y ortogonales; la HFC da **grupos de series, cada uno con su propio factor**, y los factores pueden correlacionarse. (b) Idea del índice: al fusionar dos grupos, el segundo valor propio es la inercia que se pierde al resumirlos con un solo factor; índice bajo = «son lo mismo»; alto = «son cosas distintas». (c) Por qué 0,7: umbral de Jolliffe para valores propios despreciables, según Camiz et al. (2020) (citar «como se cita en»): un segundo eje por debajo de 0,7 de una serie se trata como ruido. (d) La fusión depende de r² y no del signo: series con correlación negativa (TAMN) entran al mismo grupo. (e) Identidad útil: suma de índices + λ₁ de la raíz = p. (f) Limitaciones: algoritmo aglomerativo voraz (no óptimo; la optimización de Denimal queda como trabajo futuro), jerarquía anidada forzada, representante elegido por correlación. | `camiz_et_al_2020`, `denimal_2007` (solo resumen), `jolliffe_2002` |
| **2.2.6 EPCA y HFC evolutiva** | (a) Problema: el PCA global supone una estructura igual en toda la muestra. (b) Lectura de λ₁(t): coherencia unidimensional de la ventana; si baja, las series se desincronizan; las correlaciones evolutivas dicen **quién** provoca el cambio. (c) Pesos gaussianos: por qué (suavizar la entrada y salida de meses extremos) y su costo: **tamaño efectivo de Kish** (n_ω = 37,0 meses para 48 meses con ν = 3: `06c_aede_valores_propios_resumen.csv`). (d) **Resolución temporal**: cada valor se fecha en el centro, pero un evento del mes s afecta a todas las ventanas centradas entre s − 24 y s + 23; dos cambios a menos de n_w meses no se separan; bordes de ventana (D7, D13). (e) Ventana más larga que número de series (si n_w ≤ p, la matriz es singular). (f) Ventanas sucesivas comparten casi todos los meses: la curva es suave por construcción y **no es una prueba**. (g) Alineación de signo y cruce de ejes. (h) HFC evolutiva: qué añade (qué series cambian de grupo), problema de emparejar clases entre ventanas, mismas limitaciones de resolución. (i) Lectura multiescala de la grilla (D10). | `camiz_maulucci_roig_2010`, `camiz_roig_2011`, `camiz_cerda_atoche_2026`; Camiz y Diblasi (2013) y Kish (1965) con `[VERIFICAR]` |
| **2.2.7 Comparación de configuraciones** | Qué mide la congruencia de Tucker (coseno de cargas, sin centrar) y el RV (correlación entre matrices); **el RV no vale 0 bajo independencia y depende de n y p**, por eso se compara con un nulo y no con un umbral fijo; por qué se usan cargas sin centrar (D17.2). | `tucker_1951` y `josse_pages_husson_2008` (con `[VERIFICAR]`), `robert_escoufier_1976` |
| **2.2.8 Fisher y número de tramos** | (a) Por qué una partición **contigua**: un régimen es un intervalo; la clasificación libre mezclaría meses lejanos. (b) Exactitud y ausencia de inicialización. (c) El método no elige K: por qué eso es el punto débil. (d) Por qué el CH tiende a crecer con K en trayectorias suaves (la suma intra cae rápido) y, por eso, **no se usa como selector (D11)**: bajo el nulo de estructura constante, el CH de `aede` elige el tope en 100 % de las réplicas con 48 meses gaussianos (`07b_nulo_estructura_kstar_posicion.csv`). (e) Regla K de D12 y codo, longitud mínima de 12 meses (qué evita y que es una elección), monotonía del costo. | `fisher_1958`, `calinski_harabasz_1974` (ambos con `[VERIFICAR]`) |
| **2.2.9 Nulos y bootstrap** | (a) Qué es un nulo en un análisis exploratorio: «qué mostraría el método si no existiera la estructura buscada, conservando todo lo demás». (b) Para cada nulo: qué conserva y qué destruye (tendencias: conserva la dinámica de cada serie y rompe la relación entre series; estructura constante: conserva la correlación contemporánea y destruye el cambio en el tiempo). (c) **La conclusión depende del nulo**: con deriva el eje 1 no es significativo (0,910) y sin deriva sí (0,008) (`05_nulo_tendencias.csv`); por eso D5 y D8 fijan el nulo mixto de antemano. (d) El p es una proporción de réplicas, no la probabilidad de la hipótesis. (e) **Potencia**: no superar el nulo no prueba que la estructura sea constante. (f) Bootstrap por bloques: por qué bloques, compromiso del largo de bloque, mismos inicios para conservar la correlación cruzada. | `kunsch_1989`, `lahiri_2003`, `newey_west_1987` (todos con `[VERIFICAR]`), `granger_newbold_1974` |
| **2.2.10 AE y LSTM** | (a) Autoencoder como PCA no lineal (anidamiento: Baldi y Hornik, 1989). (b) LSTM en palabras: memoria que decide qué conservar y qué olvidar, útil para secuencias. (c) LSTM-autoencoder: resume una ventana de meses en un vector. (d) **Supuestos arquitectónicos** que no vienen de los datos (capas, activación, dimensión latente, ventana, semilla) y los cuatro principios de la tesis (anidamiento, anclaje lineal, estabilidad, subordinación: `02_marco_teorico.tex:338-362`). (e) Escala: Tuhin et al. usan 375 acciones diarias en 23 años; aquí hay 16 series mensuales y un tamaño efectivo mediano de 10,6: los parámetros superan con holgura a las observaciones. (f) Qué significa el Monte Carlo Dropout. | `baldi_hornik_1989`, `hinton_salakhutdinov_2006`, `hochreiter_schmidhuber_1997`, `tuhin_et_al_2025`, `gal_ghahramani_2016` |

Además: §2.3 debe crecer con los términos usados en el Cap. III y hoy no definidos: datación, corte,
tramo, transición, ventana, valor propio evolutivo, pesos gaussianos, tamaño efectivo de Kish,
borde de ventana, tolerancia, tendencia TS/DS, deriva, regresión espuria, nulo de tendencias, nulo de
estructura constante, congruencia, índice de Rand ajustado, correlación cofenética, representante
de clase, regla de fases.

#### N3. Interpretar cada resultado (observación 3): qué agregar por figura y tabla

Regla: cada figura o tabla cierra con un párrafo de **interpretación** con tres preguntas: ¿qué dice
del sistema financiero peruano?, ¿qué episodio o mecanismo lo explica (con fuente o con la propia
serie descrita, nunca como validación)?, ¿qué implica para el objetivo o la hipótesis? Los hechos
económicos externos que no tienen ficha se marcan **«propuesta para el bibliotecario, por
verificar»**. Las trayectorias de las series sí pueden describirse con los datos congelados
(descripción, no validación: regla 6).

| Elemento | Interpretación que debe agregarse (con cifras verificadas) |
|---|---|
| **§3.1.1, Figura 2** | Informar el diagnóstico D5 que hoy falta (Tabla 3, etapa 1, promete «diagnóstico de raíz unitaria»): 12 series DS, 3 indeterminadas (crédito de consumo, TIPMN, PBI) y 1 TS (EMBIG) (`05_tendencia_series.csv`, `clase_d5`). Deriva significativa (|t| HAC > 2) en créditos, M1, M3, IPC, RIN, PBI y demanda interna; declarar las cercanas a 2 que pide D8: PBI (2,29) y demanda interna (2,27). Matizar «casi todas crecen»: el tipo de cambio y la BVL tienen r con el tiempo de 0,81 y 0,61, pero su deriva no es significativa (t = 0,20 y 1,34). Interpretación: el crecimiento de saldos refleja profundización financiera y crecimiento nominal; la TAMN cae de 23,75 % (2007-01) a 15,89 % (2025-12) (serie congelada), por eso carga negativa en el eje 1. Cualquier explicación causal de esa caída es **propuesta para el bibliotecario, por verificar**. |
| **§3.1.2, Figuras 3 y 4** | Cuantificar lo que hoy es cualitativo: con n, el 82,5 % de los pares de correlaciones es significativo; con el n efectivo, solo el 42,5 % (`05_n_efectivo_resumen.csv`); al quitar la tendencia lineal el eje 1 pasa de 65,2 % a 38,5 % de la inercia y la KMO de 0,84 a 0,68 (`05_pca_contraste_tendencia.csv`). Interpretación: más de la mitad de la «estructura» visible en niveles es tendencia común; lo que sobrevive es la base de los bloques. El emparejamiento de ejes con y sin tendencia (equivalentes 4, 1, 3, 2; congruencias 0,49; 0,78; 0,82; 0,76) sugiere que el eje de tasas pasa a dominar sin tendencia; **el desarrollador debe confirmar la dirección del emparejamiento** antes de redactarlo. |
| **§3.1.3, Figura 5** | Explicar por qué los criterios discrepan en el eje 3 (λ₃ = 1,21 > 1, pero < p95 de Horn 1,36 y < vara quebrada 11,75 %): es un eje «de frontera». Justificar d = 3 con D9 (fijado antes de ver las cifras), no con «lectura clara», y citar la sensibilidad d = 2 y d = 4. Reportar el criterio de Rencher–Bartlett, que §2.2.4 promete y no aparece (`05_pca_retencion.csv` no lo tiene). |
| **§3.1.3, adecuación** | Con n_ef = 10,6 < p = 16, el estadístico de Bartlett corregido (162; p = 0,007, no «0,01») está fuera del dominio en que la aproximación χ² es razonable: el factor n_ef − 1 − (2p + 5)/6 vale ≈ 3,4. Presentarlo como indicio, no como prueba, y decir qué implica: la información independiente de la muestra equivale a unas diez observaciones, menos que las series. |
| **§3.1.3, Tablas 5 y 6, Figura 6** | Eje 1: las once series contribuyen entre 6,1 % y 9,4 %, es decir, cerca de 1/11 (9,1 %), no de 1/16 como dice el texto: el eje lo construyen **once** series por igual y las otras cinco casi no aportan. Leer la TAMN (−0,87): en niveles, su descenso secular la alinea, con signo opuesto, con los saldos. Eje 2: las tres tasas aportan 88,1 %; su *score* sigue el ciclo de la tasa de referencia (serie congelada: 6,5 % en 2008-09; 1,25 % en 2009-08; 4,25 % entre 2011-05 y 2013-10; 0,25 % entre 2020-04 y 2021-07; 7,75 % en 2023-01): mínimo del eje en 2021-07 y máximo en 2023-08 (`05_pca_scores.csv`). Es el **eje de la postura monetaria**, ortogonal a la profundización. Eje 3: opone EMBIG (+0,81) y BVL (−0,61): es un eje de **aversión al riesgo** (sube el diferencial soberano y cae la bolsa). Tipo de cambio y BVL son las peor representadas (0,77 y 0,79): su información es en parte propia. |
| **§3.1.3, nulos** | Ver N4: reportar el nulo mixto oficial (eje 1: 0,783 / 0,826; eje 2: 0,003 / 0,004; eje 3: 0,221 / 0,223) y explicar que el eje 1 se explica por tendencias independientes, el de tasas no, y el de riesgo tampoco supera el nulo. Interpretación: el único **co-movimiento** que no puede atribuirse a tendencias propias es el de las tasas, que es un hecho institucional esperable (transmisión de la tasa de referencia a la interbancaria y a la pasiva). Decirlo con una fuente o como **propuesta para el bibliotecario, por verificar**. |
| **§3.1.3, Figura 7** | Picos del eje 3: 2008-12 (4,47, máximo del EMBIG, 523 pb), 2016-02 (2,23), 2020-04 (2,41) (`05_pca_scores.csv`); hay además picos en 2021-08 (1,67) y 2022-07 (1,48) que el texto omite y que **no tienen episodio** en la Tabla 4. Interpretarlos o declararlos como señal sin episodio (candidatos externos para el bibliotecario, por verificar: el proceso electoral peruano de 2021). |
| **§3.1.3, bootstrap** | Explicar la cifra: p5 de la congruencia 0,926; 0,786; 0,796 frente a 0,604 del eje 4 (L = 24): los tres primeros ejes conservan su orientación en 95 % de las réplicas con congruencia ≥ 0,79, el cuarto no. Añadir que con L = 36 el p5 baja a 0,71 y 0,74 en los ejes 2 y 3 (`05_bootstrap_congruencia.csv`): la estabilidad depende del largo de bloque. |
| **§3.1.4, Figura 8 y Tabla 7** | Interpretar los nodos: el factor de la raíz tiene λ₁ = 10,337 (64,6 %), casi igual que el primer eje del PCA (10,437; 65,2 %): **la HFC resume casi lo mismo que el PCA, pero con grupos interpretables**. El índice de la raíz (2,768) es casi la varianza total del factor de tasas (2,791): al fusionar tasas con el resto no se gana casi nada, porque sus factores no están correlacionados (r = −0,07; `07c_hfc_correlaciones3.csv`). El nodo 30 (índice 1,11) une riesgo y tendencia con pérdida moderada: sus factores tienen r = −0,48 [p5 −0,64; p95 −0,18], es decir, el riesgo soberano baja cuando la tendencia sube. Nodo 28: el tipo de cambio entra último al bloque (0,353), coherente con su cos² de 0,64. Nodo 29 (EMBIG + BVL, % local 75,3) es el grupo menos homogéneo, como el grupo 29 de Camiz et al. (2026), que también lo describen como dipolo (ficha). |
| **§3.1.4, Tabla 8 y estabilidad** | Representantes: crédito hipotecario (r = 0,994), tasa interbancaria (0,985) y EMBIG (0,868): son las series que mejor «hablan» por su bloque, útiles como indicadores de seguimiento. La partición de tres clases se reproduce en 80 % de las réplicas y la de cuatro en 63 %: los tres bloques son un hallazgo; la separación de EMBIG y BVL, no. Sin tendencia, la correlación entre los factores de tendencia y tasas pasa a −0,41 [−0,64; −0,005]: el bloque de tasas sí se relaciona con las desviaciones del bloque de saldos, aunque no con su tendencia. Esta cifra está calculada y no se usa. |
| **§3.1.5, Figura 9 y Tabla 9** | Leer la curva: λ₁ entre 9,5 y 12,1 hasta 2020 (las 16 series se mueven casi como una) y caída a 6,20 en la ventana centrada en 2021-05 (ventana 2019-05 a 2023-04). Mecanismo descriptivo con la propia data: en 2020–2021 el crédito empresarial creció 24,4 % interanual (2020-09) mientras el de consumo cayó 10,5 % (2021-03) y M1 creció 47,8 % (2020-09; máximo 49,8 % en 2021-01); la inflación llegó a 8,81 % (2022-06) y la tasa de referencia subió de 0,25 % a 7,75 %. Las series dejaron de moverse juntas. La explicación institucional (programas de crédito garantizado de 2020) es **propuesta para el bibliotecario, por verificar**. Corregir la datación según N5. |
| **§3.1.5, Figura 10** | Añadir dos lecturas: (a) la correlación de las tasas con el eje 1 cambia de signo según la postura monetaria dentro de la ventana: positiva en ventanas con alzas de tasa mientras crecen los saldos (aprox. 2011–2012, 2015–2016, 2021–2023) y negativa en ventanas de recorte o pausa (2009–2010, 2013–2014, 2017–2020); lectura visual de la Figura 10, que el desarrollador debe respaldar con el CSV de correlaciones evolutivas: el eje 1 de cada ventana mezcla tendencia y política. (b) En 2021 λ₁ ≈ 6,2 y λ₂ ≈ 5,8: **con valores propios casi iguales, los ejes 1 y 2 no están identificados por separado**; el «cambio» de las tasas al eje 1 y el salto de signo del crédito empresarial pueden ser una rotación dentro del plano. Debe leerse el plano 1–2, no cada eje. |
| **§3.1.5, Figura 11 y nulo** | Explicar la regla del 06 (no está en el Cap. II) y su umbral (media − 1 desviación). Decir que las cinco candidatas de 60 meses no se confirman: ninguna está fuera del nulo y 2017-10 es «transición no confirmada» (D13; `07b_clasificacion_2017_10.csv`). Interpretar el nulo de estructura: en ninguno de los 8 anchos y esquemas la proporción de pares de ventanas «demasiado distintos» supera a la de una estructura constante (menor p = 0,38). Significado: con estos datos, los cambios de estructura no se distinguen del ruido; con un tamaño efectivo tan bajo, el nulo puede tener poca potencia (ver N4 y la recomendación 2 del propio informe). Añadir el resultado del apunte 7 (D14): con 48 meses gaussianos, λ₂ queda bajo el p95 de Horn en 32 de 181 ventanas y λ₃ en 164 de 181 (`06c_aede_valores_propios_resumen.csv`): en la mayoría de las ventanas solo dos ejes superan el ruido, lo que justifica seguir λ₁ y λ₂. |
| **§3.1.6, Figuras 12 y 13** | Corregir la lectura de la Figura 12: el índice de la raíz **no** «crece a partir de 2016»: oscila entre ≈ 1 y ≈ 3,7 hasta 2018, cae a ≈ 1 alrededor de 2017-12–2018-03 y alcanza sus máximos (≈ 4,5) en ventanas centradas en 2021–2022. Interpretación: después de la pandemia los grupos están **más separados entre sí**, coherente con la caída de λ₁. Figura 13: en 2009-07 las tasas, la TAMN y la TIPMN forman un grupo con EMBIG y BVL (crisis: tasas y riesgo se mueven juntos); en 2014-07 el bloque de riesgo se integra al de saldos y las tasas quedan aparte; en 2020-07 la BVL se une a PBI y demanda interna (caída y rebote en V comunes) y la TIPMN se separa de la tasa de referencia; en 2023-07 la demanda interna queda aislada. Ver N7 sobre el origen de estos resultados. |
| **§3.1.7, Tabla 10 y Figura 14** | (a) Explicar la regla de fases con sus umbrales (expansión si la media del componente de crédito > 0,25; contracción si < −0,25; transición si está entre ambos o si el régimen dura < 18 meses: `notebooks/09a_datacion_pca.ipynb`), para que se entienda por qué el régimen 4 (0,17) y los dos primeros (< 18 meses) son «transición». (b) Interpretar los cortes sin episodio con la propia data, como descripción: 2010-03 coincide con el fin del tramo de tasa mínima (1,25 % hasta 2010-04) y 2022-11 con la meseta de tasa máxima (7,25–7,75 % entre 2022-11 y 2023-08). No pueden validarse con la serie de tasa (regla 6); como episodio externo requerirían una fuente (comunicado del BCRP: **propuesta para el bibliotecario, por verificar**, y decisión 5.2). (c) Sensibilidad a d (D9): con d = 2 los cortes son 2010-01, 2011-09, 2018-02, 2020-08, 2022-09; con d = 4, 2012-04, 2020-05, 2022-11 (`09a_datacion_dimension.csv`). Solo los cortes de **mediados de 2020** y **fines de 2022** son robustos a d; el de 2008-12 depende del eje 3 (riesgo), lo que a la vez lo interpreta (pico del EMBIG). (d) Desfase de la media móvil: N6. |
| **§3.1.8, Figuras 15–18** | Reducir a un párrafo con el estatus de antecedente (D17.4) y una interpretación por figura: el AE no supera al PCA fuera de muestra con 228 meses, lo que es esperable por escala, no por Baldi y Hornik (que tratan el caso lineal); el error de reconstrucción sube en la crisis y la pandemia (meses que no comparten la estructura típica: es la utilidad declarada del AE). |
| **§3.2 Discusión** | (b) Comparación **bloque por bloque** con Camiz et al. (2026) en una tabla: su grupo de tasas incluye tasas activas y pasivas en MN y ME (ficha, línea 26), aquí la TAMN cae en el bloque de saldos; su grupo de riesgo incluye reservas y dolarización, aquí las RIN van al bloque de saldos; su grupo de salud no incluye PBI ni IPC. Explicar las diferencias por conjunto de series, período y niveles. Comparar también sus lecturas dinámicas (tasas como alerta temprana; riesgo afectado por 2008 y 2018–2019) con los picos del eje 3 y la Figura 13. Contrastar con Drehmann et al.: allí la bolsa no sincroniza con el crédito; aquí la BVL carga 0,62 en el eje 1 en niveles, pero forma su propio bloque con el EMBIG. |

#### N4. Usar el nulo de tendencias oficial (D8) y reportar los nulos completos

**Ubicación:** Resumen y Abstract; §3.1.3 ¶ «Eje 1» y «Eje 2»; §3.2 ¶1; Tabla 11 (HE2); Conclusión 2.

**Problema:** el texto usa el nulo global **con deriva** (`nuloConDerivaPCUno` = 0,910;
`nuloConDerivaPCDos` = 0,014), mientras D8 fija el **nulo mixto por serie** como el pertinente, y
§2.2.9 describe el mixto. Además, «es el único eje que supera con claridad **los** nulos» es falso:
con el nulo sin deriva, el eje 2 no lo supera (0,474) y el eje 1 sí (0,008)
(`05_nulo_tendencias.csv`). Contradice una decisión vigente (regla 4): se avisa aquí.

**Qué debe decir:** «Frente al nulo mixto de D8, el eje 1 no supera a series independientes con sus
propias tendencias (proporción 0,783 con las indeterminadas como TS; 0,826 como DS); el eje de tasas
sí (0,003 y 0,004), y el de riesgo no (0,221 y 0,223). Los nulos globales con y sin deriva, que
D5 descartó como referencia, dan conclusiones opuestas para el eje 1 (0,910 y 0,008), lo que muestra
por qué el nulo se fijó serie por serie antes de calcularlo.» Las claves `nuloMixtoTsPCUno`,
`nuloMixtoTsPCDos` y `nuloMixtoDsPCDos` ya existen en `_cifras.yml`; faltan las del eje 3 y la
del eje 1 en DS.

#### N5. Corregir la datación del EPCA: el k = 3 por Caliński-Harabasz contradice D11

**Ubicación:** Resumen y Abstract; §3.1.5 ¶1 y ¶2; Tabla 9 (nota); §3.2 (síntesis, hallazgo b);
Tabla 11 (HE3: «EPCA: dos de dos cortes compatibles»); Conclusión 3.

**Problema:** el texto elige 3 tramos (cortes 2014-12 y 2020-07) con el CH de `aede`. D11 dice que el
CH se **informa pero no selecciona**, salvo óptimo interior con maxcl = 20 y fuera del nulo. Con
48 meses gaussianos: CH de `aede` → k = 3 solo con maxcl = 10; con 15 y 20 va al tope; CH habitual y
codo → k = 2 con un solo corte en **2020-05** (`06c_aede_cortes.csv`). Bajo el nulo de estructura
constante, ese CH elige el tope en 100 % de las réplicas (`07b_nulo_estructura_kstar_posicion.csv`).
El corte de 2014-12 depende, por tanto, de la cota.

**Qué debe decir:** (a) que la configuración de Camiz et al. (2026) se reproduce para comparar (OE3
de la tesis), y que con su criterio salen 2014-12 y 2020-07; (b) que bajo las reglas fijadas (D11,
D12) el único corte es **2020-05**; (c) que el corte de mediados de 2020 aparece con el codo en casi
toda la grilla (36 meses: 2020-05 y 2020-09; 48: 2020-04 y 2020-05; 60: 2020-02 y 2020-04) y es el
hallazgo dinámico más robusto; (d) la frase «con 24 meses… cortes en julio de 2008 y junio de 2009»
omite tres de los cinco cortes de ese caso (2011-11, 2020-10, 2024-03). Reescribir el Resumen y la
HE3 en consecuencia.

#### N6. Corregir o declarar el desfase de la media móvil causal en la datación con *scores*

**Ubicación:** §2.2.8 (al final), §3.1.7 ¶3 (compatibilidades), Tabla 10 (nota), Tabla 11 (HE3).

**Problema:** la trayectoria es una media móvil **causal** de 12 meses (`parametros_diseno.csv`,
`ventana_media_movil`; `02_marco_teorico.tex:1277`). Un cambio de nivel en el mes τ aparece en la
media gradualmente entre τ y τ + 11, con retardo medio de (12 − 1)/2 = 5,5 meses. Los cortes de
Fisher sobre la serie suavizada tienden, por tanto, a fecharse **después** del cambio. La
compatibilidad ±3 meses se evalúa sin corregirlo: 2014-04 (a 2 meses del inicio del colapso) y
2020-06 (a 2 meses del fin de COVID) podrían corresponder a cambios ocurridos medio año antes. Ningún
documento del repositorio trata este punto.

**Qué debe decir / hacer:** declarar el retardo en §2.2.8 y, como **cálculo nuevo del desarrollador**,
repetir la evaluación de compatibilidad con los cortes adelantados 5–6 meses o con una media móvil
centrada (sensibilidad, no reemplazo, porque la causal se fijó antes: D12). Hasta tenerlo, la HE3
para los *scores* debe decir «compatibilidad sujeta al retardo del suavizado».

#### N7. Trazabilidad de los resultados del asesor (claede, aede, clahfac)

**Ubicación:** Introducción ¶3; §3.1 ¶1; §3.1.6 ¶1; notas de Figuras 8, 9, 10, 12, 13; Tabla 3
(columna «Programa»).

**Problema:** (a) la «HFC evolutiva con claede» es `cp.clahfac` aplicado a ventanas de 48 meses
**sin pesos** (`resultados_camiz.py:221-229`); `Claede-2_2.R` no está en el repositorio ni en el
sistema, de modo que no se verificó que reproduzca el programa del asesor (pesos, estandarización,
corte). Además, el EPCA usa ventana gaussiana y la HFC evolutiva, uniforme: las Figuras 9–10 y 12–13
no son comparables entre sí sin decirlo. (b) Las cifras `cz*` se leen de
`/home/claude/informe/camiz/camiz_resumen.csv`, fuera de `data/results/` y sin réplica en R (reglas
3 y D6). (c) La Introducción afirma que los programas se trasladaron «con verificación de que
reproducen sus resultados»: es cierto para `aede` y `clahfac` (D6), no para claede.

**Qué debe decir / hacer:** «réplica en Python del procedimiento de claede (clahfac en cada ventana
de 48 meses con pesos uniformes); la paridad con el programa original está pendiente». Desarrollador:
mover estas salidas a `data/results/final/` con prefijo de notebook y paridad R; Roberto: pedir
`Claede-2_2.R` al Dr. Camiz.

#### N8. Referencias sin ficha, marcas de verificación y Anexo 3

**Ubicación:** Referencias; §1.4.4; §2.2.4–2.2.7; Tabla 3 (nota); Anexo 3.

**Problemas (regla 2):**

1. Sin ficha en `papers/` ni entrada en `tesis/referencias.bib` (están solo en
   `referencias_extra.bib`): Abdi (2010), Camiz y Diblasi (2013), Camiz (2021), Camiz (s. f.)
   AedeClahfac, Camiz (2025) claede.R y Samaniego Salcedo (2026). Camiz y Diblasi (2013) figura en el
   registro como **«No localizada»** (`registro_verificacion.md:47`), pero el informe la cita como
   leída.
2. El informe no lleva ninguna marca `[VERIFICAR]`, aunque Fisher (1958), Pyper y Peterman (1998),
   Künsch (1989), Hubert y Arabie (1985), Calinski y Harabasz (1974), Denimal (2007, solo resumen) y
   otros constan como no leídos. El Anexo 3 no sustituye la marca en el texto.
3. El Anexo 3 dice que Horn (1965) y Fisher (1958) se leyeron completos el 7-11-2026; sus fichas
   dicen «Resumen leído» y «No leído», y el registro los tiene pendientes. Además, el texto atribuye a
   esas fuentes contenidos concretos (Horn discute la justificación de Kaiser; el lema de
   suboptimización y la caída de D en Fisher) que solo una lectura registrada sostiene.
4. Fuentes con ficha que el informe no usa y que darían peso al Cap. II frente al jurado: Jolliffe
   (2002), Eckart y Young (1936), Rencher y Christensen (2012), Tucker (1951), Josse et al. (2008),
   Lahiri (2003), Kaiser (1960), Newey y West (1987), Kish (1965). Hoy el PCA se apoya casi solo en
   Camiz (2021), material de clase no publicado.

**Qué hacer:** bibliotecario: fichas y entradas para las seis referencias (o retiro), actualizar
fichas de Horn y Fisher con lo leído el 7-11 y el registro; editor: `[VERIFICAR: motivo]` en cada
cita de fuente no leída y «como se cita en» donde corresponda.

#### N9. Antecedentes de los últimos cinco años (Guía N.° 2)

**Ubicación:** §2.1.

**Problema:** 6 de 9 antecedentes son anteriores a 2021 (2010, 2011, 2012, 2013, 2018, 2020).

**Qué hacer:** separar en §2.1 los **antecedentes 2021–2026** (Atoche Murrieta, 2022; Tuhin et al.,
2025; Camiz et al., 2026, más los que se encuentren) y trasladar los trabajos fundacionales a las
bases teóricas como fuente de cada método, con una frase que justifique su inclusión (fuente
original). Búsquedas propuestas para el bibliotecario, **por verificar**, sin dar ningún título por
cierto: «ciclo financiero Perú» en documentos de trabajo y revistas del BCRP (2021–2026); «financial
cycle emerging markets» y «financial cycle Latin America» (2021–2026); aplicaciones recientes de
PCA evolutivo o de correlación variable en el tiempo a datos macrofinancieros; «LSTM autoencoder
regime detection» en finanzas (2021–2026). Decisión 5.1.

#### N10. Alinear objetivos, hipótesis y métodos con la tesis maestra

**Ubicación:** §1.2.2, §1.3.2, Tabla 11, Matriz de consistencia (Anexo 1), Tabla 3.

**Problema:** el informe tiene OE1–OE5; la tesis, 12 objetivos (`01_introduccion.tex:88-120`), y las
decisiones D9, D10 y D17 se refieren a OE4 (criterio de ventana) y OE6 (dimensión) con la numeración
de la tesis. En el informe, OE4 es «fechar regímenes», y el criterio de ventana —una contribución
declarada, con resultados en §3.1.5— no figura como objetivo. Las hipótesis se llaman HE en el informe
y HT en la tesis. El informe no puede afirmar ni omitir lo que la tesis sostiene (CLAUDE.md).
Además, la Tabla 3 lista el CH como método de la etapa 5 (contra D11) y la «réplica con Rcamiz» (la
referencia es `R/camiz_port.R`; Rcamiz es opcional).

**Qué hacer:** o bien el informe adopta los objetivos de la tesis agrupados (con una tabla de
correspondencia en la matriz), o bien añade un objetivo explícito de criterio de ventana y una nota
de correspondencia de numeraciones. Corregir la Tabla 3.

#### N11. Métodos usados en resultados que el Cap. II no presenta

Regla del 06 y su umbral (Figura 11), tabla y regla de 2017-10 (D13), umbrales por ventana de Kaiser
y Horn con n de Kish (D14), regla K (D12), longitud mínima de 12 meses, regla de fases con sus
umbrales, nulo de estructura con pares no solapados y umbral por posición (D10, D17.2). Cada uno
necesita, al menos, un párrafo conceptual en §2.2 (qué es y por qué) antes de aparecer en el Cap. III.

### 2.2 Recomendables (fortalecen)

- **R1. Usar resultados ya calculados del anexo de robustez.** El informe dice que el análisis con
  transformadas «está pendiente» (Limitaciones; Anexo 2, etapa 4), pero `anexo/05c_pasos.csv` muestra
  que el logaritmo no cambia la estructura (congruencias 0,999; 0,996; 0,992) y la diferencia sí
  (eje 1: 23,5 %), y `anexo/09b_discriminacion_episodios.csv` tiene la detección fuera de muestra con
  el PCA (falsas alarmas 0,92 % con ±3 meses). Decir «parcialmente realizado» y usarlo en §2.2.2 y en
  la discusión.
- **R2. Tabla de correlaciones entre factores de clase** (`07c_hfc_correlaciones3.csv`), en niveles y
  sin tendencia, en §3.1.4.
- **R3. Conclusiones por objetivo.** Hoy son 3 conclusiones; la Guía pide cada una con su
  recomendación. Reorganizar en una por objetivo o hipótesis (OE1 base de datos, que hoy no tiene
  conclusión; estructura; dinámica; datación; aprendizaje profundo) y marcar el estado.
- **R4. Implicaciones (§3.2).** La frase «los regímenes deberán buscarse en la posición del sistema
  dentro de una estructura estable» es la tesis central emergente y está enterrada; convertirla en
  hallazgo explícito, condicionado a la potencia del nulo (N3, Figura 11).
- **R5. Episodios ausentes.** Los picos del eje 3 en 2021 y los cortes 2010-03 y 2022-11 sugieren
  episodios domésticos (proceso electoral de 2021, ciclo de la tasa de referencia) que la Tabla 4 no
  tiene. Propuesta para el bibliotecario, **por verificar**: fuentes oficiales con fecha (JNE, BCRP),
  sujeta a la decisión 5.2.
- **R6. Formato APA.** «−0,00» en la Tabla 5 → «0,00»; p con tres decimales cuando es < 0,01
  (p = 0,007); verificar que las ecuaciones del Cap. II se ven en el .docx (en el texto extraído
  aparecen vacías).
- **R7. Figura 1.** Verificar que la figura tomada del informe MMC101 no muestre elementos ya
  descartados (17 series, dos vías, EHFC como fusión); si los muestra, rehacerla con la cadena
  vigente.

### 2.3 Opcionales (trabajo futuro)

- O1. Lectura del plano 1–2 del EPCA (o del RV por ventana) en lugar de ejes separados cuando
  λ₁ ≈ λ₂.
- O2. Índice de concordancia de Harding y Pagan para comparar dataciones entre métodos (sugerido en
  la ficha de Drehmann; fuente **por verificar**).
- O3. EPCA por bloque HFC, como Camiz et al. (2026).

---

## 3. Riesgos ante el Dr. Camiz y el jurado

1. **Dr. Camiz, sobre claede.** Es su programa. Si la HFC evolutiva no reproduce `Claede-2_2.R`
   (pesos, corte, estandarización), lo notará de inmediato. Llevarlo como «réplica pendiente de
   paridad» (N7).
2. **Dr. Camiz, sobre el CH.** Sabe que su artículo usa CH; D11 dice que aquí no selecciona. Si el
   informe usa CH sin explicarlo, parece incoherente; si lo descarta sin evidencia, parece correctivo.
   La evidencia existe: el CH elige el tope en 100 % de las réplicas del nulo. Presentarlo como
   hallazgo y como pregunta (D11 ya prevé preguntarle por el k de `aede`).
3. **Dr. Camiz, «datos primero».** El nulo de tendencias, la eliminación de la tendencia y la regla
   de fases parecen imponer supuestos. Defensa: los nulos no transforman los datos, los contrastan; la
   ganancia de la diferencia (0,43 % a 8 años) es el argumento a favor de no diferenciar.
4. **Jurado, metodología.** Preguntas previsibles: ¿qué significa un PCA con tamaño efectivo 10,6 y
   16 series?; ¿por qué una prueba de Bartlett con n_ef < p?; ¿por qué el nulo con deriva si D8 dice
   mixto?; ¿por qué ±3 meses con una media causal de 12?; ¿qué potencia tiene el nulo de estructura?;
   ¿qué es «datación»? Hoy el informe no responde ninguna.
5. **Jurado, contribución.** Si la HE1 no se respalda, la HE4 tampoco y las fases no son válidas, el
   aporte frente a Camiz et al. (2026) se reduce a extender el período y a la validación con nulos.
   Hay que decirlo así, y mostrar que esa validación es en sí un aporte (cambia la lectura de los
   cortes del antecedente).
6. **Jurado, formato.** Antecedentes fuera de los cinco años; referencias no publicadas (material de
   clase, programas) como fuente principal del PCA; aprendizaje profundo reportado con 17 series
   cuando el análisis tiene 16.
7. **Regla 7.** El informe contiene el capítulo de resultados; no debe publicarse en el sitio sin la
   aprobación explícita de Roberto (el README ya lo dice: solo Word).

---

## 4. Afirmaciones no sustentadas, incorrectas o imprecisas

| # | Ubicación | Afirmación | Verificación | Corrección |
|---|---|---|---|---|
| 1 | Resumen; §3.1.3 «Eje 1»; Concl. 2 | El eje 1 «no superó un nulo de caminatas aleatorias con deriva» | Cifra correcta (0,910), pero no es el nulo oficial (D8) | Usar el mixto: 0,783 / 0,826 (N4) |
| 2 | §3.1.3 «Eje 2» | «Es el único eje que supera con claridad los nulos (0,014)» | Sin deriva: eje 2 = 0,474 (no supera) y eje 1 = 0,008 (supera) | «Supera el nulo mixto (0,003 y 0,004)» |
| 3 | Resumen; §3.1.5 ¶1; Tabla 11 HE3; Concl. 3 | El EPCA «fechó dos cortes», 2014-12 y 2020-07, «dos de dos compatibles» | Solo con CH de `aede` y maxcl = 10; codo y CH habitual: un corte, 2020-05; CH al tope con maxcl 15 y 20 (`06c_aede_cortes.csv`); contradice D11 | N5 |
| 4 | §3.1.5 ¶2 | «con 24 meses y pesos uniformes, el criterio de la mayor caída… da cortes en julio de 2008 y junio de 2009» | Da cinco cortes: 2008-07, 2009-06, 2011-11, 2020-10, 2024-03 | Citar los cinco |
| 5 | §3.1.3 ¶ Tabla 6 | El eje 1 recibe contribuciones «cercanas a 1/16 (6,25 %)» de once series | Están entre 6,1 % y 9,4 %; ocho superan 8,3 %; ≈ 1/11 | «Cercanas a 1/11 (9,1 %)» |
| 6 | §3.1.3 ¶1 | Bartlett con n_ef: «p = 0,01» | p = 0,0067 (`05_adecuacion.csv`); además n_ef < p | «p = 0,007», y advertencia de validez |
| 7 | §3.1.3 ¶1 | «Se trabaja con tres ejes porque el tercero tiene una lectura clara y es estable» | La razón registrada es D9 (fijado antes de las cifras) | Citar D9 y la sensibilidad d = 2, 4 |
| 8 | §2.2.4 / §3.1.3 | Se combinan «cuatro criterios» de retención | Rencher–Bartlett no se reporta (`05_pca_retencion.csv`) | Reportarlo o quitarlo de §2.2.4 |
| 9 | §3.1.4 ¶1 | «Los factores de los nodos resumen el 64,6 % de la inercia» | 64,6 % es la varianza del factor de la raíz (10,337/16) | «El factor de la raíz resume 64,6 %, frente a 65,2 % del eje 1» |
| 10 | §3.1.6 ¶1 | «El índice de la raíz crece a partir de 2016» | La figura muestra oscilación 1–3,7 hasta 2018, mínimo ≈ 1 en 2017-12–2018-03 y máximos ≈ 4,5 en 2021–2022 | Describir así |
| 11 | Intro ¶3; §3.1.6; notas Fig. 12–13 | HFC evolutiva «con el programa claede» y programas «trasladados con verificación» | Es `clahfac` por ventana sin pesos en Python; claede no está en el repositorio ni tiene paridad | N7 |
| 12 | §3.1.7 ¶3; Tabla 11 | Tres de cinco cortes compatibles con ±3 meses | Cortes sobre media móvil causal de 12 meses: retardo ≈ 5,5 meses no considerado | N6 |
| 13 | §3.1.7 ¶3 | «las dos dataciones coinciden… en otro [corte] entre 2014 y 2015» | 2014-04 (*scores*) y 2014-12 (EPCA, solo con CH y maxcl = 10): 8 meses y miden cosas distintas (N1) | Retirar o matizar |
| 14 | §3.1.5 ¶3 | Tras 2020 «las tasas pasan a correlacionarse con el eje 1» | En 2021, λ₁ ≈ 6,2 y λ₂ ≈ 5,8: ejes no identificados por separado | Leer el plano 1–2 |
| 15 | §3.1.5 ¶4 | Cinco «transiciones candidatas» con 60 meses, sin calificar | Ninguna fuera del nulo; 2017-10 es «no confirmada» (D13; `07b_tabla_2017_10.csv`) | Calificarlas |
| 16 | §3.2 ¶2 | «La coincidencia sugiere que la organización transversal es robusta a la elección de series y de período» | No se comparó bloque por bloque; TAMN y RIN cambian de grupo frente a Camiz et al. (2026) | Matizar y añadir la comparación (N3) |
| 17 | §3.2 ¶2 | «Con unas 10,6 observaciones efectivas, las ventanas del EPCA contienen poca información» | 10,6 es la mediana global de pares; no se calculó por ventana | Decirlo como inferencia o calcular por ventana |
| 18 | §3.2 ¶2 | Que el AE no supere al PCA «es coherente con Baldi y Hornik (1989)» | Baldi y Hornik tratan el AE **lineal**; no predicen nada sobre el no lineal | Atribuirlo al tamaño de muestra |
| 19 | §3.2 Limitaciones; Anexo 2 | Robustez con transformadas «pendiente» | `anexo/05c_*` y `09b_*` ya existen | «Parcialmente realizado» (R1) |
| 20 | Anexo 3 | Horn (1965) y Fisher (1958) leídos completos el 7-11-2026 | Fichas: «Resumen leído» y «No leído»; registro pendiente | Actualizar fichas o corregir el anexo (N8) |
| 21 | Anexo 3 | «Todas las afirmaciones sobre métodos se apoyan en una fuente» | Seis referencias sin ficha; Camiz y Diblasi (2013) «no localizada» en el registro | N8 |
| 22 | §2.2.6 ¶3 | «la HFC evolutiva los integra» (HFC y EPCA) | Contribución plausible, pero la HFC evolutiva es del asesor (claede) y no se ha mostrado qué integra respecto del EPCA | Atribuir y precisar |
| 23 | §3.1.1 | «Casi todas crecen de forma sostenida» | TC y BVL: deriva no significativa (t = 0,20 y 1,34) | Matizar con D5/D8 |
| 24 | §3.1.2 | Sin tendencia «aparecen relaciones de signo distinto» | Cualitativo, sin cifra | Citar KMO 0,68, inercia 38,5 %, 42,5 % de pares significativos |
| 25 | §3.2 ¶2 | «en ese trabajo el grupo de riesgo incluye… reservas y dolarización» | Correcto para Camiz et al. (2026) (ficha), no para Atoche Murrieta (2022), también nombrada en la frase | Nombrar el trabajo |

Cifras verificadas sin observaciones: inercias 65,2/19,4/7,6; Kaiser 3, Horn y vara 2; KMO 0,84;
n_ef 10,6; χ² 10 492 → 162; cargas y cos²/contribuciones de las Tablas 5–6; r = 0,993; p5 de la
congruencia; nodos de la Tabla 7; 64,6/35,4 %; 500 réplicas, 0,80, 0,63, 0,99; λ₁ 6,20–12,07 y mínimo
en 2021-05; Tabla 9; 181 ventanas, 2–6 clases, moda 4, 0,41; menor p = 0,38 en 8 configuraciones;
seis regímenes, cortes y frecuencias de la Tabla 10; k = 11 con cota mayor.

---

## 5. Decisiones que solo Roberto o el Dr. Camiz pueden tomar

1. **Antecedentes (N9).** (a) Limitar §2.1 a 2021–2026 y mover los fundacionales a bases teóricas;
   (b) mantener todos con una nota de justificación. **Recomiendo (a)**: es lo que pide la Guía y no
   pierde contenido.
2. **Episodios domésticos fechados por el BCRP (R5).** Fechar episodios de política monetaria con
   comunicados del BCRP es «externo al análisis» según D18, pero la tasa de referencia es una de las
   series: hay riesgo de circularidad. **Recomiendo no añadirlos como episodios de validación** y usar
   la trayectoria de la tasa solo como descripción; los electorales sí pueden añadirse con fuente
   oficial.
3. **Datación del EPCA en el informe (N5).** (a) Presentar como principal la regla de D11/D12 (un
   corte, 2020-05) y la del antecedente como comparación; (b) al revés. **Recomiendo (a)**, por D11.
4. **Media móvil (N6).** Aceptar una sensibilidad con media centrada o con cortes adelantados
   (nuevo cálculo). **Recomiendo aceptarla** como sensibilidad; la causal sigue siendo la principal.
5. **Pedir `Claede-2_2.R` al Dr. Camiz** (N7) y preguntarle por el k de `aede` (ya previsto en D11).

---

## 6. Plan de la iteración (corrección del informe)

**Objetivo:** informe preliminar con marco teórico desarrollado, «datación» definida, resultados
interpretados y cifras alineadas con D8, D11 y D12, sin referencias sin ficha.

| Agente | Tareas | Criterio de aceptación verificable | Depende de |
|---|---|---|---|
| Bibliotecario (fase 0) | N8: fichas/entradas o retiro de las seis referencias; actualizar Horn, Fisher y Camiz y Diblasi en fichas y registro; búsquedas de N9 y N1 (Bry y Boschan; Harding y Pagan) y de R5, todas «por verificar» | Toda clave citada en el informe existe en `tesis/referencias.bib` y en `papers/`; el registro coincide con el Anexo 3 | — |
| Desarrollador (fase 0) | N7: salidas de clahfac/aede/claede en `data/results/final/` con prefijo y paridad R; claves de `_cifras.yml` para el nulo mixto completo, D9, D14, 07c y anexo | Ninguna cifra del informe se lee fuera de `data/results/`; paridad R ≤ tolerancia vigente | — |
| Desarrollador | N6: sensibilidad de la datación al retardo de la media móvil; confirmar dirección del emparejamiento de `05_pca_contraste_tendencia.csv` | CSV nuevo en `data/results/final/` con cortes y distancias a episodios en ambas versiones | Decisión 5.4 |
| Redactor LaTeX | Llevar a la tesis maestra los nuevos párrafos conceptuales que no estén (datación, lectura de λ₁≈λ₂, retardo de la media, validez de Bartlett con n_ef < p) | Ningún concepto del informe falta en la tesis | Bibliotecario |
| Editor del informe | N1–N5, N9–N11, R1–R7 según este documento | Cada fila de la tabla de la sección 4 corregida; cada figura/tabla del Cap. III con párrafo de interpretación; §2.3 con los términos listados en N2 | Todos los anteriores; decisiones 5.1–5.3 |
| Auditor | Revisión independiente del informe contra CSV, fichas y decisiones | Dictamen APROBADO | Editor |

---

## 7. Resumen (recomendaciones necesarias)

1. N1: definir «datación» en §2.2.3 y §2.3: partir una trayectoria en tramos con Fisher; distinguirla del fechado externo de episodios y de los puntos de giro de Drehmann/NBER.
2. N2: reescribir §2.2.1–2.2.10 con qué es, por qué, cómo se lee, supuestos y límites de cada método; trasladar el desarrollo que ya está en `02_marco_teorico.tex`.
3. N3: cerrar cada figura y tabla del Cap. III con interpretación económica y metodológica apoyada en los CSV y en las series congeladas.
4. N3 (claves): eje 1 = profundización (once series ≈ 1/11 cada una); eje 2 = postura monetaria (mínimo 2021-07, máximo 2023-08); eje 3 = aversión al riesgo (picos 2008-12, 2016-02, 2020-04 y 2021).
5. N3 (EPCA): la caída de λ₁ a 6,20 en 2021-05 refleja la desincronización de 2020–2022 (crédito empresarial +24 %, consumo −10 %, M1 +48 %, inflación 8,8 %); con λ₁ ≈ λ₂ hay que leer el plano.
6. N4: sustituir el nulo con deriva por el nulo mixto de D8 (eje 1: 0,783/0,826; eje 2: 0,003/0,004) y corregir «supera los nulos».
7. N5: el k = 3 del EPCA por CH contradice D11; con las reglas fijadas solo queda el corte 2020-05, robusto en la grilla.
8. N6: la media móvil causal de 12 meses retrasa los cortes ≈ 5,5 meses; declarar el retardo y calcular una sensibilidad antes de afirmar la compatibilidad con episodios.
9. N7: la «HFC evolutiva con claede» es una emulación sin pesos y sin paridad; pedir el programa al Dr. Camiz y llevar las cifras a `data/results/`.
10. N8: seis referencias sin ficha, ningún `[VERIFICAR]` en el texto, y un Anexo 3 que contradice las fichas de Horn y Fisher.
11. N9: los antecedentes deben ser de 2021–2026; los fundacionales pasan a bases teóricas.
12. N10: alinear objetivos e hipótesis con la tesis (el criterio de ventana falta como objetivo) y corregir la Tabla 3 (CH, Rcamiz).
13. N11: presentar en el Cap. II la regla del 06, D12–D14, la regla de fases con sus umbrales y el nulo de estructura antes de usarlos en el Cap. III.
14. Corregir las 25 afirmaciones de la sección 4 (p. ej., 1/16 → 1/11; p = 0,007; índice de la raíz; cinco cortes con 24 meses).
15. Riesgo mayor ante el jurado: n_ef ≈ 10,6 < 16 series; hay que decir qué permite concluir y qué no, y discutir la potencia del nulo de estructura.
