# 5. CONCLUSIONES Y RECOMENDACIONES

La estructura factorial y su evolución están establecidas con las series en niveles; la identificación de los regímenes, en cambio, no supera todavía el contraste con las series de referencia simuladas, y su validación estadística está en estudio. Los regímenes que se caracterizan en este informe se presentan, por ello, como una descripción tentativa.

## 5.1 Conclusiones

1. **Estructura factorial global (OE1).** Los 16 indicadores se organizan en tres bloques (escala del sistema financiero, condiciones monetarias y riesgo de mercado), que el análisis en componentes principales y la clasificación factorial jerárquica identifican por caminos distintos y que equivalen a los grupos reportados por los antecedentes peruanos. En niveles, el bloque de escala no se distingue de series independientes con tendencia, y la partición en bloques es sensible a la trayectoria particular de las series; el único co-movimiento que supera el contraste es el de las tasas de interés.

2. **Evolución de la estructura (OE2).** La intensidad del movimiento común es alta y relativamente estable hasta 2019 y cae desde 2020, cuando los bloques se fragmentan y el crédito empresarial y los agregados monetarios dejan de moverse con el resto. El crédito hipotecario y el índice de precios permanecen en la misma clase en todas las ventanas, y desde mayo de 2021 esa clase incluye, en la mayoría de las ventanas, las tasas de interés. Las discontinuidades de las correlaciones evolutivas se deben al intercambio del segundo y el tercer eje cuando sus valores propios se cruzan, y no al signo de los ejes. El mayor cambio de estructura del período ocurre alrededor de junio de 2020, pero no se distingue de las variaciones que produciría una estructura constante con la autocorrelación de los datos.

3. **Segmentación temporal (OE3).** Con las series en niveles, ninguna partición de las trayectorias de estructura y de posición supera a las series de referencia simuladas. El corte de 2020 en la trayectoria de estructura queda en el límite ($\hat p=0{,}065$), y los regímenes de posición no se distinguen de los que produce la tendencia común. El contraste con series de referencia simuladas muestra que la partición de una trayectoria con tendencia produce regímenes aparentes, y es por ello un componente necesario del modelo.

4. **Caracterización de los regímenes (OE4).** Con la especificación de trabajo, los seis regímenes de posición describen una secuencia económica coherente (auge previo a la crisis, crisis, expansión, desaceleración, reactivación con estancamiento del crédito real y contracción real del crédito), y tres de sus cinco cortes coinciden con episodios documentados, más de lo esperable por azar, aunque sin significación. La regla de fases basada en el crecimiento real del crédito produce una secuencia con sentido económico con $c=0{,}5$, y con $c=1$ clasifica la mayoría de los regímenes como transición.

5. **Representaciones no lineales (OE5).** En la corrida exploratoria, el autoencoder no supera al PCA en el error de reconstrucción fuera de muestra, y su principal aporte es señalar los meses atípicos de la pandemia. La comparación definitiva requiere repetir los modelos con la base vigente.

## 5.2 Recomendaciones

El proceso de análisis está en desarrollo, y los resultados de este informe son parciales. La representación factorial global y su evolución están establecidas, pero la segmentación en regímenes todavía no supera el contraste con las series de referencia simuladas, y la comparación con las representaciones no lineales se hizo con una versión anterior de la base.

Lo que aún falta mejorar es lo siguiente:

1. **Validación de la segmentación.** Completar la partición por tendencias segmentadas, que distingue la velocidad del crecimiento de su nivel acumulado sin transformar las series, con un contraste global sobre el número de tramos, tramos de al menos 24 meses, el análisis de la influencia de los choques transitorios de 2008–2009 y 2020, la sensibilidad al largo de los bloques del remuestreo y la descomposición del resultado por eje.
2. **Potencia del contraste de cambio de estructura.** Simular series con un cambio de estructura de tamaño conocido para establecer si el cambio de 2020 no se detecta por falta de información o porque la estructura es estable.
3. **Representaciones no lineales.** Repetir el autoencoder y el autoencoder LSTM con las 16 series y la especificación de la sección 3.2.7, y documentar los hiperparámetros con los que se obtienen los resultados.
4. **HFC evolutiva.** Verificar la implementación contra el programa original del asesor.
5. **Datos.** Obtener el crédito de 2006 y el crédito a tipo de cambio constante, para completar la regla de fases y separar el efecto del tipo de cambio; extender la muestra hacia 1999, con verificación serie por serie, para aumentar la información independiente, y buscar una serie mensual de precios inmobiliarios o un sustituto documentado.
6. **Regla de fases.** Fijar con el asesor el valor del parámetro $c$ antes de recalcular.

Algunas variantes que podrían ayudar son las siguientes:

- *En los componentes.* Aplicar el análisis evolutivo a cada bloque de indicadores por separado, como proponen @camiz_cerda_atoche_2026; elegir el ancho de la ventana con un criterio de estabilidad, como el coeficiente RV entre ventanas sucesivas; seguir el plano 1–2 completo, y no cada eje, en los períodos en que los dos primeros valores propios son casi iguales, como en 2021, y segmentar una trayectoria que combine los tres primeros valores propios con las correlaciones evolutivas, en lugar del primer valor propio solo.
- *En los autoencoders.* Preentrenar la red por capas [@hinton_salakhutdinov_2006] para estabilizar la estimación con pocas observaciones; aumentar los datos de entrenamiento con réplicas del remuestreo por bloques, que conservan la dependencia temporal, y usar el error de reconstrucción como insumo del diagnóstico de meses atípicos de la segmentación.
