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
4. **Decisiones metodológicas:** `decisiones.qmd` es la fuente de verdad. Vigentes: D1
   (niveles como análisis oficial), D2 (análisis en dos vías; la propuesta de la Parte C está
   pendiente de discutir con el asesor) y D3 (solo frecuencia mensual; `06a` superado, `05` rehecho en
   mensual en la iteración 3a), D4 (datos congelados), D5 (regla de tendencia fijada de antemano), D6
   (`aede` y HFC también en Python) y D7–D14 (decisiones de la iteración 3b: fechado de episodios,
   nulo mixto, d = 3, grilla de ventanas, uso del CH, regla de respaldo, lectura de 2017-10 y
   alcance de los apuntes 2 y 7), D15 (Rmd final solo en niveles; el Rmd actual queda como
   exploración y las transformadas pasan a un anexo de robustez), D16 (se excluye M2: 16 series) y D17
   (criterios de la parte dinámica con 16 series: regla K, RV, D13 en el 06, AE/LSTM pendientes).
   Si algo contradice una decisión, se avisa; no se corrige en
   silencio.
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
data/processed/   Datasets mensuales vigentes: niveles 228 meses × 16 series (2007-01 a 2025-12,
                  análisis oficial D1; el archivo trae 19 columnas y se excluyen el crédito
                  total del SF, el IPC subyacente y, desde D16, la Liquidez M2); transformadas
                  227 × 16 (2007-02 a 2025-12), solo para el anexo de robustez (D15)
data/results/     Salidas con prefijo del notebook que las genera
papers/           Fichas bibliográficas apellido_año.qmd (Ficha Estándar)
R/                Versión en R (fuera del sitio; R puro + R/camiz_port.R; Rcamiz es opcional)
tesis/            Informe del curso (Seminario de Tesis II, MMC102) en Quarto → HTML y .docx
tesis_latex/      Tesis maestra en LaTeX → PDF
asesoria/         Diagnósticos y planes de iteración del asesor de tesis
herramientas/     Scripts compartidos (generar_cifras.py)
auditorias/       Dictámenes del auditor por iteración
.claude/agents/   Definición de los agentes
```

## Documentos y fuentes únicas

- **Tesis (documento maestro):** `tesis_latex/` → PDF. Es la versión más rigurosa.
- **Informe del curso (MMC102):** `tesis/` (Quarto → Word y sitio). Se deriva de la tesis y no
  puede afirmar nada que la tesis no sostenga.
- **Cifras:** solo desde `data/results/`. `herramientas/generar_cifras.py` las convierte en macros
  LaTeX (`tesis_latex/cifras.tex`) y en valores para Quarto; ningún documento las copia a mano.
- **Bibliografía:** un único `tesis/referencias.bib`, compartido por la tesis y el informe. Cada
  entrada tiene su ficha en `papers/`, y solo el bibliotecario modifica el archivo.

## Equipo de agentes

| Agente | Archivo | Rol |
|---|---|---|
| Asesor de tesis | `.claude/agents/asesor-tesis.md` | Diagnostica el avance y propone la siguiente iteración; no edita |
| Desarrollador | `.claude/agents/desarrollador.md` | Código en Python y en R (Rmd), resultados y cifras |
| Redactor LaTeX | `.claude/agents/redactor-latex.md` | Tesis maestra en LaTeX: rigor formal, notación y PDF |
| Editor del informe | `.claude/agents/editor-informe.md` | Informe MMC102 en Quarto/Word, APA 7, derivado de la tesis |
| Bibliotecario | `.claude/agents/bibliotecario.md` | Fichas, verificación de metadatos, `.bib` y registro |
| Auditor | `.claude/agents/auditor.md` | Valida todo de forma independiente antes de publicar |

## Ciclo de iteración (el orquestador es la sesión principal)

1. **Asesor de tesis** diagnostica y propone el plan de la iteración en `asesoria/`: objetivo,
   tareas por agente y criterios de aceptación.
2. **Roberto da su conforme al plan**, con ajustes si los hay. Desde ese momento la iteración
   avanza sin nuevas consultas, salvo decisiones irreversibles o que solo él puede tomar.
   **Fase 0 sin esperar (desde el 24-oct-2026):** apenas el asesor entrega el plan, el
   orquestador lanza las tareas que el plan marca como independientes de toda decisión
   pendiente (fase 0), en la rama `iteracion-N`. Lo que depende de una decisión espera el
   conforme. La fase 0 no escribe resultados en la tesis ni en el informe.
3. **Desarrollador** implementa y ejecuta en Python y en el Rmd (paridad) y regenera las cifras.
   **Bibliotecario** cierra las fichas y verificaciones que el plan requiera. Ambos trabajan en
   paralelo si no dependen uno del otro.
4. **Redactor LaTeX** integra el contenido en la tesis maestra. Luego **editor del informe**
   actualiza el informe a partir de la tesis.
5. **Auditor** revisa sin recibir el razonamiento de los otros agentes y emite
   `auditorias/AAAA-MM-DD_iteracion-N.md` con dictamen **APROBADO / OBSERVADO**.
6. Si hay hallazgos bloqueantes o mayores, vuelven al agente responsable:
   - código, resultados y Rmd → **desarrollador**;
   - tesis LaTeX → **redactor LaTeX**;
   - informe → **editor del informe**;
   - fichas y `.bib` → **bibliotecario**.

   Como máximo hay dos vueltas; si los hallazgos persisten, se escalan a Roberto.
7. El trabajo en curso se respalda en la rama `iteracion-N`, nunca en `main`.

## Seguimiento diario (tarea programada, desde el 24-oct-2026)

Cada mañana una tarea programada abre una sesión que:

1. lee este archivo, el último plan de `asesoria/`, la última auditoría y el estado de la rama
   `iteracion-N` en curso;
2. si el último commit de esa rama tiene menos de 3 horas, asume que hay otra sesión trabajando y
   **solo informa**;
3. si no, identifica el siguiente paso del ciclo y lo ejecuta (lanza al agente que corresponde),
   salvo que dependa de un conforme o una decisión de Roberto;
4. envía a Roberto un aviso breve: qué avanzó, qué sigue y, si algo espera de él, la decisión
   concreta en una línea.

La tarea nunca integra en `main`, nunca publica el sitio y nunca toma decisiones metodológicas.

## Conforme de Roberto

Cuando Roberto da su **conforme a una iteración auditada** («conforme iteración N»), el
orquestador, sin más consultas:

1. integra `iteracion-N` en `main`;
2. agrega la entrada en `linea_temporal.qmd`;
3. hace `quarto render` y `quarto publish gh-pages`;
4. lanza al **asesor de tesis** para el plan de la iteración N+1 y se lo presenta a Roberto.

Si Roberto ya aprobó ese plan por adelantado, lo ejecuta directamente.

El capítulo de resultados, tanto en la tesis como en el informe, no se publica sin aprobación
explícita de Roberto (regla 7).

## Comandos

```
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/NN_*.ipynb
Rscript -e "rmarkdown::render('R/tesis_ciclo_financiero.Rmd')"
quarto render tesis/ --to docx      # informe MMC102
latexmk -lualatex -cd tesis_latex/tesis.tex   # tesis maestra
quarto render                       # sitio completo
quarto publish gh-pages             # paso separado de git push
```

En zsh no usar comentarios `#` inline en comandos de terminal.
