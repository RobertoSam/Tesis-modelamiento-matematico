# Asesoría · Adenda al plan de la iteración 3b · 26 de octubre de 2026

**Base:** `iteracion-3b` en `2be3665`. **Lee:** `decisiones.qmd` (D15, D16), el plan del 21-oct y
`auditorias/notas/2026-10-26_desarrollador.md` (en adelante, «la nota»). Solo se indica lo que cambia;
lo demás del plan sigue vigente. NIV-17 y TRA-17 son las salidas actuales con 17 series.

## 1. Diagnóstico breve

1. D15 y D16 dejan como **antecedente** toda la fase 0 de 3b (89 filas de paridad) y el PCA de 3a:
   todo se calculó con 17 series y en dos vías. El código, en cambio, se conserva: ya está validado.
2. **Hallazgo necesario (no lo previó el plan):** `coef_rv` centra las columnas (`src/multivariado.py:167`,
   Rmd `:376`). Aplicado a cargas (series × ejes), el centrado resta la carga media de cada eje. En
   niveles, el PC1 tiene cargas casi iguales y del mismo signo, así que se borra justo lo que es común.
   Es la explicación probable de los RV bajos en niveles, tanto observados como nulos (p5 entre 0,105 y
   0,174; `07b_nulo_estructura_rv_nulo.csv`, filas 10–16). Hay que corregirlo antes de D10 (§4.2).
3. **`torch` sigue ausente:** 08 y 09 no pueden reentrenarse con 16 series. `09_walkforward_errores.csv`
   (que alimenta la detección de episodios del anexo) tiene 17 series.
4. **Ventaja:** con 16 series no se conoce aún ningún resultado. Si las tres confirmaciones del §4
   quedan registradas **antes** de volver a calcular, D9–D13 se fijan realmente de antemano.

## 2. Rmd final y anexo (D15)

**Archivo:** `R/ciclo_financiero_final.Rmd` (nombre propuesto), con `version_asesor` y salidas en
`data/results/final/` (niveles) y `data/results/final/anexo/` (transformadas). El Rmd actual no se
modifica ni se vuelve a renderizar en 3b, y su HTML queda como exploración.

| Sección del Rmd final | Contenido | Se reutiliza del Rmd actual |
|---|---|---|
| 0 · Configuración y funciones | locale, paquetes, `camiz_port.R`, funciones | `configuracion`, `paquetes`, `funciones` (`:22–660`), con la lista de series de D16 y los episodios leídos del CSV de D9 |
| 1 · Series y criterio de inclusión | ficha (16 series), cobertura, gráficos y «qué entra»: crédito total, IPC subyacente y M2 (D16, con las correlaciones calculadas en línea) | `b1-*` (`:667–995`) |
| 2 · Diagnóstico sin transformar | D5, $n_{ef}$, adecuación, nulo de tendencias **mixto** (D8/D11), contraste sin tendencia | partes de §2 (`:1182–1374`) y de A.1 |
| 3 · PCA estático | PCA, bootstrap, Horn y vara quebrada; d = 3 con sensibilidad 2 y 4 (D9); M2 como **variable suplementaria** (§5) | A.2 (`:1690–2273`) |
| 4 · EPCA | `aede` en grilla, λ por ventana, regla del 06 por ancho, nulo de estructura, criterio de OE4 y tabla de 2017-10 | A.3 y Anexo 3b (`b3b-aede-grilla`, `b3b-valores-propios`, `b3b-regla06`, `b3b-nulo`) |
| 5 · HFC | 3 y 4 clases, factores, representantes, bootstrap | A.4 y `b3b-hfc` |
| 6 · Datación de regímenes | PCA-MM12, grilla de maxcl × criterio, estabilidad de cortes, d ∈ {2, 3, 4} | A.6 y `b3b-datacion` |
| 7 · Autoencoders y LSTM | `\pendiente` hasta reentrenar con 16 series (decisión R1) | — |
| 8 · Síntesis descriptiva | sin conclusiones sobre la Parte C (regla 7) | — |
| Anexo R · Robustez (transformadas) | **R.a** sustento de no diferenciar: pasos log/diferencia, ganancia $2\sin(\pi/P)$, espectro, PCA en los dos pasos. **R.b** detección de episodios fuera de muestra con el error *walk-forward* del **PCA** (sin `torch`) y 16 series; los de AE y LSTM, como antecedente con 17. **R.c** (recomendable) congruencia entre 16 y 17 series de los resultados clave | `b2s-pasos`, `b2s-ganancia`, `b2s-espectro`, `b2s-estacional`; B.6 solo para el *walk-forward* |
| Anexo P · Paridad | `R_paridad_python.csv` de `final/` y `final/anexo/` | `anexo` de paridad (`:5060–`) |

