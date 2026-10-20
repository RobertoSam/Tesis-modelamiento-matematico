# CLAUDE.md — Reglas del repositorio de tesis

Tesis de maestría (UNI, Maestría en Ciencias en Modelización Matemática y Computacional):
**"Detección evolutiva de regímenes del ciclo financiero peruano mediante Clasificación
Factorial Jerárquica y aprendizaje automático"**. Tesista: Roberto Carlos Samaniego Salcedo.
Asesor: Dr. Sergio Camiz. El asesor revisa este repositorio y el sitio publicado.

## Reglas permanentes (aplican a todo agente y a toda sesión)

1. **Idioma:** español académico formal. Código en Python, comentado en español.
2. **Citas:** APA 7.ª edición. **Nunca inventar referencias.** Solo se cita lo que tiene ficha
   en `papers/` y entrada en `tesis/referencias.bib`. Toda referencia con verificación pendiente
   se marca `[VERIFICAR: motivo]` en el texto y se lista en `tesis/registro_verificacion.md`.
3. **Cifras:** ninguna cifra se escribe a mano en el borrador. Se leen de `data/results/`
   (código inline de Quarto) o se citan con su archivo de origen. Nunca se corre ni se reporta
   un resultado con data incompleta.
4. **Decisiones metodológicas:** `decisiones.qmd` es la fuente de verdad. Vigente: D1
   (niveles como análisis oficial) y D2 (análisis en dos vías; la propuesta de la Parte C está
   pendiente de discutir con el asesor). Si algo contradice una decisión, se avisa; no se
   corrige en silencio.
5. **Epistemología:** posición del asesor «datos primero» (Benzécri, *laisser parler les
   données*). Los Autoencoders/LSTM se presentan como complemento, con discusión explícita de
   los supuestos que imponen.
6. **Episodios de referencia:** se fechan con fuentes externas, nunca a partir de las propias
   series ni de un indicador.
7. **Resultados ante el asesor:** no se presentan resultados sin interpretación consolidada.
   El capítulo de resultados del borrador no se publica sin aprobación explícita de Roberto.

## Estructura

```
notebooks/        Pipeline numerada 01–09 (prefijo 999 = desarrollo)
src/              Funciones reutilizables
data/processed/   Datasets mensuales vigentes: niveles 228 meses × 17 series (2007-01 a 2025-12,
                  análisis oficial D1); transformadas 227 × 17 (2007-02 a 2025-12)
data/results/     Salidas con prefijo del notebook que las genera
papers/           Fichas bibliográficas apellido_año.qmd (Ficha Estándar)
R/                Versión en R (fuera del sitio; requiere Rcamiz/AedeClahfac locales)
tesis/            Borrador de tesis (Seminario de Tesis II, MMC102) en Quarto → HTML y .docx
auditorias/       Dictámenes del auditor por iteración
.claude/agents/   Definición de los agentes
```

## Equipo de agentes y ciclo de iteración

| Agente | Archivo | Rol |
|---|---|---|
| Desarrollador | `.claude/agents/desarrollador.md` | Construye y ejecuta el código en Python y en R (Rmd), produce resultados |
| Editor APA | `.claude/agents/editor-apa.md` | Redacta el borrador y aplica APA 7 |
| Auditor | `.claude/agents/auditor.md` | Valida todo de forma independiente |

**Ciclo por iteración** (el orquestador es la sesión principal):

1. Roberto fija el objetivo de la iteración.
2. **Desarrollador** implementa y ejecuta en Python y en el Rmd (paridad); entrega
   `data/results/` + nota de resultados.
3. **Editor APA** integra en `tesis/` con citas y referencias cruzadas.
4. **Auditor** revisa sin recibir el razonamiento de los otros agentes; emite
   `auditorias/AAAA-MM-DD_iteracion-N.md` con dictamen **APROBADO / OBSERVADO**.
5. Si hay hallazgos bloqueantes o mayores, vuelven al agente responsable: código, resultados y
   Rmd → **desarrollador**; texto, citas y formato → **editor APA**. Máximo dos vueltas; si
   persisten, se escalan a Roberto.
6. Roberto aprueba → commit en `main`, entrada en `linea_temporal.qmd`, render y
   `quarto publish gh-pages`.

## Comandos

```
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/NN_*.ipynb
Rscript -e "rmarkdown::render('R/tesis_ciclo_financiero.Rmd')"
quarto render tesis/ --to docx      # entregable UNI
quarto render                       # sitio completo
quarto publish gh-pages             # paso separado de git push
```

En zsh no usar comentarios `#` inline en comandos de terminal.
