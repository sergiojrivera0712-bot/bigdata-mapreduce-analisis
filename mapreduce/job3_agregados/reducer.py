#!/usr/bin/env python3
"""Job 3 - Reducer: número de ventas, ingreso total y ticket promedio por dimensión.

Salida: dimension \t num_ventas \t ingreso_total \t ticket_promedio
"""
import sys

actual, n, total = None, 0, 0
for linea in sys.stdin:
    clave, valor = linea.rstrip("\n").split("\t")
    if clave != actual:
        if actual is not None:
            print(f"{actual}\t{n}\t{total}\t{round(total / n)}")
        actual, n, total = clave, 0, 0
    n += 1
    total += int(valor)
if actual is not None:
    print(f"{actual}\t{n}\t{total}\t{round(total / n)}")
