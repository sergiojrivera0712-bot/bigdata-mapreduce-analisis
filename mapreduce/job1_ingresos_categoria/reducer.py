#!/usr/bin/env python3
"""Job 1 - Reducer: suma ingresos y unidades por categoría.

Hadoop entrega las claves ordenadas; se acumula mientras la clave no cambie.
También sirve como combiner porque la suma es asociativa y conmutativa.
Salida: categoria \t ingreso_total \t unidades_totales
"""
import sys

clave_actual, ingreso, unidades = None, 0, 0
for linea in sys.stdin:
    clave, valor_ingreso, valor_unidades = linea.rstrip("\n").split("\t")
    if clave != clave_actual:
        if clave_actual is not None:
            print(f"{clave_actual}\t{ingreso}\t{unidades}")
        clave_actual, ingreso, unidades = clave, 0, 0
    ingreso += int(valor_ingreso)
    unidades += int(valor_unidades)
if clave_actual is not None:
    print(f"{clave_actual}\t{ingreso}\t{unidades}")
