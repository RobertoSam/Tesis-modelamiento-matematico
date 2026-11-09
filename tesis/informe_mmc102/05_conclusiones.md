# 5. CONCLUSIONES Y RECOMENDACIONES

La estructura factorial y su evolución están establecidas con las series en niveles; la identificación de los regímenes, en cambio, no supera todavía el contraste con las series de referencia simuladas, y su validación estadística está en estudio. Los regímenes que se caracterizan en este informe se presentan, por ello, como una descripción tentativa.

## 5.1 Conclusiones

1. **Estructura factorial global (OE1).** Los 16 indicadores se organizan en tres bloques —escala del sistema financiero, condiciones monetarias y riesgo de mercado—, que el análisis en componentes principales y la clasificación factorial jerárquica identifican por caminos distintos y que equivalen a los grupos reportados por los antecedentes peruanos. En niveles, el bloque de escala no se distingue de series independientes con tendencia, y la partición en bloques es sensible a la trayectoria particular de las series; el único co-movimiento que supera el contraste es el de las tasas de interés.

2. **Evolución de la estructura (OE2).** La intensidad del movimiento común es alta y relativamente estable hasta 2019 y cae desde 2020, cuando los bloques se fragmentan y el crédito empresarial y los agregados monetarios dejan de moverse con el resto. El mayor cambio de estructura del período ocurre alrededor de junio de 2020, pero no se distingue de las variaciones que produce una estructura constante con la autocorrelación de los datos.

3. **Segmentación temporal (OE3).** Con las series en niveles, ninguna partición de las trayectorias de estructura y de posición supera a las series de referencia simuladas: el corte de 2020 en la trayectoria de estructura queda en el límite ($\hat p=0{,}065$), y los regímenes de posición no se distinguen de los que produce la tendencia común. El contraste con series de referencia simuladas muestra que la partición de una trayectoria con tendencia produce regímenes aparentes, y es por ello un componente necesario del modelo.

4. **Caracterización de los regímenes (OE4).** Con la especificación de trabajo, los seis regímenes de posición describen una secuencia económica coherente —auge previo a la crisis, crisis, expansión, desaceleración, reactivación con estancamiento del crédito real y contracción real del crédito—, y tres de sus cinco cortes coinciden con episodios documentados, más de lo esperable por azar, aunque sin significación. La regla de fases basada en el crecimiento real del crédito produce una secuencia con sentido económico con $c=0{,}5$, y con $c=1$ clasifica la mayoría de los regímenes como transición.

5. **Representaciones no lineales (OE5).** En la corrida exploratoria, el autoencoder no supera al PCA en el error de reconstrucción fuera de muestra, y su principal aporte es señalar los meses atípicos de la pandemia. La comparación definitiva requiere repetir los modelos con la base vigente.

## 5.2 Recomendaciones

1. Completar la validación de la segmentación con formulaciones que distingan la velocidad del crecimiento de su nivel acumulado sin transformar las series, en particular la partición por tendencias segmentadas, con un contraste global sobre el número de tramos, tramos de al menos 24 meses y un análisis de la influencia de los choques transitorios de 2008–2009 y 2020.
2. Medir la potencia del contraste de cambio de estructura con series simuladas que contengan un cambio de tamaño conocido, para establecer si el cambio de 2020 no es detectable por falta de información o porque la estructura es estable.
3. Extender la muestra hacia 1999 y obtener el crédito de 2006 y el crédito a tipo de cambio constante, para aumentar la información independiente y completar la regla de fases.
4. Fijar con el asesor el valor del parámetro $c$ de la regla de fases antes de recalcular.
5. Verificar la HFC evolutiva contra el programa original y repetir los autoencoders con las 16 series y la especificación de la sección 3.2.7.
6. Como trabajo futuro, aplicar el análisis evolutivo a cada bloque por separado, como proponen @camiz_cerda_atoche_2026.