Contenido **mínimo** del anexo: R.a y R.b. Quedan fuera B.1–B.5 y la Parte C.

## 3. Qué se rehace y qué queda como antecedente

- **Antecedente congelado.** Se crea el tag `v0.4-17series-dos-vias` sobre `2be3665`. Se agrega un
  `LEEME.md` en `data/results/` y en `niveles/` que diga «antecedente, 17 series, no consumir». Ningún
  CSV antiguo se borra ni se sobrescribe.
- **Se rehace con 16 series y solo en niveles:** 05 (3a), D3, D4, D5, D6, D7 y D8.
- **Se rehace en el anexo (transformadas):** solo R.a y el *walk-forward* del PCA para R.b.
- **No se rehace:** 06a, 06b (D3) y 08/09 (sin `torch`). Tampoco la HFC, el nulo de estructura ni
  `aede` de la vía transformada: quedan como antecedente.
- **Datos.** `src/datos.py` y el Rmd final excluyen M2 al leer, con el md5 de D4 sin cambios
  (228 × 16 y 227 × 16). La lista de series excluidas es un parámetro único.
- **Notebooks.** No se duplican. Los vigentes (05, 06, 06c, 07b, 07c, 09a) reciben un bloque de
  parámetros (`VIA`, `EXCLUIDAS`, `CARPETA`), corren en NIV-final por defecto y escriben en
  `final/`. El código de dos vías se conserva detrás del parámetro.
- **Paridad (D6) sigue vigente.** Las mismas reglas de 3b (índices y umbrales de Horn compartidos;
  réplicas 21–200 del nulo solo en Python, declaradas), ahora entre el Rmd final y los notebooks.
- **Prueba de no regresión del código (sustituye al criterio 3):** con `EXCLUIDAS` sin M2 y
  `CARPETA` temporal, el pipeline nuevo reproduce byte a byte, en NIV-17, `R_aede_cortes.csv`,
  `09a_datacion_criterios.csv`, `R_hfc_clases3.csv` y `05_pca_valores_propios.csv`. Así se demuestra
  que lo único que cambió es la exclusión.

## 4. Tareas y criterios afectados

**Nuevas tareas del desarrollador (antes de D9):** **D0** (tag, `LEEME`, parámetros de datos);
**DF** (esqueleto del Rmd final y secciones 1–3, incluido 05); **DR** (secciones 4–6 con 16 series:
D3–D8 rehechas); **DX** (anexo R.a y R.b). Para D7: corregir `coef_rv` como indica §5.2.

