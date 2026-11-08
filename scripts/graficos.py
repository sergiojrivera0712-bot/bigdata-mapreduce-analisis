#!/usr/bin/env python3
"""Genera los gráficos del informe a partir de las salidas de los jobs MapReduce."""
import csv
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RES = os.path.join(os.path.dirname(__file__), "..", "results")
OUT = os.path.join(RES, "graficos")
os.makedirs(OUT, exist_ok=True)
AZUL, GRIS, NARANJA = "#2B5C8A", "#9AA5B1", "#D9822B"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False})


def leer(nombre):
    with open(os.path.join(RES, nombre), encoding="utf-8") as f:
        return [l for l in csv.reader(f, delimiter="\t")]


def mill(x):
    return x / 1e6


def guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, nombre), dpi=200)
    plt.close(fig)


# Figura 1: ingresos por producto
filas = sorted(leer("job1_ingresos_producto.tsv"), key=lambda r: int(r[1]))
fig, ax = plt.subplots(figsize=(7, 3.8))
b = ax.barh([r[0] for r in filas], [mill(int(r[1])) for r in filas], color=AZUL)
ax.bar_label(b, labels=[f"{mill(int(r[1])):.2f}" for r in filas], padding=3, fontsize=8)
ax.set_xlabel("Ingresos (millones de COP)")
guardar(fig, "fig1_ingresos_producto.png")

# Figura 2: ingresos por ciudad y ticket promedio
filas = sorted(leer("job3_por_ciudad.tsv"), key=lambda r: -int(r[2]))
fig, ax = plt.subplots(figsize=(7, 3.4))
b = ax.bar([r[0] for r in filas], [mill(int(r[2])) for r in filas], color=AZUL)
ax.bar_label(b, labels=[f"{mill(int(r[2])):.2f}\n({r[1]} ventas)" for r in filas], fontsize=8, padding=2)
ax.set_ylabel("Ingresos (millones de COP)")
ax.set_ylim(0, 40)
guardar(fig, "fig2_ingresos_ciudad.png")

# Figura 3: ingresos por mes
filas = sorted(leer("job3_por_mes.tsv"))
fig, ax = plt.subplots(figsize=(7, 3.2))
x = [r[0] for r in filas]
ax.plot(x, [mill(int(r[2])) for r in filas], marker="o", color=AZUL)
for xi, r in zip(x, filas):
    ax.annotate(f"{mill(int(r[2])):.1f}", (xi, mill(int(r[2]))), textcoords="offset points",
                xytext=(0, 6), ha="center", fontsize=8)
ax.set_ylabel("Ingresos (millones de COP)")
ax.set_ylim(0, 16)
guardar(fig, "fig3_ingresos_mes.png")

# Figura 4: calificación promedio por producto
filas = sorted(leer("job4_calificacion_producto.tsv"), key=lambda r: float(r[2]))
fig, ax = plt.subplots(figsize=(7, 3.6))
b = ax.barh([f"{r[0]} (n={r[1]})" for r in filas], [float(r[2]) for r in filas],
            color=[NARANJA if float(r[2]) < 3.5 else AZUL for r in filas])
ax.bar_label(b, labels=[r[2] for r in filas], padding=3, fontsize=8)
ax.axvline(3.875, color=GRIS, ls="--", lw=1)
ax.text(3.875, len(filas) - 0.4, " promedio general 3.88", fontsize=8, color="#555")
ax.set_xlim(0, 5.3)
ax.set_xlabel("Calificación promedio (1 a 5)")
guardar(fig, "fig4_calificacion_producto.png")

# Figura 5: etiquetas en reseñas altas vs bajas
filas = sorted(leer("job5_etiquetas.tsv"), key=lambda r: -int(r[1]))
fig, ax = plt.subplots(figsize=(7, 3.2))
et = [r[0] for r in filas]
bajas = [int(r[2]) for r in filas]
altas = [int(r[1]) - int(r[2]) for r in filas]
ax.bar(et, altas, color=AZUL, label="Reseñas con calificación ≥ 4")
ax.bar(et, bajas, bottom=altas, color=NARANJA, label="Reseñas con calificación ≤ 3")
for i, r in enumerate(filas):
    ax.text(i, int(r[1]) + 0.3, f"{r[3]}% bajas", ha="center", fontsize=8)
ax.set_ylabel("Frecuencia")
ax.set_ylim(0, 23)
ax.legend(frameon=False, fontsize=8, loc="upper right")
guardar(fig, "fig5_etiquetas.png")
print("Gráficos generados en", OUT)
