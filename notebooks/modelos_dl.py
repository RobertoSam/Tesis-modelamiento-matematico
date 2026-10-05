"""
modelos_dl.py
=============

Módulo común para los notebooks 08 (Autoencoders) y 09 (LSTM-Autoencoder).

Tesis: Medición del ciclo financiero en Perú mediante técnicas de reducción
dimensional y machine learning.
Autor: Roberto Samaniego Salcedo — Asesor: Dr. Sergio Camiz

Contenido:
    1. Utilidades de reproducibilidad y rutas
    2. Autoencoder de pesos atados (tied weights) — lineal o no lineal
    3. LSTM-Autoencoder secuencia-a-secuencia (reconstrucción en orden inverso)
    4. Entrenamiento con parada temprana, ruido de entrada (denoising) y
       weight decay
    5. Monte Carlo Dropout (Gal & Ghahramani, 2016)
    6. Comparación de subespacios: ángulos principales, coeficiente RV,
       rotación de Procrustes
    7. Análisis paralelo de Horn (1965)
    8. Partición óptima de Fisher (1958) para series ordenadas en el tiempo

Las definiciones formales de cada componente están en
`marco_matematico_ae_lstm.qmd`. Toda referencia citada en los comentarios
debe estar verificada en la sección de referencias de ese documento.

Requisitos: numpy, pandas, scikit-learn, torch (CPU es suficiente).
"""

import os
import random

import numpy as np
import pandas as pd
import torch
import torch.nn as nn


# =============================================================================
# 1. Reproducibilidad y rutas
# =============================================================================

def ir_a_raiz_del_repo(marcador='_quarto.yml'):
    """
    Sube directorios hasta encontrar el archivo marcador de la raíz del repo.
    Es idempotente: se puede ejecutar varias veces sin acumular `cd ..`.
    """
    actual = os.path.abspath(os.getcwd())
    while True:
        if os.path.exists(os.path.join(actual, marcador)):
            os.chdir(actual)
            return actual
        padre = os.path.dirname(actual)
        if padre == actual:
            raise FileNotFoundError(f'No se encontró {marcador} en ningún directorio superior')
        actual = padre


def fijar_semillas(semilla=42):
    """Fija todas las semillas para que cada corrida sea reproducible."""
    random.seed(semilla)
    np.random.seed(semilla)
    torch.manual_seed(semilla)
    torch.use_deterministic_algorithms(True, warn_only=True)


def a_tensor(X):
    """Convierte un arreglo (o DataFrame) a tensor float32."""
    if isinstance(X, pd.DataFrame):
        X = X.values
    return torch.as_tensor(np.asarray(X), dtype=torch.float32)


# =============================================================================
# 2. Autoencoder de pesos atados
# =============================================================================

class AutoencoderAtado(nn.Module):
    """
    Autoencoder simétrico con pesos atados: el decodificador usa las
    transpuestas de las matrices del codificador (W_dec,l = W_enc,l^T).

    Con activacion='lineal', una sola capa y pérdida MSE, el óptimo global
    genera el mismo subespacio que el PCA (Bourlard & Kamp, 1988;
    Baldi & Hornik, 1989). Esto lo convierte en el puente formal entre el
    PCA de la cadena Camiz y los modelos no lineales.

    Parámetros
    ----------
    dims : list[int]
        Dimensiones de las capas del codificador, p. ej. [17, 8, 3]
        significa 17 -> 8 -> 3 (cuello de botella = 3).
    activacion : {'lineal', 'tanh'}
        Activación de las capas ocultas. La capa de salida siempre es
        lineal porque los datos están estandarizados (no acotados).
    dropout : float
        Probabilidad de dropout en las capas ocultas. Se usa tanto como
        regularización como para Monte Carlo Dropout.
    """

    def __init__(self, dims, activacion='tanh', dropout=0.0):
        super().__init__()
        self.dims = list(dims)
        self.activacion = activacion
        # Matrices de pesos del codificador (se reutilizan transpuestas)
        self.W = nn.ParameterList()
        self.b_enc = nn.ParameterList()
        self.b_dec = nn.ParameterList()
        for d_in, d_out in zip(self.dims[:-1], self.dims[1:]):
            w = torch.empty(d_out, d_in)
            nn.init.xavier_uniform_(w)
            self.W.append(nn.Parameter(w))
            self.b_enc.append(nn.Parameter(torch.zeros(d_out)))
            self.b_dec.append(nn.Parameter(torch.zeros(d_in)))
        self.drop = nn.Dropout(dropout)

    def _act(self, h):
        return torch.tanh(h) if self.activacion == 'tanh' else h

    def codificar(self, x):
        """Mapa codificador f: R^p -> R^d."""
        h = x
        n = len(self.W)
        for i in range(n):
            h = h @ self.W[i].T + self.b_enc[i]
            # La última capa del codificador (cuello de botella) es lineal,
            # para que el código latente no quede acotado en [-1, 1].
            if i < n - 1:
                h = self.drop(self._act(h))
        return h

    def decodificar(self, z):
        """Mapa decodificador g: R^d -> R^p (pesos transpuestos)."""
        h = z
        n = len(self.W)
        for i in reversed(range(n)):
            h = h @ self.W[i] + self.b_dec[i]
            if i > 0:
                h = self.drop(self._act(h))
        return h

    def forward(self, x):
        return self.decodificar(self.codificar(x))

    def matriz_decodificador_lineal(self):
        """
        Para el AE lineal de una capa devuelve W^T (p x d), cuyas columnas
        generan el subespacio de reconstrucción.
        """
        if len(self.W) != 1:
            raise ValueError('Solo definido para el autoencoder de una capa')
        return self.W[0].detach().numpy().T


