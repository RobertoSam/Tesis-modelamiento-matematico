"""Lectura de la parte dinámica con los criterios de D10, D13 y D17 (iteración 3b, tarea D10).

Funciones que usan el notebook 07b y su traducción en el Rmd final (sección 4):

- `rv_correlacion`: coeficiente RV entre dos matrices de correlación completas (sensibilidad de
  D17.2): RV = tr(R_a R_b) / sqrt(tr(R_a²) tr(R_b²)). Con cargas completas (p ejes), es el RV de
  las cargas sin centrar, porque C Cᵀ = R.
- `criterio_oe4`: criterio de OE4 de D17.2. El p5 del nulo de estructura constante se toma **por
  posición** (cada par de ventanas adyacentes no solapadas tiene su propio p5 entre las réplicas);
  el estadístico es la proporción de pares observados bajo su p5, y se compara con la distribución
  nula de esa misma proporción, en la que el p5 de cada réplica se calcula **dejándola fuera**.
- `marcar_transiciones`: para cada transición candidata (regla del 06 y `aede`), si coincide con un
  borde de ventana (D7, D13) y si queda fuera del nulo (D10, D17.3).
- `tabla_2017_10`: la regla de D13 con la lectura de D17.3 para la transición de 2017-10.

Definiciones operativas propias (declaradas en la nota del desarrollador y en el Rmd):

- *Cuantil:* tipo 7 de R (`numpy.quantile`, método lineal), como en el resto del repositorio.
- *p-valor del criterio de OE4:* proporción de réplicas nulas cuya proporción de pares bajo el p5
  (dejándolas fuera) es mayor o igual que la observada.
- *Frontera de un par:* el primer mes de la segunda ventana del par (fila i + n_w), es decir, el
  punto medio entre los centros de las dos ventanas.
- *Transición fuera del nulo:* algún par del mismo ancho y esquema de pesos, con frontera a ±3 meses
  (tolerancia de D7) de la transición, tiene un RV observado menor que su p5 por posición. Para la
  regla del 06, que no tiene pesos, se usan los pares con pesos uniformes (D17.3).
"""

import numpy as np
import pandas as pd

from src.episodios import borde_ventana, meses_entre

ALFA = 0.05
TOLERANCIA = 3                     # meses (D7)
OBJETOS_RV = ('cargas_sin_centrar', 'correlacion')   # D17.2: principal y sensibilidad
OBJETO_PRINCIPAL = 'cargas_sin_centrar'


def rv_correlacion(Ra, Rb):
    """RV entre dos matrices de correlación (simétricas): tr(Ra Rb) / sqrt(tr(Ra²) tr(Rb²))."""
    Ra = np.asarray(Ra, dtype=float)
    Rb = np.asarray(Rb, dtype=float)
    return float(np.sum(Ra * Rb) / np.sqrt(np.sum(Ra * Ra) * np.sum(Rb * Rb)))


def p5_posicion(R, alfa=ALFA):
    """Cuantil alfa de cada columna (posición) de la matriz réplicas × pares."""
    return np.quantile(np.asarray(R, dtype=float), alfa, axis=0)


def criterio_oe4(rv_obs, R, alfa=ALFA):
    """Criterio de OE4 (D17.2) para un ancho y un esquema de pesos.

    rv_obs: vector de m pares observados; R: matriz B × m de los mismos pares en las réplicas nulas.
    Devuelve un dict con el p5 por posición, la marca de cada par observado, la proporción
    observada, la proporción de cada réplica (con su p5 calculado sin ella) y el p-valor.
    """
    rv_obs = np.asarray(rv_obs, dtype=float)
    R = np.asarray(R, dtype=float)
    B, m = R.shape
    assert m == len(rv_obs) and B >= 2
    p5 = p5_posicion(R, alfa)
    bajo = rv_obs < p5
    prop_obs = float(bajo.mean())
    props = np.array([float(np.mean(R[b] < p5_posicion(np.delete(R, b, axis=0), alfa))) for b in range(B)])
    return {'p5': p5, 'bajo': bajo, 'prop_obs': prop_obs, 'props_nulo': props,
            'p_valor': float(np.mean(props >= prop_obs))}


def _mes(f):
    return pd.Timestamp(str(f)[:7] + '-01')


def fuera_del_nulo(fecha, pares, tol=TOLERANCIA):
    """¿Algún par con frontera a ±tol meses de `fecha` tiene RV observado bajo su p5?

    `pares`: DataFrame con columnas `frontera` (AAAA-MM) y `bajo_p5` (bool) de un ancho y pesos.
    Devuelve (bool, número de pares cercanos, número de pares cercanos bajo el p5).
    """
    f = _mes(fecha)
    cerca = np.array([meses_entre(f, _mes(x)) <= tol for x in pares['frontera']], dtype=bool)
    n_cerca = int(cerca.sum())
    n_bajo = int(np.asarray(pares['bajo_p5'], dtype=bool)[cerca].sum()) if n_cerca else 0
    return n_bajo > 0, n_cerca, n_bajo


