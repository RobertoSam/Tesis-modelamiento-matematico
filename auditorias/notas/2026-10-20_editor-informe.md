# Nota del editor del informe · Iteración 3a · 20 de octubre de 2026

**Agente:** editor del informe (`.claude/agents/editor-informe.md`). **Rama:** `iteracion-3a`, sin
commit ni push. **Encargo:** sección 7 de `asesoria/2026-10-20_plan-iteracion-3.md`, apartado
«Editor del informe», más dos pedidos del coordinador: el problema de fechas del CSL y la
comprobación de los dos `quarto render`.

**Archivos modificados:** `tesis/_capitulos/01_introduccion.qmd`,
`tesis/_capitulos/02_marco_teorico.qmd`, `tesis/_capitulos/03_metodologia.qmd` (una línea),
`tesis/_metadata.yml` (declara `_cifras.yml`), `tesis/README.md`, `tesis/index.qmd` (tabla de
estado) y `tesis/registro_verificacion.md` (solo la fila C-02). No se tocaron `apa.csl`,
`referencias.bib`, `tesis_latex/`, `R/`, `notebooks/`, `src/` ni `data/`. El capítulo de
resultados no cambia (regla 7).

## 1. Secciones redactadas y fuentes

**Fuente maestra:** `tesis_latex/capitulos/01_introduccion.tex` y `02_marco_teorico.tex`, con
`tesis_latex/notacion.tex` para la notación. Datos: `tesis/_cifras.yml`. Estado de las citas:
`tesis/referencias.bib`, `tesis/registro_verificacion.md` y las fichas de `papers/`. No se usó
ninguna otra fuente para el contenido.

**Capítulo 1.** Traslado del `.tex`, sin afirmaciones nuevas. Cambios respecto del informe
aprobado, todos tomados de la tesis:

- cifras desde `_cifras.yml`;
- la vía transformada lleva sus fechas y la frase «pierde el primer mes»;
- objetivos con etiqueta (OE1–OE12, OC1–OC4);
- Horn (1965) citado en OE6, con la vara quebrada y Rencher como `[CITA PENDIENTE]`;
- remisión a la proposición del autoencoder lineal del capítulo 2. Es texto, no una referencia
  cruzada, porque cada capítulo es una página aparte.

**Capítulo 2.** Versión condensada del `.tex`, en el orden de la tesis (2.1 a 2.12). Se
conserva todo el texto narrativo. Las definiciones, los lemas y las proposiciones se enuncian con
los entornos de Quarto (`def-`, `lem-`, `prp-`), **sin demostraciones**. Los supuestos, las
observaciones y el algoritmo `aede` van en párrafos con encabezado en negrita, porque Quarto no
tiene entornos numerados para ellos. Se condensó o se omitió lo siguiente, sin agregar nada:

- el teorema de Eckart y Young se reduce a un párrafo;
- el Lema 2.35 (costo por sumas acumuladas) solo se menciona dentro de la Prop. 2.36;
- en el Lema 2.22 se omite la dirección del vector propio;
- en la Def. 2.6 se omiten las fórmulas de la media y de la desviación típica;
- en la Prop. 2.30(a) y en la Obs. 2.31 se omiten los pasos intermedios.

Cada elemento remite a su etiqueta de LaTeX en la tabla nueva de `tesis/README.md`.

| Sección del informe | Fuente en la tesis |
|---|---|
| Introducción del cap. 2, 2.1 a 2.3 | `sec:antecedentes`, `sec:ciclo`, `sec:regimen`, `sec:validacion`, `sec:epistemologia` (l. 11–240) |
| Datos y PCA (cos², retención, KMO, Bartlett) | `sec:datos`, `sec:pca` y subsecciones (l. 243–503) |
| HFC | `sec:hfc` (l. 506–631) |
| EPCA y `aede` | `sec:epca` (l. 634–793) |
| Fisher y CH | `sec:fisher` (l. 796–918) |
| RV, Procrustes y Tucker | `sec:comparacion` (l. 921–1000) |
| Autoencoder, LSTM y LSTM-autoencoder | `sec:dl` (l. 1003–1159) |
| Criterios y vacíos | `sec:criterios`, `sec:vacios` (l. 1162–1225) |

