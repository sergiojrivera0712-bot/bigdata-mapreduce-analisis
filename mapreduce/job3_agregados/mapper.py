#!/usr/bin/env python3
"""Job 3 - Mapper genérico sobre la salida del Job 2 (encadenamiento de jobs).

Recibe como argumento la dimensión de agrupación: ciudad, mes, medio_pago o cliente.
Salida: dimension \t total_venta
"""
import sys

COLUMNAS = {"cliente": 1, "ciudad": 2, "mes": 3, "medio_pago": 4}
indice = COLUMNAS[sys.argv[1]]

for linea in sys.stdin:
    campos = linea.rstrip("\n").split("\t")
    if len(campos) != 8:
        continue
    print(f"{campos[indice]}\t{campos[5]}")