# =============================================================================
# 3. LSTM-Autoencoder secuencia a secuencia
# =============================================================================

class LSTMAutoencoder(nn.Module):
    """
    LSTM-Autoencoder en el esquema de Srivastava, Mansimov & Salakhutdinov
    (2015): un LSTM codificador lee la ventana x_{t-L+1}, ..., x_t; su estado
    final se proyecta a un código z_t en R^d; un LSTM decodificador
    (no condicionado) reconstruye la ventana en ORDEN INVERSO.

    El código z_t resume la dinámica reciente (L meses) del sistema
    financiero, no solo el estado contemporáneo: es la contraparte temporal
    del score de PCA.
    """

    def __init__(self, n_vars, dim_oculta=16, dim_latente=3, dropout=0.0):
        super().__init__()
        self.n_vars = n_vars
        self.dim_oculta = dim_oculta
        self.dim_latente = dim_latente
        self.enc = nn.LSTM(n_vars, dim_oculta, batch_first=True)
        self.a_latente = nn.Linear(dim_oculta, dim_latente)
        self.desde_latente = nn.Linear(dim_latente, dim_oculta)
        self.dec = nn.LSTM(dim_oculta, dim_oculta, batch_first=True)
        self.salida = nn.Linear(dim_oculta, n_vars)
        self.drop = nn.Dropout(dropout)

    def codificar(self, x):
        """x: (lote, L, p) -> z: (lote, d)."""
        _, (h, _) = self.enc(x)
        return self.a_latente(self.drop(h[-1]))

    def decodificar(self, z, L):
        """z: (lote, d) -> reconstrucción invertida en el tiempo (lote, L, p)."""
        h0 = torch.tanh(self.desde_latente(z))
        # Decodificador no condicionado: recibe el mismo vector en cada paso
        entrada = h0.unsqueeze(1).repeat(1, L, 1)
        y, _ = self.dec(entrada)
        return self.salida(self.drop(y))

    def forward(self, x):
        z = self.codificar(x)
        rec_invertida = self.decodificar(z, x.shape[1])
        # Se devuelve en orden cronológico para calcular la pérdida
        return torch.flip(rec_invertida, dims=[1])


def crear_ventanas(X, L):
    """
    Construye ventanas deslizantes de longitud L (paso 1).
    X: (n, p) -> (n - L + 1, L, p). La ventana k termina en la fila k + L - 1,
    por lo que el código z se fecha al ÚLTIMO mes de la ventana (sin mirar
    al futuro).
    """
    X = np.asarray(X, dtype=np.float32)
    return np.stack([X[i:i + L] for i in range(len(X) - L + 1)])


# =============================================================================
# 4. Entrenamiento
# =============================================================================