**Notación alineada con `notacion.tex`.** Se aplicó la lista de la sección 6, punto 8, de la nota
del redactor:

- datos: `X` → $\mathbf{X}$ (sin estandarizar) y $\mathbf{Z}$ (estandarizados);
- `W_d` → $\mathbf{V}_d$; la candidata `V` del PCA → $\mathbf{E}$;
- `w` → $n_w$; `R_t^{(w)}` → $\mathbf{R}_t$;
- `y_A` → $\boldsymbol{\varphi}_{\mathcal{A}}$, con componente de diferencias
  $\boldsymbol{\psi}$; configuraciones del RV `Y, Z` → $\mathbf{F}_1, \mathbf{F}_2$;
- `G(P)` → $\gamma(P)$; `d(·,·)` → $\delta$; `S(·)` → $\mathcal{S}$;
- compuertas `i_t, f_t, o_t, c_t` → $\mathbf{g}^{\mathrm e}_t, \mathbf{g}^{\mathrm o}_t,
  \mathbf{g}^{\mathrm s}_t, \mathbf{s}_t$; código latente `z_t` → $\boldsymbol{\eta}_t$;
  estado oculto en $\mathbb{R}^{n_h}$;
- trayectoria $\mathbf{y}_1,\dots,\mathbf{y}_N$ con $K$ segmentos (antes $Y_t$, $k$ y $n$).

Se eliminó la frase superada «Ese subespacio se denota $W_d$, siguiendo la notación de la
descomposición $\mathbf{X}=U\Sigma W^\top$». La ecuación (@eq-ae-pca) del informe es ahora la
Prop. 2.46(c) de la tesis, $\mathbf{A}^\top\mathbf{A}=\mathbf{V}_d\mathbf{V}_d^\top$, con pesos
atados y bajo sus hipótesis.

**Cifras.** `_metadata.yml` declara `metadata-files: [_cifras.yml]`, y el texto usa el
*shortcode* `meta` con `nSeries`, `nMesesNiveles`, `nMesesTransformadas`,
`fechaInicioNiveles`, `fechaInicioTransformadas`, `fechaFinDatos`, `anioInicioDatos` y
`anioFinDatos`. No se usa ninguna macro de resultados (regla 7). Los números que quedan escritos
son los mismos que la tesis deja escritos (sección 7 de la nota del redactor): años de cita,
cifras de las fuentes (17 series, 48 meses, 0,7, 8 a 30 años, 1999, 2020, S&P 500 de 2000 a
2022), constantes matemáticas y datos bibliográficos de las notas VERIFICAR.
`python3 herramientas/generar_cifras.py --comprobar` termina con código 0.

## 2. Tareas 2 a 4

- **Tabla de correspondencia.** Está en `tesis/README.md`, en la sección «Correspondencia con la
  tesis LaTeX». Tiene dos tablas: secciones → `\label`, y elementos formales del cap. 2 → `\label`.
  Entre paréntesis va el número del PDF actual, tomado de los `.aux`.
- **«227 × 17» en `03_metodologia.qmd`.** Ahora dice «228 meses × 17 series del BCRP en niveles,
  análisis oficial según D1, y 227 meses × 17 series en la vía transformada». Los tres valores se
  leen de `_cifras.yml`.
- **C-02.** En la fila de la descarga de control de la API del BCRP del registro, la columna «Qué
  falta verificar» dice ahora «Ninguno» y explica la salida que se eligió: las cifras se retiraron
  del Rmd. Se quitaron además los dos valores escritos a mano (194,00 y 242,86). Un `grep` de
  `R/tesis_ciclo_financiero.Rmd` confirma que ya no están. La columna «Estado» no se tocó.

