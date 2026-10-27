#!/usr/bin/env python3
"""
Genera las cifras de la tesis a partir de `data/results/` y `data/referencia/` (regla 3 de CLAUDE.md).

Lee el mapa versionado `herramientas/cifras_mapa.csv`, con una fila por cifra:

    macro, archivo, filtro, columna, formato, descripcion

- `macro`: nombre de la macro LaTeX, solo letras (p. ej. `nMesesNiveles` → `\\nMesesNiveles`).
- `archivo`: CSV de `data/results/` (resultados, métodos y datos) o de `data/referencia/` (datos de
  referencia externos, como las fechas de los episodios de D7), relativo a la raíz del repositorio.
  Desde D15 y D16, las cifras vigentes se leen de `data/results/final/`; las carpetas del
  antecedente (`data/results/*.csv` y `data/results/niveles/`) no deben consumirse
  (`data/results/LEEME.md`).
- `filtro`: condiciones `columna=valor` separadas por `;` que deben identificar **una sola fila**
  (comparación de texto exacta, tal como está escrito en el CSV). Vacío solo si el CSV tiene una fila.
- `columna`: columna del CSV con el valor.
- `formato`: `entero`, `decimal:N` (N decimales, coma decimal), `texto`, `fecha_mes`
  (`AAAA-MM` → «enero de 2007») o `anio` (`AAAA-MM` → «2007»). Los enteros de cuatro o más cifras llevan espacio fino de miles.

Escribe dos archivos con el mismo contenido:

- `tesis_latex/cifras.tex`: `\\newcommand{\\macro}{valor}`, con un comentario de origen por macro;
- `tesis/_cifras.yml`: clave `cifras:` con un valor por macro, para Quarto
  (`{{< meta cifras.nMesesNiveles >}}`; ver `herramientas/README.md`).

Es idempotente: sin marcas de tiempo ni dependencias del entorno; dos ejecuciones sobre los mismos
CSV dan archivos idénticos byte a byte. Con `--comprobar` no escribe nada y termina con código 1
si alguno de los dos archivos no está al día.

Uso (desde la raíz del repositorio):

    python3 herramientas/generar_cifras.py
    python3 herramientas/generar_cifras.py --comprobar
"""

import argparse
import csv
import math
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Carpetas de las que se admiten cifras (iteración 3b: se añade data/referencia/ para las fechas
# de los episodios, decisión D7 y tarea L1)
CARPETAS_ADMITIDAS = ('data/results/', 'data/referencia/')
MAPA = os.path.join(RAIZ, 'herramientas', 'cifras_mapa.csv')
SALIDA_TEX = os.path.join(RAIZ, 'tesis_latex', 'cifras.tex')
SALIDA_YML = os.path.join(RAIZ, 'tesis', '_cifras.yml')

MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre',
         'octubre', 'noviembre', 'diciembre']


class ErrorCifra(Exception):
    """Error en una fila del mapa: se informa la macro y se detiene sin escribir nada."""


