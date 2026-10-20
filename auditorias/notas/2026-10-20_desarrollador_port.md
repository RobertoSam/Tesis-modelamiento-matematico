# Nota del desarrollador · Iteración 3a · Port a Python de `R/camiz_port.R` (D6)

Fecha: 20 de octubre de 2026 · Rama: `iteracion-3a` (sin commit ni push).

## 1. Alcance

Decisión D6 (`decisiones.qmd`): portar a Python `aede` y `clahfac` de `R/camiz_port.R`, junto
con las utilidades de las que dependen, y verificar que reproducen los CSV `R_*` de las dos vías.
Solo se tocaron estos archivos: `src/camiz_port.py`, `notebooks/999_port_camiz.ipynb`,
`tests/test_camiz_port.py`, `data/results/999_port_*.csv` y `data/results/niveles/999_port_*.csv`.
No se tocaron el Rmd, `R/camiz_port.R`, `notebooks/05*`, `notebooks/modelos_dl.py`,
`src/multivariado.py`, `src/remuestreo.py`, `src/particion.py` ni `herramientas/`.

## 2. Archivos y comandos

| Archivo | Estado | Contenido |
|---|---|---|
| `src/camiz_port.py` | nuevo | Port, función por función, de `R/camiz_port.R` |
| `notebooks/999_port_camiz.ipynb` | nuevo | Verificación de la paridad en las dos vías |
| `tests/test_camiz_port.py` | nuevo | 9 pruebas `pytest` |
| `data/results/999_port_paridad.csv` | nuevo | 162 pruebas: grupo, prueba, vía, referencia, motor, tipo, tolerancia, `dif_max`, estado, explicación |
| `data/results/999_port_{aede_cortes,hfc_jerarquia,ehfc_cofenetica}.csv` | nuevos | Salidas del port, vía transformada |
| `data/results/niveles/999_port_{aede_cortes,hfc_jerarquia,ehfc_cofenetica}.csv` | nuevos | Salidas del port, vía sin transformar (D1) |

```
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/999_port_camiz.ipynb
python3 -m pytest tests/test_camiz_port.py -q
```

El notebook corre de principio a fin sin errores (unos 20 s) y termina con un `assert`: todas las
pruebas de aceptación deben coincidir y toda diferencia complementaria debe quedar explicada.
Resultado de `pytest`: 9 pruebas aprobadas. Semillas: el notebook no tiene componentes
aleatorios y lo declara (`SEMILLA = None`); las pruebas usan `SEMILLA = 2026` para los datos
simulados.

**Entorno.** Instalé `pytest` 9.1.1 con `pip`, porque no estaba disponible. R 4.3.3 está en el
entorno con BLAS y LAPACK de referencia (`/usr/lib/x86_64-linux-gnu/{blas,lapack}`).

## 3. Funciones portadas

- **EPCA.** `aede` (pesos uniformes y gaussianos; regla de signo propia de `aede`, que compara la
  suma lineal de los coeficientes positivos con la de los negativos, seguida de la alineación con
  la ventana anterior por mínimos cuadrados; Fisher sobre λ1; Calinski-Harabász con k grados de
  libertad, como en `aede`), `fisher` (de `fisher_r`, que reemplaza a `fishersub`), `pesos_aede`,
  `bstatw`, `ustatw` y `covp`.
- **HFC.** `clahfac` (jerarquía, λ1 y λ2 por nodo, porcentajes, `Eigentab` y `Ratio`, factores de
  nodo con su corrección de signo, inercias, `hier` de tipo hclust), `clahfacsub`, `agrega`
  (`agrega5`), `distancia_hfc`, `clahpart`, `partclas` (`.partclas_ac`), `hc2axes` y `dendhier`
  (sin el gráfico).
- **Utilidades del Rmd que dependen de las anteriores.** `ch_variantes` (CH con k y con k−1),
  `resumen_aede` (codo, k de las dos variantes de CH y fechas de corte, como `correr_aede`),
  `cofenetica` y `cor_cofenetica` (equivalentes a `dendextend::cor_cophenetic` sobre
  `as.dendrogram`) y `rand_ajustado`.
- **Utilidades de paridad.** `leer_csv_como_r` / `strtod_r` (el lector de números de R) y
  `activar_lapack_referencia` (opcional: `dsyevr` del LAPACK del sistema vía `ctypes`).

Reproduzco tal cual, sin corregirlos, los comportamientos del binario que documenta `R/camiz_port.R`:
`poid` no tiene efecto, `Eigentab` sale de una NIPALS de dos iteraciones, el último elemento
diagonal de `correp` queda en 0 y `rho` no se reinicia entre fases. También conservo la
indexación `hierar[..., 7.8]` de `clahpart`, que R trunca a la columna 7.