## 3. Citas

Se usan las mismas claves que la tesis. Entran en el informe `horn_1965`,
`calinski_harabasz_1974`, `benzecri_1973`, `eckart_young_1936`, `kaiser_1960`, `bartlett_1950`,
`bartlett_1951`, `kaiser_1970`, `kaiser_rice_1974`, `pyper_peterman_1998` y
`lorenzo_seva_ten_berge_2006`. Todas existen en el `.bib`, y el render no avisa de claves
faltantes. Cada cita con verificación pendiente lleva una nota al pie «VERIFICAR: …», que
reproduce el `\verificar{}` de la tesis, salvo en los dos casos superados de la sección 5.1.
Benzécri se cita como en la tesis: «suele resumirse como», no como cita textual.

**Citas pendientes del informe (15 marcas `[CITA PENDIENTE]`; 2 en el cap. 1 y 13 en el cap. 2):**

- Atoche Murrieta (2022), en los dos capítulos;
- fuentes de la vara quebrada y del criterio de Rencher (cap. 1, OE6; cap. 2, 2.5.3), con marcas
  separadas en el cap. 2;
- las cinco fuentes externas de los episodios, que siguen pendientes de la decisión I;
- Jolliffe (2002);
- terminología de cos² y contribuciones;
- relación entre $\mathbf{R}^{-1}$ y las correlaciones parciales;
- Denimal (2001, 2007), en nota al pie;
- Bruynooghe (vecinos reducibles);
- Camiz y Diblasi (2013);
- Tukey (1977);
- Lavit (1988);
- **Tucker (1951)**.

Todas tienen fila en el registro **salvo Tucker (1951)**, la fuente primaria del coeficiente de
congruencia (`\pendiente` de la Def. 2.44 de la tesis, fila 21 de la tabla del redactor). **Pedido
al bibliotecario:** agregar esa fila. Yo no puedo modificar el registro fuera de C-02.

## 4. Fechas en la bibliografía (pedido del bibliotecario)

**Diagnóstico.** La macro `date-issued-month-day` de `apa.csl` escribe el mes antes que el día.
El bloque `<locale xml:lang="es">` del CSL no lo corrige, y CSL 1.0 no permite condicionar una
macro al idioma.

**Alcance:**

- **Citas en el texto:** no se ven afectadas. Las obras con URL muestran solo el año, por
  ejemplo «(Bernanke, 2013)».
- **Capítulos 1 y 2 y `borrador_completo`:** tampoco se ven afectados. No citan ninguna fuente de
  episodio, porque esas fuentes siguen como `[CITA PENDIENTE]` en espera de la decisión I.
- **Página de referencias:** **sí se ve afectada.** `tesis/06_referencias.qmd` usa `nocite: @*`,
  y en ella salen con el orden invertido diez entradas: `bernanke_2013`,
  `reserva_federal_2013`, `congreso_2016`, `congreso_2018`, `lehman_brothers_2008`, `nber_2010`,
  `ustr_2018`, `doj_2016`, `oms_2020a` y `oms_2020b`. Las dos últimas aparecen como «(2020a,
  enero 30)».
- **A futuro:** el problema llegará al borrador en cuanto el cap. 2 cite esas fuentes.

**Hallazgo relacionado (APA, anterior a esta iteración).** Con el mismo CSL, citeproc escribe
también las citas **narrativas** con «&»: «Camiz & Roig (2011)», «Kaiser & Rice (1974)».
Según la regla 1 del editor, la forma correcta es «Camiz y Roig (2011)». Afecta a las 18 citas
narrativas de dos autores de los capítulos 1 y 2 (conteo sobre el HTML renderizado). `tesis/README.md` afirmaba que el CSL generaba
«y», y lo corregí. Las parentéticas, «(Camiz & Roig, 2011)», sí son correctas.

