#!/usr/bin/env python3
"""Job 5 - Reducer: frecuencia total de cada etiqueta y cuántas veces aparece en reseñas bajas.

Salida: etiqueta \t frecuencia \t en_resenas_bajas \t pct_bajas
"""
import sys

actual, total, bajas = None, 0, 0
for linea in sys.stdin:
    etiqueta, uno, baja = linea.rstrip("\n").split("\t")
    if etiqueta != actual:
        if actual is not None:
            print(f"{actual}\t{total}\t{bajas}\t{100 * bajas / total:.1f}")
        actual, total, bajas = etiqueta, 0, 0
    total += int(uno)
    bajas += int(baja)
if actual is not None:
    print(f"{actual}\t{total}\t{bajas}\t{100 * bajas / total:.1f}")
