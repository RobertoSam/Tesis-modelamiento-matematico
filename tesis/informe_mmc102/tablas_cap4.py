"""Genera 04_resultados_discusion.md a partir de la plantilla y de los resultados (tablas sin transcribir)."""
import re
from pathlib import Path

import pandas as pd

RAIZ = Path.cwd()
F = RAIZ / "data/results/final"
M = F / "mmc102"
AQUI = RAIZ / "tesis/informe_mmc102"


def num(v, d=2):
    if isinstance(v, str):
        return v
    if pd.isna(v):
        return "—"
    return f"{v:.{d}f}".replace(".", ",").replace("-", "−")


def md(df):
    filas = ["| " + " | ".join(map(str, df.columns)) + " |", "|" + "---|" * len(df.columns)]
    filas += ["| " + " | ".join(map(str, r)) + " |" for r in df.itertuples(index=False)]
    return "\n".join(filas)


T = {}
v = pd.read_csv(F / "05_pca_valores_propios.csv").head(6)
T["valores"] = md(pd.DataFrame({"Eje": v.componente, "Valor propio": v.valor_propio.map(lambda x: num(x, 3)),
                                "Inercia (%)": v.inercia.map(lambda x: num(x, 1)),
                                "Acumulada (%)": v.inercia_acumulada.map(lambda x: num(x, 1)),
                                "Umbral del análisis paralelo": v.horn_umbral_p95.map(lambda x: num(x, 3)),
                                "Vara quebrada (%)": v.vara_quebrada.map(lambda x: num(x, 1))}))
# PCA: por eje, correlación de la serie con el eje, cos² y contribución (salidas del programa)
pi = pd.read_csv(M / "camiz_pca_indicadores.csv")
tab = {"Serie": pi.Serie}
for k in (1, 2, 3):
    tab[f"r eje {k}"] = [f"**{num(v)}**" if abs(v) >= 0.6 else num(v) for v in pi[f"r{k}"]]
    tab[f"cos² eje {k}"] = pi[f"cos2_{k}"].map(num)
    tab[f"Ctr. eje {k} (%)"] = pi[f"ctr{k}"].map(lambda x: num(x, 1))
tab["Calidad (1–3)"] = pi.calidad.map(num)
T["pca"] = md(pd.DataFrame(tab))
c2 = pd.read_csv(F / "05_pca_cos2.csv")
ad = pd.read_csv(F / "05_adecuacion.csv").set_index(["ambito", "medida"]).valor
T["kmo"] = md(pd.DataFrame({"Serie": c2.serie, "KMO": c2.kmo_individual.map(num),
                            "Calidad en los ejes 1–3": c2.suma_1_3.map(num)}))
r = pd.read_csv(M / "referencia_tendencia_ejes.csv")
r["version"] = r.version.map({"ind_TS": "Indeterminadas como TS", "ind_DS": "Indeterminadas como DS"})
T["ref_ejes"] = md(pd.DataFrame({"Versión": r.version, "Eje": r.eje, "Inercia observada (%)": (100 * r.inercia_obs).map(lambda x: num(x, 1)),
                                 "Mediana simulada (%)": (100 * r.p50).map(lambda x: num(x, 1)),
                                 "Percentil 95 simulado (%)": (100 * r.p95).map(lambda x: num(x, 1)), "p̂": r.p.map(lambda x: num(x, 3))}))
e = pd.read_csv(M / "estabilidad_resumen.csv")
T["estab"] = md(pd.DataFrame({"Bloque (meses)": e.L,
                              **{f"Congruencia eje {k}: mediana [p5]": [f"{num(a)} [{num(b)}]" for a, b in zip(e[f"cong{k}_mediana"], e[f"cong{k}_p5"])] for k in (1, 2, 3)},
                              "λ₁ [p5; p95]": [f"[{num(a, 1)}; {num(b, 1)}]" for a, b in zip(e.lambda1_p5, e.lambda1_p95)]}))