**Propuesta (no aplicada; requiere el conforme del orquestador o de Roberto).** No conviene
modificar `apa.csl`: es el estilo oficial generado, y cualquier cambio se pierde al actualizarlo.
Propongo un filtro Lua del informe, `tesis/herramientas/apa_es.lua`, que corrija la salida de
citeproc en los dos puntos. Lo probé en mi scratchpad con copias de `apa.csl` y
`referencias.bib`, en HTML y en docx, sin advertencias:

- «Camiz & Roig (2011)» pasa a «Camiz y Roig (2011)», y la parentética no cambia;
- «(2013, mayo 22)» pasa a «(2013, 22 de mayo)», y «(2020a, enero 30)», a «(2020a, 30 de enero)»;
- las entradas que solo tienen año no cambian.

Para activarlo, se agregaría a `tesis/_metadata.yml`:

```yaml
citeproc: false
filters:
  - path: herramientas/apa_es.lua
    at: post-quarto
```

`citeproc: false` es necesario: Quarto ejecuta citeproc después de todos los filtros Lua, y el
nombre `citeproc` no se acepta en la lista `filters`. Por eso el filtro llama a
`pandoc.utils.citeproc` y corrige su salida. Texto del filtro probado:

```lua
-- Ajustes APA 7 en español sobre la salida de citeproc (informe MMC102).
-- 1) Citas narrativas: «&» -> «y».  2) Bibliografía: «(2013, mayo 22)» -> «(2013, 22 de mayo)».
local meses = {enero=1,febrero=1,marzo=1,abril=1,mayo=1,junio=1,julio=1,agosto=1,
  septiembre=1,setiembre=1,octubre=1,noviembre=1,diciembre=1}

local function Cite(c)
  if c.citations[1] and c.citations[1].mode == "AuthorInText" then
    c.content = c.content:walk({ Str = function(s) if s.text == "&" then return pandoc.Str("y") end end })
    return c
  end
end

local function reordenar(inl)
  local out, i = pandoc.Inlines{}, 1
  while i <= #inl do
    local a, b, c, d = inl[i], inl[i+1], inl[i+2], inl[i+3]
    if a and a.t == "Str" and a.text:match("^%(%d%d%d%d%l?,$")
       and b and b.t == "Space" and c and c.t == "Str" and meses[c.text]
       and d and d.t == "Space" and inl[i+4] and inl[i+4].t == "Str" then
      local dia, resto = inl[i+4].text:match("^(%d%d?)(%).*)$")
      if dia then
        out:extend{a, pandoc.Space(), pandoc.Str(dia), pandoc.Space(), pandoc.Str("de"),
                   pandoc.Space(), pandoc.Str(c.text .. resto)}
        i = i + 5
        goto continue
      end
    end
    out:insert(a); i = i + 1
    ::continue::
  end
  return out
end

local function Div(d)
  if d.identifier:match("^ref%-") then
    return d:walk({ Para = function(p) p.content = reordenar(p.content); return p end })
  end
end

function Pandoc(doc)
  doc = pandoc.utils.citeproc(doc)
  doc = doc:walk({ Cite = Cite })
  return doc:walk({ Div = Div })
end
```

Límites que conviene conocer:

- El filtro no cambia «y» por «e» ante un apellido que empiece por /i/ («Camiz e Ibáñez»). Hoy
  no hay ningún caso.
- Habría que comprobar que las referencias cruzadas de Quarto (`@def-…`, `@prp-…`) siguen
  resolviéndose con `citeproc: false` en el proyecto completo. En la prueba del scratchpad no
  había referencias cruzadas.
- La alternativa sin filtro es escribir las narrativas a mano, como «Camiz y Roig
  [-@camiz_roig_2011]». La desaconsejo, porque duplica los apellidos fuera del `.bib`.

## 5. Contradicciones detectadas

