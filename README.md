# Tesis Maestría — Medición del Ciclo Financiero en Perú

**Autor:** Roberto  
**Programa:** Maestría  
**Estado:** En progreso — Revisión bibliográfica + exploración empírica

## Descripción
Medición del ciclo financiero en Perú mediante técnicas de reducción 
dimensional y machine learning (PCA, HFC, EPCA/EHFC, Autoencoders, LSTM).

## Fuente de datos
BCRP — Banco Central de Reserva del Perú

## Estructura
```
data/raw/          → Series descargadas del BCRP sin modificar
data/processed/    → Dataset limpio y sincronizado
data/simulated/    → Data simulada para validación de modelos
notebooks/         → Jupyter Notebooks por etapa
src/               → Funciones reutilizables (módulos Python)
reports/figures/   → Gráficos y visualizaciones
reports/tables/    → Tablas de resultados
docs/              → Fichas bibliográficas y notas
```

## Requisitos para los notebooks de aprendizaje profundo (08, 09)

```
pip install torch
```

Basta la versión CPU. Las funciones comunes están en `notebooks/modelos_dl.py`.

## Orden de ejecución del pipeline

```
01_extraccion_bcrp → 04_preprocesamiento → 02_carga_y_verificacion → 05_pca → 06a
01_extraccion_bcrp → 04b_preprocesamiento_mensual → 05b → 06b → 06_epca → 07_pca_rcamiz.R → 07_verificacion_rcamiz → 08_autoencoder → 09_lstm_autoencoder
01b_extraccion_extendida_1985 → 04c_preprocesamiento_extendido
```