| Tarea | Cambio |
|---|---|
| D9 | Sin cambios de fondo. Los consumidores **vigentes** son el Rmd final, 05, 06, 09a y `modelos_dl.py`. El Rmd de exploración, 06a y 06b quedan fuera del criterio 7, con una nota. El criterio 8 (reproducir `09_discriminacion_episodios.csv`) se mantiene como prueba única con 17 series; la discriminación oficial pasa a R.b |
| D10 | Solo NIV-final, con el RV de §5.2 y la regla de §5.3 |
| D11 | Solo NIV-final (el nulo mixto es, de hecho, solo de niveles) |
| D12 | d ∈ {2, 3, 4} en NIV-final. Macros de métodos desde `final/`, incluida $p = 16$ |
| L1, L4 | Sin cambios. L4 agrega la macro de $p$ y la notación de variable suplementaria |
| L2 | El nulo de D7 solo sobre los incrementos acumulados. Se añade la definición del RV de cargas sin centrar |
| L3 | Datos: 16 series y D16 por macro. Diseño: análisis en niveles y anexo de robustez (D15), descrito **como diseño adoptado, sujeto a la reunión N**. La sección «Qué vía mide qué» sigue en `\pendiente` |
| E1–E3 | Derivan de L1–L4, sin cambios de procedimiento |

**Criterios del plan modificados:** 2 (renderiza el Rmd final; el de exploración no cambia, md5 del
`.Rmd` igual al de `2be3665`); 3 (lo sustituye la prueba del §3); 4 (paridad en `final/` y
`final/anexo/`); 5 (λ1 + λ2 + λ3 ≤ 16); 7 (consumidores vigentes). **Nuevos:** 16) ningún CSV de
`final/` contiene la columna «Liquidez M2», salvo la proyección suplementaria; 17) los CSV
antecedentes son idénticos a los de `2be3665` (md5); 18) D17 (§5) tiene un commit anterior al
primer resultado con 16 series.

## 5. Las tres confirmaciones del desarrollador (nota, §7)

Se recomienda registrarlas juntas como **D17** antes de DR.

**5.1 maxcl de la regla K.** Opciones: (a) 10, (b) 15, (c) 20, (d) no fijar una principal.
**Recomendación: (a) maxcl = 10 como principal**, porque es la especificación anterior a 3b
(`datar` del Rmd, `:418`: «k <= 10», y notebook 09). Es la misma lógica de D9. Se informan 15 y 20
como sensibilidad. Las soluciones en que todos los segmentos miden exactamente $n_{\min}$ = 12 se
marcan como artefacto (columna `segmentos_en_minimo`), sin acotar la grilla. Si con 16 series la
regla cae al paso 2 con maxcl = 10, como ocurrió con 17 (nota §4.1), se informa tal cual.

**5.2 Lectura del RV.** Opciones de objeto: (a) cargas 16 × 3 centradas (lo implementado);
(b) cargas 16 × 3 **sin centrar**; (c) matrices de correlación completas 16 × 16. Opciones de
umbral: p5 agrupado o p5 por posición.
**Recomendación: (b) como principal y (c) como sensibilidad;** (a) se descarta por el §1.2.
(b) compara los subespacios de d = 3 ponderados por sus cargas: es invariante al signo, al orden y
a las rotaciones de los ejes, de modo que los cruces λ2 ↔ λ3 no lo afectan, y responde a OE4 con la
d de D9. (c) no depende de d ni de `aede`, que es la lectura de «datos primero». En niveles, sin
embargo, la domina el PC1 de profundización.
**Umbral: p5 por posición.** El nulo en niveles acumula incrementos desde 0 y no es estacionario
en el tiempo, por lo que el agrupado mezcla posiciones distintas. **Estadístico de OE4:** la
proporción de pares observados bajo su p5, comparada con la **distribución nula de esa misma
proporción** en las réplicas (el p5 de cada réplica se calcula dejándola fuera). Así se trata la
dependencia entre pares contiguos y las comparaciones múltiples (riesgo 1 del plan). Cuesta poco:
el costo está en `aede`, no en el RV.

**5.3 D13 y la regla del 06, que no tiene pesos.** Opciones: (a) la regla del 06 queda fuera de
D13; (b) cuenta como evidencia de **pesos uniformes**, y la de pesos gaussianos solo puede venir de
`aede` gaussiano; (c) se reemplaza la condición de pesos por «confirmada por otro método».
**Recomendación: (b).** Es la lectura literal más conservadora: la regla del 06 es una ventana de
pesos iguales. Confirmación = un candidato dentro de ±3 meses de 2017-10 (D7) que aparezca con ≥ 2
anchos (en el 06 o en `aede` uniforme), aparezca en `aede` gaussiano con algún ancho, no sea borde y
quede fuera del nulo (D10). (c) cambiaría la regla después de ver la nota y se descarta.