def entrenar(modelo, X_ent, X_val=None, epocas=2000, lr=1e-2, weight_decay=1e-4,
             ruido=0.0, paciencia=150, tam_lote=None, semilla=42, verbose=False):
    """
    Entrena por mínimos cuadrados (MSE de reconstrucción) con Adam.

    Parámetros clave
    ----------------
    ruido : float
        Desviación estándar del ruido gaussiano aditivo en la entrada
        (autoencoder denoising, Vincent et al., 2008). La pérdida siempre se
        mide contra la entrada LIMPIA.
    weight_decay : float
        Penalización L2 sobre los pesos (regularización).
    paciencia : int
        Épocas sin mejora en validación antes de detener. Si no hay
        validación, se monitorea la pérdida de entrenamiento.

    Devuelve
    --------
    dict con historiales de pérdida y la mejor época. El modelo queda con
    los pesos de la mejor época.
    """
    fijar_semillas(semilla)
    X_ent = a_tensor(X_ent)
    X_val = a_tensor(X_val) if X_val is not None else None
    opt = torch.optim.Adam(modelo.parameters(), lr=lr, weight_decay=weight_decay)
    mse = nn.MSELoss()

    mejor, mejor_estado, mejor_epoca, sin_mejora = np.inf, None, 0, 0
    hist_ent, hist_val = [], []
    n = len(X_ent)
    tam_lote = tam_lote or n

    for epoca in range(epocas):
        modelo.train()
        perm = torch.randperm(n)
        perdida_epoca = 0.0
        for i in range(0, n, tam_lote):
            lote = X_ent[perm[i:i + tam_lote]]
            entrada = lote + ruido * torch.randn_like(lote) if ruido > 0 else lote
            opt.zero_grad()
            perdida = mse(modelo(entrada), lote)
            perdida.backward()
            opt.step()
            perdida_epoca += perdida.item() * len(lote)
        hist_ent.append(perdida_epoca / n)

        modelo.eval()
        with torch.no_grad():
            if X_val is not None:
                monitor = mse(modelo(X_val), X_val).item()
                hist_val.append(monitor)
            else:
                monitor = mse(modelo(X_ent), X_ent).item()

        if monitor < mejor - 1e-7:
            mejor, mejor_epoca, sin_mejora = monitor, epoca, 0
            mejor_estado = {k: v.detach().clone() for k, v in modelo.state_dict().items()}
        else:
            sin_mejora += 1
            if sin_mejora >= paciencia:
                break
        if verbose and epoca % 200 == 0:
            print(f'  época {epoca:5d}  pérdida ent={hist_ent[-1]:.4f}  monitor={monitor:.4f}')

    modelo.load_state_dict(mejor_estado)
    modelo.eval()
    return {'hist_ent': hist_ent, 'hist_val': hist_val,
            'mejor_epoca': mejor_epoca, 'mejor_perdida': mejor}


def preentrenar_por_capas(modelo, X, **kwargs_entrenar):
    """
    Pre-entrenamiento codicioso capa por capa (en el espíritu de Hinton &
    Salakhutdinov, 2006, pero con autoencoders atados en lugar de RBM):
    cada par (W_l, W_l^T) se entrena como un AE superficial sobre los
    códigos de la capa anterior. Luego se hace el ajuste fino de toda la
    red con `entrenar`.

    Se modifica `modelo` en el sitio y se devuelve la lista de pérdidas
    finales de cada capa.
    """
    perdidas = []
    H = np.asarray(X, dtype=np.float32)
    n_capas = len(modelo.W)
    for l in range(n_capas):
        es_ultima = (l == n_capas - 1)
        # AE superficial de una capa con la misma activación (la del cuello
        # de botella es lineal, igual que en el modelo completo)
        sub = AutoencoderAtado([modelo.dims[l], modelo.dims[l + 1]],
                               activacion='lineal' if es_ultima else modelo.activacion)
        # En un AE de una capa la activación oculta no se aplica (es el
        # cuello de botella); para capas intermedias se usa tanh explícita
        if not es_ultima and modelo.activacion == 'tanh':
            sub.codificar = lambda x, s=sub: torch.tanh(x @ s.W[0].T + s.b_enc[0])
            sub.decodificar = lambda z, s=sub: z @ s.W[0] + s.b_dec[0]
        res = entrenar(sub, H, **kwargs_entrenar)
        perdidas.append(res['mejor_perdida'])
        with torch.no_grad():
            modelo.W[l].copy_(sub.W[0])
            modelo.b_enc[l].copy_(sub.b_enc[0])
            modelo.b_dec[l].copy_(sub.b_dec[0])
            H = sub.codificar(a_tensor(H)).numpy()
    return perdidas