1. **Notas `\verificar` superadas en la tesis (para el redactor LaTeX).** En el informe usé el
   estado vigente del `.bib` y del registro. La tesis debería actualizarse:
   - `fisher_1958`, en `01_introduccion.tex:52` y `02_marco_teorico.tex:42`: la tesis dice
     «número (284) y DOI», pero el bibliotecario ya verificó el volumen, el número y el DOI. Lo
     pendiente son las páginas (789–798) y la lectura del texto.
   - `baldi_hornik_1989`, en `01_introduccion.tex:59–61` («texto completo no consultado. Ambas
     fichas son preliminares») y en `02_marco_teorico.tex:1021–1023` («Ambas fichas son
     preliminares»): según la ficha y el registro, el texto completo de Baldi y Hornik está leído
     y solo falta el DOI. Sigue siendo preliminar solo Bourlard y Kamp.
2. **Pesos de la ventana (para el redactor LaTeX).** `02_marco_teorico.tex:675–678` dice que el
   máximo de $\tilde\omega_u$ es uno, en el centro, y que $\nu$ fija el cociente entre el peso de
   los extremos y el del centro. Eso vale con $n_w$ impar. Con $n_w$ par, ninguna posición entera
   cae en $(n_w+1)/2$, el máximo es menor que uno y el cociente depende de $n_w$. El informe
   reproduce la frase porque la tesis la sostiene; conviene precisarla.
3. **Capítulo 3 del informe (para el coordinador).** El recuadro de «Desarrollo del modelo» dice
   todavía «formalización de PCA, HFC, EPCA, autoencoders y LSTM a partir de
   `marco_matematico_ae_lstm.qmd`». Esa formalización ya está en el capítulo 2 de la tesis y del
   informe. No lo cambié porque está fuera del encargo, que en el capítulo 3 se limitaba a la
   cifra. Propongo reescribir el recuadro en 3b.
4. **`lorenzo_seva_ten_berge_2006` (para el bibliotecario y el redactor).** El registro da la
   fila por «Cerrado», pero la tesis mantiene un `\verificar` («se leyó el resumen de la
   editorial, no el texto»). No hay contradicción de fondo: los metadatos están cerrados y el
   contenido solo se conoce por el resumen. Aun así, convendría que el registro lo dijera, como
   en `horn_1965`. El informe sigue a la tesis.
5. **`tesis/README.md`** afirmaba que el CSL genera «y» en español. Era falso para las citas
   narrativas (sección 4) y quedó corregido.

## 6. Comprobaciones

- `quarto render tesis/`: termina con código 0 y **sin advertencias**. En la primera pasada hubo
  cuatro `[WARNING] Could not convert TeX math`, porque texmath no admite `\Bigl`/`\Bigr` en las
  ecuaciones numeradas del docx de `borrador_completo`. Se reemplazaron por `\left`/`\right` en
  cuatro ecuaciones del cap. 2, sin cambiar su contenido.
- `quarto render tesis/borrador_completo.qmd --to docx`: termina con código 0 y sin
  advertencias. El docx tiene 430 objetos matemáticos de Word, ningún *shortcode* sin resolver y
  las cifras resueltas (228, 227, diciembre de 2025).
- No queda ninguna referencia cruzada sin resolver (`?@`) en las páginas HTML de `tesis/`.
  Las definiciones y proposiciones salen como «Definición 1 (Régimen)», «Proposición 11», etc.
- Cada nota al pie del informe tiene su llamada y su definición.

## 7. Para la memoria del proyecto

- El informe toma las cifras con `{{< meta cifras.<clave> >}}`, a partir de
  `tesis/_cifras.yml` declarado en `tesis/_metadata.yml`.
- En las ecuaciones numeradas del informe no se usa `\Bigl`/`\Bigr`, porque rompen el docx.
- Con el `apa.csl` actual, citeproc escribe «&» en las citas narrativas y «2013, mayo 22» en las
  fechas. La solución propuesta es el filtro de la sección 4.

## Vuelta 1 (dictamen `auditorias/2026-10-20_iteracion-3a.md`)

