# Nota del redactor LaTeX — 2026-11-27 (iteración 3c, fase 0, tarea F0-7)

Rama `iteracion-3c`, sobre HEAD `402f6f3`. Sin commit (lo hace el orquestador).

## Lo redactado

1. **`tesis_latex/capitulos/04_metodologia.tex`, `sec:met-hfc`.** Tras la frase que declara la
   definición operativa del representante se agrega la `obs:hfc-representante-dos` (Observación
   4.2 en el PDF), con su demostración:
   en una clase $\gA=\{j,j'\}$ de dos series estandarizadas con $r=r_{jj'}\ne0$,
   $|\rho(\vz_j,\fac_\gA)|=|\rho(\vz_{j'},\fac_\gA)|=\sqrt{(1+|r|)/2}$, de modo que el criterio
   «mayor |r| con el factor» no define representante.
   - No se duplica lo existente: la demostración se apoya en `prop:hfc-hojas` (factor
     $(\vz_j+\operatorname{sgn}(r)\vz_{j'})/\sqrt2$ y $\mu_1=1+|r|$), en `prop:hfc-inercia`(b)
     (igualdad con $\lambda_1(\mR_\gA)$ en dos series, de donde el factor es la primera componente
     de la clase) y en `def:hfc` (un grupo de dos series solo puede nacer de la fusión de dos
     hojas, en cualquier paso de la jerarquía). Lo nuevo es el cálculo de las dos covarianzas
     con el factor.
   - Se añade un párrafo breve: el caso $r=0$ queda fuera (el `lem:pca2` no determina el
     factor), y con $r\ne0$ la igualdad es exacta, por lo que las dos correlaciones solo difieren
     por redondeo numérico; se remite a `sec:pend-representante`.
2. **`tesis_latex/capitulos/07_pendientes.tex`, `sec:pend-representante`.** El estado del
   pendiente incluye ahora el caso de dos series (con `\cref{obs:hfc-representante-dos}`) y la
   pregunta al asesor se amplía: regla de desempate fijada de antemano, nombrar a ambas series o
   informar solo el factor.

Notación: solo símbolos ya definidos en `notacion.tex` ($\gA$, $\fac_\gA$, $\vz_j$, $r_{jj'}$,
$\rho(\cdot,\cdot)$, $\operatorname{sgn}$, $\mR_\gA$, $\lambda_1(\mR_\gA)$, $\mathbf{w}^\gA$,
$\mu_1^{\gA\gB}$, $\kappa$). No se introdujo ningún símbolo nuevo; la lista de símbolos no cambia.

## Fuentes por sección

- Observación y demostración: derivación propia a partir de `def:hfc`, `lem:pca2`,
  `prop:hfc-hojas` y `prop:hfc-inercia` del cap. 3. Sin citas nuevas.
- Coherencia con el código: el notebook `07c_hfc_clases.ipynb` (columna `empate_representante`,
  F0-1 del desarrollador, hallazgo m-01) declara el mismo empate estructural; la observación es su
  fundamento formal. No hay inconsistencia entre código y teoría.

## Restricciones verificadas (criterios 5 y 6 del plan 3c, sec. 5.3)

- El texto nuevo no nombra ninguna serie, clase ni cifra de `data/results/`.
- No se tocaron `05_resultados.tex`, `06_conclusiones.tex`, `tesis/`, `decisiones.qmd`,
  `CLAUDE.md` ni el `.bib`.
- `git diff 7c58906 -- tesis_latex/capitulos/05_resultados.tex tesis/` **no sale vacío**: muestra
  `tesis/_cifras.yml` (18 inserciones, 2 supresiones). Ese cambio ya está en commits de la rama
  (`9357a8f` y `402f6f3`, del desarrollador, por F0-1 y F0-2: macros de cifras regeneradas) y no
  es de este agente; se informa al orquestador para que el
  auditor lo valore frente al criterio 6.

## Compilación

`latexmk -lualatex -cd tesis_latex/tesis.tex`: termina con código 0; 0 referencias
indefinidas, 0 citas indefinidas, 0 `Overfull \hbox`. La línea base (HEAD `402f6f3`, compilada en
una copia aparte) también daba 0 cajas desbordadas: no hay cajas nuevas.
Para compilar se instalaron con apt `biber` y los paquetes de TeX para el español y las fuentes
(`texlive-lang-spanish`, `texlive-luatex`, `texlive-latex-extra`, `texlive-bibtex-extra`,
`texlive-fonts-recommended`), que faltaban en el entorno. Los auxiliares quedan ignorados por
`tesis_latex/.gitignore`.

## Pendientes

- La definición del representante en clases de dos series queda para el asesor
  (`sec:pend-representante`). Cuando se fije, W-3 declara el empate en `tab:res-hfc` (m-01).

## Inconsistencias detectadas

- Ninguna entre código y teoría.
