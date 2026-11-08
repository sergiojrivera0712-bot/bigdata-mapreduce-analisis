#!/usr/bin/env python3
"""Job 4 - Reducer: estadísticas de reseñas por producto.

Salida: producto \t n_resenas \t promedio \t minimo \t maximo \t pct_verificadas \t pct_respondidas \t dias_resp_prom
"""
import sys


def emitir(producto, cal, ver, resp, dias):
    n = len(cal)
    prom_dias = round(dias / resp, 2) if resp else 0
    print(f"{producto}\t{n}\t{sum(cal) / n:.2f}\t{min(cal)}\t{max(cal)}\t"
          f"{100 * ver / n:.1f}\t{100 * resp / n:.1f}\t{prom_dias}")


actual, cal, ver, resp, dias = None, [], 0, 0, 0
for linea in sys.stdin:
    producto, c, v, r, d = linea.rstrip("\n").split("\t")
    if producto != actual:
        if actual is not None:
            emitir(actual, cal, ver, resp, dias)
        actual, cal, ver, resp, dias = producto, [], 0, 0, 0
    cal.append(int(c))
    ver += int(v)
    resp += int(r)
    dias += int(d)
if actual is not None:
    emitir(actual, cal, ver, resp, dias)
