#!/usr/bin/env python3
"""Job 5 - Mapper: conteo de etiquetas (variante del clásico WordCount).

Emite cada etiqueta con un 1 y, además, la etiqueta cruzada con la
calificación para medir qué temas aparecen en reseñas bajas (<=3) o altas (>=4).
Salida: etiqueta \t 1 \t es_baja(0/1)
"""
import json
import sys

for linea in sys.stdin:
    linea = linea.strip()
    if not linea:
        continue
    r = json.loads(linea)
    baja = 1 if r["calificacion"] <= 3 else 0
    for etiqueta in r.get("etiquetas", []):
        print(f"{etiqueta.strip().lower()}\t1\t{baja}")