def error_reconstruccion(modelo, X, por_variable=False):
    """
    Error cuadrático medio de reconstrucción por observación (o por
    observación y variable). Para el LSTM-AE se toma el error del ÚLTIMO
    paso de cada ventana, que corresponde al mes que fecha la ventana.
    """
    modelo.eval()
    with torch.no_grad():
        Xt = a_tensor(X)
        R = modelo(Xt)
        E = (R - Xt) ** 2
        if E.dim() == 3:
            E = E[:, -1, :]
    E = E.numpy()
    return E if por_variable else E.mean(axis=1)


# =============================================================================
# 5. Monte Carlo Dropout
# =============================================================================

def mc_dropout(modelo, X, T=200, funcion='codigo', semilla=0):
    """
    Monte Carlo Dropout (Gal & Ghahramani, 2016): se mantiene el dropout
    ACTIVO en inferencia y se hacen T pasadas estocásticas.

    funcion='codigo'  -> distribución del código latente z
    funcion='error'   -> distribución del error de reconstrucción

    Devuelve un arreglo (T, n, d) o (T, n).
    """
    torch.manual_seed(semilla)
    modelo.train()  # activa dropout
    Xt = a_tensor(X)
    muestras = []
    with torch.no_grad():
        for _ in range(T):
            if funcion == 'codigo':
                muestras.append(modelo.codificar(Xt).numpy())
            else:
                R = modelo(Xt)
                E = (R - Xt) ** 2
                if E.dim() == 3:
                    E = E[:, -1, :]
                muestras.append(E.mean(dim=1).numpy())
    modelo.eval()
    return np.stack(muestras)


# =============================================================================
# 6. Comparación de subespacios y configuraciones
# =============================================================================

def angulos_principales(A, B):
    """
    Ángulos principales (en grados) entre los subespacios generados por las
    columnas de A (p x d) y B (p x d). 0° en todos = subespacios idénticos.
    """
    Qa, _ = np.linalg.qr(A)
    Qb, _ = np.linalg.qr(B)
    s = np.clip(np.linalg.svd(Qa.T @ Qb, compute_uv=False), -1, 1)
    return np.degrees(np.arccos(s))


def componentes_desde_decodificador(W_dec, X):
    """
    Recuperación de las direcciones principales a partir de los pesos de un
    AE lineal (idea de Plaut, 2018 — preprint): como W_dec genera el
    subespacio principal pero en una base rotada arbitraria, se proyectan
    los datos sobre ese subespacio y se aplica una SVD dentro de él.
    Devuelve (p x d) con columnas ordenadas por varianza decreciente.
    """
    Q, _ = np.linalg.qr(W_dec)
    _, _, Vt = np.linalg.svd(X @ Q, full_matrices=False)
    return Q @ Vt.T


def coeficiente_rv(X, Y):
    """
    Coeficiente RV de Robert & Escoufier (1976) entre dos configuraciones de
    las MISMAS n observaciones (X: n x p, Y: n x q). Varía en [0, 1] y es
    invariante a rotaciones y escalamientos isotrópicos: compara la
    geometría de las nubes de puntos, no sus coordenadas.
    """
    X = X - X.mean(axis=0)
    Y = Y - Y.mean(axis=0)
    Sx, Sy = X @ X.T, Y @ Y.T
    return float(np.trace(Sx @ Sy) / np.sqrt(np.trace(Sx @ Sx) * np.trace(Sy @ Sy)))


def rotar_procrustes(Z, referencia):
    """
    Rota ortogonalmente Z (n x d) para que se parezca lo más posible a la
    referencia (n x d), p. ej. los scores de PCA. Resuelve el problema de
    Procrustes ortogonal min ||Z R - ref||_F con R^T R = I.

    Motivo: el código de un autoencoder solo está identificado salvo
    rotaciones, igual que el problema de signos ya detectado en EPCA.
    Rotar contra PCA vuelve los ejes interpretables y comparables.
    """
    Zc = Z - Z.mean(axis=0)
    Rc = referencia - referencia.mean(axis=0)
    U, _, Vt = np.linalg.svd(Zc.T @ Rc)
    R = U @ Vt
    return Zc @ R, R


