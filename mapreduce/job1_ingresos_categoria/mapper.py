#!/usr/bin/env python3
"""Job 1 - Mapper: ingresos y unidades por categoría (o por producto).

Entrada : detalle_venta.csv (id_detalle,id_venta,id_producto,cantidad,precio_unitario)
Caché   : productos.csv (enviado a cada nodo con -files) para el join en el mapa
Argumento opcional: "categoria" (por defecto) o "producto".
Salida  : clave \t ingreso \t unidades
"""
import csv
import sys

# Join en el lado del mapa: la tabla pequeña (productos) se carga en memoria.
DIMENSION = sys.argv[1] if len(sys.argv) > 1 else "categoria"
CAMPO = "nombre" if DIMENSION == "producto" else "categoria"

categorias = {}
with open("productos.csv", encoding="utf-8") as f:
    for fila in csv.DictReader(f):
        categorias[fila["id_producto"]] = fila[CAMPO]

for linea in sys.stdin:
    linea = linea.strip()
    if not linea or linea.startswith("id_detalle"):
        continue  # se omite el encabezado y las líneas vacías
    try:
        _, _, id_producto, cantidad, precio = linea.split(",")
        cantidad, precio = int(cantidad), int(precio)
    except ValueError:
        continue  # registro mal formado
    categoria = categorias.get(id_producto, "Desconocida")
    print(f"{categoria}\t{cantidad * precio}\t{cantidad}")
