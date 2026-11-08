#!/usr/bin/env python3
"""Preprocesamiento: convierte resenas.json (arreglo JSON multilínea) a JSON Lines.

Hadoop divide la entrada por líneas (TextInputFormat). Un JSON multilínea
quedaría partido entre registros, así que cada reseña debe ocupar una línea.
Uso: python3 json_a_jsonl.py data/resenas.json data/resenas.jsonl
"""
import json
import sys

entrada, salida = sys.argv[1], sys.argv[2]
with open(entrada, encoding="utf-8") as f:
    registros = json.load(f)
with open(salida, "w", encoding="utf-8") as f:
    for r in registros:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"{len(registros)} reseñas escritas en {salida}", file=sys.stderr)