## 4. Resultados de la paridad

Fuente única: `data/results/999_port_paridad.csv` (fila = fila de datos sin el encabezado).

| Resultado | Cifra | Origen | Lectura |
|---|---|---|---|
| Pruebas de aceptación contra los CSV `R_*` | 32 de 32 coinciden | filas 1–32, columna `estado` | El port reproduce las dos vías. |
| k elegidos y fechas de corte de `aede` (6 criterios × 2 vías) | 0 diferencias | filas 1–4, `dif_max` | Coinciden los mismos k (niveles: 2, 10, 2, 2, 10, 10) y las mismas fechas. |
| Jerarquía HFC (N1/N2 por código BCRP, nombres, `Num`) | 0 diferencias | filas 5–7 y 12–14 | Coinciden la jerarquía y las uniones, serie por serie. |
| Cifras de la jerarquía HFC | máx. 5,0e-14 | filas 8–11 y 15–18, `dif_max` | El residuo viene de las 15 cifras con que se escriben los CSV, no del cálculo. |
| HFC por ventanas: fechas, cofenética y Rand ajustado | fechas exactas; máx. 6,7e-16 | filas 19–24 | 57 y 56 ventanas, con las mismas jerarquías. |
| Criterios de la datación PCA-MM12 (`R_regimenes_criterios`) | máx. 5,7e-13; k de CH exactos | filas 25–32 | También coinciden las dos variantes de CH. |
| Lector de pandas en lugar del de R | aede y HFC sin cambios | filas 33–38 | Con el otro lector, k, cortes y jerarquía no cambian. |
| Comparación directa con R ejecutado en este entorno, `numpy` | 60 de 62 coinciden | filas 39–100 | Solo difiere el CH de `aede` en la vía transformada (sección 5). |
| Comparación directa con el LAPACK de referencia | 62 de 62 coinciden, `dif_max` = 0 en todas las cifras salvo 6 | filas 101–162 | Con la misma rutina de valores propios, el port reproduce R bit a bit. |

Las 6 excepciones del LAPACK de referencia son `corout`, `correp` y las coordenadas de `clahpart`
en cada vía, con un máximo de 4,4e-16. Las tres derivan de `cor()` de R, que se recalcula después
de la corrección de signo. No las perseguí más porque su orden de magnitud es el de un ulp.

**Dudas abiertas para Roberto.**

- El port deja disponibles en Python los métodos del asesor. ¿Conviene que `06_epca.ipynb` y la
  HFC de Python pasen a usar `src/camiz_port.py`, o se mantienen solo como verificación? Esa
  decisión es metodológica: queda como propuesta (sección 7).
- Los resultados sustantivos (raíz de la HFC, cortes de `aede`) son los mismos que ya reporta el
  Rmd. Esta nota no agrega interpretación nueva de ellos.

## 5. Diferencias y sus causas

1. **Calinski-Harabász de `aede` en la vía transformada, con el motor por defecto (`numpy`).**
   Difiere en 2,85e-10 con pesos uniformes (fila 72) y en 1,60e-10 con pesos gaussianos
   (fila 79), sobre índices de hasta 946,9 y 900,0: un error relativo de unos 3e-13. No afecta
   ningún k ni ningún corte (filas 3–4, 73 y 80).
   - **Causa.** La rutina de valores propios. R usa `dsyevr` del LAPACK de referencia; numpy usa
     `dsyevd` sobre OpenBLAS. Los λ1 difieren en los últimos bits (máx. 1,0e-14, filas 70 y 77).
     La SC intra de Fisher resta cantidades grandes y casi iguales (Σλ1² de unos 3 000 frente a
     una SC de unos 2), y esa cancelación lleva el error hasta el CH.
   - **Cómo se aisló.** Con `cp.activar_lapack_referencia()`, la misma prueba da diferencia 0
     (filas 134 y 141), y lo mismo ocurre con la SC intra y los λ1 (filas 132–133 y 139–140).
   - **Tratamiento.** No amplié la tolerancia. Ambas filas quedan como `difiere`, con la causa en
     la columna `explicacion`.
2. **Lector de CSV.** `read.csv` de R (`R_strtod`) redondea dos veces y lee
   `Liquidez M1` = 85281.551109 de 2018-09 como 85281.55110899999, a 1 ulp del valor que da pandas.
   Es 1 de los 4 332 valores en niveles y 0 de los 3 859 en transformadas. El notebook lee con
   `cp.leer_csv_como_r` para partir de los mismos bits que R. Con el lector de pandas, las pruebas
   principales tampoco cambian (filas 33–38).
