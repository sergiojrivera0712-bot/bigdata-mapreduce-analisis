#!/usr/bin/env python3
"""Job 2 - Mapper: join en el lado del reduce entre ventas y detalle_venta.

Recibe ambos archivos como entrada. La clave es id_venta y cada valor se
etiqueta con su origen: V (cabecera de venta) o D (línea de detalle).
clientes.csv llega por caché distribuida para añadir la ciudad.
Salida: id_venta \t V|id_cliente|ciudad|fecha|medio_pago   o   id_venta \t D|subtotal|unidades
"""
import csv
import sys

ciudades = {}
with open("clientes.csv", encoding="utf-8") as f:
    for fila in csv.DictReader(f):
        ciudades[fila["id_cliente"]] = fila["ciudad"]

for linea in sys.stdin:
    linea = linea.strip()
    if not linea or linea.startswith("id_"):
        continue
    campos = linea.split(",")
    if len(campos) == 4:  # ventas.csv: id_venta,id_cliente,fecha_venta,medio_pago
        id_venta, id_cliente, fecha, medio = campos
        ciudad = ciudades.get(id_cliente, "Desconocida")
        print(f"{int(id_venta):05d}\tV|{id_cliente}|{ciudad}|{fecha}|{medio}")
    elif len(campos) == 5:  # detalle_venta.csv
        _, id_venta, _, cantidad, precio = campos
        print(f"{int(id_venta):05d}\tD|{int(cantidad) * int(precio)}|{cantidad}")