# =============================================================================
# 7. Análisis paralelo de Horn (1965)
# =============================================================================

def analisis_paralelo_horn(X, n_sim=500, percentil=95, semilla=42):
    """
    Retiene los componentes cuyo autovalor (matriz de correlación) supera el
    percentil indicado de los autovalores obtenidos con datos aleatorios
    gaussianos de la misma dimensión n x p.

    Devuelve (autovalores_observados, umbral_aleatorio, n_retener).
    """
    rng = np.random.default_rng(semilla)
    n, p = X.shape
    obs = np.sort(np.linalg.eigvalsh(np.corrcoef(X, rowvar=False)))[::-1]
    sims = np.empty((n_sim, p))
    for s in range(n_sim):
        Z = rng.standard_normal((n, p))
        sims[s] = np.sort(np.linalg.eigvalsh(np.corrcoef(Z, rowvar=False)))[::-1]
    umbral = np.percentile(sims, percentil, axis=0)
    # Se cuentan los componentes consecutivos desde el primero que superan el umbral
    retener = 0
    for o, u in zip(obs, umbral):
        if o > u:
            retener += 1
        else:
            break
    return obs, umbral, retener


# =============================================================================
# 8. Partición óptima de Fisher (1958) para datos ordenados
# =============================================================================

def particion_fisher(Y, k_max=8, tam_min=6):
    """
    Partición óptima de una serie ordenada (n x q) en k segmentos CONTIGUOS
    que minimiza la suma de cuadrados intra-segmento (Fisher, 1958), por
    programación dinámica exacta. Respeta el orden temporal: cada segmento
    es un intervalo de meses, es decir, un candidato a régimen.

    Parámetros
    ----------
    Y : array (n,) o (n, q)
    k_max : número máximo de segmentos evaluados
    tam_min : longitud mínima de un segmento (meses), evita regímenes de
              uno o dos meses causados por un dato atípico.

    Devuelve
    --------
    dict k -> {'sce': suma de cuadrados intra, 'cortes': índices de inicio de
    cada segmento (excepto el primero)}
    """
    Y = np.asarray(Y, dtype=float)
    if Y.ndim == 1:
        Y = Y[:, None]
    n = len(Y)
    # Sumas acumuladas para obtener la SCE de cualquier segmento en O(1)
    S1 = np.vstack([np.zeros(Y.shape[1]), np.cumsum(Y, axis=0)])
    S2 = np.concatenate([[0.0], np.cumsum((Y ** 2).sum(axis=1))])

    def sce(i, j):  # segmento Y[i:j]
        m = j - i
        s = S1[j] - S1[i]
        return S2[j] - S2[i] - (s @ s) / m

    INF = np.inf
    # D[k][j] = mínimo costo de partir Y[:j] en k segmentos
    D = np.full((k_max + 1, n + 1), INF)
    B = np.zeros((k_max + 1, n + 1), dtype=int)
    for j in range(tam_min, n + 1):
        D[1][j] = sce(0, j)
    for k in range(2, k_max + 1):
        for j in range(k * tam_min, n + 1):
            mejor, arg = INF, -1
            for i in range((k - 1) * tam_min, j - tam_min + 1):
                c = D[k - 1][i] + sce(i, j)
                if c < mejor:
                    mejor, arg = c, i
            D[k][j], B[k][j] = mejor, arg

    resultados = {}
    for k in range(1, k_max + 1):
        if not np.isfinite(D[k][n]):
            continue
        cortes, j = [], n
        for kk in range(k, 1, -1):
            i = B[kk][j]
            cortes.append(i)
            j = i
        resultados[k] = {'sce': float(D[k][n]), 'cortes': sorted(cortes)}
    return resultados


# =============================================================================
# 9. Episodios de referencia para validación externa
# =============================================================================

# Fechas de referencia de episodios de estrés conocidos. Se usan SOLO para
# validar ex post (nunca como insumo del entrenamiento). Las fechas son
# aproximaciones a nivel de mes y deben sustentarse con fuente en el marco
# teórico antes de publicarse como resultado.
EPISODIOS_REFERENCIA = {
    'Crisis financiera global': ('2008-09-01', '2009-06-01'),
    'Taper tantrum':            ('2013-05-01', '2013-12-01'),
    'COVID-19':                 ('2020-03-01', '2020-12-01'),
}