def marcar_transiciones(candidatos, pares_obs, episodios, tol=TOLERANCIA, tol_sens=6):
    """Marca cada transición candidata con el borde de ventana (D7) y la posición frente al nulo.

    candidatos: DataFrame con `metodo`, `nw`, `pesos` (los de la regla del 06 se leen con
    `pesos = 'uniformes'`, D17.3) y `fecha` (AAAA-MM, centro de ventana).
    pares_obs: DataFrame del criterio de OE4 con `objeto`, `nw`, `pesos`, `frontera` y `bajo_p5`
    (objeto principal de D17.2).
    """
    filas = []
    for r in candidatos.itertuples():
        pz = r.pesos
        pares = pares_obs[(pares_obs.nw == r.nw) & (pares_obs.pesos == pz)]
        fuera, n_cerca, n_bajo = fuera_del_nulo(r.fecha, pares, tol)
        b3 = borde_ventana(_mes(r.fecha), int(r.nw), episodios, tol=tol)
        b6 = borde_ventana(_mes(r.fecha), int(r.nw), episodios, tol=tol_sens)
        filas.append({'metodo': r.metodo, 'nw': int(r.nw), 'pesos': pz, 'fecha': str(r.fecha)[:7],
                      'borde_3': b3, 'es_borde_3': b3 != '—', 'borde_6': b6, 'es_borde_6': b6 != '—',
                      'pares_cercanos': n_cerca, 'pares_cercanos_bajo_p5': n_bajo, 'fuera_del_nulo': fuera})
    return pd.DataFrame(filas)


def tabla_2017_10(marcadas, objetivo='2017-10', tol=TOLERANCIA, anchos=(24, 36, 48, 60)):
    """Regla de D13 con la lectura de D17.3 para la transición de `objetivo`.

    Una combinación método × ancho × pesos tiene candidato si alguna de sus transiciones está a
    ±tol meses de `objetivo`. Un candidato **cuenta** si no es borde de ventana (±3 meses) y queda
    fuera del nulo. Confirmación (D13 con D17.3): candidatos que cuentan con al menos dos anchos
    distintos en la regla del 06 o en `aede` con pesos uniformes, **y** al menos uno en `aede` con
    pesos gaussianos (con cualquier ancho). En otro caso: «transición no confirmada».

    Devuelve (tabla por combinación, dict con las condiciones y la clasificación).
    """
    f0 = _mes(objetivo)
    filas = []
    combinaciones = [(m, nw, pz) for m, pz in [('regla 06 (PC2)', 'uniformes'), ('aede codo', 'uniformes'),
                                                ('aede codo', 'gaussianos_nsd3')] for nw in anchos]
    for metodo, nw, pz in combinaciones:
        g = marcadas[(marcadas.metodo == metodo) & (marcadas.nw == nw) & (marcadas.pesos == pz)]
        g = g[np.array([meses_entre(f0, _mes(x)) <= tol for x in g.fecha], dtype=bool)]
        cuenta = g[(~g.es_borde_3.astype(bool)) & g.fuera_del_nulo.astype(bool)]
        filas.append({'metodo': metodo, 'nw': nw, 'pesos': pz,
                      'candidatos': ' '.join(g.fecha) if len(g) else '',
                      'candidato': len(g) > 0,
                      'algun_no_borde': bool((~g.es_borde_3.astype(bool)).any()) if len(g) else False,
                      'algun_fuera_del_nulo': bool(g.fuera_del_nulo.astype(bool).any()) if len(g) else False,
                      'cuenta': len(cuenta) > 0})
    t = pd.DataFrame(filas)
    unif = t[(t.pesos == 'uniformes') & t.cuenta]
    anchos_unif = sorted(set(unif.nw))
    gauss = t[(t.pesos == 'gaussianos_nsd3') & t.cuenta]
    cond_a = len(anchos_unif) >= 2
    cond_b = len(gauss) > 0
    clas = 'confirmada' if cond_a and cond_b else 'transición no confirmada'
    resumen = {'objetivo': objetivo, 'anchos_que_cuentan_06_o_aede_uniformes': ' '.join(map(str, anchos_unif)),
               'condicion_dos_anchos': cond_a,
               'anchos_que_cuentan_aede_gaussianos': ' '.join(map(str, sorted(set(gauss.nw)))),
               'condicion_gaussianos': cond_b, 'clasificacion': clas}
    return t, resumen