Las definiciones operativas de la nota (representante de la HFC; cruce λ2 ↔ λ3) se aceptan
declaradas. La del representante se lleva como pregunta al Dr. Camiz.

**R1 (decisión nueva) · AE y LSTM con 16 series.** Opciones: (a) instalar `torch` y reentrenar en
3b; (b) dejar la sección 7 en `\pendiente` y AE/LSTM como antecedente con 17 series, para la
iteración 4; (c) retirarlos. **Recomendación: (b).** Son complemento (regla 5), y R.b se sostiene con
el PCA sin `torch`.

## 6. Riesgos ante el Dr. Camiz y la reunión N

1. **Hecho consumado.** D15 adopta en la práctica la Parte C antes de discutirla. Él pidió sustentar
   la transformación y probar sin transformar (D2), no abandonar las transformadas. Mitigación: el
   anexo R conserva el contraste. Se presenta como propuesta y se deja reversible: los notebooks
   siguen con `VIA` como parámetro.
2. **«Esto mide tendencias, no el ciclo».** En niveles, PC1 no supera al nulo de tendencias (p ≈ 0,90,
   con 17 series), $n_{ef}$ = 10,4 y Bartlett con $n_{ef}$ da p = 0,060. Es la objeción más fuerte,
   también ante el jurado y frente al título. Hay que llevar una respuesta explícita sobre qué se
   llama «ciclo» en niveles: regímenes de estructura, no oscilación.
3. **Excluir M2.** En la tradición de Benzécri no se depuran variables a priori, y la HFC trata la
   redundancia por construcción (M2 y M3 se agregarían primero). Mitigación: M2 como **variable
   suplementaria** (proyectada, sin peso) en el PCA y en la HFC, más R.c (16 frente a 17). Propuesta
   para el bibliotecario, **por verificar**: una fuente sobre elementos suplementarios en el análisis
   factorial (p. ej., Lebart, Morineau y Piron, o Escofier y Pagès).
4. **Cambiar el conjunto de variables después de ver resultados** (jardín de senderos). Mitigación:
   declarar que D16 se tomó con correlaciones de los datos y no con resultados del análisis, y
   publicar el antecedente con 17 series.

**Qué llevar a la reunión N** (sin resultados nuevos, regla 7): (i) D15 con la sección 2 en
`version_asesor = TRUE` y el índice del Rmd final; (ii) D16 con las correlaciones y la propuesta de
M2 suplementaria; (iii) preguntas: si el k de `aede` es deliberado (en el nulo, el CH con k gl elige
el tope en ≥ 80 % de las réplicas; insumo metodológico con 17 series, rotulado como antecedente),
el ancho de 48 meses como referencia, la definición del representante de clase y el diseño del nulo.

## 7. Orden de ejecución

1. **Ya, sin más confirmaciones (fase 0'):** D0, DF (secciones 0–3, con 05 y nulo mixto D11) y DX
   (R.a); D9 (episodios); la corrección de `coef_rv` con prueba unitaria (se conserva la versión
   centrada para la no regresión); bibliotecario, propuesta del §6.3. Nada de esto depende del §5.
2. **Roberto registra D17 (§5.1–5.3) y R1.** Es una línea por punto, con commit propio.
3. **DR** (D3–D8 con 16 series) y, después, **D10** y **D12**, y **DX** R.b (necesita D9).
4. L1–L4 → E1–E3 → auditoría. Si la reunión N ocurre antes, L3 se ajusta a lo que diga el Dr. Camiz.

Recomendación de proceso: si DR se demora, auditar 0' como **3b-1**, para no acumular otra fase
sin respaldo.