**Archivos modificados:** `tesis/_capitulos/02_marco_teorico.qmd` y
`tesis/_capitulos/01_introduccion.qmd`. No se tocó nada más.

1. **M-02, Prop. 2.5 (a).** El enunciado de `prp-ganancia` reproduce ahora la reformulación del
   redactor (`02_marco_teorico.tex:184–194`), sin la demostración:
   - define la media temporal $\langle y\rangle_{t_0,T}$ y la varianza temporal
     $\operatorname{var}_{t_0,T}(y)$ sobre $T$ meses consecutivos. Son la forma Markdown de
     `\prom` y `\vart` de `notacion.tex`;
   - (a) distingue dos casos: $P$ entero, sobre cualquier período completo de $P$ meses, y $P\ge2$
     real, como límite de largo plazo. Este límite vale $\varrho^2/2$ si $P>2$ y
     $\varrho^2\cos^2\psi_0$ si $P=2$, y se excluye el caso degenerado $x\equiv0$;
   - (b) y (c) no cambian, y tampoco el párrafo que sigue a la proposición, igual que en la tesis.
2. **N-01, notas de verificación.** Se copiaron las notas nuevas de la tesis:
   - Fisher (1958), en el cap. 1 (`01_introduccion.tex:52`) y en el cap. 2 (`:42`);
   - Bourlard y Kamp (1988) y Baldi y Hornik (1989), en el cap. 1 (`01_introduccion.tex:59–61`);
   - en el cap. 2, la nota conjunta se separó en dos, como en `02_marco_teorico.tex:1055–1059`:
     `[^v2-bk]` para Bourlard y Kamp y `[^v2-bh]` («solo el DOI; el texto completo ya se leyó»)
     para Baldi y Hornik.
3. **N-02, Lorenzo-Seva y ten Berge (2006).** La tesis retiró el `\verificar` en la Def. 2.44
   (`02_marco_teorico.tex:1030`), en línea con el registro («Cerrado · Ninguno»). El informe retira
   también su nota `[^v2-lst]`. Queda resuelto el punto 4 de la sección 5.
4. **Renders.** `quarto render tesis/` y `quarto render tesis/borrador_completo.qmd --to docx`
   terminan con exit 0, sin advertencias y sin referencias cruzadas sin resolver.

Sigue pendiente el pedido al bibliotecario de la fila del registro para Tucker (1951), de la
sección 3.

## Pasada corta previa a la verificación final

Archivo modificado: `tesis/_capitulos/02_marco_teorico.qmd`.

1. **Prop. 2.5 (a):** ya se replicó en la vuelta 1; no se volvió a tocar.
2. **`def-tucker`:** el `[CITA PENDIENTE: … Tucker (1951)…]` pasa a `[@tucker_1951]`, entrada que
   ya existe en el `.bib` y en `papers/tucker_1951.qmd`. Lleva la nota `[^v2-tk]`, que reproduce el
   `\verificar` de `02_marco_teorico.tex:1031–1033`: ficha preliminar, entidad emisora y lugar sin
   confirmar, texto no leído. Con esto se resuelve el pedido al bibliotecario de la sección 3, y
   quedan 12 marcas `[CITA PENDIENTE]` en el capítulo 2.
3. **`v2-lst`:** ya se había retirado en la vuelta 1. Se comprobó que no queda en el archivo.
4. **«LSTM-autoencoder»:** la cita de Tuhin et al. (2025) lleva la nota nueva `[^v2-tu2]`, «lista
   completa de autores contra la fuente original», como en `02_marco_teorico.tex:1191`.
5. **`v2-cmr`, `v2-cr` y `v2-tu`** se conservan. Todas las notas al pie tienen su llamada y su
   definición.

Renders: `quarto render tesis/` y `quarto render tesis/borrador_completo.qmd --to docx` terminan
con exit 0, sin advertencias y sin referencias cruzadas sin resolver.