3. **Empates de signo en la HFC.** Algunos nodos de dos series con pesos iguales empatan: la regla
   de signo de `clahfac` compara dos sumas iguales, con una diferencia de entre 6e-16 y 0. En la
   primera versión del port eso invertía el signo del factor B del nodo 18 en la vía transformada.
   - **Corrección.** Traduje también el orden de operaciones de R: `colSums` y `cumsum` con long
     double, el orden de suma del BLAS de referencia en `crossprod` y `%*%`, y el `cor()` del C de
     `stats`. Ahora `repvar` y `datout` coinciden bit a bit (filas 54, 58, 85 y 89).
   - **Advertencia.** En esos nodos el signo depende del redondeo, tanto en R como en Python, como
     ya advierte `R/camiz_port.R`. Con otra BLAS (por ejemplo, Accelerate en macOS) el signo del
     factor puede cambiar, aunque su valor absoluto sea idéntico.

## 6. Qué no se compara y por qué

- **`R_paridad_python.csv`** es la tabla de paridad del Rmd con los notebooks de Python, no una
  salida de `aede` ni de `clahfac`.
- **Los nuevos CSV de R del bloque PCA** (`R_adecuacion`, `R_bootstrap_*`, `R_nulo_*`,
  `R_tendencia_*`, `R_pca_contraste_tendencia`) aparecieron durante esta iteración. Los genera el
  trabajo del otro desarrollador sobre 05 y no dependen de los métodos portados.
- **Estado de las referencias.** Los CSV de referencia (`R_aede_cortes`, `R_hfc_jerarquia`,
  `R_ehfc_cofenetica` y `R_regimenes_criterios`, en las dos vías) son idénticos a los del inicio
  de la sesión. El Rmd sí cambió en paralelo, pero el diff no toca `aede`, `clahfac`,
  `cor_cophenetic`, `datar` ni `ch_variantes`.

| Archivo | md5 |
|---|---|
| `data/results/R_aede_cortes.csv` | `f210d0e6a77110c554965f25331e7ddb` |
| `data/results/R_ehfc_cofenetica.csv` | `a22403a3ca80e5ff1431a38658d4a64e` |
| `data/results/R_hfc_jerarquia.csv` | `a5ca68957899d03de71469f6505746f2` |
| `data/results/R_regimenes_criterios.csv` | `9157259885b80372424e33574b531195` |
| `data/results/niveles/R_aede_cortes.csv` | `3cfe91a20fc8bc06d3c9e04f9fa028b2` |
| `data/results/niveles/R_ehfc_cofenetica.csv` | `baf72e2d962f235ed55ba6fdcdc6ffc5` |
| `data/results/niveles/R_hfc_jerarquia.csv` | `e2355a067d9ce1825c992245720fa33a` |
| `data/results/niveles/R_regimenes_criterios.csv` | `14a0c43caebb80c0581140c1567b8ade` |

Los datos están congelados (D4) y el notebook verifica su md5: `dataset_niveles_mensual.csv`
`8088c28c…` y `dataset_transformado_mensual.csv` `8c49f3e5…`. Verifica también el calendario
mensual continuo, la ausencia de faltantes y las dimensiones: 228 × 17 y 227 × 17.

## 7. Desviaciones y propuestas

- **Validación de `R_regimenes_criterios`.** Este CSV no sale de `aede` ni de `clahfac`, sino de
  `datar()` del Rmd. Lo validé con funciones locales del notebook, marcadas «solo validación»:
  `pca_basico`, `mm_causal` y `particion_fisher` traducidas del Rmd. No usé ni modifiqué
  `src/particion.py`, que pertenece al otro desarrollador. **Propuesta:** cuando
  `src/particion.py` esté cerrado, reemplazar esas funciones locales por las oficiales.
- **Fidelidad numérica.** El port reproduce el orden de operaciones de R: long double en sumas y
  orden de suma del BLAS de referencia. Gracias a eso los empates de signo se resuelven igual que
  en R. Su costo es un `crossprod` en Python puro, lento para matrices grandes: aquí no pesa, pero
  conviene saberlo.
- **Motor de valores propios.** Por defecto, el port usa `numpy.linalg.eigh`, que es portable. El
  modo LAPACK de referencia es opcional y solo sirve para verificar.
- **Sin cambios metodológicos.** No hay desviaciones respecto de D1 a D6. Uso la HFC del asesor,
  sin sustituirla por `hclust`/`scipy`. La «HFC por ventanas» es `clahfac` aplicada a cada
  ventana, como en el Rmd, y no se presenta como un algoritmo EHFC publicado.
- **Propuesta para el Rmd** (no lo toqué; corresponde a quien lo mantiene): agregar al anexo de
  paridad una fila que lea `data/results/999_port_paridad.csv`.
