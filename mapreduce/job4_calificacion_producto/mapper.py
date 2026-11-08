#!/usr/bin/env python3
"""Job 4 - Mapper: calificaciones por producto a partir de resenas.jsonl.

Los campos 'verificada' y 'respuesta_tienda' son opcionales (datos semiestructurados),
por eso se leen con valores por defecto.
Salida: producto \t calificacion \t verificada(0/1) \t respondida(0/1) \t dias_respuesta
"""
import json
import sys

for linea in sys.stdin:
    linea = linea.strip()
    if not linea:
        continue
    try:
        r = json.loads(linea)
    except json.JSONDecodeError:
        continue
    producto = r["producto"]["nombre"]
    verificada = 1 if r.get("verificada", False) else 0
    respuesta = r.get("respuesta_tienda")
    respondida = 1 if respuesta else 0
    dias = respuesta["dias_respuesta"] if respuesta else 0
    print(f"{producto}\t{r['calificacion']}\t{verificada}\t{respondida}\t{dias}")