def leer_csv(ruta):
    with open(ruta, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def seleccionar(filas, filtro, macro):
    """Devuelve la única fila que cumple todas las condiciones del filtro."""
    condiciones = []
    if filtro.strip():
        for parte in filtro.split(';'):
            if '=' not in parte:
                raise ErrorCifra(f'{macro}: condición sin "=" en el filtro: {parte!r}')
            col, val = parte.split('=', 1)
            condiciones.append((col.strip(), val.strip()))
    elegidas = []
    for fila in filas:
        for col, val in condiciones:
            if col not in fila:
                raise ErrorCifra(f'{macro}: la columna del filtro {col!r} no existe en el archivo')
        if all(fila[col] == val for col, val in condiciones):
            elegidas.append(fila)
    if len(elegidas) != 1:
        raise ErrorCifra(f'{macro}: el filtro {filtro!r} selecciona {len(elegidas)} filas (debe ser 1)')
    return elegidas[0]


def _miles(entero_txt, sep):
    """Agrupa en miles con el separador dado (solo si tiene 4 o más cifras)."""
    signo = '-' if entero_txt.startswith('-') else ''
    d = entero_txt.lstrip('-')
    if len(d) < 4:
        return signo + d
    grupos = []
    while d:
        grupos.insert(0, d[-3:])
        d = d[:-3]
    return signo + sep.join(grupos)


def formatear(valor_txt, formato, macro):
    """Devuelve (texto LaTeX, texto plano) con coma decimal."""
    if formato == 'texto':
        if re.search(r'[\\{}$&#%_^~]', valor_txt):
            raise ErrorCifra(f'{macro}: el texto contiene caracteres especiales de LaTeX: {valor_txt!r}')
        return valor_txt, valor_txt
    if formato == 'anio':
        m = re.fullmatch(r'(\d{4})(-\d{2}){0,2}', valor_txt)
        if not m:
            raise ErrorCifra(f'{macro}: fecha con formato inesperado: {valor_txt!r}')
        return m.group(1), m.group(1)
    if formato == 'fecha_mes':
        m = re.fullmatch(r'(\d{4})-(\d{2})(-\d{2})?', valor_txt)
        if not m:
            raise ErrorCifra(f'{macro}: fecha con formato inesperado: {valor_txt!r}')
        t = f'{MESES[int(m.group(2)) - 1]} de {m.group(1)}'
        return t, t
    try:
        x = float(valor_txt)
    except ValueError:
        raise ErrorCifra(f'{macro}: el valor {valor_txt!r} no es numérico')
    if not math.isfinite(x):
        raise ErrorCifra(f'{macro}: el valor no es finito ({valor_txt!r}); revisar el CSV de origen')
    if formato == 'entero':
        # los valores no enteros se redondean (p. ej. el χ² de Bartlett se informa sin decimales)
        e = str(int(round(x)))
        return _miles(e, '\\,'), _miles(e, ' ')
    m = re.fullmatch(r'decimal:(\d+)', formato)
    if m:
        dec = int(m.group(1))
        t = f'{x:.{dec}f}'
        if t.startswith('-') and float(t) == 0:
            t = t[1:]                       # sin «-0,0»
        ent, _, frac = t.partition('.')
        tex = _miles(ent, '\\,') + ('{,}' + frac if dec else '')
        txt = _miles(ent, ' ') + (',' + frac if dec else '')
        return tex, txt
    raise ErrorCifra(f'{macro}: formato desconocido {formato!r}')


def construir():
    filas_mapa = leer_csv(MAPA)
    requeridas = ['macro', 'archivo', 'filtro', 'columna', 'formato', 'descripcion']
    if not filas_mapa or list(filas_mapa[0].keys()) != requeridas:
        raise ErrorCifra(f'el mapa debe tener exactamente las columnas {requeridas}')
    vistas, cache, cifras = set(), {}, []
    for fm in filas_mapa:
        macro = fm['macro'].strip()
        if not re.fullmatch(r'[A-Za-z]+', macro):
            raise ErrorCifra(f'{macro!r}: el nombre de una macro LaTeX solo admite letras')
        if macro in vistas:
            raise ErrorCifra(f'{macro}: macro duplicada en el mapa')
        vistas.add(macro)
        archivo = fm['archivo'].strip()
        if not archivo.startswith(CARPETAS_ADMITIDAS):
            raise ErrorCifra(f'{macro}: las cifras solo se leen de {" o ".join(CARPETAS_ADMITIDAS)} '
                             f'(archivo {archivo!r})')
        ruta = os.path.join(RAIZ, archivo)
        if not os.path.exists(ruta):
            raise ErrorCifra(f'{macro}: no existe el archivo {archivo}')
        if archivo not in cache:
            cache[archivo] = leer_csv(ruta)
        fila = seleccionar(cache[archivo], fm['filtro'], macro)
        col = fm['columna'].strip()
        if col not in fila:
            raise ErrorCifra(f'{macro}: la columna {col!r} no existe en {archivo}')
        tex, txt = formatear(fila[col].strip(), fm['formato'].strip(), macro)
        cifras.append((macro, tex, txt, archivo, fm['filtro'].strip(), col, fm['descripcion'].strip()))
    return cifras


def texto_tex(cifras):
    lineas = ['% Archivo generado por herramientas/generar_cifras.py a partir de herramientas/cifras_mapa.csv.',
              '% No editar a mano: cada cifra se lee de data/results/ o data/referencia/ (regla 3 de CLAUDE.md).',
              '% Para regenerarlo: python3 herramientas/generar_cifras.py', '']
    for macro, tex, _, archivo, filtro, col, desc in cifras:
        lineas.append(f'% {desc} | {archivo} | {filtro or "(única fila)"} | {col}')
        lineas.append(f'\\newcommand{{\\{macro}}}{{{tex}}}')
    return '\n'.join(lineas) + '\n'


def texto_yml(cifras):
    lineas = ['# Archivo generado por herramientas/generar_cifras.py a partir de herramientas/cifras_mapa.csv.',
              '# No editar a mano. Uso en Quarto: {{< meta cifras.<macro> >}} (ver herramientas/README.md).',
              'cifras:']
    for macro, _, txt, archivo, filtro, col, _ in cifras:
        lineas.append(f'  {macro}: "{txt}"  # {archivo} | {filtro or "(única fila)"} | {col}')
    return '\n'.join(lineas) + '\n'


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    ap.add_argument('--comprobar', action='store_true', help='no escribe; falla si los archivos no están al día')
    args = ap.parse_args()
    try:
        cifras = construir()
    except ErrorCifra as e:
        print(f'ERROR: {e}', file=sys.stderr)
        return 2
    salidas = {SALIDA_TEX: texto_tex(cifras), SALIDA_YML: texto_yml(cifras)}
    if args.comprobar:
        desactualizados = [r for r, t in salidas.items()
                           if not os.path.exists(r) or open(r, encoding='utf-8').read() != t]
        for r in desactualizados:
            print(f'Desactualizado: {os.path.relpath(r, RAIZ)}', file=sys.stderr)
        return 1 if desactualizados else 0
    for ruta, contenido in salidas.items():
        # Solo se crea el archivo de salida; no se toca el resto de la carpeta
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, 'w', encoding='utf-8', newline='\n') as f:
            f.write(contenido)
    print(f'{len(cifras)} cifras escritas en {os.path.relpath(SALIDA_TEX, RAIZ)} y {os.path.relpath(SALIDA_YML, RAIZ)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
