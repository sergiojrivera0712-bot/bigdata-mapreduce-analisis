#!/usr/bin/env python3
"""Job 2 - Reducer: une la cabecera de cada venta con sus líneas de detalle.

Salida (una línea por venta, CSV con tabulador):
id_venta \t id_cliente \t ciudad \t mes \t medio_pago \t total \t unidades \t num_items
"""
import sys


def emitir(id_venta, cabecera, total, unidades, items):
    if cabecera is None:
        print(f"Venta {id_venta} sin cabecera", file=sys.stderr)
        return
    id_cliente, ciudad, fecha, medio = cabecera
    print(f"{int(id_venta)}\t{id_cliente}\t{ciudad}\t{fecha[:7]}\t{medio}\t{total}\t{unidades}\t{items}")


actual, cabecera, total, unidades, items = None, None, 0, 0, 0
for linea in sys.stdin:
    id_venta, valor = linea.rstrip("\n").split("\t")
    if id_venta != actual:
        if actual is not None:
            emitir(actual, cabecera, total, unidades, items)
        actual, cabecera, total, unidades, items = id_venta, None, 0, 0, 0
    partes = valor.split("|")
    if partes[0] == "V":
        cabecera = partes[1:]
    else:
        total += int(partes[1])
        unidades += int(partes[2])
        items += 1
if actual is not None:
    emitir(actual, cabecera, total, unidades, items)