nod = pd.read_csv(M / "camiz_hfc_nodos_completo.csv")
T["nodos"] = md(pd.DataFrame({"Nodo": nod.nodo, "Une": nod.une, "Series": nod.series,
                              "λ1": nod.lambda1.map(lambda x: num(x, 3)), "Índice (λ2)": nod.indice.map(lambda x: num(x, 3)),
                              "% local λ1": nod.local1.map(lambda x: num(x, 1)), "% local λ2": nod.local2.map(lambda x: num(x, 1)),
                              "% global λ1": nod.global1.map(lambda x: num(x, 1)), "% global λ2": nod.global2.map(lambda x: num(x, 2)),
                              "% acum. λ2": nod.acum2.map(lambda x: num(x, 2))}))
T["hfc"] = (RAIZ / "tesis/avance/_avance_tabla_hfc.md").read_text().strip()
c = pd.read_csv(M / "contraste_particion.csv")
fil = []
for tr, col, pc in [("estructura", "p95_estructura constante", "p_estructura constante"), ("posición", "p95_ind_DS", "p_ind_DS")]:
    d = c[c.trayectoria == tr]
    for x in d.itertuples():
        fil.append({"Trayectoria": tr.capitalize(), "K": x.K, "Δ observado": num(x.delta_obs, 3),
                    "Percentil 95 simulado": num(getattr(x, col.replace(" ", "_")), 3) if False else num(d.loc[x.Index, col], 3),
                    "p̂": num(d.loc[x.Index, pc], 3)})
T["contraste"] = md(pd.DataFrame(fil))
s = pd.read_csv(M / "cortes_sensibilidad.csv").fillna("—")
s["cortes"] = s.cortes.astype(str).str.replace(" ", ", ")
T["sens"] = md(pd.DataFrame({"Trayectoria": s.trayectoria.str.capitalize(), "Variante": s.variante, "K": s.K, "Cortes": s.cortes}))
car = pd.read_csv(M / "preliminar_caracterizacion.csv")
for tipo in ("posición", "estructura"):
    d = car[car.tipo == tipo]
    T[f"reg_{tipo}"] = md(pd.DataFrame({
        "N.º": d.regimen, "Período": [f"{a} a {b}" for a, b in zip(d.inicio, d.fin)], "Meses": d.meses,
        "Crédito real (%)": d.credito_real_mediana.map(lambda x: num(x, 1)),
        "PBI (%)": d.pbi.map(lambda x: num(x, 1)), "Inflación (%)": d.inflacion.map(lambda x: num(x, 1)),
        "Tasa BCRP (%)": [f"{num(a)} → {num(b)}" for a, b in zip(d.tasa_inicio, d.tasa_fin)],
        "EMBIG (pb)": d.embig.map(lambda x: num(x, 0)),
        "Fase (c = 1; c = 0,5)": [f"{a}; {b}" for a, b in zip(d.fase_c1, d.fase_c05)]}))
pr = pd.read_csv(M / "preliminar_precision_cortes.csv")
T["precision"] = md(pd.DataFrame({"Trayectoria": pr.trayectoria.str.capitalize(), "Corte": pr.corte,
                                  "Frecuencia ±3 meses": pr.frecuencia_3m.map(num),
                                  "Intervalo p5–p95": [f"{a} a {b}" for a, b in zip(pr.p5, pr.p95)],
                                  "Tramo previo (meses)": pr.meses_tramo_previo, "Tramo siguiente (meses)": pr.meses_tramo_siguiente}))
ep = pd.read_csv(M / "preliminar_episodios.csv")
T["episodios"] = md(pd.DataFrame({"Trayectoria": ep.trayectoria.str.capitalize(), "Tolerancia (meses)": ep.tolerancia,
                                  "Compatibles": [f"{a} de {b}" for a, b in zip(ep.compatibles, ep.cortes)],
                                  "Esperados por azar": ep.esperados_azar.map(lambda x: num(x, 1)),
                                  "Probabilidad por azar": ep.p_azar.map(num),
                                  "Distancias (meses)": ep.distancias.str.replace(" ", ", ")}))
plantilla = (AQUI / "04_plantilla.md").read_text()
salida = re.sub(r"\{\{TABLA:(\w+)\}\}", lambda m_: T[m_.group(1)], plantilla)
assert "{{TABLA" not in salida
(AQUI / "04_resultados_discusion.md").write_text(salida)
print("04_resultados_discusion.md generado;", len(T), "tablas")
